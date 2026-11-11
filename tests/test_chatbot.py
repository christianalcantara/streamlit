"""Testes sem rede: execute python -m unittest discover -s tests -v."""

import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import httpx
from google.genai import errors
from streamlit.testing.v1 import AppTest

from utils.gemini import gerar_resposta, para_formato_gemini

RAIZ = Path(__file__).resolve().parents[1]


class TestIntegracao(unittest.TestCase):
    def test_converte_papeis_e_preserva_textos(self):
        mensagens = [
            {"role": "user", "content": "O que é tensão?"},
            {"role": "assistant", "content": "É uma diferença de potencial."},
            {"role": "user", "content": "E a unidade?"},
        ]
        conteudos = para_formato_gemini(mensagens)
        self.assertEqual([c.role for c in conteudos], ["user", "model", "user"])
        self.assertEqual([c.parts[0].text for c in conteudos], [m["content"] for m in mensagens])

    @patch("utils.gemini.genai.Client")
    def test_streaming_entrega_trechos_e_ignora_eventos_sem_texto(self, criar_cliente):
        cliente = criar_cliente.return_value.__enter__.return_value
        cliente.models.generate_content_stream.return_value = [
            SimpleNamespace(text=None),
            SimpleNamespace(text="Olá, "),
            SimpleNamespace(text="estudante!"),
        ]
        mensagens = [{"role": "user", "content": "Olá"}]
        self.assertEqual(list(gerar_resposta("chave-ficticia", "modelo-teste", mensagens)),
                         ["Olá, ", "estudante!"])
        argumentos = cliente.models.generate_content_stream.call_args.kwargs
        self.assertEqual(argumentos["model"], "modelo-teste")
        self.assertEqual(argumentos["contents"][0].parts[0].text, "Olá")
        criar_cliente.return_value.__exit__.assert_called_once()

    @patch("utils.gemini.genai.Client")
    def test_resposta_vazia_gera_erro(self, criar_cliente):
        cliente = criar_cliente.return_value.__enter__.return_value
        cliente.models.generate_content_stream.return_value = [SimpleNamespace(text=None)]
        with self.assertRaises(ValueError):
            list(gerar_resposta("chave-ficticia", "modelo-teste", []))
        criar_cliente.return_value.__exit__.assert_called_once()


class TestInterface(unittest.TestCase):
    def setUp(self):
        # Isola as configurações: nenhum teste lê ou usa uma chave verdadeira.
        segredo = patch("streamlit.secrets", {"GEMINI_API_KEY": "chave-ficticia"})
        segredo.start()
        self.addCleanup(segredo.stop)

    def abrir(self):
        app = AppTest.from_file(str(RAIZ / "streamlit_app.py"), default_timeout=15).run()
        self.assertFalse(app.exception)
        return app

    def test_sem_chave_mostra_orientacao_e_desabilita_envio(self):
        with patch("streamlit.secrets", {}), patch.dict("os.environ", {}, clear=True):
            app = self.abrir()
        self.assertTrue(app.info)
        self.assertTrue(app.chat_input[0].disabled)
        self.assertEqual(app.session_state.mensagens, [])

    @patch("utils.gemini.gerar_resposta")
    def test_resposta_e_contexto_sobrevivem_a_reexecucao(self, gerar):
        gerar.side_effect = [iter(["A corrente é ", "1,2 A."]), iter(["Agora é 2,4 A."])]
        app = self.abrir()
        app.chat_input[0].set_value("12 V em 10 ohms: qual corrente?").run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state.mensagens[-1]["content"], "A corrente é 1,2 A.")
        app.run()  # Uma reexecução não deve repetir a chamada nem perder o histórico.
        self.assertEqual(gerar.call_count, 1)
        self.assertEqual(len(app.chat_message), 2)
        app.chat_input[0].set_value("E com o dobro da tensão?").run()
        self.assertFalse(app.exception)
        historico_enviado = gerar.call_args.args[2]
        self.assertEqual(len(historico_enviado), 3)
        self.assertEqual(historico_enviado[1]["content"], "A corrente é 1,2 A.")
        self.assertEqual(len(app.session_state.mensagens), 4)

    @patch("utils.gemini.gerar_resposta", return_value=iter(["Resposta de teste"]))
    def test_limpar_remove_historico(self, gerar):
        app = self.abrir()
        app.chat_input[0].set_value("Olá").run()
        app.button[0].click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state.mensagens, [])
        self.assertEqual(len(app.chat_message), 0)

    @patch("utils.gemini.gerar_resposta")
    def test_espacos_nao_chamam_api(self, gerar):
        app = self.abrir()
        app.chat_input[0].set_value("   ").run()
        self.assertFalse(app.exception)
        gerar.assert_not_called()
        self.assertEqual(app.session_state.mensagens, [])

    def test_codigos_de_erro_da_api(self):
        for codigo, texto in [(400, "chave"), (401, "chave"), (403, "chave"),
                              (404, "Modelo"), (429, "Cota"), (503, "indisponível")]:
            with self.subTest(codigo=codigo):
                erro = errors.APIError(codigo, {"error": {"message": "falha simulada"}})
                with patch("utils.gemini.gerar_resposta", side_effect=erro):
                    app = self.abrir()
                    app.chat_input[0].set_value("Olá").run()
                self.assertFalse(app.exception)
                self.assertIn(texto, app.error[0].value)
                self.assertEqual(app.session_state.mensagens, [])

    @patch("utils.gemini.gerar_resposta", side_effect=httpx.ConnectError("sem internet"))
    def test_falha_de_conexao(self, gerar):
        app = self.abrir()
        app.chat_input[0].set_value("Olá").run()
        self.assertFalse(app.exception)
        self.assertIn("conexão", app.error[0].value)
        self.assertEqual(app.session_state.mensagens, [])

    @patch("utils.gemini.gerar_resposta", side_effect=ValueError("sem texto"))
    def test_resposta_sem_texto(self, gerar):
        app = self.abrir()
        app.chat_input[0].set_value("Olá").run()
        self.assertFalse(app.exception)
        self.assertIn("resposta de texto", app.error[0].value)
        self.assertEqual(app.session_state.mensagens, [])

    def test_falha_no_meio_do_stream_preserva_conversa_anterior(self):
        def fluxo_com_falha(*args):
            yield "Trecho incompleto que deve sumir"
            raise httpx.ReadTimeout("interrupção simulada")

        app = self.abrir()
        anterior = [
            {"role": "user", "content": "Oi"},
            {"role": "assistant", "content": "Olá!"},
        ]
        app.session_state.mensagens = anterior.copy()
        with patch("utils.gemini.gerar_resposta", side_effect=fluxo_com_falha):
            app.chat_input[0].set_value("Continue").run()
        self.assertFalse(app.exception)
        self.assertTrue(app.error)
        self.assertEqual(app.session_state.mensagens, anterior)
        self.assertFalse(any("Trecho incompleto" in m.value for m in app.markdown))

    def test_exemplos_progressivos_abrem_e_guardam_historico(self):
        for caminho in ["exemplos/01_primeira_tela.py", "exemplos/02_chat_sem_ia.py",
                        "exemplos/03_chat_com_historico.py"]:
            with self.subTest(caminho=caminho):
                app = AppTest.from_file(str(RAIZ / caminho), default_timeout=15).run()
                self.assertFalse(app.exception)
        app.chat_input[0].set_value("Primeira mensagem").run()
        app.chat_input[0].set_value("Segunda mensagem").run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.session_state.mensagens), 4)


if __name__ == "__main__":
    unittest.main()

"""Módulo de integração: traduz nosso histórico e recebe texto da API Gemini."""

from collections.abc import Iterator

from google import genai
from google.genai import types

# Constantes guardam configurações que não variam durante uma resposta.
MODELO_PADRAO = "gemini-3.5-flash-lite"
INSTRUCAO = (
    "Você é um assistente de estudos de um curso técnico. "
    "Responda em português do Brasil, com explicações curtas, exemplos e unidades. "
    "Ajude o aluno a entender Python e conceitos de eletricidade passo a passo. "
    "Se não souber, diga que não sabe. Use exemplos teóricos de eletricidade."
)


def para_formato_gemini(mensagens: list[dict]) -> list[types.Content]:
    """O Streamlit usa 'assistant'; a API Gemini usa 'model' para a IA."""
    conteudos = []
    for mensagem in mensagens:
        papel = "model" if mensagem["role"] == "assistant" else "user"
        conteudo = types.Content(
            role=papel,
            parts=[types.Part(text=mensagem["content"])],
        )
        conteudos.append(conteudo)
    return conteudos


def gerar_resposta(chave: str, modelo: str, mensagens: list[dict]) -> Iterator[str]:
    """Entrega cada trecho assim que chega; propaga falhas para a interface tratar.

    Iterator[str] indica uma sequência de textos produzida aos poucos.
    O yield faz desta função um gerador, explicado no guia passo a passo.
    """
    recebeu_texto = False
    # O cliente abre uma conexão HTTP. 'with' fecha os recursos ao terminar,
    # inclusive quando acontece um erro. O timeout está em milissegundos.
    with genai.Client(api_key=chave, http_options=types.HttpOptions(timeout=30000)) as cliente:
        fluxo = cliente.models.generate_content_stream(
            model=modelo,
            contents=para_formato_gemini(mensagens),
            config=types.GenerateContentConfig(
                system_instruction=INSTRUCAO,
                max_output_tokens=1024,
            ),
        )
        for trecho in fluxo:
            if trecho.text:  # Nem todo evento da API contém texto.
                if trecho.text.strip():
                    recebeu_texto = True
                yield trecho.text

    if not recebeu_texto:
        # Pode ocorrer por bloqueio de conteúdo ou uma resposta sem texto.
        raise ValueError("A API não retornou texto.")

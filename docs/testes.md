# Testes e evidências do chatbot

Use este roteiro para conferir os requisitos das páginas 11 e 12 e preparar evidências para a entrega. Testes automáticos simulam o provedor; a integração real deve ser demonstrada separadamente com uma chave válida.

## Testes automáticos sem consumir a API

Na raiz, com o ambiente ativo:

```bash
python -m unittest discover -s tests -v
```

`unittest` já vem com Python. `AppTest` vem com Streamlit e permite enviar mensagens e clicar em botões sem abrir navegador. `unittest.mock.patch` substitui a API por uma simulação controlada durante o teste.

O arquivo `tests/test_chatbot.py` verifica conversão do histórico, trechos de streaming, eventos vazios, resposta sem texto, tela sem chave, contexto entre perguntas, limpeza, pergunta só com espaços, erros de API, falhas de rede, interrupção no meio da resposta e abertura dos exemplos progressivos. Chaves usadas nos testes são fictícias.

Um teste aprovado mostra que nosso código trata o cenário simulado. Não comprova que a chave é válida, que existe cota ou que o provedor está disponível. O código não usa a API real nesses testes.

### Verificação durante a preparação do projeto

Em 10/11/2026, a execução de `python -m unittest discover -s tests -v` concluiu com **12 testes aprovados**, incluindo subcasos para os códigos de API 400, 401, 403, 404, 429 e 503. Ambiente: Python 3.12.13, Streamlit 1.67.0 e Google Gen AI SDK 2.31.0.

Essa execução utilizou exclusivamente respostas e falhas simuladas, sem chamada ao provedor. A execução real com a configuração da equipe fica no registro manual abaixo. O aviso `missing ScriptRunContext` pode aparecer durante o AppTest; confira o resultado final `OK` para saber se os testes passaram.

## Testes manuais da equipe

Use uma configuração de teste e restaure qualquer alteração ao terminar. Para testar ausência de chave, lembre-se de que uma variável de ambiente também pode fornecê-la. Após mudar os segredos, reinicie a aplicação se necessário.

| Caso | Procedimento | Resultado esperado |
| --- | --- | --- |
| Sem chave | Execute sem chave no arquivo e no ambiente | Aviso de configuração e campo desabilitado |
| Pergunta normal | Use uma chave válida e pergunte sobre lei de Ohm | Texto da API apresentado em partes |
| Contexto | Pergunte por corrente em 12 V e 10 ohms; depois dobre a tensão | Resposta considera o resistor mencionado antes |
| Reexecução | Envie outra pergunta ou interaja com o app | Mensagens anteriores continuam na sessão |
| Limpeza | Clique em Limpar conversa | Histórico desaparece e nova pergunta não envia o histórico antigo |
| Chave inválida | Use temporariamente uma chave fictícia | Mensagem de configuração ou permissão, sem travar |
| Modelo inexistente | Configure temporariamente `GEMINI_MODEL` com um nome inexistente | Mensagem de erro da API, normalmente de modelo/configuração |
| Falha de internet | Desconecte a rede antes de enviar uma pergunta | Erro de conexão/timeout, ou erro do serviço se houver resposta intermediária |
| Cota excedida | Observe se o provedor devolver 429; não esgote cota propositalmente | Aviso de limite ou cota; cenário também coberto por simulação |
| Resposta interrompida | Confira no teste automático de interrupção | Trecho parcial apagado e histórico anterior preservado |
| Nova sessão | Abra outra sessão do navegador, como uma janela anônima | Conversa independente, sem as mensagens da sessão anterior |

O provedor pode usar códigos diferentes conforme a configuração da conta. Na dúvida, confira chave, permissões, modelo e cota no AI Studio. A aplicação evita mostrar o erro bruto na tela.

## Registro para preencher após executar

Copie as linhas conforme a necessidade. Marque como não executado o que não foi conferido. Nunca preencha uma evidência com resultado esperado como se fosse observado.

| Data | Responsável | Caso executado | Resultado observado | Evidência |
| --- | --- | --- | --- | --- |
| A preencher | A preencher | API real e streaming | A preencher após executar | Print ou vídeo sem chave |
| A preencher | A preencher | Histórico e contexto | A preencher após executar | Print da conversa |
| A preencher | A preencher | Tratamento de falhas | A preencher após executar | Print do aviso |
| A preencher | A preencher | Testes automáticos | A preencher após executar | Saída do terminal |

Registre também o modelo utilizado e as versões com `python --version` e `python -m pip show streamlit google-genai`. Para o vídeo de streaming, escolha uma pergunta que gere alguns parágrafos curtos. Não é garantido que respostas muito pequenas permitam perceber os trechos visualmente.

## Problemas comuns

| Problema | Como resolver |
| --- | --- |
| `No module named streamlit` | Ative a `.venv` e instale `requirements.txt` com o mesmo Python |
| `No module named utils` | Execute na raiz do projeto, mantendo a pasta `utils` ao lado do arquivo principal |
| App abre no Python comum e falha | Use `python -m streamlit run streamlit_app.py` |
| Porta 8501 ocupada | Pare a execução anterior ou acrescente `--server.port 8502` |
| Chave não reconhecida | Confira o nome do arquivo, a pasta `.streamlit`, a sintaxe TOML e as permissões |
| Aviso continua após mudar variável de ambiente | Abra outro terminal ou reinicie o app com o ambiente correto |
| Resposta cortada | Faça pergunta menor; a saída é limitada a 1.024 tokens |
| Histórico sumiu ao reconectar | Ele é temporário e não foi salvo em banco de dados |

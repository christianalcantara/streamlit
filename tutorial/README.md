# Desenvolvendo um chatbot com Python e Streamlit

Este tutorial é para quem está começando em programação. Primeiro vamos baixar o projeto do GitHub e preparar o Python no Windows. Depois vamos construir a aplicação em pequenas etapas e entender o que cada ferramenta faz. O projeto atende ao tema 4, das páginas 11 e 12 do material de Informática Aplicada.

Ao estudar com seu responsável, faça uma etapa por vez: digite, execute, altere algo e explique o resultado com suas palavras. Os três exemplos iniciais funcionam sem internet depois da instalação. O chatbot final precisa de internet e chave de API.

## 1 Definir o problema

**Problema:** estudantes precisam revisar conceitos de Python e eletricidade com exemplos e podem querer continuar uma explicação com perguntas relacionadas.

**Solução:** uma tela de conversa que envia perguntas e o histórico a uma API de IA, mostrando a resposta em partes.

**Escopo inicial:** perguntar, receber respostas, manter contexto na sessão, limpar a conversa e apresentar mensagens quando algo falhar. Não haverá cadastro, banco de dados, upload de documentos ou treinamento de modelos.

Explique antes de programar: qual é a entrada? A pergunta. Qual é o processamento? A chamada à API usando o histórico. Qual é a saída? O texto da resposta.

## 2 Conhecer as ferramentas

| Ferramenta | Papel neste projeto |
| --- | --- |
| Python | Linguagem que executa as instruções |
| Terminal | Local onde digitamos comandos para o computador |
| Editor | Local onde escrevemos e salvamos os arquivos de código |
| Ambiente virtual | Pasta com um Python e bibliotecas isolados para o projeto |
| pip | Instalador de bibliotecas Python |
| Streamlit | Biblioteca que cria a interface web usando comandos Python |
| Google Gen AI SDK | Biblioteca cliente que facilita chamadas à API Gemini |
| API | Interface de comunicação com um serviço externo |
| Git | Ferramenta que registra versões dos arquivos |
| GitHub | Serviço que pode hospedar o repositório Git |

Uma biblioteca oferece código pronto para reutilizar. O Streamlit desenha campos e mensagens. O SDK do Google organiza requisições e respostas. Nosso programa combina essas peças.

## 3 Baixar o projeto do GitHub

Instale Python 3.12 ou superior e Git. Na página do repositório da equipe, clique em **Code** e copie o endereço HTTPS. Abra o **Prompt de Comando** (Iniciar, digite `cmd`) e escolha onde guardar o projeto. Troque o endereço de exemplo pelo endereço real do repositório:

```bat
cd %USERPROFILE%\Documents
git clone https://github.com/USUARIO/NOME-DO-REPOSITORIO.git
cd NOME-DO-REPOSITORIO
```

`git clone` baixa uma cópia dos arquivos. `cd` entra em uma pasta. O último comando deve levar à pasta que contém `streamlit_app.py` e `requirements.txt`. Se preferir não instalar Git, no GitHub clique em **Code → Download ZIP**, extraia o arquivo e abra a pasta extraída. O ZIP não recebe atualizações automaticamente.

## 4 Preparar o Python

No Prompt de Comando, confira se o Python está instalado:

```bat
py -3.12 --version
```

Crie um ambiente isolado chamado `.venv` e ative-o:

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
```

A primeira linha usa Python 3.12 para criar o ambiente. A segunda ativa-o nesta janela do terminal. Quando estiver ligado, você verá `(.venv)` no começo da linha. Ao abrir outra janela, ative o ambiente nela também. Para desligar, digite `deactivate`.

Agora instale as bibliotecas do projeto com pip:

```bat
python -m pip install -r requirements.txt
```

`requirements.txt` é uma lista de bibliotecas que o projeto precisa. `pip` instala essas bibliotecas. `-r` pede ao pip que leia os nomes dessa lista. Usamos `python -m pip` para garantir que o pip pertence ao mesmo Python ativo. Não é preciso instalar uv nem usar outros instaladores. A pasta `.venv` fica só no seu computador e não precisa ir ao GitHub.

No PowerShell, ative o ambiente com `.venv\Scripts\Activate.ps1`. Se o PowerShell bloquear esse comando, use o Prompt de Comando.

**Confira:** execute `python --version` e `python -m pip show streamlit`. O primeiro mostra a versão do Python; o segundo confirma que o Streamlit foi instalado.

## 5 Criar a primeira tela

Abra ou crie `exemplos/01_primeira_tela.py`:

```python
import streamlit as st

st.title("Minha primeira aplicação")
nome = st.text_input("Qual é o seu nome?")
if nome:
    st.success(f"Olá, {nome}!")
```

Execute na raiz do projeto:

```bash
python -m streamlit run exemplos/01_primeira_tela.py
```

O terminal mostra um endereço. Abra-o no navegador. Python executa no processo servidor; o navegador apresenta a interface. Não abra o arquivo `.py` como se fosse um site.

| Código | Significado |
| --- | --- |
| `import streamlit as st` | Importa a biblioteca e dá a ela o apelido `st` |
| `st.title(...)` | Chama uma função que desenha o título |
| `nome = ...` | Guarda um valor em uma variável |
| `st.text_input(...)` | Mostra um campo e devolve o texto digitado |
| `if nome:` | Executa o bloco se o texto não estiver vazio |
| `f"Olá, {nome}!"` | Monta um texto inserindo o valor de `nome` |
| Espaços antes de `st.success` | Definem o bloco que pertence ao `if` |

Textos em Python são chamados de strings (`str`). O sinal `=` atribui um valor; para comparar igualdade usamos `==`. Linhas começando com `#` são comentários e não são executadas. Um texto entre três aspas no início do arquivo ou de uma função é uma documentação chamada docstring.

**Exercício:** altere o título e acrescente `st.caption("Projeto de Informática Aplicada")`. Explique a diferença entre uma variável e uma função.

Pare a aplicação com `Ctrl+C` no terminal antes de executar a próxima etapa.

## 6 Receber mensagens sem usar IA

Execute:

```bash
python -m streamlit run exemplos/02_chat_sem_ia.py
```

Leia o arquivo. Os comandos centrais são:

```python
pergunta = st.chat_input("Digite uma mensagem")
if pergunta:
    with st.chat_message("user"):
        st.markdown(pergunta)
    with st.chat_message("assistant"):
        st.markdown(f"Você escreveu: {pergunta}")
```

`st.chat_input` recebe o texto enviado. `st.chat_message` cria a área visual de uma mensagem. `user` identifica o usuário e `assistant` identifica a resposta do programa. `st.markdown` mostra texto que pode ter formatação, como `**negrito**`.

`with` define um contexto. Aqui, os comandos indentados desenham dentro da mensagem correspondente. Seu uso não está limitado à interface: na integração final também ajuda a fechar os recursos de conexão.

Esse exemplo é um **eco**, sem IA: ele só repete a entrada. Ao enviar a segunda mensagem, observe que a primeira some. Isso acontece porque o Streamlit executa o script novamente nas interações; uma variável comum não é um histórico persistente.

**Exercício:** envie duas mensagens e explique por que desenhar texto na tela não significa guardá-lo.

## 7 Guardar o histórico com listas e dicionários

Primeiro entenda a estrutura de uma mensagem:

```python
mensagem = {"role": "user", "content": "O que é corrente elétrica?"}
print(mensagem["content"])
```

Isso é um **dicionário** (`dict`): associa chaves a valores. A chave `role` informa quem falou e `content` guarda o texto. `mensagem["content"]` consulta esse valor.

Uma **lista** (`list`) guarda uma sequência de elementos:

```python
mensagens = []
mensagens.append(mensagem)
```

`[]` cria uma lista vazia. `.append(...)` acrescenta um elemento ao fim. Diferentemente das chaves de um dicionário, as posições da lista são consultadas por números começando em zero.

Execute o terceiro exemplo:

```bash
python -m streamlit run exemplos/03_chat_com_historico.py
```

Agora usamos:

```python
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []
```

`st.session_state` guarda valores entre reexecuções da mesma sessão. O `if` cria a lista apenas quando ela ainda não existe. Se atribuíssemos `[]` em toda execução, apagaríamos o histórico sempre que alguém enviasse uma pergunta.

Para redesenhar o que já foi salvo:

```python
for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])
```

`for` percorre os elementos da lista, um de cada vez. Na inclusão das mensagens do exemplo, `for papel, texto in ...` lê pares: cada par tem o papel e o texto que serão salvos.

O botão de limpeza atribui uma nova lista vazia e chama `st.rerun()`, que recomeça a execução do script para redesenhar a tela. O histórico não é um banco de dados: uma reconexão ou reinício pode apagá-lo, e cada sessão tem sua própria lista.

**Exercício:** envie três perguntas, confira as mensagens e depois limpe. Explique a diferença entre lista, dicionário e `session_state`.

## 8 Entender módulos e importações

Um **módulo** é um arquivo Python que pode reunir funções e valores para reutilização. Neste projeto, `utils/gemini.py` é nosso módulo de comunicação com a IA. A pasta `utils`, com `__init__.py`, é um **pacote**, que organiza módulos.

A separação permite ler a interface sem misturá-la aos detalhes de conexão. Não precisamos criar classes ou várias camadas para este trabalho.

```python
from utils.gemini import MODELO_PADRAO, gerar_resposta
```

Leia assim: “do módulo `gemini`, dentro do pacote `utils`, importe a constante `MODELO_PADRAO` e a função `gerar_resposta`”. O arquivo `__init__.py` não precisa ter lógica; ele identifica explicitamente nosso pacote.

| Importação do projeto | Origem |
| --- | --- |
| `import os` | Biblioteca padrão do Python; acesso a variáveis de ambiente |
| `from collections.abc import Iterator` | Biblioteca padrão; descreve o tipo retornado por um gerador |
| `import streamlit as st` | Biblioteca instalada pelo pip; interface |
| `import httpx` | Biblioteca instalada pelo pip; tipos de erro de rede |
| `from google import genai` | SDK instalado como `google-genai`; cliente da API |
| `from google.genai import types` | Estruturas de dados e configurações aceitas pelo SDK |
| `from google.genai import errors` | Tipos de erro devolvidos pelo SDK |
| `from utils.gemini import gerar_resposta` | Módulo escrito pela equipe |

O nome do pacote no pip nem sempre é igual ao nome usado em `import`: instalamos `google-genai`, mas importamos `google.genai`. Não instale um pacote chamado apenas `google` para este projeto.

Importar um módulo executa suas instruções de nível superior na primeira importação daquele processo. Definir uma função não executa seu corpo: por isso nosso módulo não chama a API durante a importação.

Para experimentar fora da interface, crie temporariamente `calculos.py` na raiz:

```python
def calcular_corrente(tensao, resistencia):
    return tensao / resistencia
```

No terminal Python, aberto na raiz com `python`, execute:

```python
from calculos import calcular_corrente
print(calcular_corrente(12, 10))
```

O resultado é `1.2` ampere. `def` define uma função; os nomes entre parênteses são parâmetros; `12` e `10` são argumentos fornecidos na chamada; `return` devolve o resultado. Use resistência diferente de zero neste exemplo. Saia com `exit()`.

**Exercício:** explique por que `calcular_corrente` pode ser importada por dois programas diferentes e por que um arquivo não deve se chamar `streamlit.py` ou `google.py` (ele poderia esconder a biblioteca original).

## 9 Entender a API e configurar a chave

A inteligência artificial executa no serviço do provedor. O programa envia uma requisição pela internet usando o SDK; o serviço processa a entrada e devolve eventos com a resposta. A chave identifica e autoriza o uso da API. Ela não é a senha da sua conta e não deve ficar dentro do código publicado.

Siga a seção **Configurar a API** do [README](../README.md): gere a chave no AI Studio e preencha a cópia local de `.streamlit/secrets.toml.example`, chamada `.streamlit/secrets.toml`.

No arquivo principal, `ler_configuracao` é uma função nossa:

```python
def ler_configuracao(nome: str, padrao: str = "") -> str:
    try:
        valor = st.secrets.get(nome)
    except FileNotFoundError:
        valor = None
    return valor or os.getenv(nome) or padrao
```

`nome: str` indica que o parâmetro é um texto. `padrao: str = ""` define um valor opcional. `-> str` informa o tipo esperado do retorno. Essas anotações ajudam a leitura e o editor; não substituem a validação de dados.

`st.secrets` lê segredos locais ou do serviço de hospedagem. Se o arquivo não existe, tratamos a exceção. `os.getenv` procura uma variável de ambiente. O operador `or` escolhe o primeiro valor não vazio, nesta ordem: segredo, ambiente e padrão.

`GEMINI_MODEL` é o identificador do modelo. Usamos o modelo padrão já escolhido no projeto; é possível alterá-lo na configuração se a conta não tiver acesso a ele. **Não é necessário alterar o código para trocar a chave ou o modelo.**

## 10 Ler o módulo de integração

Abra `utils/gemini.py`. Estude primeiro `para_formato_gemini`:

1. Recebe nossa lista de mensagens.
2. Percorre a lista com `for`.
3. Troca o papel `assistant` por `model`, nome usado pelo Gemini.
4. Coloca o texto em `types.Part` e cada mensagem em `types.Content`.
5. Devolve a lista no formato aceito pela API.

O SDK usa esses objetos para preparar os dados transmitidos. As respostas antigas também vão na requisição: assim o modelo recebe o contexto. Guardar histórico apenas na tela não bastaria.

Depois estude `gerar_resposta(chave, modelo, mensagens)`:

| Trecho | O que faz |
| --- | --- |
| `INSTRUCAO` | Texto fixo que orienta o comportamento do assistente |
| `with genai.Client(...) as cliente` | Cria o cliente e fecha seus recursos ao sair do bloco |
| `types.HttpOptions(timeout=30000)` | Configura o tempo de espera HTTP em milissegundos |
| `generate_content_stream(...)` | Solicita eventos incrementais de resposta |
| `contents=...` | Envia o histórico convertido, incluindo a nova pergunta |
| `system_instruction=INSTRUCAO` | Orienta idioma, estilo e assunto das respostas |
| `max_output_tokens=1024` | Limita a saída; respostas grandes podem ser cortadas |
| `for trecho in fluxo` | Lê os eventos conforme chegam |
| `if trecho.text` | Ignora eventos que não contêm texto |
| `yield trecho.text` | Entrega o trecho à interface e permite continuar depois |

O tempo de espera HTTP ajuda a evitar uma espera indefinida por conexão ou dados. Ele não é uma garantia de duração máxima da conversa inteira. O aplicativo não implementa repetição automática de uma pergunta que falhou.

## 11 Entender streaming e geradores

Uma função com `return` devolve seu resultado e termina. Uma função com `yield` é um **gerador**: produz valores aos poucos, pausando entre eles.

Este exemplo pode ser executado no terminal Python:

```python
def partes():
    yield "Olá, "
    yield "estudante!"

for texto in partes():
    print(texto)
```

No chatbot, quem percorre o gerador é `st.write_stream`:

```python
resposta = st.write_stream(gerar_resposta(chave, modelo, historico))
```

`gerar_resposta(...)` fornece um trecho por vez conforme a API envia. `st.write_stream` mostra os trechos e, ao terminar, devolve o texto completo, que é guardado no histórico. O tamanho de cada trecho varia; não precisamos receber exatamente uma palavra ou um token por evento.

**Tempo real neste projeto** significa começar a mostrar a resposta enquanto ela chega. Ainda existe latência de rede e processamento. Não usamos esperas artificiais para fingir geração de IA.

**Exercício:** explique por que juntar tudo antes de chamar `st.markdown` atrasaria a primeira visualização da resposta.

## 12 Montar e executar o chatbot final

O arquivo `streamlit_app.py` reúne a interface da versão final. Leia seus blocos nesta ordem:

1. Importações: bibliotecas externas, biblioteca padrão e nosso módulo.
2. Configuração da página e função de leitura das configurações.
3. Inicialização do histórico em `st.session_state`.
4. Barra lateral com modelo, explicação e limpeza.
5. Leitura da chave e aviso se estiver ausente.
6. Laço que redesenha as mensagens antigas.
7. Campo de pergunta, desabilitado quando não há chave.
8. Exibição da pergunta, chamada à API e streaming da resposta.
9. Gravação da conversa completa ou apresentação de erro.

Execute na raiz, com os exemplos anteriores encerrados:

```bash
python -m streamlit run streamlit_app.py
```

O fluxo é:

```text
Navegador recebe a pergunta
    -> Streamlit reexecuta o script
    -> recupera e desenha o histórico da sessão
    -> acrescenta a pergunta a uma lista temporária
    -> utils.gemini envia essa lista à API
    -> API entrega trechos de texto
    -> yield repassa os trechos para st.write_stream
    -> tela mostra a resposta aos poucos
    -> histórico recebe pergunta e resposta completas
```

`historico = st.session_state.mensagens + [nova_mensagem]` cria uma nova lista. Assim, se algo falhar, o histórico anterior continua consistente. Somente depois da resposta concluída guardamos o novo par de mensagens. A pergunta que falhou aparece naquela execução, mas não fica gravada; envie-a novamente para tentar de novo.

Não é necessário `if __name__ == "__main__"` no arquivo da interface: o Streamlit executa esse script diretamente. Já o arquivo de testes usa essa convenção para permitir execução como programa de teste.

## 13 Entender o tratamento de erros

`try` delimita uma tentativa; `except` trata uma exceção conhecida para que o usuário receba uma explicação.

- `errors.APIError`: a API respondeu com um problema, como permissão, modelo indisponível, cota ou falha do serviço.
- `httpx.HTTPError`: houve falha de rede ou tempo de espera esgotado.
- `ValueError`: não houve texto utilizável na resposta.

Os códigos de API ajudam a decidir a mensagem: 400/401/403 pedem revisão de credenciais e configuração; 404 pede revisão do modelo; 429 indica limite ou cota. Não mostramos o erro bruto, que pode conter detalhes internos.

O bloco `saida = st.empty()` reserva um espaço para a resposta. Se o fluxo falha depois de escrever parte do texto, `saida.empty()` limpa essa parte para evitar apresentar uma resposta incompleta como concluída. O histórico também permanece sem esse turno.

**Exercício:** sem alterar uma chave válida definitivamente, descreva como testar ausência de chave, modelo incorreto e perda de conexão. Use o [plano de testes](testes.md).

## 14 Enviar alterações ao GitHub e preparar a entrega

Como baixamos o código com `git clone`, o Git já está preparado. Não é necessário executar `git init`.

O `.gitignore` orienta quais arquivos locais não devem ser adicionados, incluindo `.venv`, caches, `.env` e `.streamlit/secrets.toml`. Antes de registrar alterações:

```bash
git status --short
git check-ignore .streamlit/secrets.toml
git ls-files .streamlit/secrets.toml
```

O segundo comando deve mostrar o caminho ignorado; o terceiro não deve listar nada. Ignorar um arquivo não remove versões já registradas no Git. Se uma chave vazar, revogue-a no provedor.

Revise os arquivos e registre apenas o trabalho do projeto. Exemplo, para uma cópia didática nova:

```bash
git add .
git commit -m "Cria chatbot de estudos com Streamlit"
git push
```

`git add .` prepara os arquivos desta pasta, `git commit` guarda uma versão e `git push` envia essa versão ao GitHub. Antes de enviar, confira a lista que aparece em `git status` e nunca inclua sua chave da API. O professor ou a equipe deve compartilhar o endereço e as permissões do repositório.

Se a entrega for por arquivo compactado, selecione os arquivos do projeto e exclua `.venv`, `.git`, configurações pessoais do editor e segredos. Acrescente prints sem credenciais e o registro dos testes reais realizados.

## 15 Conferir o aprendizado

Antes do seminário, tente responder sem ler o código:

1. Qual problema o projeto resolve e quais são suas entradas e saídas?
2. O que o ambiente virtual isola e o que o pip instala?
3. Qual a diferença entre módulo, pacote e biblioteca?
4. Quais importações são nossas e quais vêm de terceiros?
5. Por que usamos `session_state` em vez de uma lista comum?
6. Por que enviamos o histórico para a API?
7. Qual a diferença entre `return` e `yield`?
8. O que ocorre se a conexão cair no meio da resposta?
9. Onde fica a chave e por que ela não vai para o GitHub?
10. Quais resultados ainda precisam ser conferidos com o material da disciplina?

Use as referências do [README](../README.md) e o [roteiro de apresentação](apresentacao.md) para aprofundar e demonstrar essas respostas.

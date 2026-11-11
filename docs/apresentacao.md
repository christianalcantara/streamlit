# Roteiro do seminário sobre chatbot com IA

Prepare uma apresentação de aproximadamente 8 a 10 minutos, ajustando ao tempo definido pelo professor. O foco é demonstrar o tema 4, descrito nas páginas 11 e 12. A organização abaixo acompanha a estrutura sugerida na página 14.

## 1 Título e integrantes

**Assistente de estudos com Python, Streamlit e API Gemini.** Preencha os nomes dos integrantes, a turma e a data nos slides da equipe.

Explique: “Criamos um chatbot para revisar conceitos de programação e eletricidade, com histórico e respostas exibidas enquanto chegam.”

## 2 Problema e objetivo

O estudante pode precisar de outro exemplo ou querer continuar uma explicação. O objetivo é permitir perguntas em linguagem natural, preservando o contexto durante a sessão.

Exemplo de uso: calcular a corrente em um resistor e depois perguntar o que acontece quando a tensão dobra.

## 3 Ferramentas e decisões

- Python controla o fluxo e organiza os dados.
- Streamlit cria a interface sem escrever HTML ou JavaScript.
- O SDK Google Gen AI facilita o acesso à API Gemini.
- Git registra versões e o GitHub pode hospedar o código.

Escolhemos apenas uma tela e um módulo auxiliar para facilitar a leitura. Não há banco de dados, cadastro nem treinamento de IA. O modelo já existe no serviço do provedor.

## 4 Funcionamento

Mostre este fluxo em um slide:

```text
Pergunta -> interface Streamlit -> histórico -> módulo Gemini
                                                    |
                                                    v
Tela com texto em partes <- gerador Python <- API de IA
```

Abra o código para mostrar três pontos:

1. `st.session_state.mensagens`: mantém a conversa entre reexecuções.
2. `from utils.gemini import ...`: importa nossa função de outro módulo.
3. `yield` com `st.write_stream`: entrega e apresenta os trechos da resposta.

Explique que enviamos o histórico ao modelo. Apenas exibir mensagens antigas não daria contexto à API.

## 5 Demonstração ao vivo

Antes de começar, confira internet, chave, modelo e cota. Abra o app na tela de conversa, sem abrir o arquivo de segredos durante a apresentação.

1. Pergunte: “Um resistor de 10 ohms está ligado a 12 volts. Calcule a corrente e explique a fórmula.”
2. Observe a resposta sendo escrita em partes. Confira o cálculo: `I = V / R = 12 / 10 = 1,2 A`.
3. Pergunte: “E se a tensão dobrar, mantendo o mesmo resistor?”. Confira: `2,4 A`.
4. Mostre que a resposta usa o contexto anterior.
5. Clique em **Limpar conversa** e mostre que o histórico desapareceu.
6. Demonstre uma falha já ensaiada, como modelo inexistente, em uma configuração de teste. Restaure o modelo correto em seguida.

Se o serviço ficar indisponível, mostre as evidências gravadas de uma execução real anterior e os exemplos sem IA. Identifique claramente os exemplos como simulações e explique a dependência externa. Não apresente eco ou testes simulados como integração real.

## 6 Testes e resultados

Execute antes do seminário:

```bash
python -m unittest discover -s tests -v
```

Mostre uma evidência dos testes e outra do chatbot usando a API real. Preencha o registro de testes em `docs/testes.md` com o que a equipe de fato observou.

Não afirme que todo resultado de IA é correto. Relate o comportamento observado: contexto preservado, texto chegando em partes, conversa limpa e erros tratados. Dê um exemplo de resposta que foi conferida no material da disciplina.

## 7 Dificuldades e limitações

Explique as dificuldades que a equipe realmente encontrou. Possíveis pontos para discutir: entender a reexecução do Streamlit, converter o papel `assistant` para `model` e receber respostas incrementalmente.

Limitações: a IA pode errar; o serviço precisa de internet e tem cotas; o histórico dura apenas a sessão; respostas têm limite de tamanho. Perguntas e histórico são enviados ao provedor. O PDF da atividade não é uma fonte consultada automaticamente pelo chatbot.

## 8 Conclusão e referências

Conclua explicando o que aprenderam: entrada e saída, variáveis, listas, dicionários, módulos, funções, estado de sessão, API, geradores e exceções.

Use as referências oficiais listadas no README e identifique o material de Informática Aplicada do professor Allan Pinto, tema 4, páginas 11 e 12. Se fizerem melhorias futuras, comecem por exportar a conversa ou publicar o app.

## Checklist da entrega

- [ ] Integrantes e turma preenchidos nos slides.
- [ ] Código comentado e instruções conferidas em outro ambiente.
- [ ] API real funcionando com a configuração da equipe.
- [ ] Demonstração de contexto e streaming ensaiada.
- [ ] Falhas e limitações compreendidas.
- [ ] Testes executados e evidências reais registradas.
- [ ] Referências incluídas nos slides.
- [ ] Nenhuma chave em código, prints, slides, repositório ou ZIP.
- [ ] Repositório ou arquivo compactado preparado conforme orientação do professor.

import streamlit as st

st.markdown(
    "Este app foi feito como **trabalho escolar** para demonstrar o "
    "[Streamlit](https://streamlit.io), uma biblioteca Python que transforma scripts "
    "em aplicações web interativas — sem precisar escrever HTML, CSS ou JavaScript."
)

with st.container(horizontal=True):
    st.badge("Python", icon=":material/code:", color="blue")
    st.badge("Streamlit", icon=":material/rocket_launch:", color="red")
    st.badge("Google Gemini", icon=":material/smart_toy:", color="violet")
    st.badge("Streamlit Community Cloud", icon=":material/cloud:", color="green")

st.subheader("O que tem aqui", divider="gray")

with st.container(horizontal=True):
    with st.container(border=True, height="stretch"):
        st.markdown("**:material/smart_toy: Chatbot Gemini**")
        st.caption("Chat com IA e respostas em tempo real (streaming), usando `st.chat_message` e `st.write_stream`.")
        st.page_link("app_pages/chat.py", label="Abrir chatbot", icon=":material/arrow_forward:")
    # with st.container(border=True, height="stretch"):
    #     st.markdown("**:material/tune: Widgets**")
    #     st.caption("Entradas do usuário: sliders, seletores, datas, cores, formulários e upload de arquivos.")
    #     st.page_link("app_pages/widgets.py", label="Ver widgets", icon=":material/arrow_forward:")
    # with st.container(border=True, height="stretch"):
    #     st.markdown("**:material/bar_chart: Dados e gráficos**")
    #     st.caption("Métricas, gráficos, mapas e tabelas interativas com pandas.")
    #     st.page_link("app_pages/dados.py", label="Ver dados", icon=":material/arrow_forward:")
    # with st.container(border=True, height="stretch"):
    #     st.markdown("**:material/dashboard: Layout e status**")
    #     st.caption("Colunas, abas, expansores, diálogos, alertas e barras de progresso.")
    #     st.page_link("app_pages/layout.py", label="Ver layout", icon=":material/arrow_forward:")

st.subheader("Como o Streamlit funciona", divider="gray")

st.markdown(
    """
1. Você escreve um script Python comum.
2. Cada comando `st.*` desenha um elemento na tela.
3. Quando o usuário interage com um widget, **o script inteiro roda de novo**, de cima para baixo.
4. Para guardar informações entre essas execuções, usamos `st.session_state`.
"""
)

st.code(
    '''import streamlit as st

nome = st.text_input("Qual é o seu nome?")
if nome:
    st.write(f"Olá, {nome}! 👋")''',
    language="python",
)

nome = st.text_input("Teste aqui: qual é o seu nome?")
if nome:
    st.success(f"Olá, {nome}! 👋")

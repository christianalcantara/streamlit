import time

import streamlit as st

# ---------------------------------------------------------------
# Texto formatado
# ---------------------------------------------------------------
st.subheader("Texto formatado", divider="gray")
st.markdown(
    "Markdown com **negrito**, *itálico*, `código`, :red[cores], :blue-background[fundo] "
    "e ícones :material/favorite:."
)
st.latex(r"E = mc^2 \qquad \int_0^1 x^2\,dx = \frac{1}{3}")
st.code("for i in range(3):\n    print('Olá, Streamlit!')", language="python")

# ---------------------------------------------------------------
# Colunas e containers
# ---------------------------------------------------------------
st.subheader("Colunas e containers", divider="gray")
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    with st.container(border=True, height="stretch"):
        st.markdown("**Coluna larga (2/4)**")
        st.caption("`st.columns([2, 1, 1])` divide o espaço em proporções.")
with col2:
    with st.container(border=True, height="stretch"):
        st.markdown("**Coluna (1/4)**")
with col3:
    with st.container(border=True, height="stretch"):
        st.markdown("**Coluna (1/4)**")

# ---------------------------------------------------------------
# Abas, expansor, popover e diálogo
# ---------------------------------------------------------------
st.subheader("Abas, expansor, popover e diálogo", divider="gray")
aba1, aba2, aba3 = st.tabs([":material/info: Sobre", ":material/school: Escola", ":material/group: Equipe"])
with aba1:
    st.write("Conteúdo da primeira aba.")
with aba2:
    st.write("Conteúdo da segunda aba.")
with aba3:
    st.write("Conteúdo da terceira aba.")

with st.expander("Clique para expandir", icon=":material/expand_more:"):
    st.write("Conteúdo escondido que aparece quando o expansor é aberto.")


@st.dialog("Exemplo de diálogo")
def abrir_dialogo():
    st.write("Isto é uma janela modal criada com `@st.dialog`.")
    resposta = st.text_input("Qual sua matéria favorita?")
    if st.button("Confirmar", type="primary"):
        st.session_state.materia_favorita = resposta
        st.rerun()


with st.container(horizontal=True):
    with st.popover("Abrir popover", icon=":material/chat_bubble:"):
        st.write("Um popover é um pequeno painel flutuante.")
        st.checkbox("Opção dentro do popover")
    if st.button("Abrir diálogo", icon=":material/open_in_new:"):
        abrir_dialogo()

if "materia_favorita" in st.session_state:
    st.write(f"Matéria favorita (vinda do diálogo): **{st.session_state.materia_favorita}**")

# ---------------------------------------------------------------
# Alertas
# ---------------------------------------------------------------
st.subheader("Alertas", divider="gray")
col1, col2 = st.columns(2)
with col1:
    st.success("Operação concluída.", title="Sucesso", icon=":material/check_circle:")
    st.info("Informação útil para o usuário.", title="Informação", icon=":material/info:")
with col2:
    st.warning("Algo merece atenção.", title="Aviso", icon=":material/warning:")
    st.error("Algo deu errado.", title="Erro", icon=":material/error:")

# ---------------------------------------------------------------
# Progresso e status
# ---------------------------------------------------------------
st.subheader("Progresso e status", divider="gray")
if st.button("Simular processamento", icon=":material/play_arrow:", type="primary"):
    with st.status("Processando dados...", expanded=True) as status:
        barra = st.progress(0, text="Iniciando")
        etapas = ["Baixando dados", "Limpando dados", "Treinando modelo", "Gerando relatório"]
        for i, etapa in enumerate(etapas, start=1):
            st.write(f":material/check: {etapa}")
            barra.progress(i / len(etapas), text=etapa)
            time.sleep(0.6)
        status.update(label="Processamento concluído!", state="complete", expanded=False)
    st.toast("Tudo pronto!", icon=":material/done_all:")

if st.button("Mostrar spinner", icon=":material/progress_activity:"):
    with st.spinner("Carregando..."):
        time.sleep(2)
    st.success("Carregado!", icon=":material/check:")

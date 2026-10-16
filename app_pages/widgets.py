import datetime

import streamlit as st

st.caption("Widgets são os elementos de entrada. Cada interação faz o script rodar de novo.")

# ---------------------------------------------------------------
# Texto e números
# ---------------------------------------------------------------
st.subheader("Texto e números", divider="gray")
col1, col2 = st.columns(2)
with col1:
    texto = st.text_input("Texto curto", placeholder="Digite algo")
    numero = st.number_input("Número", min_value=0, max_value=100, value=42)
    area = st.text_area("Texto longo", placeholder="Escreva um parágrafo")
with col2:
    idade = st.slider("Slider", 0, 100, 25)
    faixa = st.slider("Slider de intervalo", 0, 100, (20, 80))
    nivel = st.select_slider("Select slider", ["Baixo", "Médio", "Alto", "Máximo"], value="Médio")

with st.expander("Valores lidos", icon=":material/data_object:"):
    st.json(
        {
            "texto": texto,
            "numero": numero,
            "area": area,
            "idade": idade,
            "faixa": faixa,
            "nivel": nivel,
        }
    )

# ---------------------------------------------------------------
# Seleção
# ---------------------------------------------------------------
st.subheader("Seleção", divider="gray")
col1, col2 = st.columns(2)
with col1:
    linguagem = st.selectbox("Selectbox", ["Python", "JavaScript", "Java", "C", "Rust"])
    frutas = st.multiselect("Multiselect", ["Maçã", "Banana", "Uva", "Manga", "Laranja"], default=["Manga"])
    turno = st.segmented_control("Segmented control", ["Manhã", "Tarde", "Noite"], default="Manhã")
with col2:
    materias = st.pills(
        "Pills (seleção múltipla)",
        ["Matemática", "Português", "História", "Física"],
        selection_mode="multi",
        default=["Matemática"],
    )
    aceito = st.checkbox("Checkbox: aceito os termos")
    modo = st.toggle("Toggle: modo avançado")
    st.write(
        f"Você escolheu **{linguagem}**, {len(frutas)} fruta(s), turno **{turno}**, "
        f"{len(materias)} matéria(s). Termos: {aceito}. Modo avançado: {modo}."
    )

# ---------------------------------------------------------------
# Datas, cores e avaliação
# ---------------------------------------------------------------
st.subheader("Datas, cores e avaliação", divider="gray")
col1, col2, col3 = st.columns(3)
with col1:
    data = st.date_input("Data", datetime.date.today(), format="DD/MM/YYYY")
    hora = st.time_input("Hora", datetime.time(14, 30))
with col2:
    cor = st.color_picker("Cor favorita", "#FF4B4B")
    st.markdown(f"Cor escolhida: `{cor}`")
with col3:
    st.markdown("Quanto você gostou do app?")
    estrelas = st.feedback("stars")
    if estrelas is not None:
        st.write(f"Você deu {estrelas + 1} estrela(s)!")

# ---------------------------------------------------------------
# Botões
# ---------------------------------------------------------------
st.subheader("Botões", divider="gray")
with st.container(horizontal=True, vertical_alignment="center"):
    if st.button("Comemorar", icon=":material/celebration:", type="primary"):
        st.balloons()
    if st.button("Nevar", icon=":material/ac_unit:"):
        st.snow()
    if st.button("Notificação", icon=":material/notifications:"):
        st.toast("Isto é um st.toast!", icon=":material/check_circle:")
    acao = st.menu_button(
        "Menu button",
        ["Copiar", "Compartilhar", "Arquivar"],
        icon=":material/more_vert:",
    )
    st.link_button("Documentação", "https://docs.streamlit.io", icon=":material/open_in_new:")
if acao:
    st.toast(f"Ação escolhida: {acao}")

# ---------------------------------------------------------------
# Formulário
# ---------------------------------------------------------------
st.subheader("Formulário", divider="gray")
st.caption("Dentro de um `st.form`, o script só roda de novo quando o botão de envio é clicado.")
with st.form("cadastro", border=True):
    nome = st.text_input("Nome")
    email = st.text_input("E-mail")
    serie = st.selectbox("Série", ["1º ano", "2º ano", "3º ano"])
    enviado = st.form_submit_button("Enviar", icon=":material/send:", type="primary")

if enviado:
    if nome and email:
        st.success(f"Cadastro de **{nome}** ({serie}) enviado!", icon=":material/check:")
    else:
        st.warning("Preencha nome e e-mail.", icon=":material/warning:")

# ---------------------------------------------------------------
# Upload de arquivos
# ---------------------------------------------------------------
st.subheader("Upload de arquivos", divider="gray")
arquivo = st.file_uploader("Envie uma imagem", type=["png", "jpg", "jpeg"])
if arquivo:
    st.image(arquivo, caption=arquivo.name, width=300, alt=f"Imagem enviada: {arquivo.name}")

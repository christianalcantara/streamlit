"""
Ponto de entrada do app (Streamlit Community Cloud procura este arquivo).

Como rodar localmente:
    uv pip install -r requirements.txt
    streamlit run streamlit_app.py
"""

import streamlit as st

st.set_page_config(
    page_title="Demonstração do Streamlit",
    page_icon=":material/rocket_launch:",
    layout="wide",
)

pagina = st.navigation(
    {
        "": [
            st.Page("app_pages/inicio.py", title="Início", icon=":material/home:", default=True),
            st.Page("app_pages/chat.py", title="Chatbot Gemini", icon=":material/smart_toy:"),
        ],
        "Componentes": [
            st.Page("app_pages/widgets.py", title="Widgets", icon=":material/tune:", visibility="hidden"),
            st.Page("app_pages/dados.py", title="Dados e gráficos", icon=":material/bar_chart:", visibility="hidden"),
            st.Page("app_pages/layout.py", title="Layout e status", icon=":material/dashboard:", visibility="hidden"),
        ],
    },
    position="sidebar",
)

st.title(pagina.title, icon=pagina.icon)
pagina.run()

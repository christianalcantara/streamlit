import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

CAPITAIS = pd.DataFrame(
    {
        "cidade": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Fortaleza", "Belo Horizonte", "Manaus", "Curitiba", "Recife", "Porto Alegre"],
        "lat": [-23.55, -22.91, -15.79, -12.97, -3.72, -19.92, -3.12, -25.43, -8.05, -30.03],
        "lon": [-46.63, -43.17, -47.88, -38.50, -38.54, -43.94, -60.02, -49.27, -34.88, -51.23],
        "populacao_mi": [11.45, 6.21, 2.82, 2.42, 2.43, 2.32, 2.06, 1.77, 1.49, 1.33],
    }
)


@st.cache_data(ttl="1h")
def carregar_vendas() -> pd.DataFrame:
    """Gera dados fictícios de vendas. Em um app real, aqui leríamos um CSV ou banco."""
    rng = np.random.default_rng(42)
    datas = pd.date_range("2026-01-01", periods=180, freq="D")
    produtos = ["Caderno", "Caneta", "Mochila", "Livro"]
    linhas = []
    for produto, base in zip(produtos, [120, 300, 40, 80]):
        tendencia = np.linspace(0, base * 0.4, len(datas))
        vendas = base + tendencia + rng.normal(0, base * 0.15, len(datas))
        linhas.append(pd.DataFrame({"data": datas, "produto": produto, "vendas": vendas.round().clip(0)}))
    return pd.concat(linhas, ignore_index=True)


vendas = carregar_vendas()

# ---------------------------------------------------------------
# Filtros (rápidos, fora da função em cache)
# ---------------------------------------------------------------
with st.container(horizontal=True, vertical_alignment="bottom"):
    produtos = st.pills(
        "Produtos",
        sorted(vendas["produto"].unique()),
        selection_mode="multi",
        default=sorted(vendas["produto"].unique()),
    )
    periodo = st.segmented_control("Período", ["30 dias", "90 dias", "Tudo"], default="Tudo", required=True)

dias = {"30 dias": 30, "90 dias": 90, "Tudo": None}[periodo]
filtrado = vendas[vendas["produto"].isin(produtos)]
if dias:
    filtrado = filtrado[filtrado["data"] > filtrado["data"].max() - pd.Timedelta(days=dias)]

if filtrado.empty:
    st.warning("Selecione pelo menos um produto.", icon=":material/filter_alt_off:")
    st.stop()

# ---------------------------------------------------------------
# Métricas
# ---------------------------------------------------------------
diario = filtrado.groupby("data")["vendas"].sum()
metade = len(diario) // 2
variacao = (diario.iloc[metade:].mean() / diario.iloc[:metade].mean() - 1) * 100

with st.container(horizontal=True):
    st.metric(
        "Total vendido",
        f"{int(diario.sum()):,}".replace(",", "."),
        f"{variacao:.1f}%",
        border=True,
        chart_data=diario.resample("W").sum(),
        chart_type="area",
    )
    st.metric(
        "Média diária",
        f"{diario.mean():.0f}",
        f"{variacao:.1f}%",
        border=True,
        chart_data=diario.resample("W").mean(),
        chart_type="line",
    )
    st.metric(
        "Melhor dia",
        f"{int(diario.max())}",
        diario.idxmax().strftime("%d/%m"),
        delta_color="off",
        delta_arrow="off",
        border=True,
        chart_data=diario.resample("W").max(),
        chart_type="bar",
    )

# ---------------------------------------------------------------
# Gráficos
# ---------------------------------------------------------------
tabela_larga = filtrado.pivot_table(index="data", columns="produto", values="vendas")

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.markdown("**Vendas por dia** · `st.line_chart`")
        st.line_chart(tabela_larga, y_label="Vendas", alt="Vendas diárias por produto")
with col2:
    with st.container(border=True):
        st.markdown("**Total por produto** · `st.bar_chart`")
        st.bar_chart(
            filtrado.groupby("produto", as_index=False)["vendas"].sum(),
            x="produto",
            y="vendas",
            horizontal=True,
            alt="Total de vendas por produto",
        )

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.markdown("**Vendas acumuladas** · `st.area_chart`")
        st.area_chart(tabela_larga.cumsum(), alt="Vendas acumuladas por produto")
with col2:
    with st.container(border=True):
        st.markdown("**Distribuição de vendas** · `st.altair_chart`")
        grafico = (
            alt.Chart(filtrado)
            .mark_boxplot()
            .encode(x=alt.X("produto:N", title="Produto"), y=alt.Y("vendas:Q", title="Vendas"), color="produto:N")
        )
        st.altair_chart(grafico, alt="Boxplot da distribuição de vendas por produto")

# ---------------------------------------------------------------
# Mapa
# ---------------------------------------------------------------
st.subheader("Mapa", divider="gray")
st.map(CAPITAIS, size="populacao_mi", zoom=3, height=400, alt="Mapa das 10 maiores capitais do Brasil")

# ---------------------------------------------------------------
# Tabelas
# ---------------------------------------------------------------
st.subheader("Tabelas", divider="gray")
tab_ver, tab_editar = st.tabs(["Visualizar (st.dataframe)", "Editar (st.data_editor)"])

with tab_ver:
    st.dataframe(
        CAPITAIS,
        hide_index=True,
        column_config={
            "cidade": st.column_config.TextColumn("Cidade"),
            "lat": st.column_config.NumberColumn("Latitude", format="%.2f"),
            "lon": st.column_config.NumberColumn("Longitude", format="%.2f"),
            "populacao_mi": st.column_config.ProgressColumn(
                "População (mi)", min_value=0, max_value=12, format="%.2f"
            ),
        },
        alt="Capitais brasileiras com coordenadas e população",
    )

with tab_editar:
    st.caption("Clique nas células para editar, ou adicione linhas no final.")
    tarefas = st.data_editor(
        pd.DataFrame(
            {
                "tarefa": ["Estudar Streamlit", "Fazer o app", "Publicar no Cloud"],
                "concluida": [True, True, False],
                "prioridade": ["Alta", "Alta", "Média"],
            }
        ),
        num_rows="dynamic",
        hide_index=True,
        column_config={
            "tarefa": st.column_config.TextColumn("Tarefa"),
            "concluida": st.column_config.CheckboxColumn("Concluída"),
            "prioridade": st.column_config.SelectboxColumn("Prioridade", options=["Baixa", "Média", "Alta"]),
        },
        key="tarefas",
        alt="Lista de tarefas editável",
    )
    concluidas = int(tarefas["concluida"].fillna(False).sum())
    st.progress(concluidas / max(len(tarefas), 1), text=f"{concluidas} de {len(tarefas)} tarefas concluídas")

st.download_button(
    "Baixar vendas filtradas (CSV)",
    data=filtrado.to_csv(index=False),
    file_name="vendas.csv",
    mime="text/csv",
    icon=":material/download:",
    on_click="ignore",
)

import streamlit as st
import pandas as pd
import folium
import plotly.express as px
from streamlit_folium import folium_static

# Carregar os dados
@st.cache_data
def load_data():
    df = pd.read_csv("data/dataset.csv", delimiter=",")  # Ajuste o delimitador se necessário

    # Converter colunas de Latitude e Longitude para número (evita erro no mapa)
    df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")

    return df

df = load_data()

# Título do dashboard
st.title("📊 Dashboard de Escolas")

# -------- FILTRO POR MUNICÍPIO --------

cidade = st.selectbox("🔍 Selecione o município:", options=df["Município"].unique())

# Filtrar os dados pela cidade selecionada
df_filtered = df[df["Município"] == cidade]

st.write(f"### 🎓 Escolas em {cidade}")
st.dataframe(df_filtered)

# -------- GRÁFICOS --------

# 🥧 Gráfico de Pizza - Categoria da Escola
if "Categoria Escola Privada" in df.columns:
    st.write("### 🎭 Distribuição das Escolas Privadas")
    categoria_privada = df["Categoria Escola Privada"].value_counts().reset_index()
    categoria_privada.columns = ["Categoria", "Quantidade"]

    fig_pizza = px.pie(categoria_privada, names="Categoria", values="Quantidade",
                        title="Distribuição das Escolas Privadas", color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_pizza)

# 📈 Gráfico de Histograma - Tamanho da Escola
if "Porte da Escola" in df.columns:
    st.write("### 📏 Tamanho das Escolas")
    fig_hist = px.histogram(df, x="Porte da Escola", title="Distribuição do Porte das Escolas",
                             color="Porte da Escola", color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_hist)

# Remover escolas sem Latitude/Longitude
df_filtered = df_filtered.dropna(subset=["Latitude", "Longitude"])

# Verificar se há coordenadas para exibir no mapa
if df_filtered.empty:
    st.warning("⚠️ Nenhuma escola com coordenadas disponíveis para este município.")
else:
    # Criar mapa
    st.write("### 🗺️ Mapa das Escolas")

    m = folium.Map(location=[df_filtered["Latitude"].mean(), df_filtered["Longitude"].mean()], zoom_start=12)

    for _, row in df_filtered.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=f"{row['Escola']}",
            tooltip=row["Escola"]
        ).add_to(m)

    folium_static(m)

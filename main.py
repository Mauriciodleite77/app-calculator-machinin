import base64
import streamlit as st
import math
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def gerar_pdf(ferramenta, material, tipo, D, Z, Vc, n, avanco):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    y = 800
    linhas = [
        f"Ferramenta: {ferramenta.upper()}",
        f"Material: {material}",
        f"Tipo da Ferramenta: {tipo}",
        f"Diâmetro: {D:.2f} mm",
        f"Nº de dentes: {Z}",
        f"Vc: {Vc} m/min",
        f"Rotação (n): {n:.0f} rpm",
        f"Avanço: {avanco:.1f} mm/min"
    ]
    for linha in linhas:
        c.drawString(50, y, linha)
        y -= 20
    c.save()
    buffer.seek(0)
    return buffer

st.set_page_config(page_title="Calculator Machining", layout="centered")

# Função para aplicar imagem de fundo
def set_background(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Chama a função de fundo
set_background("drill-milling-milling-machine-drilling-50691.jpeg")
###ffffff
# CSS com div escura + estilos aplicados corretamente
custom_css = """
<style>
    .stApp {
        color: white
    }
    h1, h2, h3 {
        color: black;
        text-shadow: 1px 1px 3px black;
    }
    label, .stSelectbox label, .stNumberInput label {
        color: white !important;
    }
</style>
"""

# Aplica o estilo
st.markdown(custom_css, unsafe_allow_html=True)

# Começa a div personalizada
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Coloca o título DENTRO da div estilizada
##st.title("Cálculo de Velocidade de Corte")
st.markdown("---")


# Dados ISO base
dados_materiais = {
    'broca': {
        "Aço baixo carbono (P1)":        {'Vc_b': 30,  'Vc_md': 100, 'fz': 0.08},
        "Aço temperado até 45 HRC (P5)": {'Vc_b': 16,  'Vc_md': 55,  'fz': 0.06},
        "Aço inoxidável (M1)":           {'Vc_b': 15,  'Vc_md': 45,  'fz': 0.07},
        "Alumínio 6352 (N1)":            {'Vc_b': 100, 'Vc_md': 500, 'fz': 0.20},
        "Cobre / Latão (N2)":            {'Vc_b': 80,  'Vc_md': 240, 'fz': 0.16},
        "Titânio (S1)":                  {'Vc_b': 15,  'Vc_md': 40,  'fz': 0.05},
        "Poliacetal (POM / Delrin)":     {'Vc_b': 150, 'Vc_md': 350, 'fz': 0.20},
    },
    'fresa': {
        "Aço baixo carbono (P1)":        {'Vc_b': 25,  'Vc_md': 120, 'fz': 0.10},
        "Aço temperado até 45 HRC (P5)": {'Vc_b': 14,  'Vc_md': 60,  'fz': 0.08},
        "Aço inoxidável (M1)":           {'Vc_b': 12,  'Vc_md': 40,  'fz': 0.10},
        "Alumínio 6352 (N1)":            {'Vc_b': 100, 'Vc_md': 500, 'fz': 0.30},
        "Cobre / Latão (N2)":            {'Vc_b': 90,  'Vc_md': 260, 'fz': 0.20},
        "Titânio (S1)":                  {'Vc_b': 12,  'Vc_md': 40,  'fz': 0.06},
        "Poliacetal (POM / Delrin)":     {'Vc_b': 150, 'Vc_md': 350, 'fz': 0.25},
    }
}

st.title("Calculator Machining")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    ferramenta = st.selectbox("Tipo de Ferramenta", list(dados_materiais.keys()))

with col2:
    tipo = st.selectbox("Tipo da Ferramenta", ["HSS", "MD"])

material = st.selectbox("Material da Peça", list(dados_materiais[ferramenta].keys()))

col3, col4 = st.columns(2)

with col3:
    D = st.number_input("Diâmetro da ferramenta (mm)", min_value=0.1, step=0.1)

with col4:
    Z = st.number_input("Nº de dentes", min_value=1, step=1)

if st.button("Calcular"):
    dados = dados_materiais[ferramenta][material]
    Vc = dados['Vc_b'] if tipo == 'HSS' else dados['Vc_md']
    fz = dados['fz']

    n = (Vc * 1000) / (math.pi * D) if D > 0 else 0
    avanco = fz * Z * n

    st.markdown("### Resultado:")
    st.success(f"""
    - **Ferramenta**: {ferramenta.upper()}
    - **Material**: {material}
    - **Tipo da Ferramenta**: {tipo}
    - **Diâmetro**: {D:.2f} mm
    - **Nº de dentes**: {Z}
    - **Vc**: {Vc} m/min
    - **Rotação (n)**: {n:.0f} rpm
    - **Avanço**: {avanco:.1f} mm/min
    """)

    # Gráfico
    d_vals = [i for i in range(1, 51)]
    n_vals = [(Vc * 1000) / (math.pi * d) for d in d_vals]

    fig, ax = plt.subplots()
    ax.plot(d_vals, n_vals, label="n = f(D)")
    ax.set_xlabel("Diâmetro (mm)")
    ax.set_ylabel("Rotação (rpm)")
    ax.set_title("Rotação vs Diâmetro")
    ax.grid(True)
    st.pyplot(fig)

    # Exportar PDF
    if st.download_button("Exportar PDF", data=gerar_pdf(
        ferramenta, material, tipo, D, Z, Vc, n, avanco
    ), file_name="resultado.pdf"):
        st.success("PDF gerado com sucesso!")

# Fechamento da div principal
st.markdown("</div>", unsafe_allow_html=True)

# Função para gerar PDF


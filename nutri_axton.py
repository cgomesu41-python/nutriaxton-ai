import os
import json
import streamlit as st
from openai import OpenAI
from pypdf import PdfReader

# =========================
# CAMINHOS
# =========================
BASE_DIR = os.path.dirname(__file__)                 # pasta /main
ROOT_DIR = os.path.dirname(BASE_DIR)                 # pasta raiz do projeto

ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
BASE_TXT_PATH = os.path.join(BASE_DIR, "base_nutriaxton.txt")
LOGO_PATH = os.path.join(ASSETS_DIR, "logo.png")
PRECOS_PATH = os.path.join(DOCS_DIR, "tabela_preco.json")

# =========================
# CAMINHOS
# =========================
BASE_DIR = os.path.dirname(__file__)                 # pasta /main
ROOT_DIR = os.path.dirname(BASE_DIR)                 # pasta raiz do projeto

ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
BASE_TXT_PATH = os.path.join(BASE_DIR, "base_nutriaxton.txt")
LOGO_PATH = os.path.join(ASSETS_DIR, "logo.png")

# =========================
# CONFIG DA PÁGINA
# =========================

st.set_page_config(
    page_title="Nutri Intelligent",
    page_icon="🌿",
    layout="wide"
)

st.link_button(
    "🌐 Acessar site da Nutriaxton",
    "https://nutriaxton.com"
)

# =========================
# CSS / ESTILO
# =========================
st.markdown("""
<style>
:root {
    --bg: #050816;
    --panel: #0B1220;
    --card: #0F172A;
    --line: #1F2937;
    --text: #F8FAFC;
    --muted: #94A3B8;
    --brand: #10B981;
}

html, body, [class*="css"] {
    color: var(--text);
}

.stApp {
    background: linear-gradient(180deg, #030712 0%, #06101f 100%);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1220px;
}

h1, h2, h3 {
    color: var(--text) !important;
    letter-spacing: -0.02em;
}

p, label, div {
    color: var(--text);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #081225 0%, #0A1020 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}

.stChatMessage {
    border-radius: 16px;
    padding: 10px;
    background: rgba(255,255,255,0.02);
}

.stButton > button, .stLinkButton > a {
    width: 100%;
    border-radius: 14px !important;
    border: 1px solid rgba(16,185,129,0.35) !important;
    background: rgba(16,185,129,0.08) !important;
    color: #ECFDF5 !important;
    font-weight: 600 !important;
}

.stButton > button:hover, .stLinkButton > a:hover {
    border-color: rgba(16,185,129,0.8) !important;
    background: rgba(16,185,129,0.14) !important;
}

.card-box {
    background: linear-gradient(180deg, #0B1324 0%, #0A162B 100%);
    border: 1px solid rgba(16,185,129,0.16);
    border-radius: 20px;
    padding: 22px;
    min-height: 250px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.25);
    transition: transform .18s ease, border-color .18s ease;
}

.card-box:hover {
    transform: translateY(-3px);
    border-color: rgba(16,185,129,0.45);
}

.hero-sub {
    color: var(--muted);
    font-size: 1.03rem;
    margin-top: .25rem;
    margin-bottom: 1rem;
}

.soft-line {
    height: 1px;
    background: linear-gradient(90deg, rgba(16,185,129,0), rgba(16,185,129,.35), rgba(16,185,129,0));
    margin: 1.2rem 0 1.8rem 0;
    border: 0;
}
</style>
""", unsafe_allow_html=True)

# =========================
# CLIENTE OPENAI
# =========================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# =========================
# FUNÇÕES
# =========================

PRECOS_PATH = os.path.join(DOCS_DIR, "tabela_preco.json")

texto_usuario = st.chat_input("Pergunte sobre suplementos, performance ou bem-estar")


def ler_base_txt():
    if os.path.exists(BASE_TXT_PATH):
        with open(BASE_TXT_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "Base textual da empresa não encontrada."

def buscar_preco(produto):
    produto = produto.lower()

    palavras_chave = ["creatina", "collaxton", "cartsin"]
    produto_encontrado = None

    for palavra in palavras_chave:
        if palavra in produto:
            produto_encontrado = palavra
            break

    if not produto_encontrado:
        return None

texto_usuario = st.chat_input("Pergunte sobre suplementos, performance ou bem-estar")

if texto_usuario:
    texto = texto_usuario.lower()

    if any(p in texto for p in [
        "preço",
        "preco",
        "quanto custa",
        "valor",
        "pix",
        "débito",
        "debito",
        "custa",
        "price"
    ]):
        resultado = buscar_preco(texto_usuario)

        if resultado:
            resposta = f"""
**Produto:** {resultado['produto']}

**Preço:** R$ {resultado['preco']}
**Débito:** R$ {resultado['debito']}
**PIX:** R$ {resultado['pix']}
"""
            st.chat_message("assistant").write(resposta)
            st.stop()


def ler_pdfs():
    texto = ""

    if os.path.exists(DOCS_DIR):
        for arquivo in os.listdir(DOCS_DIR):
            if arquivo.lower().endswith(".pdf"):
                caminho = os.path.join(DOCS_DIR, arquivo)
                try:
                    reader = PdfReader(caminho)
                    texto += f"\n\n===== DOCUMENTO: {arquivo} =====\n"
                    for page in reader.pages:
                        texto += (page.extract_text() or "") + "\n"
                except Exception as e:
                    texto += f"\n[Erro ao ler {arquivo}: {e}]\n"

    if not texto.strip():
        texto = "Nenhum PDF foi encontrado ou lido na pasta docs."

    return texto

# =========================
# LEITURA DAS BASES
# =========================
base_empresa = ler_base_txt()
base_pdf = ler_pdfs()

# =========================
# SYSTEM PROMPT
# =========================
SYSTEM_PROMPT = f"""
Você é a Nutri Intelligent, assistente oficial da Nutriaxton.

Use como base principal da empresa o conteúdo abaixo:

{base_empresa}

Além disso, use os documentos oficiais abaixo como referência complementar
para produtos, valores, identidade visual, logo, cores e demais detalhes:

{base_pdf}

Regras:
- Responda em português, salvo se o usuário pedir outro idioma.
- Use apenas informações presentes na base textual e nos documentos oficiais.
- Não invente produtos, preços, benefícios, ingredientes ou características.
- Os produtos atuais da base são: Creatina Nutriaxton, Collaxton Q-10 e Cartsin.
- Se o usuário perguntar sobre preço, use os valores encontrados nos documentos.
- Se o usuário perguntar sobre logo, marca, design ou cores, use os dados presentes nos arquivos.
- Não faça promessas médicas exageradas.
- Quando não souber, diga com honestidade que a informação não foi encontrada na base atual.
- Fale com clareza, elegância, profissionalismo e tom comercial.
"""

# =========================
# ESTADO DA CONVERSA
# =========================
if "lista_mensagens" not in st.session_state:
    st.session_state["lista_mensagens"] = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## 🌿 Nutriaxton")
    st.write("Suplementos inteligentes")

    st.divider()

    st.markdown("**Produtos disponíveis**")
    st.write("Creatina Nutriaxton")
    st.write("Collaxton Q-10")
    st.write("Cartsin")

    st.divider()

# =========================
# HERO / TOPO
# =========================
if os.path.exists(LOGO_PATH):
    st.image(LOGO_PATH, width=220)

st.markdown("""
<h1 style='margin-bottom:0.2rem;'> Nutri Intelligent</h1>
<p class="hero-sub">Assistente inteligente da Nutriaxton</p>
""", unsafe_allow_html=True)

st.link_button("🌐 Acessar site da Nutriaxton", "https://www.nutriaxton.com.br/")

st.markdown('<div class="soft-line"></div>', unsafe_allow_html=True)

# =========================
# CARDS DE PRODUTOS
# =========================
st.markdown("## Nossos produtos")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="card-box">
        <h3>Creatina Nutriaxton</h3>
        <p>Suplemento voltado para desempenho, força e rotina esportiva.</p>
        <p><strong>Destaque:</strong> apoio à performance física.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card-box">
        <h3>Collaxton Q-10</h3>
        <p>Produto voltado para beleza, bem-estar e rotina de autocuidado.</p>
        <p><strong>Destaque:</strong> comunicação premium e elegante.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card-box">
        <h3>Cartsin</h3>
        <p>Produto da linha Nutriaxton com posicionamento de confiança e sofisticação.</p>
        <p><strong>Destaque:</strong> seguir sempre os documentos oficiais.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="soft-line"></div>', unsafe_allow_html=True)

# =========================
# HISTÓRICO DO CHAT
# =========================
for mensagem in st.session_state["lista_mensagens"]:
    if mensagem["role"] != "system":
        st.chat_message(mensagem["role"]).write(mensagem["content"])

# =========================
# INPUT
# =========================

if texto_usuario:
    st.session_state["lista_mensagens"].append(
        {"role": "user", "content": texto_usuario}
    )
    st.chat_message("user").write(texto_usuario)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            resposta = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state["lista_mensagens"],
                temperature=0.4
            )
            texto_resposta_ia = resposta.choices[0].message.content
            st.write(texto_resposta_ia)

    st.session_state["lista_mensagens"].append(
        {"role": "assistant", "content": texto_resposta_ia}
    )

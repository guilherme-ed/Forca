import streamlit as st
import random

# ─── Configuração da página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Jogo da Forca",
    page_icon="🎮",
    layout="centered"
)

# ─── Banco de palavras por categoria ─────────────────────────────────────────
PALAVRAS = {
    "🐾 Animais": [
        ("CACHORRO", "Melhor amigo do homem"),
        ("ELEFANTE", "O maior animal terrestre"),
        ("BORBOLETA", "Inseto com asas coloridas"),
        ("JACARE", "Réptil das águas brasileiras"),
        ("PAPAGAIO", "Ave que imita a fala humana"),
        ("TARTARUGA", "Animal com casco duro"),
        ("PINGUIM", "Ave que não voa, mas nada"),
        ("CAMALEAO", "Muda de cor para se camuflar"),
    ],
    "🌍 Países": [
        ("BRASIL", "País do carnaval e do futebol"),
        ("JAPAO", "Terra do sol nascente"),
        ("AUSTRALIA", "Continente e país ao mesmo tempo"),
        ("PORTUGAL", "Nossos irmãos de língua"),
        ("ARGENTINA", "Vizinho do futebol"),
        ("CANADA", "Tem a maior folha de maple"),
        ("MEXICO", "País das pirâmides astecas"),
        ("NORUEGA", "Terra dos fiordes e aurora boreal"),
    ],
    "💻 Tecnologia": [
        ("ALGORITMO", "Sequência de passos para resolver um problema"),
        ("INTELIGENCIA", "IA, o futuro da tecnologia"),
        ("STREAMLIT", "Framework Python para criar apps web"),
        ("PROGRAMACAO", "Arte de escrever código"),
        ("COMPUTADOR", "Máquina que processa dados"),
        ("INTERNET", "Rede global de computadores"),
        ("PYTHON", "Linguagem de programação popular"),
        ("GITHUB", "Plataforma de controle de versão"),
    ],
    "⚽ Esportes": [
        ("FUTEBOL", "Esporte mais popular do Brasil"),
        ("NATACAO", "Esporte aquático olímpico"),
        ("BASQUETE", "Esporte inventado por James Naismith"),
        ("VOLEIBOL", "Esporte da praia e da quadra"),
        ("TENIS", "Esporte com raquete e bola"),
        ("CICLISMO", "Esporte sobre duas rodas"),
        ("JUDÔ", "Arte marcial japonesa"),
        ("ATLETISMO", "Conjunto de provas olímpicas"),
    ],
}

MAX_ERROS = 6

# ─── Desenho da forca ─────────────────────────────────────────────────────────
FORCA = [
    """
```
  +---+
  |   |
      |
      |
      |
      |
=========
```""",
    """
```
  +---+
  |   |
  O   |
      |
      |
      |
=========
```""",
    """
```
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
```""",
    """
```
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========
```""",
    """
```
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========
```""",
    """
```
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========
```""",
    """
```
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
=========
```""",
]

# ─── Inicializar estado ───────────────────────────────────────────────────────
def iniciar_jogo(categoria=None):
    if categoria is None:
        categoria = random.choice(list(PALAVRAS.keys()))
    palavra, dica = random.choice(PALAVRAS[categoria])
    st.session_state.palavra = palavra
    st.session_state.dica = dica
    st.session_state.categoria = categoria
    st.session_state.letras_erradas = []
    st.session_state.letras_certas = []
    st.session_state.game_over = False
    st.session_state.vitoria = False

if "palavra" not in st.session_state:
    iniciar_jogo()
    st.session_state.vitorias = 0
    st.session_state.derrotas = 0

# ─── CSS customizado ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323:wght@400&display=swap');

/* Fundo preto */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #0a0a0a !important;
}

[data-testid="stHeader"] {
    background-color: #0a0a0a !important;
}

section[data-testid="stSidebar"] {
    background-color: #111111 !important;
}

/* Textos gerais brancos */
p, label, .stMarkdown, [data-testid="stText"] {
    color: #eeeeee !important;
}

/* Inputs */
input[type="text"] {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
    border-color: #444 !important;
}

/* Botões */
.stButton > button {
    background-color: #1a1a1a !important;
    color: #eeeeee !important;
    border-color: #444 !important;
}

.stButton > button:hover {
    background-color: #00ff8822 !important;
    border-color: #00ff88 !important;
    color: #00ff88 !important;
}

hr {
    border-color: #333 !important;
}

.titulo {
    font-family: 'Press Start 2P', monospace;
    font-size: 1.4rem;
    color: #00ff88;
    text-align: center;
    text-shadow: 0 0 20px #00ff8888;
    margin-bottom: 0.5rem;
}

.placar {
    font-family: 'VT323', monospace;
    font-size: 1.4rem;
    text-align: center;
    color: #aaa;
}

.palavra-display {
    font-family: 'Press Start 2P', monospace;
    font-size: 1.6rem;
    letter-spacing: 0.5rem;
    text-align: center;
    color: #eeeeee;
    margin: 1.2rem auto;
    background: #1a1a1a;
    border: 3px solid #00cc66;
    border-radius: 12px;
    padding: 1rem 2rem;
    max-width: 600px;
    box-shadow: 0 4px 0 #00cc66;
}

.letra-certa {
    color: #00aa44;
    display: inline-block;
    min-width: 1.5rem;
    border-bottom: 3px solid #00aa44;
    margin: 0 4px;
    text-align: center;
}

.letra-vazia {
    color: #bbbbbb;
    display: inline-block;
    min-width: 1.5rem;
    border-bottom: 3px solid #999999;
    margin: 0 4px;
    text-align: center;
}

.dica-texto {
    font-family: 'VT323', monospace;
    font-size: 1.3rem;
    text-align: center;
    color: #ffcc00;
}

.letras-erradas {
    font-family: 'VT323', monospace;
    font-size: 1.4rem;
    color: #ff4444;
    text-align: center;
}

.resultado-vitoria {
    font-family: 'Press Start 2P', monospace;
    font-size: 1.2rem;
    color: #00ff88;
    text-align: center;
    text-shadow: 0 0 15px #00ff88;
    animation: pulse 1s infinite;
}

.resultado-derrota {
    font-family: 'Press Start 2P', monospace;
    font-size: 1.2rem;
    color: #ff4444;
    text-align: center;
    text-shadow: 0 0 15px #ff4444;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}
</style>
""", unsafe_allow_html=True)

# ─── Interface ────────────────────────────────────────────────────────────────
st.markdown('<div class="titulo">🎮 JOGO DA FORCA</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="placar">✅ Vitórias: {st.session_state.vitorias} &nbsp;|&nbsp; ❌ Derrotas: {st.session_state.derrotas}</div>',
    unsafe_allow_html=True
)

st.divider()

# Forca
erros = len(st.session_state.letras_erradas)
st.markdown(FORCA[erros])

# Categoria e dica
st.markdown(f'<div class="dica-texto">📂 {st.session_state.categoria} &nbsp;|&nbsp; 💡 Dica: {st.session_state.dica}</div>', unsafe_allow_html=True)

# Palavra com lacunas
def montar_palavra():
    partes = []
    for letra in st.session_state.palavra:
        if letra in st.session_state.letras_certas:
            partes.append(f'<span class="letra-certa">{letra}</span>')
        else:
            partes.append('<span class="letra-vazia">_</span>')
    return " ".join(partes)

st.markdown(f'<div class="palavra-display">{montar_palavra()}</div>', unsafe_allow_html=True)

# Letras erradas
if st.session_state.letras_erradas:
    st.markdown(
        f'<div class="letras-erradas">Erros ({erros}/{MAX_ERROS}): {" ".join(st.session_state.letras_erradas)}</div>',
        unsafe_allow_html=True
    )

st.divider()

# ─── Resultado ───────────────────────────────────────────────────────────────
if st.session_state.vitoria:
    st.markdown('<div class="resultado-vitoria">🏆 VOCÊ GANHOU!</div>', unsafe_allow_html=True)
    st.balloons()
elif st.session_state.game_over:
    st.markdown(f'<div class="resultado-derrota">💀 GAME OVER! A palavra era: {st.session_state.palavra}</div>', unsafe_allow_html=True)

# ─── Input de letra ──────────────────────────────────────────────────────────
if not st.session_state.game_over and not st.session_state.vitoria:
    col1, col2 = st.columns([3, 1])
    with col1:
        letra_input = st.text_input(
            "Digite uma letra:",
            max_chars=1,
            key="input_letra",
            placeholder="Ex: A"
        ).upper()
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        adivinhar = st.button("✔️ Tentar", use_container_width=True)

    if adivinhar and letra_input:
        todas_letras = st.session_state.letras_certas + st.session_state.letras_erradas
        if not letra_input.isalpha():
            st.warning("⚠️ Digite apenas letras!")
        elif letra_input in todas_letras:
            st.info(f"Você já tentou a letra **{letra_input}**!")
        elif letra_input in st.session_state.palavra:
            st.session_state.letras_certas.append(letra_input)
            # Verificar vitória
            if all(l in st.session_state.letras_certas for l in st.session_state.palavra):
                st.session_state.vitoria = True
                st.session_state.vitorias += 1
        else:
            st.session_state.letras_erradas.append(letra_input)
            if len(st.session_state.letras_erradas) >= MAX_ERROS:
                st.session_state.game_over = True
                st.session_state.derrotas += 1
        st.rerun()

st.divider()

# ─── Novo jogo ───────────────────────────────────────────────────────────────
st.markdown("**Escolha a categoria para a próxima partida:**")
cols = st.columns(len(PALAVRAS))
for i, cat in enumerate(PALAVRAS.keys()):
    with cols[i]:
        if st.button(cat, use_container_width=True):
            iniciar_jogo(cat)
            st.rerun()

if st.button("🎲 Categoria Aleatória", use_container_width=True):
    iniciar_jogo()
    st.rerun()

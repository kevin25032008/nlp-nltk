import os
import sys
import streamlit as st
import spacy
import nltk
from deep_translator import GoogleTranslator

# Carrega o modelo do spaCy de forma segura
try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "pt_core_news_sm"])
    nlp = spacy.load("pt_core_news_sm")

from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon', quiet=True)
nltk.download('punkt', quiet=True)

sia = SentimentIntensityAnalyzer()

# --- FUNÇÃO DE FUSÃO (RRF) ---
def reciprocal_rank_fusion(ranking_1, ranking_2, k=60):
    rrf_scores = {}
    for rank, doc in enumerate(ranking_1, start=1):
        if doc not in rrf_scores: rrf_scores[doc] = 0.0
        rrf_scores[doc] += 1.0 / (k + rank)
    for rank, doc in enumerate(ranking_2, start=1):
        if doc not in rrf_scores: rrf_scores[doc] = 0.0
        rrf_scores[doc] += 1.0 / (k + rank)
    return sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)


# --- INTERFACE DO STREAMLIT ---
st.title("🚀 Sistema Integrado: Análise de Sentimentos + RRF")

# ==========================================
# 🆕 NOVA SEÇÃO: ANÁLISE DE SENTIMENTO IA (CAMPO DE DIGITAR)
# ==========================================
st.write("---")
st.header("🔮 Análise de Sentimento IA")
st.write("Digite uma frase abaixo para a IA classificar o sentimento em tempo real:")

# Campo de texto para o usuário digitar
frase_usuario = st.text_input("Sua frase:", placeholder="Ex: Eu adorei o atendimento, foi sensacional!")

if frase_usuario:
    # Traduz e analisa a frase digitada
    texto_usuario_en = GoogleTranslator(source='pt', target='en').translate(frase_usuario)
    score_usuario = sia.polarity_scores(texto_usuario_en)['compound']
    
    # Exibe o resultado na tela baseado no score
    if score_usuario >= 0.05:
        st.success(f"**Resultado: POSITIVO ({score_usuario:.2f})** — *\"{frase_usuario}\"*")
    elif score_usuario <= -0.05:
        st.error(f"**Resultado: NEGATIVO ({score_usuario:.2f})** — *\"{frase_usuario}\"*")
    else:
        st.info(f"**Resultado: NEUTRO ({score_usuario:.2f})** — *\"{frase_usuario}\"*")

st.write("---")


# ==========================================
# SEÇÃO ANTIGA: PROCESSAMENTO DO ARQUIVO T.TXT
# ==========================================
st.subheader("📁 Processamento em lote (Arquivo t.txt)")
st.write("Gere relatórios completos e fusão de rankings baseados no seu arquivo de texto.")

# 1. LEITURA SEGURA DO ARQUIVO T.TXT
if os.path.exists("t.txt"):
    with open("t.txt", "r", encoding="utf-8") as f:
        frases = [linha.strip() for linha in f.readlines() if linha.strip()]
    st.sidebar.success(f"📖 Arquivo `t.txt` carregado com {len(frases)} frases!")
else:
    frases = [
        "Eu adoro este produto! É maravilhoso e superou as expectativas.",
        "O atendimento foi péssimo, o produto chegou quebrado e atrasou muito.",
        "O produto é razoável, mas a entrega demorou bastante."
    ]
    with open("t.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(frases))
    st.sidebar.warning("⚠️ `t.txt` criado automaticamente com frases de teste.")

# Botão principal do arquivo
if st.button("Executar Análise Completa do Arquivo"):
    resultados_ia = []
    
    st.subheader("🤖 1. Classificação de Sentimentos individuais")
    
    for frase in frases:
        texto_en = GoogleTranslator(source='pt', target='en').translate(frase)
        score = sia.polarity_scores(texto_en)['compound']
        resultados_ia.append((frase, score))
        
        if score >= 0.05:
            st.success(f"**POSITIVO ({score:.2f}):** {frase}")
        elif score <= -0.05:
            st.error(f"**NEGATIVO ({score:.2f}):** {frase}")
        else:
            st.info(f"**NEUTRO ({score:.2f}):** {frase}")
            
    ranking_sentimento = [doc for doc, score in sorted(resultados_ia, key=lambda x: x[1], reverse=True)]
    ranking_original_txt = list(frases)
    
    st.write("---")
    st.subheader("🔀 2. Fusão de Rankings (RRF)")
    
    ranking_final_rrf = reciprocal_rank_fusion(ranking_sentimento, ranking_original_txt)
    
    st.success("### 🏆 Veredito Final Organizado pelo RRF:")
    for posicao, (doc, score_rrf) in enumerate(ranking_final_rrf, start=1):
        st.write(f"**{posicao}º Lugar:** {doc} *(Score RRF: {score_rrf:.4f})*")
        
    st.write("---")
    st.write("**Análise Gramatical dos Textos (spaCy):**")
    for frase in frases:
        documento = nlp(frase)
        fat = nltk.word_tokenize(frase)
        st.write(f"Frase: *\"{frase}\"*")
        st.caption(f"Tokens identificados: {fat}")
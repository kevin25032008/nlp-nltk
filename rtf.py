import streamlit as st

def reciprocal_rank_fusion(ranking_sistema_1, ranking_sistema_2, k=60):
    """
    Algoritmo de RRF (Reciprocal Rank Fusion)
    Combina dois rankings diferentes para gerar um resultado final melhor.
    """
    rrf_scores = {}
    
    # Processa o primeiro ranking (ex: busca por palavras-chave)
    for rank, documento in enumerate(ranking_sistema_1, start=1):
        if documento not in rrf_scores:
            rrf_scores[documento] = 0.0
        rrf_scores[documento] += 1.0 / (k + rank)
        
    # Processa o segundo ranking (ex: busca por inteligência artificial/sentimento)
    for rank, documento in enumerate(ranking_sistema_2, start=1):
        if documento not in rrf_scores:
            rrf_scores[documento] = 0.0
        rrf_scores[documento] += 1.0 / (k + rank)
        
    # Ordena os documentos do maior score para o menor
    ranking_final = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
    return ranking_final

# --- INTERFACE DE TESTE NO STREAMLIT ---
st.title("🔀 Algoritmo RRF (Reciprocal Rank Fusion)")
st.write("Misturando e recalculando a ordem dos melhores resultados.")

# Simulação de dois sistemas de busca da aula
busca_palavra_chave = ["Documento A", "Documento B", "Documento C"]
busca_ia = ["Documento B", "Documento C", "Documento A"]

st.subheader("Rankings Iniciais")
col1, col2 = st.columns(2)
with col1:
    st.write("**Sistema 1 (Palavras-chave):**", busca_palavra_chave)
with col2:
    st.write("**Sistema 2 (IA/Sentimento):**", busca_ia)

if st.button("Fundir Rankings com RRF"):
    resultado = reciprocal_rank_fusion(busca_palavra_chave, busca_ia)
    
    st.success("### 🏆 Ranking Final Otimizado:")
    for posicao, (doc, score) in enumerate(resultado, start=1):
        st.write(f"**{posicao}º Lugar:** {doc} (Score RRF: {score:.4f})")
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Garante que os recursos necessários estão baixados
nltk.download('punkt_tab')
nltk.download('stopwords')

# ============================================================
# 1. TOKENIZAÇÃO E LIMPEZA (MANTIDO DO ANTERIOR)
# ============================================================
frase = "Instalar o NLTK não é muito fácil!"
palavras = word_tokenize(frase)
stop_words = set(stopwords.words('portuguese'))
filtrando = [p for p in palavras if p.lower() not in stop_words]

print('--- Passo 1 e 2 (Configuração Inicial) ---')
print(f"Palavras originais: {palavras}")
print(f"Após filtrar stopwords: {filtrando}\n")


# ============================================================
# FRASE DE TESTE (Mista: tem pontos positivos e negativos)
# ============================================================
frase_analise = "O atendimento foi excelente, mas o preço achei bem ruim."
palavras_analise = [p.lower() for p in word_tokenize(frase_analise)]

print(f"Analisando a frase: \"{frase_analise}\"")
print("-" * 60)


# ============================================================
# 3. NÍVEL 1: CLASSIFICAÇÃO DIRETA (MANTIDO)
# ============================================================
print('--- NÍVEL 1: Classificação Direta (IF/ELIF) ---')

if "não" in palavras_analise or "ruim" in palavras_analise or "péssimo" in palavras_analise:
    print('Resultado Nível 1: Negativo ❌')
elif "excelente" in palavras_analise or "bom" in palavras_analise:
    print('Resultado Nível 1: Positivo  ')
else:
    print('Resultado Nível 1: Não classificado 🤷')

print("-" * 60)


# ============================================================
# 4. NÍVEL 2: SISTEMA DE PONTOS (DETECTA SENTIMENTOS MISTOS)
# ============================================================
print('--- NÍVEL 2: Sistema de Pontuação (Sentimentos Mistos) ---')

# Definimos nossos minidicionários de palavras
palavras_positivas = ["excelente", "bom", "gosto", "gostar", "ótimo", "lindo", "fácil"]
palavras_negativas = ["ruim", "péssimo", "difícil", "caro", "problema", "não"]

# Variáveis para contar quantas de cada tipo aparecem
pontos_positivos = 0
pontos_negativas = 0

# O código passa palavra por palavra da frase contando os pontos
for p in palavras_analise:
    if p in palavras_positivas:
        pontos_positivos += 1
    if p in palavras_negativas:
        pontos_negativas += 1

# Exibe o "placar" da frase
print(f"-> Palavras positivas encontradas: {pontos_positivos}")
print(f"-> Palavras negativas encontradas: {pontos_negativas}")

# Lógica de decisão baseada no placar
if pontos_positivos > 0 and pontos_negativas > 0:
    print('Resultado Nível 2: Sentimento Misto (Pontos Positivos e Negativos) ⚖️')
elif pontos_positivos > pontos_negativas:
    print('Resultado Nível 2: Majoritariamente Positivo ✅ ')
elif pontos_negativas > pontos_positivos:
    print('Resultado Nível 2: Majoritariamente Negativo ❌')
else:
    print('Resultado Nível 2: Neutro 😐')
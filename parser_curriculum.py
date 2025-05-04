"""
Análise automática de currículos em comparação com descrições de ocupações do mercado.

Este script realiza o pré-processamento linguístico de currículos em PDF, extrai informações
de ocupações e skills de arquivos CSV e compara o conteúdo do currículo com as descrições de ocupações.

Objetivo:
- Extrair tokens, stems e lemas de currículos em PDF.
- Obter descrições textuais detalhadas de ocupações e skills relacionadas.
- Calcular similaridade e cobertura lexical entre currículos e ocupações.

Requisitos:
- nltk, spacy, pandas, sklearn, unidecode, PyPDF2
- Modelos de linguagem 'pt_core_news_sm' do spaCy

Entradas:
- Currículos em PDF
- Arquivos CSV com informações sobre ocupações, skills e relações

Saídas:
- Resultados salvos em JSON com tokens, stems e lemas de currículos
- Impressão de métricas de comparação no terminal
"""
import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk.tokenize import word_tokenize
import spacy
import PyPDF2
import pandas as pd
from unidecode import unidecode
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import json

# Downloads necessários para o NLTK
nltk.download('stopwords')
nltk.download('punkt', download_dir=nltk.data.find("tokenizers"))
# Recursos linguísticos
stopwords_pt = set(stopwords.words('portuguese'))
stemmer = RSLPStemmer()
nlp = spacy.load("pt_core_news_sm")

def aplicar_stemmer(tokens):
    """
    Aplica stemmer RSLP aos tokens, excluindo stopwords e tokens não alfabéticos.
    """
    return [stemmer.stem(token) for token in tokens if token.lower() not in stopwords_pt and token.isalpha()]


def aplicar_lemmatizacao(tokens):
    """
    Aplica lematização aos tokens fornecidos, utilizando o modelo SpaCy para português.

    Apenas tokens alfabéticos que não sejam stopwords são considerados. Retorna os lemas das palavras.
    """
    doc = nlp(" ".join(tokens))
    return [token.lemma_ for token in doc if token.text.lower() not in stopwords_pt and token.is_alpha]


def limpar_texto_curriculo(texto):
    """
    Limpa e normaliza o texto bruto extraído de um currículo.

    Remove URLs, e-mails, números, meses, seções padrão de currículos, termos de formação,
    palavras de pouco valor informacional e caracteres especiais. Retorna um texto limpo.
    """
    texto = texto.lower()
    texto = re.sub(r'https?://\S+|www\.\S+', '', texto)
    texto = re.sub(r'http?://\S+|www\.\S+', '', texto)
    texto = re.sub(r'\S+@\S+', '', texto)
    texto = re.sub(r'\b\d+\b', '', texto)

    meses = ['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro']
    texto = re.sub(r'\b(?:' + '|'.join(meses) + r')\b', '', texto)

    seções = [
        'objetivo', 'resumo profissional', 'resumo', 'formação acadêmica',
        'experiência profissional', 'experiência', 'competências',
        'informações complementares', 'idiomas', 'qualificações', 'habilidades',
        'conquistas', 'perfil profissional'
    ]
    texto = re.sub(r'\b(?:' + '|'.join(seções) + r')\b', '', texto)

    formacoes = [
        'ensino médio', 'ensino fundamental', 'ensino superior', 'graduação',
        'pós-graduação', 'mestrado', 'doutorado', 'mba', 'tecnólogo',
        'licenciatura', 'bacharelado', 'faculdade', 'universidade', 'colégio'
    ]
    texto = re.sub(r'\b(?:' + '|'.join(formacoes) + r')\b', '', texto)

    palavras_ruido = ['anos', 'ano', 'idade', 'telefone', 'contato', 'currículo', 'curriculo', 'link', 'email', 'gmail', 'linkedin']
    texto = re.sub(r'\b(?:' + '|'.join(palavras_ruido) + r')\b', '', texto)

    texto = re.sub(r'[^\w\s]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto


def processar_pdf(caminho_pdf):
    """
    Lê e processa o conteúdo textual de um arquivo PDF de currículo.

    Realiza extração de texto, tokenização, stemming e lematização. Retorna três listas:
    tokens, stems e lemas.
    """
    with open(caminho_pdf, 'rb') as arquivo:
        leitor = PyPDF2.PdfReader(arquivo)
        texto = ""
        for pagina in leitor.pages:
            texto += pagina.extract_text()

    doc = nlp(texto)
    tokens = [token.text for token in doc if token.text.lower() not in stopwords_pt and token.is_alpha]

    tokens_stem = aplicar_stemmer(tokens)
    tokens_lemma = aplicar_lemmatizacao(tokens)

    print("\n=== TOKENIZAÇÃO ===")
    print(tokens[:10])
    print("\n=== STEMMING ===")
    print(tokens_stem[:10])
    print("\n=== LEMATIZAÇÃO ===")
    print(tokens_lemma[:10])
    return tokens, tokens_stem, tokens_lemma


def processar_texto(texto):
    """
    Processa uma string de texto com tokenização, stemming e lematização.

    O texto é tokenizado, normalizado (sem acentuação), e processado linguisticamente.
    Retorna tokens, stems e lemas.
    """
    tokens = word_tokenize(texto, language='portuguese')
    tokens = [unidecode(t.lower()) for t in tokens if t.isalpha() and t.lower() not in stopwords_pt]
    stems = aplicar_stemmer(tokens)
    lemmas = aplicar_lemmatizacao(tokens)
    return tokens, stems, lemmas


def encontrar_ocupacoes_similares(nome_ocupacao, caminho_occupations='occupations_pt.csv', caminho_similar='similar.csv'):
    """
    Encontra ocupações similares a partir do nome de uma ocupação.

    Normaliza o nome da ocupação, busca o conceptUri correspondente e retorna uma lista
    de URIs incluindo similares. Exibe os nomes das ocupações encontradas.
    """
    df_occ = pd.read_csv(caminho_occupations, quotechar='"')
    df_similar = pd.read_csv(caminho_similar)

    df_occ = df_occ.fillna('').astype(str)
    nome_normalizado = re.sub(r'[^\w\s]', '', unidecode(nome_ocupacao.lower())).strip()
    nome_normalizado = re.sub(r'\s+', ' ', nome_normalizado)
    concept_uri = None

    for _, row in df_occ.iterrows():
        campos = [
            row['preferredLabel'],
            row['altLabels'].replace('\n', ';'),
            row['hiddenLabels'].replace('\n', ';')
        ]
        for campo in campos:
            termos = [unidecode(t.strip().lower()) for t in campo.split(';') if t.strip()]
            if nome_normalizado in termos:
                concept_uri = row['conceptUri']
                break
        if concept_uri:
            break

    if not concept_uri:
        print(f"Ocupação '{nome_ocupacao}' não encontrada.")
        return []

    similares = df_similar[df_similar['conceptUri'] == concept_uri]
    if similares.empty:
        print(f"Nenhuma ocupação similar encontrada para '{nome_ocupacao}'.")
        return [concept_uri]

    row_sim = similares.iloc[0]
    similares_uris = [row_sim['UriSimilar1'], row_sim['UriSimilar2'], row_sim['UriSimilar3']]
    resultado = [concept_uri] + similares_uris
    nomes_ocupacoes = df_occ[df_occ['conceptUri'].isin(resultado)]['preferredLabel'].tolist()
    print(f"\n Ocupações encontradas:")
    for nome in nomes_ocupacoes:
        print(f" - {nome}")
    return resultado


def extrair_e_processar_descricoes(nome_ocupacao, pasta_csv='.'):
    """
    Extrai descrições de ocupações e habilidades relacionadas a partir do nome de uma ocupação.

    Lê múltiplos arquivos CSV com dados de ocupações e skills, agrega descrições e aplica
    tokenização, stemming e lematização sobre o texto combinado.
    """
    occupations = pd.read_csv(os.path.join(pasta_csv, 'occupations_pt.csv'), dtype=str).fillna('')
    relations = pd.read_csv(os.path.join(pasta_csv, 'occupationSkillRelations_pt.csv'), dtype=str).fillna('')
    skills_main = pd.read_csv(os.path.join(pasta_csv, 'skills_pt.csv'), dtype=str).fillna('')

    green = pd.read_csv(os.path.join(pasta_csv, 'greenSkillsCollection_pt.csv'), dtype=str).fillna('')
    digcomp = pd.read_csv(os.path.join(pasta_csv, 'digCompSkillsCollection_pt.csv'), dtype=str).fillna('')
    language = pd.read_csv(os.path.join(pasta_csv, 'languageSkillsCollection_pt.csv'), dtype=str).fillna('')
    transversal = pd.read_csv(os.path.join(pasta_csv, 'transversalSkillsCollection_pt.csv'), dtype=str).fillna('')
    research = pd.read_csv(os.path.join(pasta_csv, 'researchSkillsCollection_pt.csv'), dtype=str).fillna('')

    skill_groups = pd.read_csv(os.path.join(pasta_csv, 'skillGroups_pt.csv'), dtype=str).fillna('')
    skill_relations = pd.read_csv(os.path.join(pasta_csv, 'skillSkillRelations_pt.csv'), dtype=str).fillna('')
    skills_hierarchy = pd.read_csv(os.path.join(pasta_csv, 'skillsHierarchy_pt.csv'), dtype=str).fillna('')
    broader_pillars = pd.read_csv(os.path.join(pasta_csv, 'broaderRelationsSkillPillar_pt.csv'), dtype=str).fillna('')

    all_skills = pd.concat([skills_main, green, digcomp, language, transversal, research], ignore_index=True)

    uris_ocupacoes = encontrar_ocupacoes_similares(nome_ocupacao)

    textos = []

    for uri in uris_ocupacoes:
        occ_row = occupations[occupations['conceptUri'] == uri]
        if not occ_row.empty:
            desc = occ_row['description'].iloc[0]
            if desc.strip():
                textos.append(desc)

    for occ_uri in uris_ocupacoes:
        skill_uris = relations[relations['occupationUri'] == occ_uri]['skillUri'].unique()
        for uri in skill_uris:
            skill_row = all_skills[all_skills['conceptUri'] == uri]
            if not skill_row.empty:
                skill = skill_row.iloc[0]
                if skill.get('preferredLabel'):
                    textos.append(skill['preferredLabel'])
                if skill.get('description'):
                    textos.append(skill['description'])

            group_row = skill_groups[skill_groups['conceptUri'] == uri]
            if not group_row.empty and group_row['preferredLabel'].iloc[0].strip():
                textos.append(group_row['preferredLabel'].iloc[0])

            pillar_row = broader_pillars[broader_pillars['conceptUri'] == uri]
            if not pillar_row.empty:
                broader_uri = pillar_row['broaderUri'].iloc[0]
                pillar_label = all_skills[all_skills['conceptUri'] == broader_uri]['preferredLabel']
                if not pillar_label.empty:
                    textos.append(pillar_label.iloc[0])

            related_uris = skill_relations[skill_relations['originalSkillUri'] == uri]['relatedSkillUri'].unique()
            for related_uri in related_uris:
                related_label = all_skills[all_skills['conceptUri'] == related_uri]['preferredLabel']
                if not related_label.empty:
                    textos.append(related_label.iloc[0])

            for col in ['Level 0 URI', 'Level 1 URI', 'Level 2 URI', 'Level 3 URI']:
                if uri in skills_hierarchy[col].values:
                    level_label = col.split()[1]
                    textos.append(f"Nível hierárquico: {level_label}")
                    break

    texto_final = ' '.join(textos)
    doc = nlp(texto_final)
    tokens = [token.text for token in doc if token.text.lower() not in stopwords_pt and token.is_alpha]
    tokens_stem = aplicar_stemmer(tokens)
    tokens_lemma = aplicar_lemmatizacao(tokens)

    print("\n=== TOKENIZAÇÃO ===")
    print(tokens[:10])
    print("\n=== STEMMING ===")
    print(tokens_stem[:10])
    print("\n=== LEMATIZAÇÃO ===")
    print(tokens_lemma[:10])
    return tokens, tokens_stem, tokens_lemma


def comparar_curriculo_com_ocupacoes(tokens_cv, stems_cv, lemas_cv, tokens_occ, stems_occ, lemas_occ):
    """
    Compara o conteúdo de um currículo com as descrições de uma ocupação.

    Usa cobertura de vocabulário e similaridade TF-IDF entre tokens, stems e lemas.
    Exibe métricas de comparação para cada técnica de pré-processamento.
    """
    def comparar(texto1, texto2, label):
        set1, set2 = set(texto1), set(texto2)
        intersecao = set1 & set2
        cobertura = len(intersecao) / len(set2) * 100 if set2 else 0

        texto1_str = " ".join(texto1)
        texto2_str = " ".join(texto2)
        vectorizer = TfidfVectorizer()
        tfidf = vectorizer.fit_transform([texto2_str, texto1_str])
        similaridade = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

        print(f"\n {label.upper()}")
        print(f" Cobertura: {cobertura:.2f}%")
        print(f" Similaridade: {similaridade:.4f}")
        print(f" Interseção de palavras ({len(intersecao)}): {list(intersecao)[:10]}")
        return cobertura, similaridade

    cobertura_tokens, sim_tokens = comparar(tokens_cv, tokens_occ, "Tokenização")
    cobertura_stems, sim_stems = comparar(stems_cv, stems_occ, "Stemming")
    cobertura_lemmas, sim_lemmas = comparar(lemas_cv, lemas_occ, "Lematização")

    return {
        "token": {"cobertura": cobertura_tokens, "similaridade": sim_tokens},
        "stem": {"cobertura": cobertura_stems, "similaridade": sim_stems},
        "lemma": {"cobertura": cobertura_lemmas, "similaridade": sim_lemmas},
    }


def processar_pdfs_em_pasta(pasta):
    """
    Processa todos os arquivos PDF de uma pasta, retornando tokens, stems e lemas para cada currículo.

    Aplica extração de texto e pré-processamento linguístico em lote. Retorna um dicionário com os dados
    processados por arquivo.
    """
    resultados = {}
    for nome_arquivo in os.listdir(pasta):
        if nome_arquivo.lower().endswith('.pdf'):
            caminho_pdf = os.path.join(pasta, nome_arquivo)
            print(f"\n Processando: {nome_arquivo}")
            tokens, stems, lemas = processar_pdf(caminho_pdf)
            resultados[nome_arquivo] = {
                "tokens": tokens,
                "stems": stems,
                "lemmas": lemas
            }
    return resultados


if __name__ == "__main__":
    """
    Ponto de entrada do script. Processa os PDFs da pasta atual, extrai e compara com ocupações.

    Os resultados são salvos em um arquivo JSON e as comparações são exibidas no terminal.
    """
    resultados_curriculos = processar_pdfs_em_pasta(".")

    with open("resultados_curriculos.json", "w", encoding="utf-8") as f:
        json.dump(resultados_curriculos, f, ensure_ascii=False, indent=4)

    tokens_occ, stems_occ, lemas_occ = extrair_e_processar_descricoes("Analista de dados")

    for nome_arquivo, dados in resultados_curriculos.items():
        print(f"\n Comparando currículo: {nome_arquivo}")
        comparar_curriculo_com_ocupacoes(
            dados["tokens"],
            dados["stems"],
            dados["lemmas"],
            tokens_occ,
            stems_occ,
            lemas_occ
        )

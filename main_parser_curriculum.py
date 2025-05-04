"""
Processamento automatizado de currículos em PDF para análise linguística.

Este módulo percorre todos os arquivos PDF de uma pasta, extrai o texto de cada currículo
e aplica técnicas de Processamento de Linguagem Natural (PLN), incluindo tokenização,
stemming e lematização.

Objetivo:
- Automatizar a leitura e o pré-processamento de múltiplos currículos em formato PDF.
- Gerar representações textuais (tokens, stems e lemas) para posterior análise e comparação.

Entradas:
- Arquivos PDF contendo currículos localizados em uma pasta específica.

Saídas:
- Dicionário com os resultados para cada arquivo PDF processado, contendo:
    - tokens: palavras relevantes extraídas
    - stems: raízes das palavras
    - lemmas: formas canônicas das palavras
"""
from parser_curriculum import *
import unicodedata
import re


def normalizar_texto(texto):
    """
    Normaliza um texto removendo acentuação, convertendo para minúsculas e eliminando espaços extras.

    Essa função é útil para padronizar termos antes de comparações ou buscas textuais.
    """
    texto = texto.strip().lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    texto = re.sub(r'\s+', ' ', texto)
    return texto


def detalhar_ocupacoes(uris, nomes_ocupacoes, pasta_csv='.'):
    """
    Exibe informações detalhadas sobre ocupações a partir de suas URIs.

    Carrega descrições e atributos das ocupações e habilidades relacionadas de arquivos CSV.
    Mostra informações no terminal como descrição, skills, grupo, pilar, relações e hierarquia.
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
    broader_pillars = pd.read_csv(os.path.join(pasta_csv, 'broaderRelationsSkillPillar_pt.csv'), dtype=str).fillna('')
    skill_relations = pd.read_csv(os.path.join(pasta_csv, 'skillSkillRelations_pt.csv'), dtype=str).fillna('')
    skills_hierarchy = pd.read_csv(os.path.join(pasta_csv, 'skillsHierarchy_pt.csv'), dtype=str).fillna('')

    all_skills = pd.concat([skills_main, green, digcomp, language, transversal, research], ignore_index=True)

    for idx, uri in enumerate(uris):
        nome = nomes_ocupacoes[idx]
        print(f"\n--- Detalhes da ocupação: {nome} ---")

        textos = []

        occ_row = occupations[occupations['conceptUri'] == uri]
        if not occ_row.empty:
            desc = occ_row['description'].iloc[0]
            if desc.strip():
                textos.append(f"description: {desc.strip()}")

        skill_uris = relations[relations['occupationUri'] == uri]['skillUri'].unique()
        for skill_uri in skill_uris:
            skill_row = all_skills[all_skills['conceptUri'] == skill_uri]
            if not skill_row.empty:
                skill = skill_row.iloc[0]
                label = skill.get('preferredLabel', '')
                desc = skill.get('description', '')
                if label:
                    textos.append(f"Skill: {label}")
                if desc:
                    textos.append(f"Descrição da skill: {desc}")

            group_row = skill_groups[skill_groups['conceptUri'] == skill_uri]
            if not group_row.empty:
                textos.append(f"Grupo: {group_row['preferredLabel'].iloc[0]}")

            pillar_row = broader_pillars[broader_pillars['conceptUri'] == skill_uri]
            if not pillar_row.empty:
                pillar_uri = pillar_row['broaderUri'].iloc[0]
                pillar_label = all_skills[all_skills['conceptUri'] == pillar_uri]['preferredLabel']
                if not pillar_label.empty:
                    textos.append(f"Pilar: {pillar_label.iloc[0]}")

            related = skill_relations[skill_relations['originalSkillUri'] == skill_uri]['relatedSkillUri']
            for related_uri in related:
                related_label = all_skills[all_skills['conceptUri'] == related_uri]['preferredLabel']
                if not related_label.empty:
                    textos.append(f"Relacionada: {related_label.iloc[0]}")

            for col in ['Level 0 URI', 'Level 1 URI', 'Level 2 URI', 'Level 3 URI']:
                if skill_uri in skills_hierarchy[col].values:
                    textos.append(f"Nível hierárquico: {col.split()[1]}")
                    break

        if textos:
            print("\n".join(textos))
        else:
            print("Nenhuma informação detalhada encontrada.")
        input("\nPressione Enter para continuar para a próxima ocupação...")


def main():
    """
    Função principal que executa o fluxo de entrada do usuário, busca de ocupações e comparação com currículos.

    Solicita ao usuário uma ocupação, encontra URIs relacionadas, permite visualização detalhada,
    extrai descrições e realiza a comparação com currículos PDF da pasta atual.
    """
    ocupacao_input = input("Informe a ocupação que deseja consultar: ")
    ocupacao = normalizar_texto(ocupacao_input)
    print(f"\nVocê informou que quer consultar a ocupação \"{ocupacao}\".")

    uris = encontrar_ocupacoes_similares(ocupacao)
    if not uris:
        print("Não foi possível encontrar ocupações relacionadas.")
        return

    df_occ = pd.read_csv('occupations_pt.csv', quotechar='"').fillna('').astype(str)
    df_occ['normalizedLabel'] = df_occ['preferredLabel'].apply(normalizar_texto)
    nomes_ocupacoes = df_occ[df_occ['conceptUri'].isin(uris)]['preferredLabel'].tolist()

    print("\nPara esta profissão, foram encontradas as seguintes ocupações similares:")
    for idx, nome in enumerate(nomes_ocupacoes, 1):
        print(f" {idx}. {nome}")

    uris_escolhidas = []
    while not uris_escolhidas:
        print("\nDigite os números das profissões que se aplicam (ex: 1, 3)")
        print("ou digite 'd' para detalhar as ocupações antes de decidir.")
        selecao = input("Sua escolha: ").strip().lower()

        if selecao == 'd':
            detalhar_ocupacoes(uris, nomes_ocupacoes)
            continue

        try:
            indices_escolhidos = [int(i) - 1 for i in selecao.split(",") if i.strip().isdigit()]
            uris_escolhidas = [uris[i] for i in indices_escolhidos if 0 <= i < len(uris)]
            if not uris_escolhidas:
                print("Nenhuma ocupação válida selecionada. Tente novamente.")
        except Exception as e:
            print(f"Erro na leitura da seleção: {e}. Tente novamente.")


    def extrair_descricoes_por_uris(uris, pasta_csv='.'):
        """
        Extrai e processa descrições de ocupações e habilidades com base em uma lista de URIs.

        Consolida descrições e termos de múltiplos arquivos CSV, aplica técnicas de PLN (tokenização,
        stemming e lematização) e retorna os respectivos resultados linguísticos.
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
        broader_pillars = pd.read_csv(os.path.join(pasta_csv, 'broaderRelationsSkillPillar_pt.csv'), dtype=str).fillna('')
        skill_relations = pd.read_csv(os.path.join(pasta_csv, 'skillSkillRelations_pt.csv'), dtype=str).fillna('')
        skills_hierarchy = pd.read_csv(os.path.join(pasta_csv, 'skillsHierarchy_pt.csv'), dtype=str).fillna('')

        all_skills = pd.concat([skills_main, green, digcomp, language, transversal, research], ignore_index=True)

        textos = []

        for uri in uris:
            occ_row = occupations[occupations['conceptUri'] == uri]
            if not occ_row.empty:
                desc = occ_row['description'].iloc[0]
                if desc.strip():
                    textos.append(desc)

            skill_uris = relations[relations['occupationUri'] == uri]['skillUri'].unique()
            for skill_uri in skill_uris:
                skill_row = all_skills[all_skills['conceptUri'] == skill_uri]
                if not skill_row.empty:
                    skill = skill_row.iloc[0]
                    textos.append(skill.get('preferredLabel', ''))
                    textos.append(skill.get('description', ''))

                group_row = skill_groups[skill_groups['conceptUri'] == skill_uri]
                if not group_row.empty:
                    textos.append(group_row['preferredLabel'].iloc[0])

                pillar_row = broader_pillars[broader_pillars['conceptUri'] == skill_uri]
                if not pillar_row.empty:
                    pillar_uri = pillar_row['broaderUri'].iloc[0]
                    pillar_label = all_skills[all_skills['conceptUri'] == pillar_uri]['preferredLabel']
                    if not pillar_label.empty:
                        textos.append(pillar_label.iloc[0])

                related_uris = skill_relations[skill_relations['originalSkillUri'] == skill_uri]['relatedSkillUri']
                for related_uri in related_uris:
                    related_label = all_skills[all_skills['conceptUri'] == related_uri]['preferredLabel']
                    if not related_label.empty:
                        textos.append(related_label.iloc[0])

                for col in ['Level 0 URI', 'Level 1 URI', 'Level 2 URI', 'Level 3 URI']:
                    if skill_uri in skills_hierarchy[col].values:
                        textos.append(f"Nível hierárquico: {col.split()[1]}")
                        break

        texto_final = ' '.join([t for t in textos if t])
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

    tokens_occ, stems_occ, lemas_occ = extrair_descricoes_por_uris(uris_escolhidas)
    resultados_curriculos = processar_pdfs_em_pasta(".")

    for nome_arquivo, dados in resultados_curriculos.items():
        print(f"\nComparando currículo: {nome_arquivo}")
        comparar_curriculo_com_ocupacoes(
            dados["tokens"],
            dados["stems"],
            dados["lemmas"],
            tokens_occ,
            stems_occ,
            lemas_occ
        )


if __name__ == "__main__":
    """
    Ponto de entrada do script.

    Inicia a execução chamando a função main(), que realiza o processamento completo.
    """
    main()

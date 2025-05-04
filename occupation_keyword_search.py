"""
Módulo para análise detalhada de habilidades associadas a ocupações.

Este script carrega e processa diversas bases de dados CSV relacionadas a ocupações e competências.
O principal objetivo é permitir a busca por ocupações a partir de uma palavra-chave e retornar
informações completas sobre as skills associadas: descrição, grupo, pilar, hierarquia e skills relacionadas.

Requisitos:
- Pandas
- Unicodedata

Entradas:
- Arquivos CSV com dados de ocupações, relações e coleções de competências.

Saídas:
- Impressão no console de informações detalhadas sobre as habilidades de uma ou mais ocupações encontradas.

Uso:
- Chame a função `show_detailed_skills_for_occupation("palavra-chave")` para executar a busca.
"""
import pandas as pd
import unicodedata


def normalize(text):
    """
    Normaliza um texto removendo acentos e convertendo para minúsculas. 
    Caso o valor seja nulo (NaN), retorna uma string vazia.

    Parâmetros:
    - text (str): texto de entrada a ser normalizado.

    Retorno:
    - str: texto normalizado (sem acentos e em letras minúsculas).
    """
    if pd.isnull(text):
        return ''
    return unicodedata.normalize('NFKD', str(text).lower()).encode('ASCII', 'ignore').decode('ASCII')


# Coleções principais
occupations = pd.read_csv('occupations_pt.csv')
relations = pd.read_csv('occupationSkillRelations_pt.csv')
skills_main = pd.read_csv('skills_pt.csv')

# Coleções complementares
green = pd.read_csv('greenSkillsCollection_pt.csv')
digcomp = pd.read_csv('digCompSkillsCollection_pt.csv')
language = pd.read_csv('languageSkillsCollection_pt.csv')
transversal = pd.read_csv('transversalSkillsCollection_pt.csv')
research = pd.read_csv('researchSkillsCollection_pt.csv')

# Coleções relacionais
skill_groups = pd.read_csv('skillGroups_pt.csv')
skill_relations = pd.read_csv('skillSkillRelations_pt.csv')
skills_hierarchy = pd.read_csv('skillsHierarchy_pt.csv')
broader_pillars = pd.read_csv('broaderRelationsSkillPillar_pt.csv')

all_skills = pd.concat([skills_main, green, digcomp, language, transversal, research], ignore_index=True)

occupations['preferredLabel_normalized'] = occupations['preferredLabel'].apply(normalize)
occupations['definition_normalized'] = occupations['definition'].apply(normalize)


def show_detailed_skills_for_occupation(keyword):
    """
    Exibe no console as skills detalhadas relacionadas a uma ocupação com base em uma palavra-chave.

    A função realiza:
    - Normalização da palavra-chave e busca por ocupações cujo nome ou definição contenha o termo.
    - Listagem de todas as habilidades associadas a essas ocupações, incluindo:
        - Nome da skill
        - Descrição
        - Grupo (se houver)
        - Pilar mais amplo (se houver)
        - Nível hierárquico
        - Skills relacionadas

    Parâmetros:
    - keyword (str): termo ou palavra-chave a ser pesquisada nas ocupações.
    """
    keyword_norm = normalize(keyword)

    matches = occupations[
        occupations['preferredLabel_normalized'].str.contains(keyword_norm) |
        occupations['definition_normalized'].str.contains(keyword_norm)
    ]

    if matches.empty:
        print(f"Nenhuma ocupação encontrada para: {keyword}")
        return

    for _, occ in matches.iterrows():
        occ_uri = occ['conceptUri']
        occ_label = occ['preferredLabel']
        print(f"\nOcupação: {occ_label}\n{'=' * (11 + len(occ_label))}")

        skill_uris = relations[relations['occupationUri'] == occ_uri]['skillUri'].unique()
        for uri in skill_uris:
            skill_row = all_skills[all_skills['conceptUri'] == uri]
            if skill_row.empty:
                continue

            skill = skill_row.iloc[0]
            label = skill.get('preferredLabel', '').strip()
            desc = skill.get('description', '').strip()

            group_match = skill_groups[skill_groups['conceptUri'] == uri]
            group_label = group_match['preferredLabel'].iloc[0] if not group_match.empty else ''

            pillar_match = broader_pillars[broader_pillars['conceptUri'] == uri]
            pillar_uri = pillar_match['broaderUri'].iloc[0] if not pillar_match.empty else ''
            pillar_label = all_skills[all_skills['conceptUri'] == pillar_uri]['preferredLabel'].iloc[0] if pillar_uri in all_skills['conceptUri'].values else ''

            related_rows = skill_relations[skill_relations['originalSkillUri'] == uri]
            related_labels = []
            for _, r in related_rows.iterrows():
                related_uri = r['relatedSkillUri']
                related_label = all_skills[all_skills['conceptUri'] == related_uri]['preferredLabel']
                if not related_label.empty:
                    related_labels.append(related_label.iloc[0])

            hierarchy_level = None
            for col in ['Level 0 URI', 'Level 1 URI', 'Level 2 URI', 'Level 3 URI']:
                if uri in skills_hierarchy[col].values:
                    hierarchy_level = col.split()[1]
                    break

            print(f"\nSkill: {label}")
            if desc:
                print(f"Descrição: {desc}")
            if group_label:
                print(f"Grupo: {group_label}")
            if pillar_label:
                print(f"Pilar: {pillar_label}")
            if hierarchy_level:
                print(f"Nível hierárquico: {hierarchy_level}")
            if related_labels:
                print("Relacionadas:")
                for r in related_labels:
                    print(f"   - {r}\n")


show_detailed_skills_for_occupation("projeto")

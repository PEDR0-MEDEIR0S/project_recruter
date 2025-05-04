<h1 align="center">📄 Análise Inteligente de Informações de Candidato e Aderência Profissional</h1>

<p align="center">
  <em>Processamento automatizado de currículos e análise de aderência profissional com base em grandes bases de dados ocupacionais.</em>
</p>

---

<h2>🎯 Objetivo do Projeto</h2>

<p>
  Este projeto visa realizar a <strong>análise inteligente</strong> de informações dos candidatos e fazer o <strong>matching de vagas</strong>, utilizando técnicas avançadas de Processamento de Linguagem Natural (NLP) e aprendizado de máquina. O objetivo principal é analisar os perfis dos candidatos, identificar suas qualificações, e realizar o matching com mais de 3.300 profissões catalogadas em uma base de dados extensa, otimizando o processo de recrutamento e seleção.
</p>

<p>
  O sistema busca automatizar o processo de análise de currículos e dados profissionais, identificando as competências, qualificações e experiências de candidatos, e comparando-as com as necessidades das vagas de trabalho disponíveis.
</p>

---

<h2>📊 Situação Atual</h2>

<p>
  A situação atual do projeto envolve a análise de documentos PDF de currículos baixados de uma pasta local, onde o sistema é capaz de extrair e analisar as informações de forma automatizada. Isso inclui a comparação dos dados extraídos com a base de dados de profissões, habilidades e requisitos das vagas.
</p>

<p>
  Embora o sistema esteja atualmente focado na leitura e análise de arquivos PDF, essa funcionalidade representa apenas uma parte do escopo maior do projeto. A ideia é expandir a análise para outros formatos de entrada, incluindo integração com plataformas de recrutamento e APIs externas.
</p>

<ul>
  <li>Leitura e análise de currículos em PDF para extrair informações como qualificações e experiência.</li>
  <li>Comparação dos dados dos candidatos com mais de 3.300 profissões catalogadas e habilidades associadas.</li>
  <li>Uso de técnicas como <strong>TF-IDF</strong>, <strong>Cosine Similarity</strong> e NLP para análise semântica.</li>
  <li>Integração com mais de 15 arquivos de descrição de profissões e suas habilidades.</li>
</ul>

---

<h2>🔮 Expansões Futuras</h2>

<ol>
  <li><strong>Web Scraping do LinkedIn:</strong> Utilização de <code>Selenium</code> ou <code>Beautiful Soup</code> para buscar informações adicionais dos candidatos, como seus perfis no LinkedIn, qualificações, experiência e matching profissional.</li>
  <li><strong>Integração com APIs de Inteligência Artificial:</strong> Conectar o sistema com APIs de IA para realizar análises mais profundas e determinar quais candidatos estão mais aptos para determinada vaga.</li>
  <li><strong>Interface Gráfica para Windows:</strong> Desenvolvimento de uma interface gráfica amigável para facilitar a interação com o sistema.</li>
  <li><strong>Integração com Sistemas de Recrutamento:</strong> Conectar o sistema com plataformas de recrutamento para automatizar o processo de seleção de candidatos.</li>
</ol>

---

<h2>💻 Tecnologias Utilizadas</h2>

<table>
  <tr><td>🛠️ Linguagem</td><td>Python 3.12.10</td></tr>
  <tr><td>📚 Bibliotecas</td><td>pandas, nltk, spacy, sklearn, PyPDF2, unidecode, Selenium</td></tr>
  <tr><td>🧠 Técnicas</td><td>TF-IDF, Cosine Similarity, NLP, Web Scraping, APIs de IA</td></tr>
  <tr><td>🔌 APIs</td><td>LinkedIn API, APIs de IA para Matching de Candidatos</td></tr>
</table>

---

<h2>📁 Estrutura de Arquivos</h2>
<pre>
/projeto
  │
  ├── install_requirements.sh # Script para instalar as dependências do projeto
  ├── main_parser_curriculum.py # Script principal para processamento de currículos
  ├── occupation_keyword_search.py # Busca palavras-chave nas ocupações
  ├── parser_curriculum.py # Parser para currículos em PDF
  ├── requirements.txt # Arquivo com as dependências necessárias
  │
  └── database_encriptado.aes # Banco de dados criptografado com os arquivos essenciais
      ├── broaderRelationsSkillPillar_pt
      ├── digCompSkillsCollection_pt
      ├── digitalSkillsCollection_pt
      ├── greenSkillsCollection_pt
      ├── languageSkillsCollection_pt
      ├── occupations_pt
      ├── occupationSkillRelations_pt
      ├── researchOccupationsCollection_pt
      ├── researchSkillsCollection_pt
      ├── similar
      ├── skillGroups_pt
      ├── skills_pt
      ├── skillsHierarchy_pt
      ├── skillSkillRelations_pt
      └── transversalSkillsCollection_pt
</pre>

---

<h2>⚙️ Como Executar</h2>

<p>Para rodar o projeto em sua máquina local, siga as etapas abaixo:</p>

<pre>
bash install_requirements.sh  # Instala as dependências
database_encriptado.aes # Desencriptar os bancos de dados de informações
python main_parser_curriculum.py  # Executa o parser principal, mas com interações com o usuário.
occupation_keyword_search.py # Executa a busca de uma string (qualquer texto) nas ocupações.
parser_curriculum.py # Executa a busca da profissão em arquivos PDF e classifica a similiridade em 3 metodos diferentes.
</pre>

---

<h2>📄 Licença</h2>

<p>
  Este projeto está licenciado sob a <strong>Licença MIT</strong>.
</p>

---

<h2>📚 Notas sobre o arquivo <code>database_encriptado.aes</code></h2>

<p>
  O arquivo <code>database_encriptado.aes</code> contém os dados criptografados necessários para o funcionamento do sistema. Ele inclui as seguintes subpastas com informações relacionadas às profissões, habilidades e relações entre as skills:
</p>

<ul>
  <li><code>broaderRelationsSkillPillar_pt</code> – Relações mais amplas entre habilidades e pilares.</li>
  <li><code>digCompSkillsCollection_pt</code> – Competências digitais coletadas.</li>
  <li><code>digitalSkillsCollection_pt</code> – Habilidades digitais.</li>
  <li><code>greenSkillsCollection_pt</code> – Competências "verdes" (sustentabilidade, etc).</li>
  <li><code>languageSkillsCollection_pt</code> – Competências linguísticas.</li>
  <li><code>occupations_pt</code> – Base de dados com informações sobre ocupações.</li>
  <li><code>occupationSkillRelations_pt</code> – Relações entre ocupações e habilidades.</li>
  <li><code>researchOccupationsCollection_pt</code> – Base de dados com ocupações em pesquisa.</li>
  <li><code>researchSkillsCollection_pt</code> – Base de dados com habilidades em pesquisa.</li>
  <li><code>similar</code> – Arquivos de dados similares (se aplicável).</li>
  <li><code>skillGroups_pt</code> – Grupos de habilidades.</li>
  <li><code>skills_pt</code> – Habilidades principais.</li>
  <li><code>skillsHierarchy_pt</code> – Hierarquia das habilidades.</li>
  <li><code>skillSkillRelations_pt</code> – Relações entre diferentes habilidades.</li>
  <li><code>transversalSkillsCollection_pt</code> – Competências transversais.</li>
</ul>

<p>
  Este arquivo está criptografado para garantir a segurança e privacidade dos dados. 
  Para descriptografá-lo, será necessário utilizar o código de descriptografia adequado que pode ser solicitado ao desenvolvedor.
</p>

---

<h2>🤝 Contribuições</h2>

<p>
  Contribuições são muito bem-vindas! Para contribuir com o projeto.
</p>

---

<h2>📄 Licença</h2>

<p>
  Este projeto está licenciado sob a <strong>Licença MIT</strong>.
</p>

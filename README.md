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

<h2>⚙️ Como Executar</h2>

<p>Para rodar o projeto em sua máquina local, siga as etapas abaixo:</p>

<pre>
git clone https://github.com/seuusuario/nome-do-repo.git
cd nome-do-repo
pip install -r requirements.txt
python nome_do_script_principal.py
</pre>

---

<h2>📁 Estrutura de Dados</h2>

<ul>
  <li><strong>occupations_pt.csv</strong> – Base de ocupações principais, com mais de 3.300 profissões catalogadas.</li>
  <li><strong>occupationSkillRelations_pt.csv</strong> – Mapeamento de ocupações para skills, indicando quais habilidades são essenciais para cada profissão.</li>
  <li><strong>skills_pt.csv</strong>, <strong>greenSkillsCollection_pt.csv</strong>, etc – Arquivos com skills organizadas por categorias (gerais, transversais, verdes, etc).</li>
  <li><strong>skillsHierarchy_pt.csv</strong> – Níveis hierárquicos das skills, organizando o grau de expertise requerido.</li>
  <li><strong>skillSkillRelations_pt.csv</strong> – Relações entre skills, para entender a interconexão entre habilidades diferentes.</li>
</ul>

---

<h2>🤝 Contribuições</h2>

<p>
  Contribuições são muito bem-vindas! Para contribuir com o projeto, basta abrir uma <a href="https://github.com/seurepo/issues">issue</a> ou enviar um <a href="https://github.com/seurepo/pulls">pull request</a>.
</p>

---

<h2>📄 Licença</h2>

<p>
  Este projeto está licenciado sob a <strong>Licença MIT</strong>.
</p>

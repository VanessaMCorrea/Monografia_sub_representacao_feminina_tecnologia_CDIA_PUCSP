# Notebooks

Esta pasta contém os dois notebooks Jupyter desenvolvidos no Google Colab
com toda a análise exploratória, modelagem e resultados da pesquisa.

---

## Notebooks

### `TCC_modelagem_genero_tecnologia_ENEM_SISU.ipynb`

Análise com dados do ENEM 2018–2023 e SISU 2023.

**O que este notebook cobre:**
- Estatística descritiva: perfil socioeconômico das candidatas (raça, renda, escola)
- Modelo 1: fatores socioeconômicos → nota em Matemática (mulheres)
- Modelo 7.2: mesmo modelo separado por subgrupo racial (brancas / pardas / pretas)
- Análise 6.2: gap racial por área de conhecimento (MT, CN, LC, CH, Redação)
- Análise 6.4: evolução temporal do gap racial 2018–2023
- Modelo 2: notas → escolha de curso tech (mulheres)
- **Modelo 7.1: classificação multiclasse — qual área a mulher vai escolher (Tech / Saúde / Exatas / Humanas)**
- Análise 6.1: nota de corte vs nota da candidata (folga de nota)
- Análise 6.3: comparação de poder preditivo entre mulheres e homens

**Dado gerado:** `modelo_multiclasse.pkl` e `modelo_multiclasse_sem_turno.pkl` — exportado para o Hugging Face.

---

### `TCC_Mulheres_Lideranca_TI_RAIS_CENSO.ipynb`

Análise com dados da RAIS 2022 e Censo da Educação Superior 2023.

**O que este notebook cobre:**
- Participação feminina em cursos de tecnologia: ingresso (~18%), matrícula (~17%), conclusão (~15%)
- Comparação por bloco regional (MG/ES/RJ, Centro-Oeste, Nordeste etc.)
- Distribuição de profissionais em cargos de TI por gênero e raça
- Distribuição por escolaridade (77% com ensino superior completo ou em andamento)
- Achado regional: no Nordeste, mulheres pardas têm maior representatividade em liderança

---

## Como rodar

Os notebooks foram desenvolvidos e testados no **Google Colab**.
A forma mais simples de reproduzir é abrir direto no Colab pelo README principal.

### Opção 1 — Google Colab (recomendado)

1. Acesse os badges **"Open in Colab"** no [README principal](../README.md)
2. O notebook abre diretamente no Colab
3. Conecte ao Google Drive para acessar os dados (veja `../data/README.md`)
4. Execute célula a célula (`Ctrl+Enter` ou `Runtime → Run all`)

### Opção 2 — Localmente com Jupyter

```bash
pip install jupyter pandas numpy scikit-learn matplotlib seaborn plotly joblib
jupyter notebook
```
> ⚠️ Os dados brutos não estão incluídos no repositório.

# Dados brutos

Os dados brutos utilizados na pesquisa não estão incluídos neste repositório
por conta do tamanho (vários GBs cada). Esta página reúne as instruções
de download de cada fonte oficial.

---

## Fontes e instruções de download

### ENEM 2018–2023 — Microdados

**Utilizado em:** `notebooks/tcc_modelagem_genero_tecnologia_ENEM_SISU.ipynb`

**O que baixar:** microdados de cada edição (2018, 2019, 2020, 2021, 2022, 2023)

**Como baixar:**
1. Acesse [gov.br/inep — Microdados ENEM](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem)
2. Clique no ano desejado → baixe o `.zip`
3. Extraia e localize o arquivo `.csv` principal (ex: `MICRODADOS_ENEM_2023.csv`)

**Tamanho aproximado:** 2–4 GB por edição (arquivo CSV descomprimido)

**Filtros aplicados na pesquisa:**
- Sexo = Feminino (`TP_SEXO == 'F'`)
- Apenas candidatas presentes em todas as provas
- Anos: 2018 a 2023

---

### SISU 2023 — Microdados

**Utilizado em:** `notebooks/tcc_modelagem_genero_tecnologia_ENEM_SISU.ipynb`

**Como baixar:**
1. Acesse [gov.br/mec — Dados Abertos SISU](https://www.gov.br/mec/pt-br/acesso-a-informacao/dados-abertos)
2. Localize "SISU 2023" e baixe o arquivo de inscritos/selecionados

**Filtros aplicados na pesquisa:**
- Sexo = Feminino
- Opção 1 de curso (`NO_OPCAO == 1`)

---

### Censo da Educação Superior 2023 — Microdados

**Utilizado em:** `notebooks/TCC_Mulheres_Lideranca_TI_RAIS_CENSO.ipynb`

**Como baixar:**
1. Acesse [gov.br/inep — Microdados Censo Superior](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-da-educacao-superior)
2. Selecione o ano 2023 → baixe o `.zip`
3. Os arquivos relevantes são:
   - `MICRODADOS_CADASTRO_CURSOS_2023.CSV` — cursos por IES
   - `MICRODADOS_CADASTRO_ALUNOS_2023.CSV` — alunos (ingresso, matrícula, conclusão)

**Tamanho aproximado:** 1–3 GB descomprimido

**Filtros aplicados na pesquisa:**
- Cursos da área de TI (Ciência da Computação, Sistemas de Informação, Engenharia de Computação etc.)
- Variáveis de participação feminina: `QT_ING_FEM`, `QT_MAT_FEM`, `QT_CONC_FEM`

---

### RAIS 2022 — Relação Anual de Informações Sociais

**Utilizado em:** `notebooks/TCC_Mulheres_Lideranca_TI_RAIS_CENSO.ipynb`

**Como baixar:**
1. Acesse [gov.br/trabalho — RAIS](https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/rais)
2. Clique em "Microdados" → selecione 2022
3. Baixe por UF ou o arquivo nacional (requer cadastro no portal)

> ⚠️ O acesso aos microdados da RAIS pode exigir cadastro no portal do MTE.
> Como alternativa, os dados agregados estão disponíveis no
> [Portal de Dados Abertos](https://dados.gov.br/dados/conjuntos-dados/relacao-anual-de-informacoes-sociais-rais).

**Filtros aplicados na pesquisa:**
- CBO (Classificação Brasileira de Ocupações) relacionados a TI
- Recortes: gênero, raça/cor, escolaridade, faixa etária, UF


## Estrutura de pastas recomendada para rodar os notebooks

```
data/
├── samples/              ← incluído no repositório
├── enem/
│   ├── 2018/MICRODADOS_ENEM_2018.csv
│   ├── 2019/MICRODADOS_ENEM_2019.csv
│   ├── ...
│   └── 2023/MICRODADOS_ENEM_2023.csv
├── sisu/
│   └── 2023/MICRODADOS_SISU_2023.csv
├── censo/
│   └── 2023/MICRODADOS_CADASTRO_CURSOS_2023.CSV
└── rais/
    └── 2022/RAIS_2022_*.txt
```

Os notebooks referenciam os caminhos relativos a partir desta estrutura.
Se seus arquivos estiverem em locais diferentes, ajuste as variáveis de
caminho no início de cada notebook.

---

## Dependências dos notebooks

```
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.18.0
joblib>=1.3.0
scipy>=1.10.0
```

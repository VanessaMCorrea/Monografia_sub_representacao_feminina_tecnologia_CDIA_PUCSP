# Dados

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

---

## Dados de amostra (incluídos no repositório)

A pasta `samples/` contém CSVs sintéticos para testar o app sem precisar
dos dados reais:

| Arquivo | Descrição |
|---|---|
| `massa_10_alunas.csv` | 10 perfis curados com características extremas |
| `massa_30_alunas.csv` | 30 nomes femininos brasileiros, distribuição realista |
| `massa_edge_cases.csv` | 13 casos extremos para validação do modelo |

Formato: `NOME_ALUNA, NOTA_M, NOTA_CN, NOTA_L, NOTA_CH, NOTA_R, NOTA_CANDIDATO, IDADE, REGIAO, COTA`

---

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

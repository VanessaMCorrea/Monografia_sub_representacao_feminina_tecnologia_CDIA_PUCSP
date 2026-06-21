# Sub-representação feminina em tecnologia: modelagem preditiva da trajetória do ensino médio à liderança com recorte racial no Brasil

**Autora:** Vanessa Marques Correa  
**Orientador:** Prof. David de Oliveira Lemes   
**Coorientadora:** Profa. Myrt Thania de Souza Cruz 
**Instituição:** PUC-SP — Curso de Ciência de Dados e Inteligência Artificial  
**Ano:** 2026  

---

## Sobre o projeto

Este repositório contém os notebooks, dados e entregáveis do Trabalho de Conclusão de Curso (TCC) e da Iniciação Científica (IC/PIBIC–PUC-SP) desenvolvidos em paralelo com a seguinte questão de pesquisa:

> *Em que medida o desempenho acadêmico (notas do ENEM) explica a escolha por cursos de tecnologia entre mulheres no SISU, e como a modelagem preditiva pode localizar empiricamente em que ponto ao longo da trajetória do ensino médio à liderança em tecnologia a sub-representação feminina — com recorte racial — se constitui?*

A investigação partiu do mercado de trabalho (RAIS) e recuou até o ensino médio (ENEM), revelando que o gargalo principal da sub-representação feminina em tecnologia não está na contratação, mas na escolha de curso — moldada por fatores socioeconômicos e raciais que operam antes do processo seletivo.

---

## Estrutura do repositório

```
📦 tcc-mulheres-lideranca-tecnologia/
│
├── 📓 notebooks/
│   ├── TCC_Mulheres_Lideranca_TI_RAIS_CENSO.ipynb   ← IC: análise RAIS + Censo
│   └── tcc_modelagem_genero_tecnologia_ENEM_SISU.ipynb  ← TCC: modelagem preditiva
│
├── 🤖 entregavel/
│   └── app_modelo_preditivo/                         ← Cap. 8: ferramenta de apoio à decisão
│       ├── app.py                                    ← Interface Streamlit
│       ├── modelo_multiclasse.pkl                    ← Modelo 3 exportado (joblib)
│       ├── template_alunas.csv                       ← Template de entrada
│       └── requirements.txt
│
├── 📊 figuras/                                       ← Gráficos gerados pelos notebooks
│
└── README.md
```

---

## Bases de dados utilizadas

| Base | Fonte | Período | Eixo | Uso |
|---|---|---|---|---|
| RAIS | MTE | 2023 | IC | Mercado formal de TI — gênero, raça, escolaridade, liderança |
| Censo da Educação Superior | INEP | 2023 | IC | Ingressantes, matrículas e concluintes em tecnologia |
| ENEM (microdados) | INEP | 2018–2023 | TCC | Desempenho em Matemática e perfil socioeconômico |
| SISU | MEC/SESu | 2023 | TCC | Escolha de curso por área de conhecimento |

> **Nota:** As bases não estão incluídas neste repositório por restrições de tamanho e licença. Os microdados do ENEM e do SISU estão disponíveis gratuitamente no portal do INEP. Os microdados da RAIS estão disponíveis no portal do MTE. O Censo da Educação Superior está disponível no portal do INEP.

---

## Notebooks

### `TCC_Mulheres_Lideranca_TI_RAIS_CENSO.ipynb` — Eixo IC

Análise descritiva das bases RAIS 2023 e Censo da Educação Superior 2023.

**Principais análises:**
- Distribuição de mulheres em funções técnicas de TI e liderança por gênero, raça e escolaridade
- Comparação da participação feminina nas etapas de ingresso, matrícula e conclusão em cursos de tecnologia
- Construção da cadeia completa: da liderança à escolha de curso

**Principais achados:**
- 21,82% das funções técnicas de TI são ocupadas por mulheres; 23,81% das posições de liderança
- Taxa de liderança: 13,45% para mulheres vs 12,02% para homens — proporcional à presença no setor
- Concluintes em tecnologia: apenas 17,49% são mulheres — o gargalo está na formação, não na contratação
- 96,5% das mulheres líderes em TI possuem Ensino Superior completo ou pós-graduação

---

### `tcc_modelagem_genero_tecnologia_ENEM_SISU.ipynb` — Eixo TCC

Modelagem preditiva supervisionada sobre microdados do ENEM (2018–2023) e SISU (2023).

**Modelos desenvolvidos:**

#### Modelo 1 — O que determina a nota em Matemática?
- **Tipo:** Regressão Linear + Random Forest Regressor
- **Base:** ENEM 2021–2023 (1.164.428 candidatas)
- **Variável dependente:** Nota em Matemática (escala TRI)
- **R²:** 0,257 (RL) / 0,290 (RF) | **MAE:** 84,6 pts (RL) / 82,5 pts (RF)
- **Achado principal:** Ocupação dos pais é o maior preditor (53,6% de importância no RF), acima da renda. Penalização racial autônoma de −16,3 pts para mulheres negras após controle socioeconômico.

#### Modelo 2 — A nota prediz a escolha de tecnologia?
- **Tipo:** Regressão Logística + Árvore de Decisão + Random Forest (classificação binária)
- **Base:** SISU 2023 (385.929 candidatas) | Desbalanceamento 27:1 corrigido com SMOTE
- **Variável dependente:** IS_TECH (escolheu tecnologia: sim/não)
- **AUC:** 0,581 / 0,589 / 0,622 | **F1 máx.:** 0,097
- **Achado principal:** Nota em Matemática não prediz escolha de tecnologia entre mulheres (r=0,024). Para homens, r=0,054. A barreira não é cognitiva.

#### Modelo 3 — A barreira é específica de tecnologia?
- **Tipo:** Random Forest multiclasse (class_weight='balanced')
- **Base:** SISU 2023 | 4 classes: Tecnologia, Saúde, Exatas, Humanas
- **F1 por área:** Saúde 0,748 | Humanas 0,718 | Exatas 0,232 | **Tecnologia 0,136**
- **Achado principal:** O modelo prevê bem Saúde e Humanas, mas falha especificamente em Tecnologia — a barreira de escolha é específica dessa área, não uma imprevisibilidade geral.

#### Modelo 4 — O retorno socioeconômico é igual para todas?
- **Tipo:** Regressões Lineares separadas por subgrupo racial (stratified modeling)
- **Base:** ENEM 2021–2023
- **Achado principal:** O retorno do capital ocupacional dos pais vale +24,2 pts/grupo para filhas brancas e apenas +17,4 pts para negras. O mesmo capital familiar produz retornos racialmente desiguais.

---

## Entregável — Modelo preditivo de escolha de curso

O Capítulo 8 do TCC apresenta uma ferramenta de apoio à decisão para escolas, construída a partir do Modelo 3. A ferramenta permite que escolas públicas identifiquem turmas com baixo perfil previsto para tecnologia e promovam ações direcionadas antes do processo seletivo.

**Tecnologias:** Python · Streamlit · scikit-learn · joblib · pandas

**Como executar:**
```bash
pip install -r entregavel/app_modelo_preditivo/requirements.txt
streamlit run entregavel/app_modelo_preditivo/app.py
```

**Funcionalidades:**
- Upload de CSV com perfil das alunas (notas do ENEM, região, turno, modalidade de cota)
- Predição da probabilidade de escolha por área para cada aluna
- Visão agregada da turma com distribuição prevista por área
- Alertas automáticos quando o percentual previsto para tecnologia está abaixo de limiar configurável

---

## Principais resultados

| Achado | Evidência |
|---|---|
| O gargalo não está na contratação | Taxa de liderança: 13,45% (mulheres) vs 12,02% (homens) — proporcional |
| O gargalo está na formação | Concluintes em tech: 17,49% mulheres — reflete a proporção no mercado |
| A barreira não é cognitiva | Nota MT não prediz escolha de tech (r=0,024); mulheres em tech têm nota maior |
| A barreira é específica de tecnologia | F1=0,136 em tech vs 0,748 em Saúde no Modelo 3 |
| O retorno do capital familiar é racialmente desigual | OCUP_PAI: +24,2 pts (brancas) vs +17,4 pts (negras) |
| O gap racial cresce | Gap MT: 45,8 pts (2018) → 77,2 pts (2023) — +68% |

---

## Referências principais

- BREIMAN, L. Random Forests. *Machine Learning*, v. 45, n. 1, p. 5–32, 2001.
- CHAWLA, N. V. et al. SMOTE: Synthetic Minority Over-sampling Technique. *Journal of Artificial Intelligence Research*, v. 16, p. 321–357, 2002.
- CRENSHAW, K. Demarginalizing the intersection of race and sex. *University of Chicago Legal Forum*, 1989.
- INEP. Microdados do ENEM 2021–2023. Brasília: INEP, 2023.
- MEC/SESu. Sistema de Seleção Unificada — SISU 2023. Brasília: MEC, 2023.
- MTE. Relação Anual de Informações Sociais — RAIS 2023. Brasília: MTE, 2023.
- WALTON, G. M.; COHEN, G. L. A brief social-belonging intervention improves academic and health outcomes. *Science*, v. 331, p. 1447–1451, 2011.

---

## Licença

Este projeto é disponibilizado para fins acadêmicos e de pesquisa.  
Os modelos e código são de autoria de Vanessa Marques Correa (PUC-SP, 2026).

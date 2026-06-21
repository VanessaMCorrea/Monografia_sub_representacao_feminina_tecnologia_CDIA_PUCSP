# Entregável - Painel de Incentivo à Tecnologia

Aplicativo Streamlit que classifica alunas em 3 grupos de intervenção
com base nas probabilidades geradas pelo modelo Random Forest.

---

## O que o painel faz

A partir de um CSV com o perfil acadêmico das alunas, o painel:

1. Roda o modelo e gera probabilidades para cada área (Tech / Saúde / Exatas / Humanas)
2. Classifica cada aluna em um dos 3 grupos de intervenção
3. Exibe cards individuais com ranking de probabilidades, perfil e ação recomendada
4. Permite filtrar por área prevista e ajustar os parâmetros de classificação
5. Exporta o resultado com os grupos anotados em CSV

### Grupos de intervenção

| Grupo | Critério | Ação recomendada |
|---|---|---|
| 🚀 G3 Confirmadas em Tech | Área prevista = Tech | Mentoria de retenção |
| ⚡ G2 Borda de Tech | Tech em 2º/3º com gap ≤ 15pp | Encontro em grupo, visita técnica |
| 💡 G1 Potencial Técnico Oculto | NOTA_M ≥ P60 da turma, não prevista Tech | Atendimento individual |

---

## Como rodar

### 1. Pré-requisitos

- Python 3.10 ou superior
- pip

### 2. Instalar dependências

```bash
cd app
pip install -r requirements.txt
```

### 3. Rodar o app

```bash
streamlit run painel_grupos_tech.py
```

Abre em `http://localhost:8501`

**O modelo é baixado automaticamente do Hugging Face na primeira execução.**
Após o download, fica salvo localmente como `modelo_multiclasse.pkl`
e não precisa baixar novamente.

> Modelo: [VanessaMCorrea/modelo_multiclasse_sem_turno](https://huggingface.co/VanessaMCorrea/modelo_multiclasse_sem_turno)

---

## Formato do CSV de entrada

| Coluna | Tipo | Valores aceitos |
|---|---|---|
| `NOME_ALUNA` | texto | qualquer (opcional) |
| `NOTA_M` | numérico | 0–1000 |
| `NOTA_CN` | numérico | 0–1000 |
| `NOTA_L` | numérico | 0–1000 |
| `NOTA_CH` | numérico | 0–1000 |
| `NOTA_R` | numérico | 0–1000 |
| `NOTA_CANDIDATO` | numérico | média geral |
| `IDADE` | inteiro | — |
| `REGIAO` | texto | `N` · `NE` · `CO` · `SE` · `S` |
| `COTA` | texto | `Ampla` · `Cota` |

> A coluna `TURNO` é aceita mas ignorada (removida do modelo v2 após análise de importância).

### Massas de teste

Use os CSVs da pasta `../data/samples/` para testar sem dados reais:

```bash
# Na interface do app, faça upload de:
../data/samples/massa_30_alunas.csv   # recomendado para testar todos os grupos
../data/samples/massa_10_alunas.csv   # perfis curados
../data/samples/massa_edge_cases.csv  # casos extremos para validação
```

---

## Sobre o modelo

- **Algoritmo:** Random Forest Multiclasse com `class_weight='balanced'`
- **Treino:** SISU 2023 — 323.008 candidatas (mulheres, opção 1)
- **Features (12):** NOTA_M, NOTA_CN, NOTA_L, NOTA_CH, NOTA_R, NOTA_CANDIDATO, IDADE, REGIAO (dummies), COTA (dummy)
- **TURNO removido:** após análise revelar importância espúria de 36% (correlação com área, não causalidade)
- **F1-macro:** 0.346 · **F1 Tech:** 0.106 (intencional — ver README principal)

---

## Ajuste de parâmetros (sidebar)

| Parâmetro | Padrão | O que controla |
|---|---|---|
| Gap máximo G2 | 15pp | Distância máxima entre prob. 1ª área e prob. Tech para entrar no G2 |
| Percentil mínimo MT | P60 | Piso de NOTA_M relativo à turma para entrar no G1 |
| Filtro por área | Todas | Filtra cards individuais pela área prevista pelo modelo |

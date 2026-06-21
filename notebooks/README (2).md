# Notebooks

Esta pasta contém os dois notebooks Jupyter desenvolvidos no Google Colab
com toda a análise exploratória, modelagem e resultados da pesquisa.

---

## Notebooks

### `tcc_modelagem_genero_tecnologia_ENEM_SISU.ipynb`

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

**Dado gerado:** `modelo_multiclasse.pkl` — exportado para o Hugging Face.

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
> Consulte [`../data/README.md`](../data/README.md) para instruções de download.

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

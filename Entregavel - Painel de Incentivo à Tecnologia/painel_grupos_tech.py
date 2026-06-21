import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Painel de Incentivo à Tech",
    page_icon="🔍",
    layout="wide",
)

# ─────────────────────────────────────────────────────────────────────────────
# PALETA
# ─────────────────────────────────────────────────────────────────────────────
CORES_AREA = {
    "Tech":    "#D4537E",
    "Saúde":   "#5C4DBF",
    "Exatas":  "#1D9E75",
    "Humanas": "#B0AEC9",
}

GRUPOS = {
    1: {
        "nome":  "Potencial Técnico Oculto",
        "emoji": "💡",
        "cor":   "#F59E0B",
        "desc":  "Nota de Matemática acima da média da turma, mas área prevista fora de Tech. "
                 "O bloqueio não é desempenho — é pertencimento e exposição.",
        "acao":  "Atendimento individual: explorar autopercepção em relação à tecnologia, "
                 "apresentar referências femininas em TI, discutir identidade e pertencimento.",
    },
    2: {
        "nome":  "Borda de Tech",
        "emoji": "⚡",
        "cor":   "#8B5CF6",
        "desc":  "Tech aparece em 2º ou 3º lugar com margem pequena para a área prevista. "
                 "O modelo está incerto — são as mais responsivas a uma intervenção.",
        "acao":  "Encontro em grupo: exposição a carreiras de TI, visita técnica ou "
                 "conversa com profissional de tecnologia. Baixo esforço, alto potencial de impacto.",
    },
    3: {
        "nome":  "Confirmadas em Tech",
        "emoji": "🚀",
        "cor":   "#D4537E",
        "desc":  "Área prevista é Tech. Foco em retenção, aprofundamento e construção de rede.",
        "acao":  "Mentoria de continuidade: conectar com programas como RePrograma, PyLadies, "
                 "WoMakersCode. Incentivar projetos, hackathons e olimpíadas.",
    },
}

COLUNAS_OBRIGATORIAS = [
    "NOTA_M","NOTA_CN","NOTA_L","NOTA_CH","NOTA_R",
    "NOTA_CANDIDATO","IDADE","REGIAO","COTA",
]

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #F7F8FA; }

.g-card {
    background: #fff;
    border-radius: 12px;
    padding: 20px 22px;
    border-left: 5px solid;
    box-shadow: 0 1px 6px rgba(0,0,0,0.07);
    margin-bottom: 8px;
}
.g-card .g-num  { font-size: 2.4rem; font-weight: 700; font-family: 'DM Mono', monospace; }
.g-card .g-lbl  { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; color:#6B7280; margin-top:2px; }
.g-card .g-desc { font-size: 0.82rem; color:#374151; margin-top:10px; line-height:1.5; }
.g-card .g-acao { font-size: 0.8rem;  color:#6B7280;  margin-top:8px;  line-height:1.5; }

.aluna-row {
    background: #fff;
    border-radius: 8px;
    padding: 12px 16px;
    border-left: 4px solid;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    margin-bottom: 6px;
}
.aluna-row .ar-nome { font-size:0.9rem; font-weight:600; color:#111827; }
.aluna-row .ar-sub  { font-size:0.78rem; color:#6B7280; margin-top:2px; }
.aluna-row .ar-rank { font-size:0.78rem; color:#9CA3AF; margin-top:4px; }

.pill  { display:inline-block; padding:2px 9px; border-radius:20px;
         font-size:0.73rem; font-weight:600; color:#fff; margin-right:4px; }
.badge { display:inline-block; padding:2px 8px; border-radius:6px;
         font-size:0.72rem; font-weight:600; }

.section-title { font-size:0.68rem; font-weight:700; text-transform:uppercase;
                 letter-spacing:0.12em; color:#9CA3AF; margin-bottom:10px;
                 padding-bottom:6px; border-bottom:1px solid #E5E7EB; }

.dropzone { text-align:center; padding:3.5rem; border:1.5px dashed #D1D5DB;
            border-radius:12px; color:#9CA3AF; }
.info-box { background:#EFF6FF; border:1px solid #BFDBFE; border-radius:8px;
            padding:12px 16px; font-size:0.83rem; color:#1E40AF; margin:10px 0; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# MODELO
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource
def carregar_modelo():
    for path in ["modelo_multiclasse_sem_turno.pkl"]:
        if os.path.exists(path):
            return joblib.load(path)
    return None

modelo_pkg = carregar_modelo()


def preparar_features(df_raw):
    colunas_modelo = modelo_pkg["colunas"] if modelo_pkg else [
        "NOTA_M","NOTA_CN","NOTA_L","NOTA_CH","NOTA_R","NOTA_CANDIDATO","IDADE",
        "REGIAO_N","REGIAO_NE","REGIAO_S","REGIAO_SE","COTA_Cota",
    ]
    df = df_raw[["NOTA_M","NOTA_CN","NOTA_L","NOTA_CH","NOTA_R",
                 "NOTA_CANDIDATO","IDADE"]].copy().astype(float)
    for reg in ["N","NE","S","SE"]:
        df[f"REGIAO_{reg}"] = (df_raw["REGIAO"].str.strip().str.upper() == reg).astype(int)
    df["COTA_Cota"] = (df_raw["COTA"].str.strip().str.capitalize() == "Cota").astype(int)
    return df.reindex(columns=colunas_modelo, fill_value=0)


def prever(df_raw):
    feats = preparar_features(df_raw)
    if modelo_pkg is None:
        np.random.seed(42)
        p = np.random.dirichlet([1.5,4.0,1.0,6.0], size=len(df_raw))
        return pd.DataFrame(p, columns=["Tech","Saúde","Exatas","Humanas"])
    m = modelo_pkg["modelo"]
    return pd.DataFrame(modelo_pkg["modelo"].predict_proba(feats),
                        columns=m.classes_)


# ─────────────────────────────────────────────────────────────────────────────
# CLASSIFICAÇÃO DOS GRUPOS
# ─────────────────────────────────────────────────────────────────────────────
def classificar_grupos(df_raw, df_probs, limiar_gap=0.15, percentil_mt=60):
    classes = df_probs.columns.tolist()
    area_prev = df_probs.idxmax(axis=1)
    p60_mt    = df_raw["NOTA_M"].quantile(percentil_mt / 100)

    rows = []
    for i in range(len(df_probs)):
        p       = df_probs.iloc[i]
        ranked  = p.sort_values(ascending=False)
        rank_tech = ranked.index.tolist().index("Tech") + 1
        prob_1a   = ranked.iloc[0]
        gap_tech  = float(prob_1a - p["Tech"])
        prev      = area_prev.iloc[i]
        mt        = float(df_raw["NOTA_M"].iloc[i])

        if prev == "Tech":
            grupo = 3
        elif rank_tech in [2, 3] and gap_tech <= limiar_gap:
            grupo = 2
        elif mt >= p60_mt and prev != "Tech":
            grupo = 1
        else:
            grupo = 0

        rows.append({
            "area_prevista": prev,
            "prob_Tech":     float(p["Tech"]),
            "prob_1a":       float(prob_1a),
            "gap_tech":      gap_tech,
            "rank_tech":     rank_tech,
            "ranking":       " › ".join(ranked.index.tolist()),
            "grupo":         grupo,
            **{f"prob_{c}": float(p[c]) for c in classes},
        })

    return pd.DataFrame(rows), p60_mt


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS VISUAIS
# ─────────────────────────────────────────────────────────────────────────────
def pill(texto, cor):
    return f'<span class="pill" style="background:{cor}">{texto}</span>'

def badge(texto, bg, fg="#fff"):
    return f'<span class="badge" style="background:{bg};color:{fg}">{texto}</span>'

def barra_prob(prob, cor, label):
    w = int(prob * 100)
    return (f'<div style="display:flex;align-items:center;gap:6px;margin:2px 0">'
            f'<span style="font-size:0.72rem;color:#6B7280;width:68px">{label}</span>'
            f'<div style="background:#F3F4F6;border-radius:4px;width:120px;height:8px">'
            f'<div style="background:{cor};border-radius:4px;width:{w}%;height:8px"></div></div>'
            f'<span style="font-size:0.72rem;font-family:monospace;color:#374151">{prob*100:.0f}%</span>'
            f'</div>')


def card_aluna(nome, dados, res, cor_grupo):
    # Coleta colunas prob_* do res dinamicamente (robusto a acentos no Windows)
    # k[5:] remove o prefixo "prob_" para obter o nome da area
    prob_cols = sorted(
        [k for k in res.index if str(k).startswith("prob_") and k not in ("prob_1a",)],
        key=lambda k: -float(res[k]),
    )
    probs_html = "".join([
        barra_prob(
            float(res[k]),
            CORES_AREA.get(k[5:], "#888"),
            k[5:],
        )
        for k in prob_cols
    ])
    rank_badge = f'Tech #{res["rank_tech"]}'
    gap_txt    = f'gap {res["gap_tech"]*100:.0f}pp'
    return (
        f'<div class="aluna-row" style="border-color:{cor_grupo}">'
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start">'
        f'  <div>'
        f'    <div class="ar-nome">{nome}</div>'
        f'    <div class="ar-sub">'
        f'      MT={dados["NOTA_M"]:.0f} &nbsp;|&nbsp; '
        f'      Geral={dados["NOTA_CANDIDATO"]:.0f} &nbsp;|&nbsp; '
        f'      {dados["REGIAO"]} &nbsp;|&nbsp; {dados["COTA"]} &nbsp;|&nbsp; Idade {dados["IDADE"]:.0f}'
        f'    </div>'
        f'    <div class="ar-rank">Ranking: {res["ranking"]}</div>'
        f'  </div>'
        f'  <div style="text-align:right">'
        f'    {pill(res["area_prevista"], CORES_AREA.get(res["area_prevista"],"#888"))}'
        f'    {badge(rank_badge, cor_grupo)}'
        f'    &nbsp;'
        f'    {badge(gap_txt, "#F3F4F6", "#374151")}'
        f'  </div>'
        f'</div>'
        f'<div style="margin-top:10px">{probs_html}</div>'
        f'</div>'
    )


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Painel de Grupos Tech")
    st.markdown("Identificação de perfis para  \nincentivo à escolha de TI")
    st.divider()

    st.markdown("**Parâmetros de classificação**")
    limiar_gap = st.slider(
        "Gap máximo para Grupo 2 (pp)",
        min_value=5, max_value=30, value=15, step=5,
        help="Diferença máxima entre a área prevista e Tech para considerar 'borda'"
    ) / 100

    percentil_mt = st.slider(
        "Percentil mínimo NOTA_M — Grupo 1",
        min_value=40, max_value=80, value=60, step=10,
        help="Alunas acima desse percentil de Matemática são candidatas ao Grupo 1"
    )

    st.divider()
    st.markdown("**Filtrar por área prevista**")
    areas_disponiveis = ["Todas", "Tech", "Saúde", "Exatas", "Humanas"]
    filtro_area = st.selectbox(
        "Mostrar alunas cuja área prevista é:",
        options=areas_disponiveis,
        index=0,
        help="Filtra os cards individuais dentro de cada grupo pelo que o modelo previu para a aluna"
    )

    st.divider()
    st.markdown("**Legenda de grupos**")
    for g, info in GRUPOS.items():
        st.markdown(
            f'<span style="display:inline-block;width:10px;height:10px;'
            f'border-radius:50%;background:{info["cor"]};margin-right:6px"></span>'
            f'{info["emoji"]} Grupo {g} — {info["nome"]}',
            unsafe_allow_html=True,
        )
    st.divider()

    if modelo_pkg:
        st.success("✓ Modelo carregado")
        st.caption(f'{len(modelo_pkg["colunas"])} features · sem TURNO')
    else:
        st.warning("Modo demonstração")


# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("# 🔍 Painel de Incentivo à Tecnologia")
st.caption(
    "Classifica alunas em 3 grupos de intervenção com base no perfil preditivo do modelo. "
    "A fraqueza do modelo em Tech é intencional: revela que o bloqueio não é acadêmico."
)

st.markdown("""<div class="info-box">
<strong>Como interpretar:</strong> o modelo Random Forest acerta bem Humanas e Saúde,
mas falha sistematicamente em Tech (F1=0.106). Isso não é um defeito — é o achado central:
a escolha por carreiras tecnológicas por mulheres não é explicada pelo perfil de notas.
Os grupos abaixo identificam onde a intervenção tem maior potencial de impacto.
</div>""", unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# UPLOAD
# ─────────────────────────────────────────────────────────────────────────────
uploaded = st.file_uploader("Upload do CSV com os dados das alunas", type=["csv"])

if uploaded is None:
    st.markdown("""<div class="dropzone">
        <div style="font-size:40px;margin-bottom:12px">📂</div>
        <div style="font-size:15px;font-weight:500;margin-bottom:6px">
            Faça upload do CSV com os dados das alunas
        </div>
        <div style="font-size:13px">
            Colunas: NOME_ALUNA · NOTA_M · NOTA_CN · NOTA_L · NOTA_CH · NOTA_R
            · NOTA_CANDIDATO · IDADE · REGIAO · COTA
        </div>
    </div>""", unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# LEITURA E VALIDAÇÃO
# ─────────────────────────────────────────────────────────────────────────────
try:
    df_upload = pd.read_csv(uploaded, encoding="utf-8")
except Exception:
    df_upload = pd.read_csv(uploaded, encoding="latin1")

faltando = [c for c in COLUNAS_OBRIGATORIAS if c not in df_upload.columns]
if faltando:
    st.error(f"❌ Colunas faltando: `{'`, `'.join(faltando)}`")
    st.stop()

nome_col = "NOME_ALUNA" if "NOME_ALUNA" in df_upload.columns else None
nomes    = df_upload[nome_col].astype(str).tolist() if nome_col else \
           [f"Aluna {i+1}" for i in range(len(df_upload))]

# ─────────────────────────────────────────────────────────────────────────────
# PREDIÇÃO E CLASSIFICAÇÃO
# ─────────────────────────────────────────────────────────────────────────────
df_probs  = prever(df_upload)
df_res, p60_mt = classificar_grupos(df_upload, df_probs, limiar_gap, percentil_mt)
df_res.insert(0, "nome", nomes)

n_total = len(df_upload)
n_g1 = (df_res["grupo"] == 1).sum()
n_g2 = (df_res["grupo"] == 2).sum()
n_g3 = (df_res["grupo"] == 3).sum()
n_g0 = (df_res["grupo"] == 0).sum()

# Composição por área dentro de cada grupo
def composicao_grupo(g):
    sub = df_res[df_res["grupo"] == g]["area_prevista"].value_counts()
    partes = [f"{n} {a}" for a, n in sub.items()]
    return " · ".join(partes) if partes else "—"

comp = {g: composicao_grupo(g) for g in [1, 2, 3, 0]}

# ─────────────────────────────────────────────────────────────────────────────
# CARDS DE RESUMO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Distribuição da turma</div>', unsafe_allow_html=True)

c0, c1, c2, c3, c4 = st.columns(5)
for col, (n, lbl, cor, emoji) in zip([c0,c1,c2,c3,c4], [
    (n_total, "Total",                      "#374151", "👩‍🎓"),
    (n_g3,   "Confirmadas em Tech",          GRUPOS[3]["cor"], "🚀"),
    (n_g2,   "Borda de Tech",                GRUPOS[2]["cor"], "⚡"),
    (n_g1,   "Potencial oculto",             GRUPOS[1]["cor"], "💡"),
    (n_g0,   "Fora dos grupos",              "#D1D5DB", "—"),
]):
    col.markdown(
        f'<div class="g-card" style="border-color:{cor}">'
        f'<div class="g-num" style="color:{cor}">{n}</div>'
        f'<div class="g-lbl">{emoji} {lbl}</div>'
        f'<div class="g-desc" style="font-size:0.75rem;color:#9CA3AF">'
        f'{n/n_total*100:.0f}% da turma</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# GRÁFICOS DE VISÃO GERAL
# ─────────────────────────────────────────────────────────────────────────────
col_v1, col_v2 = st.columns(2)

with col_v1:
    st.markdown('<div class="section-title">Distribuição dos grupos</div>', unsafe_allow_html=True)
    GRUPOS_NOMES = {
        3: ("🚀 G3 Confirmadas em Tech",   GRUPOS[3]["cor"]),
        2: ("⚡ G2 Borda de Tech",          GRUPOS[2]["cor"]),
        1: ("💡 G1 Potencial oculto",       GRUPOS[1]["cor"]),
        0: ("— Fora dos grupos",            "#D1D5DB"),
    }
    df_dist = pd.DataFrame([
        {"Grupo": GRUPOS_NOMES[g][0], "N": n, "Cor": GRUPOS_NOMES[g][1]}
        for g, n in [(3,n_g3),(2,n_g2),(1,n_g1),(0,n_g0)]
        if n > 0
    ])
    cor_map_dist = dict(zip(df_dist["Grupo"], df_dist["Cor"]))
    fig_g = px.bar(df_dist, x="N", y="Grupo", orientation="h",
                   color="Grupo",
                   color_discrete_map=cor_map_dist,
                   text="N", template="plotly_white")
    fig_g.update_traces(textposition="outside", showlegend=False)
    fig_g.update_layout(
        height=280, margin=dict(t=10,b=10,l=10,r=40),
        xaxis_title="Nº de alunas", yaxis_title="",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#F3F4F6"),
        showlegend=False,
    )
    st.plotly_chart(fig_g, use_container_width=True)

with col_v2:
    st.markdown('<div class="section-title">Prob. Tech por grupo</div>', unsafe_allow_html=True)
    df_box = df_res[df_res["grupo"] > 0].copy()
    df_box["Grupo"] = df_box["grupo"].map(
        {1:"G1 Potencial oculto", 2:"G2 Borda de Tech", 3:"G3 Confirmadas"}
    )
    fig_box = px.box(
        df_box, x="Grupo", y="prob_Tech",
        color="Grupo",
        color_discrete_map={
            "G1 Potencial oculto": GRUPOS[1]["cor"],
            "G2 Borda de Tech":    GRUPOS[2]["cor"],
            "G3 Confirmadas":      GRUPOS[3]["cor"],
        },
        points="all", template="plotly_white",
    )
    fig_box.update_layout(
        height=280, margin=dict(t=10,b=10),
        yaxis_title="Probabilidade Tech",
        yaxis=dict(tickformat=".0%", gridcolor="#F3F4F6"),
        xaxis_title="", showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_box, use_container_width=True)

# Scatter NOTA_M × prob_Tech colorido por grupo
st.markdown('<div class="section-title">NOTA_M × Probabilidade Tech — por grupo</div>',
            unsafe_allow_html=True)

df_scatter = df_res.copy()
df_scatter["NOTA_M"] = df_upload["NOTA_M"].values
df_scatter["nome_vis"] = nomes
df_scatter["grupo_label"] = df_scatter["grupo"].map({
    0: "Fora dos grupos",
    1: "💡 G1 Potencial oculto",
    2: "⚡ G2 Borda de Tech",
    3: "🚀 G3 Confirmadas",
})
cor_map = {
    "Fora dos grupos":        "#E5E7EB",
    "💡 G1 Potencial oculto": GRUPOS[1]["cor"],
    "⚡ G2 Borda de Tech":    GRUPOS[2]["cor"],
    "🚀 G3 Confirmadas":      GRUPOS[3]["cor"],
}
fig_sc = px.scatter(
    df_scatter, x="NOTA_M", y="prob_Tech",
    color="grupo_label", color_discrete_map=cor_map,
    hover_name="nome_vis",
    hover_data={"area_prevista": True, "gap_tech": ":.2f",
                "grupo_label": False, "prob_Tech": ":.2f"},
    template="plotly_white",
    labels={"NOTA_M": "Nota Matemática", "prob_Tech": "Prob. Tech"},
)
fig_sc.add_vline(x=p60_mt, line_dash="dot", line_color="#9CA3AF",
                 annotation_text=f"P{percentil_mt} MT={p60_mt:.0f}",
                 annotation_position="top right")
fig_sc.add_hline(y=0.25, line_dash="dot", line_color="#D4537E",
                 annotation_text="25% prob. Tech",
                 annotation_position="right")
fig_sc.update_layout(
    height=360, margin=dict(t=20,b=20),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(tickformat=".0%", gridcolor="#F3F4F6"),
    xaxis=dict(gridcolor="#F3F4F6"),
    legend=dict(title="", orientation="h", y=1.08),
)
st.plotly_chart(fig_sc, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# PAINÉIS POR GRUPO
# ─────────────────────────────────────────────────────────────────────────────
for g in [3, 2, 1]:
    info   = GRUPOS[g]
    subset = df_res[df_res["grupo"] == g]
    if len(subset) == 0:
        continue

    st.markdown(
        f'<div class="g-card" style="border-color:{info["cor"]}">'
        f'<div style="display:flex;justify-content:space-between;align-items:center">'
        f'  <div>'
        f'    <div class="g-num" style="color:{info["cor"]}">'
        f'      {info["emoji"]} Grupo {g} — {info["nome"]}'
        f'    </div>'
        f'    <div class="g-desc">{info["desc"]}</div>'
        f'    <div style="margin-top:8px;font-size:0.78rem;color:#6B7280">'
        f'      <strong>Composição:</strong> {comp[g]}'
        f'    </div>'
        f'  </div>'
        f'  <div style="font-size:2rem;font-weight:700;color:{info["cor"]};'
        f'    font-family:monospace;padding-left:20px">{len(subset)}</div>'
        f'</div>'
        f'<div class="g-acao">📌 <strong>Ação recomendada:</strong> {info["acao"]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Aplicar filtro de área se selecionado
    subset_filtrado = (
        subset if filtro_area == "Todas"
        else subset[subset["area_prevista"] == filtro_area]
    )
    n_filtrado = len(subset_filtrado)
    label_exp  = f"Ver as {len(subset)} alunas do Grupo {g}"
    if filtro_area != "Todas":
        label_exp += f" ({n_filtrado} em {filtro_area})"

    with st.expander(label_exp, expanded=(g==3)):
        if n_filtrado == 0:
            st.caption(f"Nenhuma aluna do Grupo {g} com área prevista = {filtro_area}.")
        else:
            for idx in subset_filtrado.index:
                row_res  = df_res.loc[idx]
                row_dado = df_upload.iloc[idx]
                st.markdown(
                    card_aluna(row_res["nome"], row_dado, row_res, info["cor"]),
                    unsafe_allow_html=True,
                )

    st.markdown("")

# Grupo 0
if n_g0 > 0:
    with st.expander(f"Ver {n_g0} alunas fora dos grupos de interesse"):
        st.caption("Perfil intermediário — não se encaixam nos critérios de nenhum dos 3 grupos.")
        sub0 = df_res[df_res["grupo"] == 0]
        for idx in sub0.index:
            row_res  = df_res.loc[idx]
            row_dado = df_upload.iloc[idx]
            st.markdown(
                card_aluna(row_res["nome"], row_dado, row_res, "#D1D5DB"),
                unsafe_allow_html=True,
            )

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# DOWNLOAD
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Exportar</div>', unsafe_allow_html=True)

df_export = df_upload.copy()
df_export["NOME_ALUNA"]    = nomes
df_export["area_prevista"] = df_res["area_prevista"].values
df_export["grupo"]         = df_res["grupo"].values
df_export["grupo_nome"]    = df_res["grupo"].map(
    {0:"Fora dos grupos", 1:"Potencial Oculto", 2:"Borda de Tech", 3:"Confirmada Tech"}
).values
df_export["prob_Tech"]     = (df_res["prob_Tech"] * 100).round(1).values
df_export["rank_tech"]     = df_res["rank_tech"].values
df_export["gap_tech_pp"]   = (df_res["gap_tech"] * 100).round(1).values
df_export["ranking"]       = df_res["ranking"].values
for c in df_probs.columns:
    df_export[f"prob_{c}"] = (df_probs[c] * 100).round(2).values

col_d1, col_d2 = st.columns(2)
with col_d1:
    st.download_button(
        "⬇ Exportar turma com grupos (CSV)",
        data=df_export.to_csv(index=False).encode("utf-8"),
        file_name="turma_grupos_tech.csv",
        mime="text/csv",
    )
with col_d2:
    # Exportar só os grupos de interesse (G1+G2+G3)
    df_foco = df_export[df_export["grupo"] > 0]
    st.download_button(
        "⬇ Exportar apenas grupos de interesse",
        data=df_foco.to_csv(index=False).encode("utf-8"),
        file_name="grupos_interesse_tech.csv",
        mime="text/csv",
    )

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<div style='font-size:11px;color:#aaa;text-align:center'>"
    "Painel de Incentivo à Tecnologia · TCC CDIA · "
    "Random Forest SISU 2023 (sem TURNO) · "
    "Classificação por grupos não é determinística — serve como ferramenta de priorização"
    "</div>",
    unsafe_allow_html=True,
)

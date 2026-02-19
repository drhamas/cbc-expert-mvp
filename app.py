import streamlit as st

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="CBC Interpreter · Clinical Dashboard",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
# GLOBAL CSS — rendered immediately, unsafe_allow_html=True
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp {
    background: #0d1117;
    color: #e6edf3;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

/* ── Dashboard header ── */
.dash-header {
    display: flex; align-items: center; gap: 1rem;
    border-bottom: 1px solid #21262d;
    padding-bottom: 1.2rem; margin-bottom: 2rem;
}
.dash-header .logo {
    font-family: 'DM Serif Display', serif;
    font-size: 1.9rem; color: #58a6ff; letter-spacing: -0.5px;
}
.dash-header .subtitle {
    font-size: 0.78rem; color: #8b949e; letter-spacing: 0.08em;
    text-transform: uppercase; font-weight: 500;
}
.dash-tag {
    margin-left: auto;
    background: #1c2f45; color: #58a6ff;
    font-size: 0.7rem; font-family: 'DM Mono', monospace;
    padding: 0.25rem 0.7rem; border-radius: 999px;
    border: 1px solid #1f4068;
}

/* ── Cards ── */
.card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}
.card-title {
    font-size: 0.7rem; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; color: #8b949e;
    margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;
}
.card-title::before {
    content: ''; display: inline-block;
    width: 8px; height: 8px; border-radius: 50%;
    background: #58a6ff;
}

/* ── Pattern badges ── */
.pattern-row { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.8rem; }
.badge {
    display: inline-block; font-size: 0.72rem; font-weight: 500;
    padding: 0.3rem 0.8rem; border-radius: 999px;
    font-family: 'DM Mono', monospace;
}
.badge-red    { background: #2d1a1a; color: #f85149; border: 1px solid #4d1f1f; }
.badge-orange { background: #2d1f0d; color: #e3b341; border: 1px solid #4d3211; }
.badge-blue   { background: #0d2040; color: #58a6ff; border: 1px solid #1f4068; }
.badge-green  { background: #0d2a17; color: #3fb950; border: 1px solid #1a4a28; }
.badge-gray   { background: #1c2128; color: #8b949e; border: 1px solid #2d333b; }

/* ── Clinical Summary text ── */
.summary-text {
    font-size: 0.95rem; line-height: 1.7; color: #c9d1d9;
    margin-bottom: 0.6rem;
}
.summary-normal  { color: #3fb950; font-weight: 600; }
.summary-abnormal{ color: #f85149; font-weight: 600; }

/* ── Workup checklist ── */
.workup-item {
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
    padding: 0.65rem 0;
    border-bottom: 1px solid #21262d;
    font-size: 0.875rem;
    color: #c9d1d9;
}
.workup-item:last-child {
    border-bottom: none;
}
.workup-icon {
    width: 22px; height: 22px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.7rem; flex-shrink: 0; margin-top: 1px;
    font-weight: 700;
}
.icon-red    { background: #2d1a1a; color: #f85149; }
.icon-orange { background: #2d1f0d; color: #e3b341; }
.icon-blue   { background: #0d2040; color: #58a6ff; }
.icon-green  { background: #0d2a17; color: #3fb950; }

.workup-content { display: flex; flex-direction: column; gap: 0.15rem; }
.workup-label  { font-weight: 600; color: #e6edf3; font-size: 0.875rem; }
.workup-reason { font-size: 0.76rem; color: #8b949e; }

/* ── Parameter value grid ── */
.param-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.8rem;
    margin-bottom: 1rem;
}
.param-box {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    text-align: center;
}
.param-name  { font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; color: #8b949e; }
.param-value { font-family: 'DM Mono', monospace; font-size: 1.3rem; font-weight: 500; margin-top: 0.2rem; }
.param-unit  { font-size: 0.65rem; color: #8b949e; }
.val-normal  { color: #3fb950; }
.val-abnormal{ color: #f85149; }
.val-warn    { color: #e3b341; }

/* ── Disclaimer ── */
.disclaimer {
    margin-top: 2rem;
    padding: 0.8rem 1.2rem;
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
    font-size: 0.72rem;
    color: #8b949e;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# CLINICAL LOGIC ENGINE
# ──────────────────────────────────────────────

def interpret_cbc(hgb, mcv, wbc, neutrophil_pct, platelets, sex):
    """
    Returns:
        patterns  : list of (label, color_key)
        summaries : list of HTML strings
        workup    : list of dicts {label, reason, priority}
    """
    patterns  = []
    summaries = []
    workup    = []

    hgb_threshold = 12.0 if sex == "Female" else 13.0

    # ── 1. Microcytic Anaemia ──────────────────────────────────────────────
    if hgb < hgb_threshold and mcv < 80:
        patterns.append(("Microcytic Anaemia", "red"))
        summaries.append(
            f"Haemoglobin is <b>{hgb} g/dL</b> (below {hgb_threshold} g/dL for {sex}) "
            f"with a low MCV of <b>{mcv} fL</b> — consistent with <b>microcytic anaemia</b>. "
            f"Iron deficiency is the most common aetiology; thalassaemia trait and anaemia of "
            f"chronic disease should also be considered."
        )
        workup += [
            {"label": "Serum Ferritin",
             "reason": "Gold standard for iron stores; low in IDA, high in ACD",
             "priority": "red"},
            {"label": "TIBC / Transferrin Saturation",
             "reason": "Distinguish iron deficiency from anaemia of chronic disease",
             "priority": "red"},
            {"label": "Peripheral Blood Smear",
             "reason": "Assess for hypochromia, pencil cells, target cells",
             "priority": "orange"},
            {"label": "Haemoglobin Electrophoresis",
             "reason": "Rule out thalassaemia trait if ferritin is normal",
             "priority": "blue"},
        ]

    # ── 2. Macrocytic Anaemia ──────────────────────────────────────────────
    elif hgb < hgb_threshold and mcv > 100:
        patterns.append(("Macrocytic Anaemia", "orange"))
        summaries.append(
            f"Haemoglobin is <b>{hgb} g/dL</b> with an elevated MCV of <b>{mcv} fL</b> — "
            f"raising concern for <b>macrocytic / megaloblastic anaemia</b>. "
            f"B12/folate deficiency and hypothyroidism are primary considerations."
        )
        workup += [
            {"label": "Serum Vitamin B12 & Folate",
             "reason": "Most common reversible causes of macrocytosis",
             "priority": "red"},
            {"label": "Peripheral Blood Smear",
             "reason": "Look for hypersegmented neutrophils and macro-ovalocytes",
             "priority": "orange"},
            {"label": "TSH",
             "reason": "Hypothyroidism is a recognised cause of macrocytosis",
             "priority": "blue"},
            {"label": "Reticulocyte Count",
             "reason": "Assess bone marrow erythroid response",
             "priority": "blue"},
            {"label": "LDH & Indirect Bilirubin",
             "reason": "Elevated in ineffective erythropoiesis / haemolysis",
             "priority": "blue"},
        ]

    # ── 3. Normocytic Anaemia ──────────────────────────────────────────────
    elif hgb < hgb_threshold and 80 <= mcv <= 100:
        patterns.append(("Normocytic Anaemia", "orange"))
        summaries.append(
            f"Haemoglobin is <b>{hgb} g/dL</b> with a normal MCV of <b>{mcv} fL</b> — "
            f"suggesting <b>normocytic anaemia</b>. Broad differential including haemolysis, "
            f"anaemia of chronic disease, early IDA, or bone marrow failure."
        )
        workup += [
            {"label": "Reticulocyte Count + Reticulocyte Production Index",
             "reason": "Distinguish hypoproliferative from hyperproliferative cause",
             "priority": "red"},
            {"label": "Peripheral Blood Smear",
             "reason": "Identify spherocytes, sickle cells, fragmented RBCs, or blasts",
             "priority": "orange"},
            {"label": "LDH, Haptoglobin, Direct Coombs Test",
             "reason": "Rule out haemolytic anaemia",
             "priority": "blue"},
            {"label": "Serum Ferritin + CRP",
             "reason": "Ferritin elevated in ACD; CRP confirms inflammation",
             "priority": "blue"},
        ]

    else:
        summaries.append(
            f"Haemoglobin (<b>{hgb} g/dL</b>) and MCV (<b>{mcv} fL</b>) are within "
            f"normal limits for {sex}. No anaemia detected."
        )

    # ── 4. Leukocytosis with Neutrophilia ──────────────────────────────────
    neutrophil_abs = wbc * (neutrophil_pct / 100)
    if wbc > 11.0 and neutrophil_pct > 70:
        patterns.append(("Leukocytosis + Neutrophilia", "red"))
        summaries.append(
            f"WBC is elevated at <b>{wbc} ×10³/µL</b> with neutrophilia "
            f"(~{neutrophil_abs:.1f} ×10³/µL absolute). Pattern favours "
            f"<b>bacterial infection or acute inflammation</b>."
        )
        workup += [
            {"label": "Rule out Bacterial Infection / Inflammation",
             "reason": "Neutrophilic leukocytosis is the hallmark reactive pattern",
             "priority": "red"},
            {"label": "CRP & Procalcitonin",
             "reason": "Quantify inflammatory burden; PCT favours bacterial aetiology",
             "priority": "orange"},
            {"label": "Blood Cultures x2 sets",
             "reason": "Mandatory if sepsis is clinically suspected",
             "priority": "red"},
            {"label": "Peripheral Smear - Toxic Granulation / Left Shift",
             "reason": "Morphological confirmation of reactive neutrophilia",
             "priority": "orange"},
        ]
    elif wbc > 11.0:
        patterns.append(("Leukocytosis", "orange"))
        summaries.append(
            f"WBC is elevated at <b>{wbc} ×10³/µL</b> without marked neutrophilia. "
            f"Consider viral illness, medication effect, stress response, or less commonly "
            f"a lymphoproliferative process."
        )
        workup += [
            {"label": "Peripheral Blood Smear + Manual Differential",
             "reason": "Characterise cell morphology; identify atypical lymphocytes or blasts",
             "priority": "orange"},
            {"label": "Monospot / EBV / CMV Serology",
             "reason": "Viral causes of atypical lymphocytosis",
             "priority": "blue"},
        ]

    # ── 5. Leukopenia ──────────────────────────────────────────────────────
    if wbc < 4.0:
        patterns.append(("Leukopenia", "red"))
        summaries.append(
            f"WBC is low at <b>{wbc} ×10³/µL</b> — <b>leukopenia</b> detected. "
            f"Consider viral suppression, drug-induced cytopaenia (chemotherapy, "
            f"immunosuppressants), autoimmune disease, or bone marrow failure."
        )
        workup += [
            {"label": "Peripheral Smear + Manual Differential",
             "reason": "Identify which cell line is reduced; look for dysplastic changes",
             "priority": "red"},
            {"label": "ANA & Anti-dsDNA",
             "reason": "Autoimmune neutropenia; rule out SLE",
             "priority": "blue"},
            {"label": "Medication Review",
             "reason": "Drug-induced leukopenia is a common and reversible cause",
             "priority": "orange"},
            {"label": "Bone Marrow Biopsy",
             "reason": "Indicated if persistent or pancytopaenia is present",
             "priority": "blue"},
        ]

    # ── 6. Thrombocytopenia ────────────────────────────────────────────────
    if platelets < 150:
        patterns.append(("Thrombocytopenia", "red"))
        summaries.append(
            f"Platelet count is low at <b>{platelets} ×10³/µL</b>. "
            f"EDTA-induced pseudothrombocytopaenia (platelet clumping) must be excluded "
            f"before any clinical intervention. True thrombocytopaenia warrants further evaluation."
        )
        workup += [
            {"label": "Manual Platelet Count & Peripheral Smear Review",
             "reason": "Rule out EDTA-induced clumping / pseudothrombocytopaenia first",
             "priority": "red"},
            {"label": "Repeat CBC in Citrate or Heparin Tube",
             "reason": "Confirms true thrombocytopaenia if clumping is seen on smear",
             "priority": "orange"},
            {"label": "PT / aPTT / Fibrinogen",
             "reason": "Rule out DIC if clinical context warrants (bleeding, sepsis)",
             "priority": "blue"},
            {"label": "Anti-platelet Antibodies / H. pylori Testing",
             "reason": "Consider ITP workup in isolated thrombocytopaenia",
             "priority": "blue"},
        ]

    # ── 7. Thrombocytosis ──────────────────────────────────────────────────
    if platelets > 450:
        patterns.append(("Thrombocytosis", "orange"))
        summaries.append(
            f"Platelet count is elevated at <b>{platelets} ×10³/µL</b> — "
            f"<b>thrombocytosis</b> detected. Reactive causes (infection, iron deficiency, "
            f"post-splenectomy) are most common. If >1000 or persistent, consider "
            f"essential thrombocythaemia."
        )
        workup += [
            {"label": "CRP / ESR",
             "reason": "Reactive thrombocytosis screening; elevated in infection/inflammation",
             "priority": "blue"},
            {"label": "JAK2 V617F Mutation Analysis",
             "reason": "Essential thrombocythaemia / myeloproliferative neoplasm panel",
             "priority": "orange"},
            {"label": "Peripheral Blood Smear",
             "reason": "Assess platelet morphology; giant platelets suggest MPN",
             "priority": "orange"},
            {"label": "Iron Studies",
             "reason": "IDA is a common cause of reactive thrombocytosis",
             "priority": "blue"},
        ]

    # ── 8. All Normal ──────────────────────────────────────────────────────
    if not patterns:
        patterns.append(("CBC Within Normal Limits", "green"))
        summaries.append(
            "All CBC parameters are within normal reference ranges. "
            "No immediate haematological workup is indicated based on current values."
        )

    # De-duplicate workup items by label (preserve insertion order)
    seen, deduped = set(), []
    for item in workup:
        if item["label"] not in seen:
            seen.add(item["label"])
            deduped.append(item)

    return patterns, summaries, deduped


# ──────────────────────────────────────────────
# HTML BUILDER HELPERS
# ──────────────────────────────────────────────

def build_badges_html(patterns):
    badges = "".join(
        f'<span class="badge badge-{color}">{label}</span>'
        for label, color in patterns
    )
    return f'<div class="pattern-row">{badges}</div>'


def build_summary_html(summaries):
    return "".join(f'<p class="summary-text">{s}</p>' for s in summaries)


def build_workup_html(workup):
    if not workup:
        return '<p class="summary-text summary-normal">No additional workup required at this time.</p>'
    rows = []
    for item in workup:
        p    = item["priority"]
        icon = "!" if p == "red" else (">" if p == "orange" else "+")
        rows.append(
            f'<div class="workup-item">'
            f'  <div class="workup-icon icon-{p}">{icon}</div>'
            f'  <div class="workup-content">'
            f'    <div class="workup-label">&#9744; {item["label"]}</div>'
            f'    <div class="workup-reason">{item["reason"]}</div>'
            f'  </div>'
            f'</div>'
        )
    return "\n".join(rows)


def build_param_grid_html(hgb, mcv, wbc, platelets, hgb_threshold):
    hgb_cls = "val-abnormal" if hgb < hgb_threshold else "val-normal"
    mcv_cls = "val-abnormal" if mcv < 80 else ("val-warn" if mcv > 100 else "val-normal")
    wbc_cls = "val-abnormal" if wbc < 4.0 else ("val-warn" if wbc > 11.0 else "val-normal")
    plt_cls = "val-abnormal" if platelets < 150 else ("val-warn" if platelets > 450 else "val-normal")
    return (
        f'<div class="param-grid">'
        f'  <div class="param-box">'
        f'    <div class="param-name">Haemoglobin</div>'
        f'    <div class="param-value {hgb_cls}">{hgb}</div>'
        f'    <div class="param-unit">g/dL &middot; ref &ge;{hgb_threshold}</div>'
        f'  </div>'
        f'  <div class="param-box">'
        f'    <div class="param-name">MCV</div>'
        f'    <div class="param-value {mcv_cls}">{mcv}</div>'
        f'    <div class="param-unit">fL &middot; ref 80&ndash;100</div>'
        f'  </div>'
        f'  <div class="param-box">'
        f'    <div class="param-name">WBC</div>'
        f'    <div class="param-value {wbc_cls}">{wbc}</div>'
        f'    <div class="param-unit">&times;10&sup3;/&micro;L &middot; ref 4&ndash;11</div>'
        f'  </div>'
        f'  <div class="param-box">'
        f'    <div class="param-name">Platelets</div>'
        f'    <div class="param-value {plt_cls}">{platelets}</div>'
        f'    <div class="param-unit">&times;10&sup3;/&micro;L &middot; ref 150&ndash;450</div>'
        f'  </div>'
        f'</div>'
    )


# ──────────────────────────────────────────────
# RENDER: DASHBOARD HEADER
# ──────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
    <div>
        <div class="logo">&#128300; CBC Interpreter</div>
        <div class="subtitle">Clinical Decision Support &middot; Haematology</div>
    </div>
    <div class="dash-tag">WHO / ICSH Guidelines &middot; v1.0</div>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# RENDER: INPUT PANEL
# ──────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">Patient Parameters</div>', unsafe_allow_html=True)

col_sex, col_hgb, col_mcv = st.columns([1, 1, 1])
col_wbc, col_neu, col_plt  = st.columns([1, 1, 1])

with col_sex:
    sex = st.selectbox("Biological Sex", ["Female", "Male"],
                       help="Sets sex-specific Hgb reference range (F: 12 g/dL, M: 13 g/dL)")
with col_hgb:
    hgb = st.number_input("Haemoglobin (g/dL)", min_value=1.0, max_value=20.0,
                          value=11.5, step=0.1, format="%.1f")
with col_mcv:
    mcv = st.number_input("MCV (fL)", min_value=50, max_value=140, value=72, step=1)
with col_wbc:
    wbc = st.number_input("WBC (x10^3/uL)", min_value=0.1, max_value=100.0,
                          value=8.5, step=0.1, format="%.1f")
with col_neu:
    neutrophil_pct = st.slider("Neutrophils (%)", min_value=0, max_value=100, value=65,
                               help="Approximate neutrophil percentage from differential")
with col_plt:
    platelets = st.number_input("Platelets (x10^3/uL)", min_value=1, max_value=2000,
                                value=210, step=1)

st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# RUN LOGIC
# ──────────────────────────────────────────────
patterns, summaries, workup = interpret_cbc(hgb, mcv, wbc, neutrophil_pct, platelets, sex)
hgb_threshold = 12.0 if sex == "Female" else 13.0


# ──────────────────────────────────────────────
# RENDER: PARAMETER VALUE GRID
# ──────────────────────────────────────────────
st.markdown(
    build_param_grid_html(hgb, mcv, wbc, platelets, hgb_threshold),
    unsafe_allow_html=True
)


# ──────────────────────────────────────────────
# RENDER: TWO-COLUMN OUTPUT CARDS
# ──────────────────────────────────────────────
left, right = st.columns([1, 1], gap="medium")

with left:
    clinical_summary_html = (
        '<div class="card">'
        '<div class="card-title">Clinical Summary</div>'
        + build_badges_html(patterns)
        + build_summary_html(summaries)
        + '</div>'
    )
    st.markdown(clinical_summary_html, unsafe_allow_html=True)

with right:
    suggested_workup_html = (
        '<div class="card">'
        '<div class="card-title">Suggested Workup</div>'
        + build_workup_html(workup)
        + '</div>'
    )
    st.markdown(suggested_workup_html, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# RENDER: DISCLAIMER
# ──────────────────────────────────────────────
st.markdown(
    '<div class="disclaimer">'
    '<b style="color:#e3b341;">&#9888; Clinical Decision Support Tool</b> &mdash; '
    'This tool is intended to assist qualified medical professionals and does not replace '
    'clinical judgement, full patient history, or direct laboratory review. All interpretations '
    'should be correlated with clinical context. Reference ranges may vary by laboratory and '
    'patient population.'
    '</div>',
    unsafe_allow_html=True
)

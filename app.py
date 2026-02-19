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
# CUSTOM CSS  —  refined clinical dark theme
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Reset ── */
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

/* ── Background ── */
.stApp {
    background: #0d1117;
    color: #e6edf3;
}

/* ── Hide Streamlit chrome ── */
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

/* ── Summary text ── */
.summary-text {
    font-size: 0.95rem; line-height: 1.7; color: #c9d1d9;
}
.summary-normal {
    color: #3fb950; font-weight: 600;
}
.summary-abnormal {
    color: #f85149; font-weight: 600;
}

/* ── Workup checklist ── */
.workup-item {
    display: flex; align-items: flex-start; gap: 0.8rem;
    padding: 0.65rem 0; border-bottom: 1px solid #21262d;
    font-size: 0.875rem; color: #c9d1d9;
}
.workup-item:last-child { border-bottom: none; }
.workup-icon {
    width: 22px; height: 22px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.7rem; flex-shrink: 0; margin-top: 1px;
}
.icon-red    { background: #2d1a1a; color: #f85149; }
.icon-orange { background: #2d1f0d; color: #e3b341; }
.icon-blue   { background: #0d2040; color: #58a6ff; }
.icon-green  { background: #0d2a17; color: #3fb950; }
.workup-label { font-weight: 600; color: #e6edf3; }
.workup-reason { font-size: 0.78rem; color: #8b949e; margin-top: 0.15rem; }

/* ── Value display ── */
.param-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.8rem; margin-bottom: 0.5rem; }
.param-box {
    background: #0d1117; border: 1px solid #21262d;
    border-radius: 8px; padding: 0.75rem 1rem; text-align: center;
}
.param-name { font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; color: #8b949e; }
.param-value { font-family: 'DM Mono', monospace; font-size: 1.3rem; font-weight: 500; margin-top: 0.2rem; }
.param-unit  { font-size: 0.65rem; color: #8b949e; }
.val-normal  { color: #3fb950; }
.val-abnormal{ color: #f85149; }
.val-warn    { color: #e3b341; }

/* ── Streamlit slider/input overrides ── */
.stSlider > div > div > div > div { background: #58a6ff; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# CLINICAL LOGIC ENGINE
# ──────────────────────────────────────────────

def interpret_cbc(hgb, mcv, wbc, neutrophil_pct, platelets, sex):
    """
    Returns (patterns, summaries, workup_items)
    Each workup_item: dict(label, reason, priority)
    """
    patterns = []
    summaries = []
    workup = []

    hgb_low_threshold = 12.0 if sex == "Female" else 13.0

    # ── 1. Microcytic Anaemia ──────────────────
    if hgb < hgb_low_threshold and mcv < 80:
        patterns.append(("Microcytic Anaemia", "red"))
        summaries.append(
            f"Haemoglobin is <b>{hgb} g/dL</b> (below {hgb_low_threshold} g/dL for {sex}) "
            f"with a low MCV of <b>{mcv} fL</b> — consistent with <b>microcytic anaemia</b>. "
            f"Iron deficiency is the most common aetiology; thalassaemia trait and anaemia of "
            f"chronic disease should also be considered."
        )
        workup += [
            {"label": "Serum Ferritin", "reason": "Gold standard for iron stores", "priority": "red"},
            {"label": "TIBC / Transferrin Saturation", "reason": "Distinguish IDA from ACD", "priority": "red"},
            {"label": "Peripheral Blood Smear", "reason": "Hypochromia, pencil cells, target cells", "priority": "orange"},
            {"label": "Haemoglobin Electrophoresis", "reason": "Rule out thalassaemia trait", "priority": "blue"},
        ]

    # ── 2. Macrocytic Anaemia ─────────────────
    elif hgb < hgb_low_threshold and mcv > 100:
        patterns.append(("Macrocytic Anaemia", "orange"))
        summaries.append(
            f"Haemoglobin is <b>{hgb} g/dL</b> with an elevated MCV of <b>{mcv} fL</b> — "
            f"raising concern for <b>macrocytic / megaloblastic anaemia</b>. "
            f"B12/folate deficiency and hypothyroidism are primary considerations."
        )
        workup += [
            {"label": "Serum B12 & Folate", "reason": "Most common causes of macrocytosis", "priority": "red"},
            {"label": "Peripheral Blood Smear", "reason": "Hypersegmented neutrophils, macro-ovalocytes", "priority": "orange"},
            {"label": "TSH", "reason": "Hypothyroidism causes macrocytosis", "priority": "blue"},
            {"label": "Reticulocyte Count", "reason": "Assess marrow response", "priority": "blue"},
            {"label": "LDH & Indirect Bilirubin", "reason": "Ineffective erythropoiesis marker", "priority": "blue"},
        ]

    # ── 3. Normocytic Anaemia ─────────────────
    elif hgb < hgb_low_threshold and 80 <= mcv <= 100:
        patterns.append(("Normocytic Anaemia", "orange"))
        summaries.append(
            f"Haemoglobin is <b>{hgb} g/dL</b> with a normal MCV of <b>{mcv} fL</b> — "
            f"suggesting <b>normocytic anaemia</b>. Broad differential including haemolysis, "
            f"anaemia of chronic disease, early IDA, or bone marrow failure."
        )
        workup += [
            {"label": "Reticulocyte Count + Index", "reason": "Distinguish hypo- vs hyperproliferative", "priority": "red"},
            {"label": "Peripheral Blood Smear", "reason": "Spherocytes, sickle cells, blasts", "priority": "orange"},
            {"label": "LDH, Haptoglobin, Direct Coombs", "reason": "Rule out haemolysis", "priority": "blue"},
            {"label": "Serum Ferritin + CRP", "reason": "Rule out ACD", "priority": "blue"},
        ]

    else:
        summaries.append(f"Haemoglobin (<b>{hgb} g/dL</b>) and MCV (<b>{mcv} fL</b>) are within normal limits for {sex}.")

    # ── 4. Leukocytosis / Bacterial Infection ─
    neutrophil_abs = wbc * (neutrophil_pct / 100)
    if wbc > 11.0 and neutrophil_pct > 70:
        patterns.append(("Leukocytosis", "red"))
        summaries.append(
            f"WBC is elevated at <b>{wbc} ×10³/µL</b> with neutrophilia "
            f"(~{neutrophil_abs:.1f} ×10³/µL absolute). Pattern favours <b>bacterial "
            f"infection or acute inflammation</b>."
        )
        workup += [
            {"label": "Rule out Bacterial Infection / Inflammation", "reason": "Neutrophilic leukocytosis pattern", "priority": "red"},
            {"label": "CRP & Procalcitonin", "reason": "Quantify inflammatory burden", "priority": "orange"},
            {"label": "Blood Cultures × 2", "reason": "If sepsis suspected", "priority": "red"},
            {"label": "Peripheral Smear for Toxic Granulation / Left Shift", "reason": "Confirm reactive neutrophilia", "priority": "orange"},
        ]
    elif wbc > 11.0:
        patterns.append(("Leukocytosis", "orange"))
        summaries.append(
            f"WBC is elevated at <b>{wbc} ×10³/µL</b> without marked neutrophilia. "
            f"Consider viral illness, medication effect, stress response, or less commonly a lymphoproliferative process."
        )
        workup += [
            {"label": "Peripheral Blood Smear + Differential", "reason": "Characterise cell morphology", "priority": "orange"},
            {"label": "Monospot / EBV / CMV Serology", "reason": "Atypical lymphocytosis workup", "priority": "blue"},
        ]

    # ── 5. Leukopenia ─────────────────────────
    if wbc < 4.0:
        patterns.append(("Leukopenia", "red"))
        summaries.append(
            f"WBC is low at <b>{wbc} ×10³/µL</b> — <b>leukopenia</b> detected. "
            f"Consider viral suppression, medication effect (chemotherapy, immunosuppressants), "
            f"autoimmune disease, or bone marrow failure."
        )
        workup += [
            {"label": "Peripheral Smear + Manual Differential", "reason": "Identify cell type affected", "priority": "red"},
            {"label": "ANA, Anti-dsDNA", "reason": "Autoimmune neutropenia / lupus", "priority": "blue"},
            {"label": "Medication Review", "reason": "Drug-induced cytopaenia", "priority": "orange"},
            {"label": "Bone Marrow Biopsy", "reason": "If persistent or pancytopaenia suspected", "priority": "blue"},
        ]

    # ── 6. Thrombocytopenia ───────────────────
    if platelets < 150:
        patterns.append(("Thrombocytopenia", "red"))
        summaries.append(
            f"Platelet count is low at <b>{platelets} ×10³/µL</b>. "
            f"Platelet clumping (EDTA-induced pseudothrombocytopaenia) must be excluded before "
            f"clinical action. True thrombocytopaenia warrants further evaluation."
        )
        workup += [
            {"label": "Manual Platelet Count & Peripheral Smear Review", "reason": "Rule out EDTA-induced clumping / pseudothrombocytopaenia", "priority": "red"},
            {"label": "Repeat CBC in Citrate or Heparin Tube", "reason": "Confirm true thrombocytopaenia", "priority": "orange"},
            {"label": "PT / aPTT / Fibrinogen", "reason": "Rule out DIC if clinical context warrants", "priority": "blue"},
            {"label": "Anti-platelet Antibodies / H. pylori", "reason": "Consider ITP workup", "priority": "blue"},
        ]

    # ── 7. Thrombocytosis ─────────────────────
    if platelets > 450:
        patterns.append(("Thrombocytosis", "orange"))
        summaries.append(
            f"Platelet count is elevated at <b>{platelets} ×10³/µL</b> — <b>thrombocytosis</b>. "
            f"Reactive causes (infection, iron deficiency, post-splenectomy) are most common. "
            f"If >1000 or persistent, consider essential thrombocythaemia."
        )
        workup += [
            {"label": "CRP / ESR", "reason": "Reactive thrombocytosis screening", "priority": "blue"},
            {"label": "JAK2 V617F Mutation", "reason": "Essential thrombocythaemia / MPN panel", "priority": "orange"},
            {"label": "Peripheral Smear", "reason": "Platelet morphology, giant platelets", "priority": "orange"},
            {"label": "Iron Studies", "reason": "IDA-associated reactive thrombocytosis", "priority": "blue"},
        ]

    # ── 8. Normal CBC ─────────────────────────
    if not patterns:
        patterns.append(("CBC Within Normal Limits", "green"))
        summaries.append(
            "All CBC parameters are within normal reference ranges. "
            "No immediate haematological workup indicated based on current values."
        )

    # De-duplicate workup items by label
    seen = set()
    deduped = []
    for item in workup:
        if item["label"] not in seen:
            seen.add(item["label"])
            deduped.append(item)

    return patterns, summaries, deduped


# ──────────────────────────────────────────────
# UI
# ──────────────────────────────────────────────

# Header
st.markdown("""
<div class="dash-header">
    <div>
        <div class="logo">🔬 CBC Interpreter</div>
        <div class="subtitle">Clinical Decision Support · Haematology</div>
    </div>
    <div class="dash-tag">WHO / ICSH Guidelines · v1.0</div>
</div>
""", unsafe_allow_html=True)

# ── Input Panel ─────────────────────────────
st.markdown('<div class="card"><div class="card-title">Patient Parameters</div>', unsafe_allow_html=True)

col_sex, col_hgb, col_mcv = st.columns([1, 1, 1])
col_wbc, col_neu, col_plt  = st.columns([1, 1, 1])

with col_sex:
    sex = st.selectbox("Biological Sex", ["Female", "Male"], help="Used to set sex-specific Hgb reference range")

with col_hgb:
    hgb = st.number_input("Haemoglobin (g/dL)", min_value=1.0, max_value=20.0, value=11.5, step=0.1, format="%.1f")

with col_mcv:
    mcv = st.number_input("MCV (fL)", min_value=50, max_value=140, value=72, step=1)

with col_wbc:
    wbc = st.number_input("WBC (×10³/µL)", min_value=0.1, max_value=100.0, value=8.5, step=0.1, format="%.1f")

with col_neu:
    neutrophil_pct = st.slider("Neutrophils (%)", min_value=0, max_value=100, value=65,
                                help="Approximate neutrophil percentage from differential")

with col_plt:
    platelets = st.number_input("Platelets (×10³/µL)", min_value=1, max_value=2000, value=210, step=1)

st.markdown('</div>', unsafe_allow_html=True)

# ── Run Interpretation ───────────────────────
patterns, summaries, workup = interpret_cbc(hgb, mcv, wbc, neutrophil_pct, platelets, sex)

# ── Parameter Summary Row ────────────────────
hgb_threshold = 12.0 if sex == "Female" else 13.0
hgb_cls   = "val-abnormal" if hgb < hgb_threshold else "val-normal"
mcv_cls   = "val-warn" if mcv < 80 or mcv > 100 else "val-normal"
wbc_cls   = "val-abnormal" if wbc < 4.0 or wbc > 11.0 else "val-normal"
plt_cls   = "val-abnormal" if platelets < 150 else ("val-warn" if platelets > 450 else "val-normal")

st.markdown(f"""
<div class="param-grid">
  <div class="param-box">
    <div class="param-name">Haemoglobin</div>
    <div class="param-value {hgb_cls}">{hgb}</div>
    <div class="param-unit">g/dL · ref ≥{hgb_threshold}</div>
  </div>
  <div class="param-box">
    <div class="param-name">MCV</div>
    <div class="param-value {mcv_cls}">{mcv}</div>
    <div class="param-unit">fL · ref 80–100</div>
  </div>
  <div class="param-box">
    <div class="param-name">WBC</div>
    <div class="param-value {wbc_cls}">{wbc}</div>
    <div class="param-unit">×10³/µL · ref 4–11</div>
  </div>
  <div class="param-box">
    <div class="param-name">Platelets</div>
    <div class="param-value {plt_cls}">{platelets}</div>
    <div class="param-unit">×10³/µL · ref 150–450</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Two-column output ────────────────────────
left, right = st.columns([1, 1], gap="medium")

# Clinical Summary Card
with left:
    badge_html = '<div class="pattern-row">'
    for label, color in patterns:
        badge_html += f'<span class="badge badge-{color}">{label}</span>'
    badge_html += '</div>'

    summary_html = ""
    for s in summaries:
        summary_html += f'<p class="summary-text">{s}</p>'

    st.markdown(f"""
    <div class="card">
        <div class="card-title">Clinical Summary</div>
        {badge_html}
        {summary_html}
    </div>
    """, unsafe_allow_html=True)

# Suggested Workup Card
with right:
    if workup:
        items_html = ""
        for item in workup:
            p = item["priority"]
            items_html += f"""
            <div class="workup-item">
                <div class="workup-icon icon-{p}">{'!' if p == 'red' else '→'}</div>
                <div>
                    <div class="workup-label">☐ {item['label']}</div>
                    <div class="workup-reason">{item['reason']}</div>
                </div>
            </div>"""

        st.markdown(f"""
        <div class="card">
            <div class="card-title">Suggested Workup</div>
            {items_html}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card">
            <div class="card-title">Suggested Workup</div>
            <div class="summary-text summary-normal">✓ No additional workup required at this time.</div>
        </div>
        """, unsafe_allow_html=True)

# ── Disclaimer ───────────────────────────────
st.markdown("""
<div style="margin-top:2rem; padding:0.8rem 1.2rem; background:#161b22; border:1px solid #21262d;
     border-radius:8px; font-size:0.72rem; color:#8b949e; line-height:1.6;">
    <b style="color:#e3b341;">⚠ Clinical Decision Support Tool</b> — This tool is intended to assist
    qualified medical professionals and does not replace clinical judgement, full patient history,
    or direct laboratory review. All interpretations should be correlated with clinical context.
    Reference ranges may vary by laboratory and patient population.
</div>
""", unsafe_allow_html=True)

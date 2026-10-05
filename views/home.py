import streamlit as st

from utils import art, ml
from utils.loaders import get_artifacts, get_data, get_metrics
from utils.theme import card, footer, h, html, kpi, section

df = get_data()
scaler, model, _ = get_artifacts()
m = get_metrics()

# ------------------------------------------------------------------ hero
left, right = st.columns([1.1, 1], gap="large", vertical_alignment="center")
with left:
    html(f"""
    <div class="eyebrow"><span class="dot"></span> AI-assisted cardiovascular screening</div>
    <div class="hero-title">Know your heart.<br><em>Protect it early.</em></div>
    <div class="hero-sub">CardioSense looks at 19 everyday health and lifestyle factors and estimates the chance of heart disease —
    then shows you, in plain language, which factors are driving the result.</div>
    <div class="trust"><span>✓ Takes about 1 minute</span><span>✓ No sign-up, no data stored</span><span>✓ {m['accuracy']:.1%} hold-out accuracy</span></div>
    <br>
    """)
    b1, b2, _ = st.columns([1.1, 1.1, 0.5])
    with b1:
        st.page_link("views/assessment.py", label="Start my assessment", icon=":material/monitor_heart:")
    with b2:
        st.page_link("views/guide.py", label="Heart health guide", icon=":material/eco:")
with right:
    hero = art.photo_or(art.img(art.heart(72), "100%", alt="Anatomical heart illustration"), "hero")
    html(f"""
    <div class="hero-visual">
      <div style="position:absolute;left:-2%;top:2%;width:26%;z-index:0;opacity:.95">{art.img(art.leaf_sprig(), "100%", alt="")}</div>
      <div style="position:absolute;right:-1%;bottom:0;width:26%;z-index:0;opacity:.95">{art.img(art.leaf_sprig(True), "100%", alt="")}</div>
      <div style="position:relative;z-index:1">{hero}</div>
      <div class="float-card" style="left:-2%;bottom:16%;z-index:2"><span>Resting heart rate</span><b>72 bpm</b></div>
      <div class="float-card" style="right:0;top:8%;z-index:2;animation-delay:-2s"><span>Model ROC-AUC</span><b>{m['roc_auc']:.3f}</b></div>
    </div>
    """)

html(f'<div style="margin:.4rem 0 .2rem">{art.img(art.ecg_strip(), "100%", alt="ECG trace")}</div>')

# ------------------------------------------------------------------ KPIs
k1, k2, k3, k4 = st.columns(4)
k1.markdown(kpi(f"{len(df):,}", "Patient records analysed"), unsafe_allow_html=True)
k2.markdown(kpi(f"{m['accuracy']:.1%}", "Hold-out accuracy"), unsafe_allow_html=True)
k3.markdown(kpi(f"{m['roc_auc']:.3f}", "ROC-AUC score"), unsafe_allow_html=True)
k4.markdown(kpi(str(len(ml.FEATURES)), "Health factors considered"), unsafe_allow_html=True)

# ------------------------------------------------------------------ how it works
section("How it works", "From a few simple answers to a clear, explained result.")
c1, c2, c3 = st.columns(3, gap="large")
c1.markdown(card(art.img(art.icon("form"), "76px"), "Share a few details",
                 "Age, body measurements, lifestyle, medical history and a couple of heart readings — grouped into four short tabs.",
                 "STEP 01"), unsafe_allow_html=True)
c2.markdown(card(art.img(art.icon("ai"), "76px"), "The model analyses",
                 f"A tuned Logistic Regression trained on {len(df):,} patient records scores your profile in a fraction of a second.",
                 "STEP 02"), unsafe_allow_html=True)
c3.markdown(card(art.img(art.icon("report"), "76px"), "Understand the result",
                 "See your risk score, the factors pushing it up or down, a what-if explorer and a downloadable summary.",
                 "STEP 03"), unsafe_allow_html=True)

# ------------------------------------------------------------------ factors
section("What does it look at?", "Nineteen factors across four areas of heart health.")
tiles = [("scale", "Body"), ("run", "Activity"), ("apple", "Diet"), ("moon", "Sleep"),
         ("bolt", "Stress"), ("smoke", "Smoking"), ("drop", "Cholesterol"), ("family", "Family history")]
cols = st.columns(8)
for col, (ic, label) in zip(cols, tiles):
    col.markdown(h(f'<div style="text-align:center">{art.img(art.icon(ic), "100%")}<div style="font-weight:600;margin-top:.4rem;font-size:.9rem">{label}</div></div>'),
                 unsafe_allow_html=True)

# ------------------------------------------------------------------ what drives
section("What drives the prediction?", "Relative weight of each factor inside the trained model (top 6).")
coef = ml.coefficient_table(model)
top = coef.head(6)
total = top["abs"].sum()
rows = ""
for _, r in top.iterrows():
    share = r["abs"] / total
    rows += (f'<div class="bar-row"><div class="bar-label">{r["label"]}</div><div class="bar-track">'
             f'<div class="bar-fill" style="width:{share * 100:.0f}%"></div></div><div class="bar-val">{share:.0%}</div></div>')
l2, r2 = st.columns([1.4, 1], gap="large", vertical_alignment="center")
with l2:
    html(f'<div class="card">{rows}<p style="margin-top:.9rem">In this dataset, <b>diabetes, exercise-induced angina and BMI</b> carry most of the signal. '
         f'The remaining factors move the score only slightly.</p></div>')
with r2:
    html(f'<div style="text-align:center">{art.img(art.stethoscope(), "88%", alt="Stethoscope")}</div>')

# ------------------------------------------------------------------ natural band
html(f"""
<div class="band" style="margin-top:2.6rem;display:flex;align-items:center;gap:1.6rem;flex-wrap:wrap">
  <div style="width:90px">{art.img(art.icon("heart"), "90px")}</div>
  <div style="flex:1;min-width:240px"><h3>Small, natural habits protect your heart.</h3>
  <p>Move daily, eat colourful plants, sleep well, don't smoke and keep up with check-ups. Our guide explains why — and what the warning signs look like.</p></div>
</div>
""")
st.write("")
st.page_link("views/guide.py", label="Read the Heart Health Guide", icon=":material/eco:")

# ------------------------------------------------------------------ FAQ
section("Questions people ask")
with st.expander("Is this a diagnosis?"):
    st.write("No. CardioSense is an educational machine-learning demo. It estimates a statistical risk score from a dataset and cannot "
             "replace an examination, ECG, blood tests or the judgement of a doctor.")
with st.expander("Is my information stored?"):
    st.write("No. Your answers are used only to compute the score inside this session and are not saved to any database.")
with st.expander("How accurate is the model?"):
    st.write(f"On the 8,000 held-out records the model reached {m['accuracy']:.1%} accuracy and a ROC-AUC of {m['roc_auc']:.3f}. "
             "Those figures describe this dataset only — real-world performance on real patients would differ.")
with st.expander("What should I do if I have chest pain right now?"):
    st.error("Do not use this app. Chest pain, pressure, shortness of breath or fainting can be emergencies — call your local emergency number immediately.")

footer()

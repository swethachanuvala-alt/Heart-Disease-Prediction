import streamlit as st

from utils import art, ml
from utils.loaders import get_data
from utils.theme import PALETTE, footer, html, page_header, section

df = get_data()
page_header("About", "CardioSense", "From a Jupyter notebook to a deployed, heart-healthy web app.")

left, right = st.columns([1.2, 1], gap="large", vertical_alignment="center")
with left:
    section("The project", "A machine-learning heart-disease risk screener.")
    html("""
    <div class="tl">
      <div class="tl-item"><b>1 · Data</b><span>40,000 patient records, 44 columns, no missing values, perfectly balanced outcome (50 / 50).</span></div>
      <div class="tl-item"><b>2 · Preparation</b><span>Kept 19 features, label-encoded sex, stratified 80/20 split and standard scaling.</span></div>
      <div class="tl-item"><b>3 · Modelling</b><span>Logistic Regression, Decision Tree, Random Forest, XGBoost, KNN and SVM — compared and tuned.</span></div>
      <div class="tl-item"><b>4 · Selection</b><span>Logistic Regression: top default accuracy &amp; ROC-AUC, simple and explainable.</span></div>
      <div class="tl-item"><b>5 · Deployment</b><span>Saved with joblib and served through this multipage Streamlit app.</span></div>
    </div>
    """)
with right:
    html(f'<div style="text-align:center">{art.img(art.heart(68), "80%", alt="Heart")}</div>')

section("Feature dictionary", "The 19 inputs used by the model.")
desc = [
    ("Age", "years", "Age of the patient"), ("Gender", "Female / Male", "Biological sex (encoded 0 / 1)"),
    ("BMI", "kg/m²", "Body-mass index"), ("Smoking", "0 / 1", "Current smoker"), ("Alcohol", "0 / 1", "Drinks alcohol"),
    ("PhysicalActivity", "0 – 4", "Activity level (higher = more active)"), ("DietScore", "1 – 10", "Diet quality score"),
    ("SleepHours", "5 – 9 h", "Average nightly sleep"), ("StressLevel", "1 – 10", "Self-rated stress"),
    ("FamilyHistory", "0 / 1", "Family history of heart disease"), ("Diabetes", "0 / 1", "Diagnosed diabetes"),
    ("Hypertension", "0 / 1", "High blood pressure"), ("KidneyDisease", "0 / 1", "Kidney disease"),
    ("StrokeHistory", "0 / 1", "Previous stroke"), ("RestingHR", "50 – 110 bpm", "Resting heart rate"),
    ("HDL", "25 – 90 mg/dL", "HDL cholesterol"), ("LDL", "50 – 220 mg/dL", "LDL cholesterol"),
    ("ChestPainType", "0 – 3", "Chest-pain category code"), ("ExerciseAngina", "0 / 1", "Angina during exercise"),
]
rows = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>" for a, b, c in desc)
html(f'<table class="dtable"><tr><th>Feature</th><th>Values</th><th>Meaning</th></tr>{rows}'
     f'<tr><td><b>HeartDisease</b></td><td>0 / 1</td><td><b>Target</b> — 1 = heart disease</td></tr></table>')

section("Built with")
html("".join(f'<span class="chip">{t}</span>' for t in
             ["Python", "Streamlit", "scikit-learn", "pandas", "NumPy", "Plotly", "joblib", "Custom SVG artwork"]))

section("The colour story", "Every red used in the design — from blush petal to deep oxblood. Hover to stretch a swatch.")


def light(c):
    r, g, b = (int(c[i:i + 2], 16) for i in (1, 3, 5))
    return (0.299 * r + 0.587 * g + 0.114 * b) > 150


sw = "".join(f'<div class="sw" style="background:{c};color:{"#4A0A12" if light(c) else "#FFF1EE"}">{n}<br>{c}</div>' for n, c in PALETTE.items())
html(f'<div class="swatches">{sw}</div>')

section("Please note")
html("""
<div class="alert"><b>Educational demo.</b> CardioSense is a learning project built on a demonstration dataset. Its output is a statistical estimate,
<b>not</b> a medical diagnosis, and must never replace professional medical care. Seek emergency help for chest pain or other urgent symptoms.</div>
""")
footer()

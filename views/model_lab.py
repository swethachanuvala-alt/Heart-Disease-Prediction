import plotly.graph_objects as go
import streamlit as st

from utils import ml
from utils.loaders import get_artifacts, get_metrics
from utils.theme import footer, html, kpi, page_header, section, style_fig

scaler, model, source = get_artifacts()
m = get_metrics()

page_header("Model", "lab", "A transparent look under the hood of the Logistic Regression model.")
if source == "retrained":
    st.info("The saved .pkl files weren't compatible with this environment, so the model was re-trained from the CSV "
            "with the same pipeline as the notebook.")

cols = st.columns(5)
for col, (label, key) in zip(cols, [("Accuracy", "accuracy"), ("Precision", "precision"), ("Recall", "recall"),
                                    ("F1 score", "f1"), ("ROC-AUC", "roc_auc")]):
    col.markdown(kpi(f"{m[key]:.3f}", label), unsafe_allow_html=True)
st.caption(f"Scored live on {m['n_test']:,} hold-out patients (20 % stratified split, random_state=42).")

section("How well does it separate the two groups?")
c1, c2 = st.columns(2)
cm = m["cm"]
fig = go.Figure(go.Heatmap(
    z=cm, x=["Predicted: no disease", "Predicted: disease"], y=["Actually: no disease", "Actually: disease"],
    colorscale=[[0, "#FFF1EE"], [0.5, "#EF6F6C"], [1, "#8B0F1A"]], showscale=False,
    text=cm, texttemplate="<b>%{text:,}</b>", textfont=dict(size=24, color="#fff"),
    hovertemplate="%{y} / %{x}: %{z:,}<extra></extra>"))
fig.update_layout(title="Confusion matrix")
fig.update_yaxes(autorange="reversed")
c1.plotly_chart(style_fig(fig, legend=False), key="lab_cm")

fig = go.Figure()
fig.add_trace(go.Scatter(x=m["fpr"], y=m["tpr"], mode="lines", name=f"Model (AUC {m['roc_auc']:.3f})",
                         line=dict(color="#C1121F", width=4), fill="tozeroy", fillcolor="rgba(239,111,108,.22)"))
fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Random guess", line=dict(color="#6B9A6F", dash="dash", width=2)))
fig.update_layout(title="ROC curve", xaxis_title="False-positive rate", yaxis_title="True-positive rate")
c2.plotly_chart(style_fig(fig), key="lab_roc")

section("What the model learned", "Standardised coefficients — positive values push towards heart disease.")
coef = ml.coefficient_table(model).sort_values("coef")
fig = go.Figure(go.Bar(x=coef["coef"], y=coef["label"], orientation="h",
                       marker=dict(color=["#C1121F" if v >= 0 else "#6B9A6F" for v in coef["coef"]]),
                       text=[f"{v:+.2f}" for v in coef["coef"]], textposition="outside"))
fig.update_layout(title="Logistic Regression coefficients")
fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor="#4A0A12")
st.plotly_chart(style_fig(fig, height=620, legend=False), key="lab_coef")

section("Why Logistic Regression?", "Six algorithms were compared in the notebook (hold-out test accuracy).")
comparison = [  # model, default-settings accuracy, tuned accuracy, default ROC-AUC   (from GGST_8.ipynb)
    ("Logistic Regression", 0.936625, 0.936125, 0.9785),
    ("SVM", 0.935875, None, 0.9659),
    ("Random Forest", 0.934750, 0.936500, 0.9760),
    ("XGBoost", 0.930000, 0.936750, 0.9744),
    ("KNN", 0.918625, 0.921750, 0.9546),
    ("Decision Tree", 0.897375, None, 0.8974),
]
names = [r[0] for r in comparison]
fig = go.Figure()
fig.add_trace(go.Bar(name="Default settings", x=names, y=[r[1] * 100 for r in comparison], marker_color="#C1121F"))
fig.add_trace(go.Bar(name="After tuning", x=names, y=[None if r[2] is None else r[2] * 100 for r in comparison], marker_color="#F5A9A0"))
fig.update_layout(barmode="group", title="Test accuracy (%)", yaxis=dict(range=[88, 95]))
st.plotly_chart(style_fig(fig), key="lab_compare")

fmt = lambda v: "—" if v is None else f"{v:.4f}"  # noqa: E731
rows = "".join(f'<tr class="{"best" if i == 0 else ""}"><td>{n}</td><td>{a:.4f}</td><td>{fmt(t)}</td><td>{r:.4f}</td></tr>'
               for i, (n, a, t, r) in enumerate(comparison))
html(f'<table class="dtable"><tr><th>Model</th><th>Default accuracy</th><th>Tuned accuracy</th><th>ROC-AUC (default)</th></tr>{rows}</table>')
st.caption("Logistic Regression had the best accuracy and ROC-AUC with default settings. After tuning, the top models differ by about 0.1 % — "
           "within noise — so the simple, explainable Logistic Regression is the sensible choice for this app.")

section("The training recipe")
html("""
<div class="card"><span class="chip">25 unused columns dropped</span><span class="chip">Gender label-encoded</span><span class="chip">80 / 20 stratified split</span>
<span class="chip">StandardScaler</span><span class="chip">Balanced classes (SMOTE not needed)</span><span class="chip">Logistic Regression</span>
<span class="chip">C = 0.1</span><span class="chip">solver = liblinear</span><span class="chip">max_iter = 2000</span><span class="chip">RandomizedSearchCV · 5-fold</span></div>
""")
footer()

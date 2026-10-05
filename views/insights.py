import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import art, ml
from utils.loaders import get_data
from utils.theme import footer, html, kpi, page_header, section, style_fig

df = get_data().copy()
page_header("Heart data", "insights", "What 40,000 patient records show about who has heart disease.")

with st.expander("🎚️ Filter the patients"):
    c1, c2, c3 = st.columns(3)
    sexes = c1.multiselect("Sex", ["Female", "Male"], default=["Female", "Male"])
    age_rng = c2.slider("Age range", int(df.Age.min()), int(df.Age.max()), (int(df.Age.min()), int(df.Age.max())))
    bmi_rng = c3.slider("BMI range", float(df.BMI.min()), float(df.BMI.max()), (float(df.BMI.min()), float(df.BMI.max())))

view = df[df.Gender.isin(sexes) & df.Age.between(*age_rng) & df.BMI.between(*bmi_rng)]
if view.empty:
    st.warning("No patients match these filters — widen them a little.")
    footer(); st.stop()

k1, k2, k3, k4 = st.columns(4)
k1.markdown(kpi(f"{len(view):,}", "Patients in view"), unsafe_allow_html=True)
k2.markdown(kpi(f"{view.HeartDisease.mean():.1%}", "With heart disease"), unsafe_allow_html=True)
k3.markdown(kpi(f"{view.Age.mean():.0f} yrs", "Average age"), unsafe_allow_html=True)
k4.markdown(kpi(f"{view.BMI.mean():.1f}", "Average BMI"), unsafe_allow_html=True)

# ------------------------------------------------------------------ row 1
section("The strongest signals")
c1, c2 = st.columns(2)

cats = pd.cut(view.BMI, [0, 18.5, 25, 30, 35, 100], labels=["Underweight", "Healthy", "Overweight", "Obese I", "Obese II+"])
by = view.groupby(cats, observed=True).HeartDisease.agg(["mean", "count"]).reset_index()
fig = go.Figure(go.Bar(
    x=by["BMI"].astype(str), y=by["mean"] * 100,
    marker=dict(color=by["mean"], colorscale=[[0, "#FADBD8"], [0.5, "#EF6F6C"], [1, "#8B0F1A"]]),
    text=[f"{v:.0%}" for v in by["mean"]], textposition="outside", customdata=by["count"],
    hovertemplate="%{x}: %{y:.1f}% (%{customdata:,} patients)<extra></extra>"))
fig.update_layout(title="Heart-disease rate by BMI category", yaxis=dict(title="% with heart disease", range=[0, 112]))
c1.plotly_chart(style_fig(fig, legend=False), key="ins_bmi")

flags = ["Diabetes", "ExerciseAngina", "Hypertension", "Smoking", "FamilyHistory"]
no = [view.loc[view[f] == 0, "HeartDisease"].mean() * 100 for f in flags]
yes = [view.loc[view[f] == 1, "HeartDisease"].mean() * 100 for f in flags]
labels = [ml.NICE[f] for f in flags]
fig = go.Figure()
fig.add_trace(go.Bar(name="Absent", x=labels, y=no, marker_color="#F5A9A0"))
fig.add_trace(go.Bar(name="Present", x=labels, y=yes, marker_color="#A4161A"))
fig.update_layout(barmode="group", title="Heart-disease rate: factor absent vs present", yaxis=dict(title="%", range=[0, 112]))
c2.plotly_chart(style_fig(fig), key="ins_flags")

# ------------------------------------------------------------------ row 2
c3, c4 = st.columns([1.3, 1])
edges = np.linspace(view.BMI.min(), view.BMI.max(), 31)
fig = go.Figure()
for flag, name, col in ((0, "No heart disease", "#6B9A6F"), (1, "Heart disease", "#C1121F")):
    cnt, _ = np.histogram(view.loc[view.HeartDisease == flag, "BMI"], bins=edges)
    fig.add_trace(go.Bar(x=(edges[:-1] + edges[1:]) / 2, y=cnt, name=name, marker_color=col, opacity=0.75))
fig.update_layout(barmode="overlay", title="BMI distribution by outcome", xaxis_title="BMI", yaxis_title="Patients")
c3.plotly_chart(style_fig(fig), key="ins_bmi_hist")

sex = view.groupby("Gender").HeartDisease.mean() * 100
fig = go.Figure(go.Pie(labels=list(sex.index), values=sex.values, hole=0.62,
                       marker=dict(colors=["#F5A9A0", "#8B0F1A"], line=dict(color="#fff", width=3)),
                       texttemplate="%{label}<br>%{value:.1f}%"))
fig.update_layout(title="Heart-disease rate by sex")
c4.plotly_chart(style_fig(fig, legend=False), key="ins_sex")

# ------------------------------------------------------------------ row 3
section("How strongly is each factor linked to the outcome?", "Correlation with heart disease (−1 to +1).")
enc = view.copy(); enc["Gender"] = enc["Gender"].map(ml.GENDER_CODE)
corr = enc[ml.FEATURES + [ml.TARGET]].corr()[ml.TARGET].drop(ml.TARGET).sort_values()
fig = go.Figure(go.Bar(x=corr.values, y=[ml.NICE[i] for i in corr.index], orientation="h",
                       marker=dict(color=["#C1121F" if v >= 0 else "#6B9A6F" for v in corr.values]),
                       text=[f"{v:+.2f}" for v in corr.values], textposition="outside"))
fig.update_layout(title="Correlation with heart disease")
fig.update_xaxes(range=[-0.1, 0.85])
st.plotly_chart(style_fig(fig, height=560, legend=False), key="ins_corr")

html("""
<div class="note"><b>Data note:</b> only diabetes, exercise angina, BMI, hypertension, smoking and family history show a clear link in this dataset;
age, activity, diet, sleep, stress and cholesterol look almost unrelated to the outcome. That is unusual for real clinical data, which is why
the model should be treated as a learning demo, not as medical guidance.</div>
""")

with st.expander("📄 View & download the filtered data"):
    st.dataframe(view.head(2000).reset_index(drop=True), hide_index=True)
    st.caption("Showing the first 2,000 rows; the download contains every filtered row.")
    st.download_button("Download CSV", view.to_csv(index=False).encode("utf-8"), "filtered_heart_data.csv", "text/csv")

footer()

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import art, ml
from utils.loaders import get_artifacts, get_data
from utils.theme import footer, h, html, page_header, style_fig

df = get_data()
scaler, model, _ = get_artifacts()

page_header("Heart risk", "assessment", "Answer four short sections — your risk score appears on the right.")

YN = ["No", "Yes"]
b = lambda v: 1 if v == "Yes" else 0  # noqa: E731


# ------------------------------------------------------------------ reference helpers
def bmi_class(v):
    if v < 18.5: return "Underweight", False
    if v < 25: return "Healthy range", True
    if v < 30: return "Overweight", False
    return "Obese range", False


def hr_class(v):
    if v < 60: return "Below typical (athletes often)", True
    if v <= 100: return "Typical range", True
    return "Above typical", False


def ldl_class(v):
    if v < 100: return "Optimal", True
    if v < 130: return "Near optimal", True
    if v < 160: return "Borderline high", False
    return "High", False


def hdl_class(v, sex):
    low = 40 if sex == "Male" else 50
    if v < low: return "Low", False
    if v >= 60: return "Protective", True
    return "Acceptable", True


def level(p):
    if p < 0.35: return "lo", "Lower estimated risk", "🌿"
    if p < 0.65: return "mid", "Moderate estimated risk", "⚠️"
    return "hi", "Higher estimated risk", "❤️‍🔥"


def prob_with(person, **changes):
    return ml.predict_one(scaler, model, {**person, **changes})[0]


left, right = st.columns([1, 1.2], gap="large")

# ------------------------------------------------------------------ form
with left:
    with st.form("heart_form"):
        t1, t2, t3, t4 = st.tabs(["👤 About you", "🥗 Lifestyle", "🩺 History", "❤️ Heart & blood"])
        with t1:
            age = st.slider("Age", 25, 90, 50)
            sex = st.radio("Sex", ["Female", "Male"], horizontal=True)
            c1, c2 = st.columns(2)
            height = c1.number_input("Height (cm)", 130, 210, 170)
            weight = c2.number_input("Weight (kg)", 30, 200, 70)
            st.caption("BMI is calculated for you from height and weight.")
        with t2:
            c1, c2 = st.columns(2)
            smoking = c1.radio("Do you smoke?", YN, horizontal=True)
            alcohol = c2.radio("Do you drink alcohol?", YN, horizontal=True)
            activity = st.select_slider("Physical activity level", options=[0, 1, 2, 3, 4], value=2,
                                        help="0 = least active, 4 = most active (coded as in the dataset).")
            diet = st.slider("Diet quality score", 1, 10, 6)
            sleep = st.slider("Sleep (hours per night)", 5.0, 9.0, 7.0, step=0.5)
            stress = st.slider("Stress level", 1, 10, 5)
        with t3:
            c1, c2 = st.columns(2)
            family = c1.radio("Family history of heart disease", YN, horizontal=True)
            diabetes = c2.radio("Diabetes", YN, horizontal=True)
            hyper = c1.radio("Hypertension (high blood pressure)", YN, horizontal=True)
            kidney = c2.radio("Kidney disease", YN, horizontal=True)
            stroke = c1.radio("Previous stroke", YN, horizontal=True)
        with t4:
            hr = st.slider("Resting heart rate (bpm)", 50, 110, 72)
            c1, c2 = st.columns(2)
            hdl = c1.slider("HDL cholesterol (mg/dL)", 25, 90, 55)
            ldl = c2.slider("LDL cholesterol (mg/dL)", 50, 220, 120)
            chest = st.select_slider("Chest-pain type", options=[0, 1, 2, 3], value=0,
                                     help="Coded 0–3 exactly as in the training dataset.")
            angina = st.radio("Chest pain brought on by exercise (angina)?", YN, horizontal=True)
        go_btn = st.form_submit_button("Calculate my heart-risk score ❤️")

    if go_btn:
        bmi = round(weight / ((height / 100) ** 2), 1)
        person = dict(Age=age, Gender=sex, BMI=bmi, Smoking=b(smoking), Alcohol=b(alcohol), PhysicalActivity=activity,
                      DietScore=diet, SleepHours=sleep, StressLevel=stress, FamilyHistory=b(family), Diabetes=b(diabetes),
                      Hypertension=b(hyper), KidneyDisease=b(kidney), StrokeHistory=b(stroke), RestingHR=hr, HDL=hdl,
                      LDL=ldl, ChestPainType=chest, ExerciseAngina=b(angina))
        prob, contrib, intercept = ml.predict_one(scaler, model, person)
        st.session_state["heart_result"] = dict(person=person, prob=prob, contrib=contrib, intercept=intercept)

# ------------------------------------------------------------------ result
with right:
    res = st.session_state.get("heart_result")
    if not res:
        html(f"""
        <div class="card tint" style="text-align:center;padding:2rem 1.5rem">
          {art.img(art.heart(72), "62%")}
          <h4 style="font-size:1.45rem">Your results will appear here</h4>
          <p>Complete the form and press <b>Calculate</b>. You'll see a risk score, a gauge, your key health numbers,
          what is driving the score and a what-if explorer.</p>
        </div>
        """)
    else:
        person, prob, contrib, intercept = res["person"], res["prob"], res["contrib"], res["intercept"]
        cls, title, emoji = level(prob)
        html(f"""
        <div class="verdict {cls}" style="display:flex;align-items:center;gap:1rem">
          <div style="flex:1"><div class="t">{title}</div>
          <div class="s">The model estimates a <b>{prob:.0%}</b> chance of heart disease for this profile.</div>
          <span class="pill">Risk score {prob * 100:.0f} / 100</span><span class="pill">Resting HR {person['RestingHR']} bpm</span></div>
          <div style="width:140px;background:rgba(255,255,255,.92);border-radius:24px;padding:.4rem">{art.img(art.heart(person['RestingHR']), "100%")}</div>
        </div>
        """)
        gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=prob * 100,
            number=dict(suffix="%", font=dict(size=44, color="#4A0A12", family="Fraunces")),
            title=dict(text="Estimated risk", font=dict(size=15, color="#7A4A4F")),
            gauge=dict(axis=dict(range=[0, 100], tickcolor="#8A5A5E"), bar=dict(color="#4A0A12", thickness=0.22),
                       bgcolor="rgba(0,0,0,0)", borderwidth=0,
                       steps=[dict(range=[0, 35], color="#CFE3CF"), dict(range=[35, 65], color="#F5A9A0"),
                              dict(range=[65, 100], color="#E63946")]),
        ))
        style_fig(gauge, height=250, legend=False)
        gauge.update_layout(margin=dict(l=30, r=30, t=50, b=0))
        st.plotly_chart(gauge, key="risk_gauge")

        # key numbers
        p = person
        nums = [("BMI", f"{p['BMI']:.1f}", *bmi_class(p["BMI"])), ("Resting HR", f"{p['RestingHR']} bpm", *hr_class(p["RestingHR"])),
                ("LDL", f"{p['LDL']}", *ldl_class(p["LDL"])), ("HDL", f"{p['HDL']}", *hdl_class(p["HDL"], p["Gender"]))]
        cells = "".join(
            f'<div style="flex:1;min-width:120px;background:#fff;border:1px solid #FADBD8;border-radius:16px;padding:.7rem .9rem;'
            f'border-top:5px solid {"#6B9A6F" if ok else "#C1121F"}"><div style="font-size:.75rem;color:#8A5A5E">{n}</div>'
            f'<div style="font-family:Fraunces,serif;font-size:1.35rem;font-weight:700;color:#4A0A12">{v}</div>'
            f'<div style="font-size:.78rem;color:{"#4F7A57" if ok else "#A4161A"};font-weight:600">{t}</div></div>'
            for n, v, t, ok in nums)
        html(f'<div style="display:flex;gap:.6rem;flex-wrap:wrap;margin-top:.4rem">{cells}</div>')

# ------------------------------------------------------------------ deep dive
res = st.session_state.get("heart_result")
if res:
    person, prob, contrib, intercept = res["person"], res["prob"], res["contrib"], res["intercept"]
    t1, t2, t3 = st.tabs(["🔍 What's driving this", "🎛️ What-if explorer", "🌿 Next steps"])

    with t1:
        items = sorted(contrib.items(), key=lambda kv: kv[1])
        items = [kv for kv in items if abs(kv[1]) > 0.02] or items
        fig = go.Figure(go.Bar(
            x=[v for _, v in items], y=[ml.NICE[k] for k, _ in items], orientation="h",
            marker=dict(color=["#C1121F" if v >= 0 else "#6B9A6F" for _, v in items]),
            text=[f"{v:+.2f}" for _, v in items], textposition="outside",
            hovertemplate="%{y}: %{x:+.2f}<extra></extra>"))
        fig.update_layout(title="How each factor moved the score (log-odds contribution)")
        style_fig(fig, height=max(320, 34 * len(items) + 110), legend=False)
        fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor="#4A0A12")
        st.plotly_chart(fig, key="drivers")
        st.caption("Red bars raise the estimated risk, green bars lower it — each measured against an average person in the training data. "
                   "Factors with almost no effect are hidden.")

    with t2:
        c1, c2 = st.columns(2)
        grid = np.arange(16, 46, 1.0)
        frame = pd.DataFrame([person] * len(grid)); frame["BMI"] = grid
        probs = ml.predict_many(scaler, model, frame)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=grid, y=probs * 100, mode="lines", line=dict(color="#C1121F", width=4, shape="spline"),
                                 fill="tozeroy", fillcolor="rgba(239,111,108,.2)", name="Risk"))
        fig.add_trace(go.Scatter(x=[person["BMI"]], y=[prob * 100], mode="markers", name="You",
                                 marker=dict(size=15, color="#fff", line=dict(color="#4A0A12", width=4))))
        fig.update_layout(title="Estimated risk vs. BMI", xaxis_title="BMI", yaxis=dict(title="%", range=[0, 101]))
        c1.plotly_chart(style_fig(fig, height=340, legend=False), key="bmi_curve")

        changes = []
        if person["Smoking"]: changes.append(("Stop smoking", prob_with(person, Smoking=0)))
        if person["BMI"] > 24.9: changes.append(("Reach a BMI of 24.9", prob_with(person, BMI=24.9)))
        if person["Hypertension"]: changes.append(("No hypertension", prob_with(person, Hypertension=0)))
        changes = [(t, p) for t, p in changes if prob - p > 0.003]
        if changes:
            changes.sort(key=lambda x: x[1])
            fig = go.Figure(go.Bar(x=[p * 100 for _, p in changes], y=[t for t, _ in changes], orientation="h",
                                   marker=dict(color="#6B9A6F"), text=[f"{p:.0%}" for _, p in changes], textposition="outside"))
            fig.add_vline(x=prob * 100, line=dict(color="#C1121F", width=3, dash="dash"), annotation_text="today", annotation_font_color="#C1121F")
            fig.update_layout(title="Risk if one thing changed", xaxis=dict(title="%", range=[0, 105]))
            c2.plotly_chart(style_fig(fig, height=340, legend=False), key="whatif_bars")
        else:
            c2.markdown(h('<div class="card tint"><h4>No single change moves the score</h4><p>For this profile no one modifiable factor shifts the model-estimated risk by a meaningful amount.</p></div>'),
                        unsafe_allow_html=True)
        st.caption("Model-based what-ifs: each change is applied on its own to your current answers.")

    with t3:
        a, b2 = st.columns([1.3, 1], gap="large")
        with a:
            tips = [("leaf", "Talk to a clinician.", "Share this summary with a doctor — only they can interpret your risk properly, with a physical exam and tests such as blood pressure, lipid profile, glucose and ECG."),
                    ("leaf", "Move most days.", "Adults are generally advised to aim for about 150 minutes a week of moderate activity, such as brisk walking."),
                    ("leaf", "Eat more plants.", "Vegetables, fruit, whole grains, legumes and nuts; go easy on salt, sugar and ultra-processed food."),
                    ("", "Don't smoke.", "Quitting lowers heart risk at any age. Ask your doctor about support programmes.")]
            for ic, t, txt in tips:
                html(f'<div class="tip {"leaf" if ic else ""}"><b>{t}</b> {txt}</div>')
            html('<div class="note">Heads-up: in this dataset, activity, diet, sleep, stress, age and cholesterol showed almost no link to the outcome, '
                 'so changing them does not move the score. In real medicine they <b>do</b> matter — see the Heart Health Guide.</div>')
            st.write("")
            st.page_link("views/guide.py", label="Open the Heart Health Guide", icon=":material/eco:")
        with b2:
            html(f'<div style="text-align:center">{art.img(art.icon("heart"), "120px")}</div>')
            report = [f"CardioSense — heart-risk summary", "=" * 40, f"Estimated risk score: {prob:.0%}", ""]
            report += [f"{ml.NICE[k]}: {v}" for k, v in person.items()]
            report += ["", "Educational demo only — not a medical device, diagnosis or medical advice.",
                       "If you have chest pain or other emergency symptoms, call your local emergency number."]
            st.download_button("⬇ Download summary (.txt)", "\n".join(report), "cardiosense_summary.txt", "text/plain")

    html('<div class="alert" style="margin-top:1.2rem"><b>Important:</b> this is an educational model trained on a demonstration dataset. '
         'It is not a diagnosis. Seek urgent medical help for chest pain, breathlessness, fainting or any emergency symptom.</div>')

footer()

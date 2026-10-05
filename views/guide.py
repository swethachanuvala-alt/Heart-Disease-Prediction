import streamlit as st

from utils import art
from utils.theme import card, footer, h, html, page_header, section

page_header("Heart health", "guide", "Plain-language facts about keeping your heart strong — general education, not personal medical advice.")

html(f"""
<div class="band" style="display:flex;align-items:center;gap:1.6rem;flex-wrap:wrap">
  <div style="flex:1;min-width:260px"><h3>Your heart beats about 100,000 times a day.</h3>
  <p>Heart and blood-vessel disease is the leading cause of death worldwide — yet much of it is preventable through everyday choices and early check-ups.</p></div>
  <div style="width:150px;background:rgba(255,255,255,.92);border-radius:28px;padding:.5rem">{art.img(art.heart(70), "100%")}</div>
</div>
""")

section("Know your numbers", "Typical adult reference ranges. Your doctor may set different targets for you.")
html("""
<table class="dtable"><tr><th>Measure</th><th>Typical / healthy</th><th>Watch closely</th></tr>
<tr><td><b>BMI</b> (kg/m²)</td><td>18.5 – 24.9</td><td>25 and above (overweight / obese range)</td></tr>
<tr><td><b>Resting heart rate</b></td><td>60 – 100 bpm</td><td>Consistently above 100 bpm</td></tr>
<tr><td><b>LDL cholesterol</b> ("bad")</td><td>Below 100 mg/dL</td><td>130 mg/dL and above</td></tr>
<tr><td><b>HDL cholesterol</b> ("good")</td><td>60 mg/dL or higher is protective</td><td>Below 40 (men) / 50 (women) mg/dL</td></tr>
<tr><td><b>Blood pressure</b></td><td>Below 120 / 80 mmHg</td><td>130 / 80 mmHg and above</td></tr>
</table>
""")

section("Major risk factors", "Some you can change, some you can't — knowing them helps you act early.")
items = [
    ("smoke", "Smoking", "Damages blood vessels and raises blood pressure. Quitting lowers heart risk, and benefits begin within weeks."),
    ("scale", "Excess weight", "Extra body fat strains the heart and is linked to high blood pressure, diabetes and cholesterol problems."),
    ("drop", "Diabetes", "High blood sugar over time injures blood vessels and nerves, sharply increasing heart-disease risk."),
    ("bolt", "High blood pressure", "Often silent. Forces the heart to work harder and can thicken or damage arteries."),
    ("drop", "High LDL cholesterol", "Can build up as plaque inside arteries, narrowing them and restricting blood flow."),
    ("run", "Physical inactivity", "Regular movement strengthens the heart, helps control weight, blood pressure and blood sugar."),
    ("apple", "Unhealthy diet", "Diets high in salt, sugar and processed food raise blood pressure and weight; plants and whole foods protect."),
    ("family", "Family history", "A close relative with early heart disease raises your risk — mention it to your doctor."),
]
for i in range(0, len(items), 4):
    cols = st.columns(4, gap="medium")
    for col, (ic, t, txt) in zip(cols, items[i:i + 4]):
        col.markdown(card(art.img(art.icon(ic), "64px"), t, txt), unsafe_allow_html=True)
    st.write("")

section("A heart-healthy day", "Small habits, repeated, add up.")
l, r = st.columns([1.3, 1], gap="large", vertical_alignment="center")
with l:
    html("""
    <div class="tip leaf"><b>Morning:</b> a short brisk walk or stretch; breakfast with fruit, oats or whole grains.</div>
    <div class="tip leaf"><b>Midday:</b> fill half your plate with vegetables; choose beans, fish or lean protein; keep salt low.</div>
    <div class="tip leaf"><b>Afternoon:</b> take movement breaks — aim for roughly 150 minutes of moderate activity each week.</div>
    <div class="tip leaf"><b>Evening:</b> unwind, limit alcohol and screens, and aim for 7–9 hours of sleep.</div>
    <div class="tip"><b>All year:</b> don't smoke, manage stress, and keep up with blood-pressure, cholesterol and sugar checks.</div>
    """)
with r:
    html(f"""
    <div style="position:relative;text-align:center">
      <div style="width:70%;margin:auto">{art.img(art.blood_cells(), "100%", alt="Red blood cells")}</div>
      <div style="display:flex;justify-content:center;gap:1rem;margin-top:.4rem">
        <div style="width:90px">{art.img(art.leaf_sprig(), "100%")}</div><div style="width:90px">{art.img(art.icon("apple"), "100%")}</div><div style="width:90px">{art.img(art.leaf_sprig(True), "100%")}</div>
      </div>
    </div>
    """)

section("Warning signs — act fast")
html("""
<div class="alert"><b>Call your local emergency number immediately</b> if you or someone else has:
<ul style="margin:.5rem 0 0 1.1rem">
<li>Chest pain, pressure, tightness or squeezing that lasts more than a few minutes or comes and goes</li>
<li>Pain or discomfort spreading to the arm, shoulder, back, neck or jaw</li>
<li>Shortness of breath, cold sweat, nausea or sudden light-headedness</li>
<li>Sudden weakness, face drooping or trouble speaking (possible stroke)</li>
</ul></div>
""")
st.write("")
html('<div class="note">This guide is general health education. It does not replace advice from a qualified healthcare professional.</div>')
footer()

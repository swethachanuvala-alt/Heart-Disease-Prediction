# ❤️ CardioSense — Heart Disease Risk Screening

A multipage Streamlit web app for the heart-disease Logistic Regression model built in `notebook/GGST_8.ipynb`.
Natural red-and-cream design with an animated anatomical heart, ECG trace, stethoscope and botanical illustrations.

**Pages:** Home · Risk Assessment · Data Insights · Heart Health Guide · Model Lab · About

## Project structure

```
heart-disease-app/
├── app.py                  # entry point, header ribbon + top navigation
├── views/                  # one file per page
│   ├── home.py
│   ├── assessment.py       # 4-tab form, risk gauge, drivers, what-ifs, downloadable summary
│   ├── insights.py         # interactive data dashboard
│   ├── guide.py            # heart-health education
│   ├── model_lab.py        # metrics, ROC, confusion matrix, model comparison
│   └── about.py
├── utils/
│   ├── ml.py               # model loading / training / prediction helpers
│   ├── loaders.py          # cached data + model loaders
│   ├── theme.py            # red design system (CSS, palette, Plotly style)
│   └── art.py              # SVG illustrations (heart, ECG, stethoscope, icons ...)
├── model/
│   ├── logistic_regression_model.pkl
│   └── scaler.pkl
├── data/heart_disease_dataset.csv   # the 20 columns used in the notebook
├── assets/                 # optional: put hero.jpg here to replace the heart illustration
├── notebook/GGST_8.ipynb
├── train_model.py          # re-creates the .pkl files from the CSV
├── requirements.txt
└── .streamlit/config.toml  # theme
```

## Run locally (Windows CMD / VS Code terminal)

```bash
cd heart-disease-app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

(macOS/Linux: `source venv/bin/activate`.) The app opens at http://localhost:8501

## Use your own model files (recommended)

The `.pkl` files in `model/` were rebuilt from your notebook's pipeline and reproduce your tuned model
(accuracy 0.936, ROC-AUC 0.9785). To use the exact files from *your* notebook, copy your `scaler.pkl` and
`logistic_regression_model.pkl` into `model/`. **Keep the file names all lowercase** — GitHub and Streamlit Cloud
run on Linux, where `Logistic_Regression_model.pkl` and `logistic_regression_model.pkl` are different files.

Or run `python train_model.py` to rebuild both files with the library versions installed on your machine.
If a `.pkl` is missing or incompatible, the app automatically re-trains from the CSV instead of crashing.

## Want real photos?

Save a heart / medical / healthy-living photo as `assets/hero.jpg` (or .png / .webp). The Home page will show it
instead of the illustrated heart automatically.

## Push to GitHub

```bash
git init
git add .
git commit -m "CardioSense: heart disease risk screening app"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

## Deploy on Streamlit Community Cloud

1. Go to https://share.streamlit.io and sign in with GitHub.
2. Click **Create app**, pick your repository and the `main` branch.
3. Set **Main file path** to `app.py`.
4. Click **Deploy** (the first build takes a few minutes).

## Important

Educational demo only — not a medical device and not medical advice.

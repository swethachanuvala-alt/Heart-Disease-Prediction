"""
Re-train the heart-disease model and refresh the .pkl files in /model.

    python train_model.py
"""
from utils.ml import MODEL_PATH, SCALER_PATH, evaluate, fit_pipeline, load_dataset, save_artifacts

if __name__ == "__main__":
    df = load_dataset()
    scaler, model = fit_pipeline(df)
    save_artifacts(scaler, model)
    m = evaluate(scaler, model, df)
    print("Saved:", SCALER_PATH.name, "and", MODEL_PATH.name)
    print(f"Accuracy {m['accuracy']:.4f} | Precision {m['precision']:.3f} | Recall {m['recall']:.3f} | "
          f"F1 {m['f1']:.3f} | ROC-AUC {m['roc_auc']:.4f}")

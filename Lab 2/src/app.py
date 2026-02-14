import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from sklearn.metrics import confusion_matrix, roc_curve

from train import train_models

st.set_page_config(page_title="Lab 2 - Breast Cancer Classifier", layout="wide")
st.title("Lab 2: Breast Cancer Prediction Dashboard")
st.caption("Custom Streamlit lab with model comparison and threshold tuning")

with st.sidebar:
    st.header("Experiment Settings")
    test_size = st.slider("Test Size", min_value=0.1, max_value=0.4, value=0.2, step=0.05)
    random_state = st.number_input("Random State", min_value=0, max_value=999, value=42, step=1)
    threshold = st.slider("Classification Threshold", min_value=0.1, max_value=0.9, value=0.5, step=0.05)

metrics, artifacts = train_models(test_size=test_size, random_state=random_state)
x_test = artifacts["x_test"]
y_test = artifacts["y_test"]
lr_probs = artifacts["lr_probs"]
rf_probs = artifacts["rf_probs"]
rf_model = artifacts["rf_model"]

st.subheader("Model Comparison")
metrics_df = pd.DataFrame(metrics).T
st.dataframe(metrics_df.style.format("{:.4f}"), use_container_width=True)

best_model_name = metrics_df["roc_auc"].idxmax()
st.success(f"Best model by ROC-AUC: {best_model_name.replace('_', ' ').title()}")

selected_model = st.selectbox("Select model for diagnostics", ["logistic_regression", "random_forest"])
selected_probs = lr_probs if selected_model == "logistic_regression" else rf_probs
selected_preds = (selected_probs >= threshold).astype(int)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Confusion Matrix")
    cm = confusion_matrix(y_test, selected_preds)
    fig_cm, ax_cm = plt.subplots(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax_cm)
    ax_cm.set_xlabel("Predicted")
    ax_cm.set_ylabel("Actual")
    ax_cm.set_title(f"{selected_model.replace('_', ' ').title()} @ threshold={threshold:.2f}")
    st.pyplot(fig_cm)

with col2:
    st.subheader("ROC Curve")
    fpr, tpr, _ = roc_curve(y_test, selected_probs)
    fig_roc, ax_roc = plt.subplots(figsize=(5, 4))
    ax_roc.plot(fpr, tpr, label=selected_model.replace("_", " ").title())
    ax_roc.plot([0, 1], [0, 1], linestyle="--", color="gray")
    ax_roc.set_xlabel("False Positive Rate")
    ax_roc.set_ylabel("True Positive Rate")
    ax_roc.set_title("ROC Curve")
    ax_roc.legend()
    st.pyplot(fig_roc)

st.subheader("Top Feature Importances (Random Forest)")
feature_importances = (
    pd.DataFrame(
        {
            "feature": x_test.columns,
            "importance": rf_model.feature_importances_,
        }
    )
    .sort_values("importance", ascending=False)
    .head(10)
)
fig_imp, ax_imp = plt.subplots(figsize=(10, 4))
sns.barplot(data=feature_importances, x="importance", y="feature", palette="viridis", ax=ax_imp)
ax_imp.set_title("Top 10 Important Features")
st.pyplot(fig_imp)

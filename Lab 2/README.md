# Lab 2 - Custom Streamlit MLOps App

This lab implements a custom Streamlit machine learning dashboard for breast cancer classification.

## What is different from the source lab
- Uses a different dataset: `sklearn` Breast Cancer dataset.
- Uses two models and compares them: Logistic Regression and Random Forest.
- Adds threshold tuning from the sidebar.
- Adds additional visual diagnostics:
  - confusion matrix
  - ROC curve
  - top 10 feature importances

## Folder structure
```text
Lab 2/
  README.md
  requirements.txt
  src/
    app.py
    train.py
  data/
  assets/
```

## Setup and run
From repository root:

```bash
cd "Lab 2"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run src/app.py
```

## Submission notes
- Submit the GitHub repository URL on Canvas.
- Ensure `Lab 2` is present and runnable from a clean environment.

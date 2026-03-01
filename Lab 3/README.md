# Lab 3 - MLflow Experiment Tracking

This lab trains a Random Forest classifier on the breast cancer dataset and logs runs to MLflow.

## What Was Done in This Lab
- Used `sklearn.datasets.load_breast_cancer` as the dataset.
- Split data into train/test sets (`test_size=0.2`, `random_state=42`).
- Trained 3 Random Forest models with different hyperparameters:
  - `n_estimators=50`
  - `n_estimators=100`
  - `n_estimators=200`
- Tracked experiments in MLflow (`Lab3_MLflow_Breast_Cancer`).
- Logged for each run:
  - Parameter: `n_estimators`
  - Metrics: `accuracy`, `f1_score`
  - Artifact: confusion matrix image (`confusion_matrix_<n>.png`)
  - Model artifact: `model_<n>`
- Compared the runs in MLflow UI at `http://127.0.0.1:5001`.

## Quick Verification
Run exactly:

```bash
git clone https://github.com/sankalphegde/MLOps.git
cd MLOps/"Lab 3"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python train.py
mlflow ui --backend-store-uri "sqlite:///mlflow.db" --default-artifact-root "./mlruns" --host 127.0.0.1 --port 5001
```

Open:
- `http://127.0.0.1:5001`

Expected:
- Experiment `Lab3_MLflow_Breast_Cancer`
- 3 runs for `n_estimators`: 50, 100, 200
- Metrics: `accuracy`, `f1_score`
- Artifacts: `confusion_matrix_50.png`, `confusion_matrix_100.png`, `confusion_matrix_200.png`

## Why UI may not show up
- Running commands outside `Lab 3` (folder name has a space).
- MLflow not installed in the active environment.
- Starting UI without a backend/artifact path can point to a different run store.

## Correct steps
```bash
cd MLOps/"Lab 3"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python train.py
```

In a second terminal:
```bash
cd MLOps/"Lab 3"
source venv/bin/activate
mlflow ui --backend-store-uri "sqlite:///mlflow.db" --default-artifact-root "./mlruns" --host 127.0.0.1 --port 5001
```

Open: `http://127.0.0.1:5001`

## One-command UI start
```bash
cd MLOps/"Lab 3"
bash run_mlflow_ui.sh
```

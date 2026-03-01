# Lab 3 - MLflow Experiment Tracking

This lab trains a Random Forest classifier on the breast cancer dataset and logs runs to MLflow.

## Why UI may not show up
- Running commands outside `Lab 3` (folder name has a space).
- MLflow not installed in the active environment.
- Starting UI without a backend/artifact path can point to a different run store.

## Correct steps
```bash
cd "/Users/sankalphegde/Desktop/MLOps_labs/MLOps/Lab 3"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python train.py
```

In a second terminal:
```bash
cd "/Users/sankalphegde/Desktop/MLOps_labs/MLOps/Lab 3"
source venv/bin/activate
mlflow ui --backend-store-uri "sqlite:///mlflow.db" --default-artifact-root "./mlruns" --host 127.0.0.1 --port 5001
```

Open: `http://127.0.0.1:5001`

## One-command UI start
```bash
cd "/Users/sankalphegde/Desktop/MLOps_labs/MLOps/Lab 3"
bash run_mlflow_ui.sh
```

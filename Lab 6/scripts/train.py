"""
Lab 6 - KServe Model Training Script
Trains a RandomForestClassifier on the Iris dataset and saves it
as a KServe-compatible model artifact using joblib.

Author: Sankalp Hegde
"""

import os
import json
import joblib
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# ── Load dataset ──────────────────────────────────────────────────────────────
iris = load_iris()
X, y = iris.data, iris.target

# ── Train / test split ────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── Train model ───────────────────────────────────────────────────────────────
clf = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    random_state=42,
)
clf.fit(X_train, y_train)

# ── Evaluate ──────────────────────────────────────────────────────────────────
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print("=" * 50)
print(f"Model       : RandomForestClassifier")
print(f"Dataset     : Iris (150 samples, 4 features, 3 classes)")
print(f"Train size  : {len(X_train)}")
print(f"Test size   : {len(X_test)}")
print(f"Accuracy    : {acc:.4f}")
print("=" * 50)
print(classification_report(y_test, y_pred, target_names=iris.target_names))

# ── Save model artifact ───────────────────────────────────────────────────────
model_dir = os.path.join(os.path.dirname(__file__), "..", "model")
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, "model.joblib")
joblib.dump(clf, model_path)
print(f"Model saved to: {os.path.abspath(model_path)}")

# ── Save model metadata ───────────────────────────────────────────────────────
metadata = {
    "model_name": "iris-classifier-sankalp",
    "model_version": "1.0.0",
    "framework": "scikit-learn",
    "algorithm": "RandomForestClassifier",
    "n_estimators": 100,
    "max_depth": 5,
    "random_state": 42,
    "test_accuracy": round(float(acc), 4),
    "features": {
        "sepal_length_cm": "Length of the sepal in centimetres",
        "sepal_width_cm": "Width of the sepal in centimetres",
        "petal_length_cm": "Length of the petal in centimetres",
        "petal_width_cm": "Width of the petal in centimetres",
    },
    "classes": {
        "0": "setosa",
        "1": "versicolor",
        "2": "virginica",
    },
}
meta_path = os.path.join(model_dir, "metadata.json")
with open(meta_path, "w") as f:
    json.dump(metadata, f, indent=2)
print(f"Metadata saved to: {os.path.abspath(meta_path)}")

# ── Quick smoke test ──────────────────────────────────────────────────────────
sample_instances = [
    [5.1, 3.5, 1.4, 0.2],   # expected: setosa (0)
    [6.7, 3.1, 4.7, 1.5],   # expected: versicolor (1)
    [7.2, 3.6, 6.1, 2.5],   # expected: virginica (2)
]
preds = clf.predict(sample_instances)
pred_labels = [iris.target_names[p] for p in preds]
print("\nSmoke-test predictions:")
for inst, label in zip(sample_instances, pred_labels):
    print(f"  {inst}  →  {label}")

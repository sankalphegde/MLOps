# Lab 6 — KServe Model Serving: Iris Classifier

**Author:** Sankalp Hegde
**Model name:** `iris-classifier-sankalp`
**Framework:** scikit-learn (RandomForestClassifier)
**Serving platform:** KServe on Kubernetes

---

## What This Lab Does

This lab demonstrates end-to-end MLOps model serving using KServe:

1. Train a scikit-learn classifier on the Iris dataset
2. Save the model artifact as `model.joblib`
3. Deploy it to Kubernetes via a KServe `InferenceService`
4. Send HTTP inference requests and receive predictions

This is a realistic MLOps workflow: model artifact → packaging → deployment config → live inference validation.

---

## Project Structure

```
Lab 6/
├── scripts/
│   └── train.py                  # Training script — produces model artifact
├── model/
│   ├── model.joblib              # Trained model artifact (joblib format)
│   └── metadata.json             # Model metadata: version, features, classes
├── kserve/
│   ├── inference-service.yaml    # KServe InferenceService with autoscaling + resource config
│   └── pvc.yaml                  # PersistentVolumeClaim for model storage
├── requests/
│   ├── predict.json              # Standard 3-sample inference payload
│   ├── predict_edge_cases.json   # Boundary-case payloads near class decision borders
│   └── curl_commands.sh          # Ready-to-run curl commands for testing
└── README.md
```

---

## The Model

### Dataset: Iris

The [Iris dataset](https://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html) has 150 samples across 3 flower species, described by 4 measurements:

| Feature index | Feature name       | Unit | Description                          |
|---------------|--------------------|------|--------------------------------------|
| 0             | `sepal_length_cm`  | cm   | Length of the outer leaf (sepal)     |
| 1             | `sepal_width_cm`   | cm   | Width of the outer leaf (sepal)      |
| 2             | `petal_length_cm`  | cm   | Length of the inner leaf (petal)     |
| 3             | `petal_width_cm`   | cm   | Width of the inner leaf (petal)      |

### Target Classes

| Label | Class name    | Characteristics                                    |
|-------|---------------|----------------------------------------------------|
| `0`   | `setosa`      | Small petals (length ~1.5 cm), easy to separate    |
| `1`   | `versicolor`  | Medium petals (length ~4.3 cm), overlaps virginica |
| `2`   | `virginica`   | Large petals (length ~5.6 cm), hardest to classify |

### Classifier

```
Algorithm   : RandomForestClassifier
n_estimators: 100
max_depth   : 5
random_state: 42
Test accuracy: 93.33%
```

A RandomForestClassifier was chosen because it handles the multi-class iris problem well without hyperparameter tuning, and its joblib serialization is natively supported by KServe's sklearn predictor.

---

## Step 1: Train and Save the Model

```bash
cd "Lab 6"
pip install -r requirements.txt
python scripts/train.py
```

Expected output:
```
==================================================
Model       : RandomForestClassifier
Dataset     : Iris (150 samples, 4 features, 3 classes)
Train size  : 120
Test size   : 30
Accuracy    : 0.9333
==================================================
              precision    recall  f1-score   support
      setosa       1.00      1.00      1.00        10
  versicolor       0.90      0.90      0.90        10
   virginica       0.90      0.90      0.90        10

Smoke-test predictions:
  [5.1, 3.5, 1.4, 0.2]  →  setosa
  [6.7, 3.1, 4.7, 1.5]  →  versicolor
  [7.2, 3.6, 6.1, 2.5]  →  virginica
```

The model is saved to `model/model.joblib` and metadata to `model/metadata.json`.

---

## Step 2: Copy Model to PVC

KServe reads the model artifact from a PersistentVolumeClaim (PVC). After the cluster is running:

```bash
# Apply the PVC
kubectl apply -f kserve/pvc.yaml

# Copy model artifact into the PVC
# (use a helper pod or kubectl cp depending on your cluster setup)
kubectl cp model/model.joblib default/<helper-pod>:/mnt/models/model/model.joblib
```

The `storageUri` in the InferenceService YAML points to `pvc://iris-model-pvc/model`, so the file must be at `/mnt/models/model/model.joblib` inside the PVC.

---

## Step 3: Deploy the InferenceService

```bash
kubectl apply -f kserve/inference-service.yaml
```

Check status:
```bash
kubectl get inferenceservice iris-classifier-sankalp -n default
```

Wait until `READY = True`:
```
NAME                        URL                                                      READY   PREV   LATEST   PREVROLLEDOUTREVISION   LATESTREADYREVISION                     AGE
iris-classifier-sankalp    http://iris-classifier-sankalp.default.example.com       True           100                              iris-classifier-sankalp-predictor-...   2m
```

---

## Step 4: Send Inference Requests

### Standard payload (`requests/predict.json`)

```json
{
  "instances": [
    [5.1, 3.5, 1.4, 0.2],
    [6.7, 3.1, 4.7, 1.5],
    [7.2, 3.6, 6.1, 2.5]
  ]
}
```

These three samples represent one clear example of each class:
- `[5.1, 3.5, 1.4, 0.2]` → tiny petals → **setosa (0)**
- `[6.7, 3.1, 4.7, 1.5]` → medium petals → **versicolor (1)**
- `[7.2, 3.6, 6.1, 2.5]` → large petals → **virginica (2)**

**Send the request:**

```bash
SERVICE_NAME="iris-classifier-sankalp"
INGRESS_HOST=$(kubectl get inferenceservice $SERVICE_NAME -n default \
  -o jsonpath='{.status.url}' | sed 's|http://||')

curl -X POST \
  -H "Content-Type: application/json" \
  -H "Host: $INGRESS_HOST" \
  http://$INGRESS_HOST/v1/models/$SERVICE_NAME:predict \
  -d @requests/predict.json
```

**Expected response:**
```json
{
  "predictions": [0, 1, 2]
}
```

---

### Edge-case payload (`requests/predict_edge_cases.json`)

```json
{
  "instances": [
    [5.8, 2.7, 4.1, 1.0],
    [6.0, 2.9, 4.5, 1.5],
    [6.3, 3.3, 6.0, 2.5]
  ]
}
```

These samples sit near the versicolor/virginica decision boundary, testing the model's robustness:
- `[5.8, 2.7, 4.1, 1.0]` → borderline → expected **versicolor (1)**
- `[6.0, 2.9, 4.5, 1.5]` → borderline → expected **versicolor (1)**
- `[6.3, 3.3, 6.0, 2.5]` → clear large petals → expected **virginica (2)**

**Expected response:**
```json
{
  "predictions": [1, 1, 2]
}
```

---

### Local port-forward (no ingress needed)

```bash
kubectl port-forward svc/knative-local-gateway 8080:80 -n istio-system &

curl -X POST http://localhost:8080/v1/models/iris-classifier-sankalp:predict \
  -H "Content-Type: application/json" \
  -H "Host: iris-classifier-sankalp.default.svc.cluster.local" \
  -d @requests/predict.json
```

---

## KServe Configuration Details

### InferenceService (`kserve/inference-service.yaml`)

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: iris-classifier-sankalp
  labels:
    model-version: "1.0.0"
    owner: sankalp-hegde
  annotations:
    autoscaling.knative.dev/minScale: "1"
    autoscaling.knative.dev/maxScale: "3"
    autoscaling.knative.dev/target: "10"
    autoscaling.knative.dev/metric: "concurrency"
spec:
  predictor:
    sklearn:
      storageUri: "pvc://iris-model-pvc/model"
      runtimeVersion: "1.3.0"
      resources:
        requests:
          memory: "128Mi"
          cpu: "250m"
        limits:
          memory: "512Mi"
          cpu: "500m"
```

**Key MLOps design decisions:**

| Setting | Value | Reason |
|---------|-------|--------|
| `minScale: 1` | Always 1 pod running | Avoids cold-start latency for demo |
| `maxScale: 3` | Up to 3 replicas | Handles burst traffic without over-provisioning |
| `target: 10` | Scale up at 10 concurrent requests | Keeps per-pod load manageable |
| `memory request: 128Mi` | Enough for a small sklearn model | Efficient resource use |
| `cpu request: 250m` | 0.25 CPU cores | Sufficient for synchronous inference |
| `runtimeVersion: 1.3.0` | Pinned sklearn version | Reproducible, avoids runtime drift |

---

## Model Version

| Property      | Value                    |
|---------------|--------------------------|
| Model name    | `iris-classifier-sankalp` |
| Version       | `1.0.0`                  |
| Trained on    | Iris dataset (sklearn)   |
| Accuracy      | 93.33% on 30-sample test |
| Saved as      | `model/model.joblib`     |

Labels in the YAML (`model-version: "1.0.0"`) allow `kubectl` queries like:
```bash
kubectl get inferenceservice -l model-version=1.0.0
```
This supports multi-version tracking when rolling out `v2.0.0` alongside `v1.0.0`.

---

## Prerequisites

- Kubernetes cluster (minikube, kind, or cloud)
- KServe installed ([install guide](https://kserve.github.io/website/master/get_started/))
- `kubectl` configured
- Python 3.8+ with dependencies from `requirements.txt`

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `READY=False` after apply | Check predictor pod logs: `kubectl logs -l serving.kserve.io/inferenceservice=iris-classifier-sankalp` |
| `404` on predict URL | Confirm `storageUri` path matches where `model.joblib` was copied |
| `500` internal error | Ensure model was saved with same sklearn version as `runtimeVersion` |
| Connection refused | Verify ingress controller is running or use port-forward |

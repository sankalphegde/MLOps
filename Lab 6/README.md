# Lab 6 - KServe Model Serving: Iris Classifier

This lab deploys a custom scikit-learn Iris classifier as a live HTTP inference service using KServe on Kubernetes.

## What This Lab Does
- Trains a `RandomForestClassifier` on the Iris dataset (150 samples, 4 features, 3 classes)
- Saves the model artifact as `model/model.joblib` using joblib
- Defines a KServe `InferenceService` with autoscaling and resource limits
- Stores the model on a Kubernetes PersistentVolumeClaim (PVC)
- Sends HTTP inference requests and returns class predictions

## Why This Is Different From The Reference Lab
- Custom model name: `iris-classifier-sankalp`
- Custom inference payloads: standard 3-sample payload and a separate edge-case payload near the versicolor/virginica decision boundary
- Autoscaling annotations: min 1 replica, max 3, scale trigger at 10 concurrent requests
- Resource limits configured: `128Mi`/`250m` request, `512Mi`/`500m` limit
- Model version label (`model-version: "1.0.0"`) in the YAML for multi-version tracking
- `model-settings.json` included for MLServer sklearn runtime compatibility

## Folder Structure
```
Lab 6/
├── scripts/
│   └── train.py                  # Trains and saves the model artifact
├── model/
│   ├── model.joblib              # Trained model (93.33% test accuracy)
│   ├── metadata.json             # Model version, features, classes
│   └── model-settings.json      # MLServer sklearn runtime config
├── kserve/
│   ├── inference-service.yaml    # KServe InferenceService YAML
│   └── pvc.yaml                  # PersistentVolumeClaim for model storage
├── requests/
│   ├── predict.json              # Standard 3-sample inference payload
│   ├── predict_edge_cases.json   # Edge-case payload near class boundaries
│   └── curl_commands.sh          # curl commands for live endpoint testing
├── requirements.txt
└── README.md
```

## How To Run

### Step 1: Train the model
```bash
cd "Lab 6"
pip install -r requirements.txt
python scripts/train.py
```

### Step 2: Deploy on Kubernetes
```bash
# Create PVC and deploy InferenceService
kubectl apply -f kserve/pvc.yaml
kubectl apply -f kserve/inference-service.yaml

# Copy model artifact to PVC (via helper pod)
kubectl cp model/model.joblib default/<helper-pod>:/mnt/models/model/model.joblib

# Wait for READY=True
kubectl get inferenceservice iris-classifier-sankalp -n default
```

### Step 3: Send inference request
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

## Expected Outputs

**Standard payload** (`predict.json`) — one sample per class:
```
[5.1, 3.5, 1.4, 0.2]  →  setosa (0)
[6.7, 3.1, 4.7, 1.5]  →  versicolor (1)
[7.2, 3.6, 6.1, 2.5]  →  virginica (2)
```
Response: `{"predictions": [0, 1, 2]}`

**Edge-case payload** (`predict_edge_cases.json`) — samples near versicolor/virginica boundary:
```
[5.8, 2.7, 4.1, 1.0]  →  versicolor (1)
[6.0, 2.9, 4.5, 1.5]  →  versicolor (1)
[6.3, 3.3, 6.0, 2.5]  →  virginica (2)
```
Response: `{"predictions": [1, 1, 2]}`

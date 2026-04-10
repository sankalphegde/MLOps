#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Lab 6 – KServe inference request examples
# Run these after the InferenceService reaches READY=True
# ─────────────────────────────────────────────────────────────────────────────

SERVICE_NAME="iris-classifier-sankalp"
NAMESPACE="default"

# ── Step 1: Check InferenceService status ────────────────────────────────────
kubectl get inferenceservice $SERVICE_NAME -n $NAMESPACE

# ── Step 2: Get the ingress URL (Knative) ────────────────────────────────────
INGRESS_HOST=$(kubectl get inferenceservice $SERVICE_NAME -n $NAMESPACE \
  -o jsonpath='{.status.url}' | sed 's|http://||')
INGRESS_PORT=80
SERVICE_HOSTNAME=$INGRESS_HOST

echo "Inference endpoint: http://$INGRESS_HOST/v1/models/$SERVICE_NAME:predict"

# ── Step 3: Send standard 3-sample prediction request ────────────────────────
# Expected predictions: ["setosa", "versicolor", "virginica"]
curl -s \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Host: $SERVICE_HOSTNAME" \
  http://$INGRESS_HOST:$INGRESS_PORT/v1/models/$SERVICE_NAME:predict \
  -d @predict.json | python3 -m json.tool

# ── Step 4: Send edge-case prediction request ─────────────────────────────────
# Expected predictions: ["versicolor", "versicolor", "virginica"]
curl -s \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Host: $SERVICE_HOSTNAME" \
  http://$INGRESS_HOST:$INGRESS_PORT/v1/models/$SERVICE_NAME:predict \
  -d @predict_edge_cases.json | python3 -m json.tool

# ── Step 5 (alternative): Port-forward for local testing ─────────────────────
# kubectl port-forward svc/knative-local-gateway 8080:80 -n istio-system &
# curl -s -X POST http://localhost:8080/v1/models/$SERVICE_NAME:predict \
#   -H "Content-Type: application/json" \
#   -H "Host: iris-classifier-sankalp.default.svc.cluster.local" \
#   -d @predict.json | python3 -m json.tool

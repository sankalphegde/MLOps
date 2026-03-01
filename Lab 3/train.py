import mlflow
import mlflow.sklearn
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

# Use a local sqlite backend store so training and UI read the same run history.
mlflow.set_tracking_uri("sqlite:///mlflow.db")

# Set experiment name (will create if doesn't exist)
mlflow.set_experiment("Lab3_MLflow_Breast_Cancer")

# Load dataset
data = load_breast_cancer()
X = data.data
y = data.target

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Hyperparameters to try
n_estimators_list = [50, 100, 200]

for n in n_estimators_list:
    with mlflow.start_run():
        # Model
        model = RandomForestClassifier(n_estimators=n, random_state=42)
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        # Metrics
        accuracy = accuracy_score(y_test, predictions)
        f1 = f1_score(y_test, predictions)

        # Log parameters & metrics
        mlflow.log_param("n_estimators", n)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1_score", f1)

        # Log confusion matrix as artifact
        cm = confusion_matrix(y_test, predictions)
        plt.figure()
        plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title("Confusion Matrix")
        plt.colorbar()
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        artifact_path = f"confusion_matrix_{n}.png"
        plt.savefig(artifact_path)
        plt.close()
        mlflow.log_artifact(artifact_path)

        # Log the model
        mlflow.sklearn.log_model(model, f"model_{n}")

print("✅ Training complete. Open MLflow UI to see experiments.")

from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_data():
    dataset = load_breast_cancer(as_frame=True)
    df = dataset.frame.copy()
    df["target_name"] = df["target"].map({0: "malignant", 1: "benign"})
    return df


def train_models(test_size=0.2, random_state=42):
    df = load_data()
    x = df.drop(columns=["target", "target_name"])
    y = df["target"]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    lr_model = LogisticRegression(max_iter=500, random_state=random_state)
    rf_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        random_state=random_state,
    )

    lr_model.fit(x_train_scaled, y_train)
    rf_model.fit(x_train, y_train)

    lr_probs = lr_model.predict_proba(x_test_scaled)[:, 1]
    rf_probs = rf_model.predict_proba(x_test)[:, 1]

    lr_preds = (lr_probs >= 0.5).astype(int)
    rf_preds = (rf_probs >= 0.5).astype(int)

    metrics = {
        "logistic_regression": {
            "accuracy": accuracy_score(y_test, lr_preds),
            "f1": f1_score(y_test, lr_preds),
            "roc_auc": roc_auc_score(y_test, lr_probs),
        },
        "random_forest": {
            "accuracy": accuracy_score(y_test, rf_preds),
            "f1": f1_score(y_test, rf_preds),
            "roc_auc": roc_auc_score(y_test, rf_probs),
        },
    }

    artifacts = {
        "x_test": x_test,
        "y_test": y_test,
        "lr_model": lr_model,
        "rf_model": rf_model,
        "scaler": scaler,
        "lr_probs": lr_probs,
        "rf_probs": rf_probs,
    }
    return metrics, artifacts

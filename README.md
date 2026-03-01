# MLOps Course - All Labs

Repository containing all lab assignments for the MLOps course at Northeastern University.

## Repository Structure
```
MLOps/
├── Lab1/          # GitHub Lab: Temperature Converter with Testing & CI/CD
├── Lab 2/         # Streamlit ML Dashboard (customized Lab 2)
├── Lab 3/         # MLflow experiment tracking (customized Lab 3)
└── README.md
```

## Labs

### Lab 1: Temperature Converter with GitHub Actions ✅
- **Topic**: Version Control, Testing, CI/CD
- **Description**: Temperature conversion functions with automated testing using pytest and unittest
- **Technologies**: Python, pytest, unittest, GitHub Actions
- **Status**: Complete

[📁 View Lab 1 →](./Lab1/)

### Lab 2: Breast Cancer Prediction Dashboard ✅
- **Topic**: Streamlit, Model Comparison, ML Evaluation
- **Description**: Custom Streamlit app comparing Logistic Regression and Random Forest on breast cancer classification.
- **Technologies**: Python, Streamlit, scikit-learn, pandas, matplotlib, seaborn
- **Key features**:
  - model comparison table (accuracy, F1, ROC-AUC)
  - threshold tuning with sidebar controls
  - confusion matrix and ROC curve
  - feature importance visualization
- **Status**: Complete

[📁 View Lab 2 →](./Lab%202/)

### Lab 3: MLflow Experiment Tracking ✅
- **Topic**: Experiment Tracking, Model Logging, Artifact Management
- **Description**: MLflow-based experiment tracking on breast cancer classification with multiple Random Forest hyperparameter runs.
- **Technologies**: Python, MLflow, scikit-learn, matplotlib
- **Key features**:
  - tracks runs for `n_estimators` = 50, 100, 200
  - logs metrics (`accuracy`, `f1_score`)
  - logs confusion matrix artifacts for each run
  - logs trained model artifacts in MLflow
- **Status**: Complete

[📁 View Lab 3 →](./Lab%203/)

## About This Repository

Each completed lab is contained in its own folder with:
- Complete source code
- Relevant tests/evaluation workflow
- Lab-specific README with detailed instructions

## Author

**Sankalp Hegde**  
Northeastern University  
Course: MLOps (Spring 2026)

## How to Use
```bash
# Clone the repository
git clone https://github.com/sankalphegde/MLOps.git
cd MLOps

# Navigate to a specific lab
cd "Lab 3"

# Follow the lab-specific README for setup and testing instructions
```

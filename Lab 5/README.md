# Lab 5 - Airflow Student Scores Pipeline

This lab implements a custom Airflow DAG named `student_scores_pipeline`.
It creates a local student score dataset, cleans it, calculates subject averages,
identifies the top 3 students, and writes a final summary report.

## What This DAG Does
- Creates a local CSV file at `data/student_scores.csv`
- Cleans and standardizes the dataset
- Calculates average scores for math, science, and english
- Identifies the top 3 students based on overall average
- Calculates pass/fail counts
- Writes a text report to `output/summary_report.txt`
- Writes cleaned and intermediate output artifacts to the `output/` folder

## Why This Is Different From The Reference Lab
- Uses a different workflow domain: student performance analytics
- Uses multiple transformation and reporting tasks
- Generates custom output artifacts:
  - `output/cleaned_scores.csv`
  - `output/subject_averages.json`
  - `output/top_students.json`
  - `output/summary_report.txt`
- Uses a different DAG structure and task sequence than the source lab

## DAG Details
- DAG name: `student_scores_pipeline`
- Dataset columns:
  - `student`
  - `math`
  - `science`
  - `english`

## Task Flow
- `create_sample_data`
- `clean_scores_data`
- `calculate_subject_averages`
- `generate_top_students_report`
- `save_report`

## How To Run With Airflow
1. Clone your repository and go to the lab folder:
```bash
git clone https://github.com/sankalphegde/MLOps.git
cd MLOps/"Lab 5"
```

2. Initialize Airflow with Docker:
```bash
docker compose up airflow-init
```

3. Start Airflow services:
```bash
docker compose up
```

4. Open the Airflow UI:
```text
http://localhost:8080
```

5. Log in with:
```text
username: airflow
password: airflow
```

6. In the Airflow UI, trigger:
```text
student_scores_pipeline
```

7. After the DAG runs, check these files:
```text
Lab 5/data/student_scores.csv
Lab 5/output/cleaned_scores.csv
Lab 5/output/subject_averages.json
Lab 5/output/top_students.json
Lab 5/output/summary_report.txt
```

## Expected Outputs
- Subject averages for math, science, and english
- Top 3 students by average score
- Pass count and fail count
- Final text report summarizing the pipeline results

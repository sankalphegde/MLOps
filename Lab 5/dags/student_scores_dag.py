from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
except ImportError:
    DAG = None
    PythonOperator = None


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
SOURCE_FILE = DATA_DIR / "student_scores.csv"
CLEANED_FILE = OUTPUT_DIR / "cleaned_scores.csv"
SUBJECT_AVERAGES_FILE = OUTPUT_DIR / "subject_averages.json"
TOP_STUDENTS_FILE = OUTPUT_DIR / "top_students.json"
REPORT_FILE = OUTPUT_DIR / "summary_report.txt"


def create_sample_data() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    rows = [
        ["student", "math", "science", "english"],
        ["Ava", 88, 91, 85],
        ["Liam", 76, 84, 80],
        ["Noah", 93, 89, 95],
        ["Emma", 81, 78, 88],
        ["Sophia", 95, 94, 92],
        ["Mason", 67, 73, 70],
        ["Olivia", 90, 86, 91],
    ]

    with SOURCE_FILE.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(rows)


def clean_scores_data() -> None:
    cleaned_rows = []

    with SOURCE_FILE.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            cleaned_rows.append(
                {
                    "student": row["student"].strip(),
                    "math": int(row["math"]),
                    "science": int(row["science"]),
                    "english": int(row["english"]),
                }
            )

    with CLEANED_FILE.open("w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["student", "math", "science", "english"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)


def calculate_subject_averages() -> None:
    records = []

    with CLEANED_FILE.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        records = list(reader)

    subject_averages = {
        "math": round(sum(int(item["math"]) for item in records) / len(records), 2),
        "science": round(sum(int(item["science"]) for item in records) / len(records), 2),
        "english": round(sum(int(item["english"]) for item in records) / len(records), 2),
    }

    with SUBJECT_AVERAGES_FILE.open("w", encoding="utf-8") as averages_file:
        json.dump(subject_averages, averages_file, indent=2)


def generate_top_students_report() -> None:
    records = []

    with CLEANED_FILE.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            average = round(
                (int(row["math"]) + int(row["science"]) + int(row["english"])) / 3,
                2,
            )
            records.append(
                {
                    "student": row["student"],
                    "average": average,
                    "status": "pass" if average >= 75 else "fail",
                }
            )

    top_students = sorted(records, key=lambda item: item["average"], reverse=True)[:3]

    with TOP_STUDENTS_FILE.open("w", encoding="utf-8") as top_students_file:
        json.dump({"students": top_students}, top_students_file, indent=2)


def save_report() -> None:
    with CLEANED_FILE.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        records = []
        for row in reader:
            average = round(
                (int(row["math"]) + int(row["science"]) + int(row["english"])) / 3,
                2,
            )
            records.append({"student": row["student"], "average": average})

    with SUBJECT_AVERAGES_FILE.open("r", encoding="utf-8") as averages_file:
        subject_averages = json.load(averages_file)

    with TOP_STUDENTS_FILE.open("r", encoding="utf-8") as top_students_file:
        top_students = json.load(top_students_file)["students"]

    pass_count = sum(1 for item in records if item["average"] >= 75)
    fail_count = len(records) - pass_count

    lines = [
        "Student Scores Summary Report",
        f"Generated: {datetime.utcnow().isoformat()}Z",
        "",
        "Subject Averages:",
        f"- Math: {subject_averages['math']}",
        f"- Science: {subject_averages['science']}",
        f"- English: {subject_averages['english']}",
        "",
        "Top 3 Students:",
    ]

    for student in top_students:
        lines.append(
            f"- {student['student']}: average={student['average']}, status={student['status']}"
        )

    lines.extend(
        [
            "",
            f"Pass Count: {pass_count}",
            f"Fail Count: {fail_count}",
        ]
    )

    with REPORT_FILE.open("w", encoding="utf-8") as report:
        report.write("\n".join(lines))


default_args = {"owner": "sankalp"}


if DAG is not None and PythonOperator is not None:
    with DAG(
        dag_id="student_scores_pipeline",
        default_args=default_args,
        description="Custom Airflow DAG for student score analytics",
        start_date=datetime(2025, 1, 1),
        schedule="@daily",
        catchup=False,
        tags=["lab5", "custom", "student-scores"],
    ) as dag:
        create_data_task = PythonOperator(
            task_id="create_sample_data",
            python_callable=create_sample_data,
        )

        clean_data_task = PythonOperator(
            task_id="clean_scores_data",
            python_callable=clean_scores_data,
        )

        averages_task = PythonOperator(
            task_id="calculate_subject_averages",
            python_callable=calculate_subject_averages,
        )

        top_students_task = PythonOperator(
            task_id="generate_top_students_report",
            python_callable=generate_top_students_report,
        )

        save_report_task = PythonOperator(
            task_id="save_report",
            python_callable=save_report,
        )

        create_data_task >> clean_data_task >> [averages_task, top_students_task] >> save_report_task

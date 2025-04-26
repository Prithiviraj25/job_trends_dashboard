# dags/fetch_jobs_dag.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from include.fetch_jobs import fetch_jobs_from_adzuna  # <-- import your function

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_fetch_jobs():
    data = fetch_jobs_from_adzuna(COUNTRY="us",SEARCH_QUERY="Data Engineer")
    if data:
        # You could save to disk or just print for now
        print("[🧹] Sample Data:", data['results'][0] if data['results'] else "No jobs found.")
    else:
        print("[⚠️] No data fetched.")

with DAG(
    dag_id='fetch_jobs_dag',
    default_args=default_args,
    description='Fetch jobs from Adzuna API every 10 minutes',
    schedule_interval='*/10 * * * *',
    start_date=datetime(2025, 4, 26),
    catchup=False,
    tags=['job-ingestion', 'adzuna'],
) as dag:

    fetch_jobs_task = PythonOperator(
        task_id='fetch_jobs',
        python_callable=run_fetch_jobs
    )

    fetch_jobs_task
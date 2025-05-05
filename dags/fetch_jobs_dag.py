# dags/fetch_jobs_dag.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from include.fetch_jobs import fetch_jobs_from_adzuna  
from include.config import it_jobs
import json
import os
from dotenv import load_dotenv

load_dotenv()

# supabase storage setup
from supabase import create_client, Client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

BUCKET_NAME = "job-data"
FILE_PATH = "output.json"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_fetch_jobs():
    file_contents = []

    # Step 1: Try to download existing file if it exists
    try:
        res = supabase.storage.from_(BUCKET_NAME).download(FILE_PATH)
        file_contents = json.loads(res.decode("utf-8"))
        print(f"[📥] Existing file '{FILE_PATH}' downloaded from Supabase.")
    except Exception as e:
        print(f"[ℹ️] No existing file found. A new one will be created: {str(e)}")
        file_contents = []

    # Step 2: Fetch new jobs and append
    for job in it_jobs:
        data = fetch_jobs_from_adzuna(COUNTRY="us", SEARCH_QUERY=job)

        if not data:
            print(f"[⚠️] No data fetched for job title: {job}. Skipping.")
            continue
        print(data)
        file_contents.append(data)
        print(f"[✅] Added data for job title: {job} and file contents are {file_contents}")

    # Step 3: Upload updated file to Supabase Storage
    try:
        json_data = json.dumps(file_contents, indent=2)
        supabase.storage.from_(BUCKET_NAME).upload(FILE_PATH, json_data.encode("utf-8"),{
            'upsert': 'true',
        })
        print(f"[🚀] Data uploaded to Supabase bucket '{BUCKET_NAME}' as '{FILE_PATH}'")
    except Exception as e:
        print(f"[❌] Failed to upload data to Supabase: {str(e)}")

    
with DAG(
    dag_id='fetch_jobs_dag',
    default_args=default_args,
    description='Fetch jobs from Adzuna API every 10 minutes',
    schedule_interval=None,
    start_date=datetime(2025, 4, 26),
    catchup=False,
    tags=['job-ingestion', 'adzuna'],
) as dag:

    fetch_jobs_task = PythonOperator(
        task_id='fetch_jobs',
        python_callable=run_fetch_jobs
    )

    fetch_jobs_task
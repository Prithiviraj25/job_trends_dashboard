from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import json
from pyspark.sql import SparkSession
from include.config import dataframe_schema  # Ensure this is available
from supabase import create_client

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Supabase connection details
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "job-data"
FILE_PATH = "output.json"
TABLE_NAME = "job_data"

def fetch_data_from_supabase():
    """ Fetch data from Supabase bucket """
    from supabase import create_client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    res = supabase.storage.from_(BUCKET_NAME).download(FILE_PATH)
    return res.decode("utf-8")

def normalize_with_spark(raw_json: str):
    """ Normalize JSON data using Spark """
    spark = SparkSession.builder.appName("Normalize JSON").getOrCreate()
    data = json.loads(raw_json)

    schema = dataframe_schema
    df = spark.createDataFrame([], schema)

    for record in data:
        json_data = json.dumps(record)
        temp_df = spark.read.json(spark.sparkContext.parallelize([json_data]))
        df = df.union(temp_df)

    return df.toPandas().to_dict(orient="records")

def insert_into_supabase(rows: list):
    """ Insert data into Supabase table """
    from supabase import create_client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    if not rows:
        print("[⚠️] No data to insert.")
        return

    for chunk in [rows[i:i + 100] for i in range(0, len(rows), 100)]:
        try:
            supabase.table(TABLE_NAME).upsert(chunk, on_conflict=["id"]).execute()
        except Exception as e:
            print(f"[❌] Error inserting chunk: {e}")
    
    print(f"[✅] Inserted or updated {len(rows)} rows into Supabase table `{TABLE_NAME}`.")

# Define the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'start_date': datetime(2025, 5, 1),  # Adjust the start date
}

dag = DAG(
    'supabase_job_data_dag',
    default_args=default_args,
    schedule_interval='@daily',  # Adjust as necessary
    catchup=False,
    tags=['supabase', 'job_data'],
)

def run_etl():
    """ETL process to fetch, normalize and insert data into Supabase."""
    raw_data = fetch_data_from_supabase()
    normalized_rows = normalize_with_spark(raw_data)
    insert_into_supabase(normalized_rows)

# Create a task to run the ETL function
etl_task = PythonOperator(
    task_id='run_etl_task',
    python_callable=run_etl,
    dag=dag,
)

etl_task
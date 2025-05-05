# 📊 Job Trends Dashboard – ETL Pipeline

This project builds a robust ETL pipeline using **Apache Airflow**, **PySpark**, and **Supabase** to power a job trends dashboard with real-time data fetched from the **Adzuna API**.

---

## ⚙️ Functional Overview

### 1. **Data Ingestion**
- **Source**: [Adzuna Job Search API](https://developer.adzuna.com/)
- **Script**: `fetch_jobs_dag.py`
- For each role in `it_jobs`, job listing data is fetched from Adzuna and appended to an `output.json` file.

### 2. **Data Storage**
- The `output.json` is uploaded to a **Supabase storage bucket** named `job-data`.
- Uses upsert to maintain historical continuity while preventing duplication.

### 3. **Data Normalization and Insertion**
- **Script**: `snormalise _and_insert_data.py`
- Downloads `output.json` from Supabase.
- Uses **PySpark** to normalize nested JSON structures and enforce schema (`dataframe_schema`).
- Final output is converted to a list of Python dictionaries and inserted (or updated) into the `job_data` table in Supabase Postgres.

---

## 🔁 DAGs & Scheduling

- `fetch_jobs_dag` – Manually triggered or scheduled (e.g., every 10 mins) to fetch new job listings.
- `normalise _and_insert_data.py` – Scheduled daily to normalize and insert data into the Supabase database.

---

## 🛠 Tech Stack

| Component      | Usage                              |
|----------------|-------------------------------------|
| **Airflow**    | Orchestration of ETL tasks          |
| **Adzuna API** | Data source for job listings        |
| **PySpark**    | JSON normalization & schema enforcement |
| **Supabase**   | Storage (buckets) + PostgreSQL DB   |
| **Docker**     | Containerized Airflow environment   |
| **Python**     | Core scripting                      |
| **dotenv**     | Credential and config management    |

---

## 📁 Bucket & Table Structure

### Supabase Bucket: `job-data`
- `output.json`: Contains raw job data (fetched daily/periodically)

### Supabase Table: `job_data`
- Schema aligned to normalized job attributes
- Inserted via `upsert` using `id` as the conflict key
## 🗃️ Supabase Table Schema: `job_data`

| Column Name         | Data Type         | Nullable | Notes                                 |
|---------------------|-------------------|----------|---------------------------------------|
| `id`                | `text`            | ❌ No    | Primary key, job ID                   |
| `title`             | `text`            | ✅ Yes   | Job title                             |
| `company`           | `text`            | ✅ Yes   | Company name                          |
| `location`          | `text`            | ✅ Yes   | Full location as string               |
| `location_hierarchy`| `text[]`          | ✅ Yes   | Array of strings (hierarchy)          |
| `category`          | `text`            | ✅ Yes   | Job category                          |
| `salary_min`        | `double precision`| ✅ Yes   | Minimum salary                        |
| `salary_max`        | `double precision`| ✅ Yes   | Maximum salary                        |
| `salary_is_predicted`| `boolean`        | ✅ Yes   | Is salary predicted? (`true/false`)   |
| `posted_date`       | `timestamptz`     | ✅ Yes   | ISO timestamp                         |
| `description`       | `text`            | ✅ Yes   | Full description                      |
| `url`               | `text`            | ✅ Yes   | Original job posting URL              |
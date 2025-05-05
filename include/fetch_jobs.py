# include/fetch_jobs.py

import requests

# Your API credentials
from dotenv import load_dotenv
import os
load_dotenv()

APP_ID=os.getenv("APP_ID")
APP_KEY=os.getenv("APP_KEY")

RESULTS_PER_PAGE = 5

def fetch_jobs_from_adzuna(COUNTRY, SEARCH_QUERY):
    url = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/1"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": RESULTS_PER_PAGE,
        "what": SEARCH_QUERY,
        "content-type": "application/json"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        job_list = []

        for job in data.get("results", []):
            job_info = {
                "id": job.get("id"),
                "title": job.get("title"),
                "company": job.get("company", {}).get("display_name"),
                "location": job.get("location", {}).get("display_name"),
                "location_hierarchy": job.get("location", {}).get("area"),
                "category": job.get("category", {}).get("label"),
                "salary_min": job.get("salary_min"),
                "salary_max": job.get("salary_max"),
                "salary_is_predicted": int(job.get("salary_is_predicted", "0")),
                "posted_date": job.get("created"),
                "description": job.get("description"),
                "url": job.get("redirect_url")
            }
            job_list.append(job_info)

        print(f"[✅] Fetched and formatted {len(job_list)} jobs.")
        return job_list
    
    else:
        print(f"[❌] Error {response.status_code}: {response.text}")
        return None
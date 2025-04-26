# include/fetch_jobs.py

import requests

# Your API credentials
APP_ID = "2326d4e5"
APP_KEY = "139483a3af97fd127865e3133b9ba188"


RESULTS_PER_PAGE = 10

def fetch_jobs_from_adzuna(COUNTRY,SEARCH_QUERY):
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
        print(f"[✅] Fetched {len(data.get('results', []))} jobs.")
        return data
    else:
        print(f"[❌] Error {response.status_code}: {response.text}")
        return None
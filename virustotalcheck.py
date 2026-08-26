import os
import time

import requests
from dotenv import load_dotenv

envPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(dotenv_path=envPath)

vtKey = os.getenv("VT_API_KEY")


def checkVT(filehash, retries=1):
    if not vtKey:
        return "Skipped (NO API KEY)"

    url = f"https://www.virustotal.com/api/v3/files/{filehash}"
    headers = {
        "accept": "application/json",
        "x-apikey": vtKey,
    }

    for attempt in range(retries + 1):
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            stats = data["data"]["attributes"]["last_analysis_stats"]
            bad = stats.get("malicious", 0)
            sus = stats.get("suspicious", 0)
            if bad or sus > 0:
                return f"Flagged, {bad} malicious, {sus}, suspicious"
            return "Clean"
        if res.status_code == 404:
            return "Unknown file(not found in global database, please proceed with caution)"
        if res.status_code == 429:
            if attempt < retries:
                time.sleep(15)
                continue
            return "Error: time limit reached, please try again later"
        return f"Error: {res.status_code}"

    return "Error: could not complete request"
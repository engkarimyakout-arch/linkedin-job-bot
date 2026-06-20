import os
import requests
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

KEYWORDS = [
    "Data Engineer",
    "Microsoft Fabric",
    "Azure Data Engineer"
]

COUNTRIES = [
    "Saudi Arabia",
    "United Arab Emirates"
]

SEEN_FILE = "seen_jobs.json"

def load_seen():
    try:
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

# TEMP DATA SOURCE (we will upgrade later if needed)
def get_jobs():
    return [
        {
            "id": "1",
            "title": "Data Engineer",
            "company": "Example Company",
            "location": "Saudi Arabia",
            "link": "https://linkedin.com/jobs/view/1"
        },
        {
            "id": "2",
            "title": "Power BI Developer",
            "company": "ABC Corp",
            "location": "UAE",
            "link": "https://linkedin.com/jobs/view/2"
        }
    ]

seen = load_seen()
jobs = get_jobs()

for job in jobs:

    text = (job["title"] + job["location"]).lower()

    if job["id"] in seen:
        continue

    if not any(k.lower() in text for k in KEYWORDS):
        continue

    if not any(c.lower() in job["location"].lower() for c in COUNTRIES):
        continue

    msg = f"""📌 {job['title']}
🏢 {job['company']}
📍 {job['location']}
🔗 {job['link']}"""

    send(msg)
    seen.add(job["id"])

save_seen(seen)

print("Done - jobs processed")

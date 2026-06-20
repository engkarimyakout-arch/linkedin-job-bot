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
    import requests
    from bs4 import BeautifulSoup

    query = "Data Engineer OR Power BI OR Microsoft Fabric jobs in Saudi Arabia OR UAE"

    url = f"https://www.google.com/search?q={query}&ibp=job"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    for g in soup.find_all("div"):
        text = g.get_text(" ", strip=True)

        if "Apply" in text and ("Saudi" in text or "UAE" in text or "Dubai" in text or "Riyadh" in text):
            jobs.append({
                "id": str(hash(text)),
                "title": "Job Found",
                "company": "Google Jobs",
                "location": "KSA/UAE",
                "link": "https://www.google.com/search?q=jobs"
            })

    return jobs[:5]

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

def send(msg):
    print("SENDING MESSAGE:")
    print(msg)

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )

    print("STATUS CODE:", response.status_code)
    print("RESPONSE TEXT:", response.text)

save_seen(seen)

print("Done - jobs processed")

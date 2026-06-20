from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events
from linkedin_jobs_scraper.query import Query
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )

def on_data(data):

    msg = f"""
📌 {data.title}

🏢 {data.company}

📍 {data.location}

🔗 {data.link}
"""

    send_telegram(msg)

scraper = LinkedinScraper()

scraper.on(Events.DATA, on_data)

queries = [
    Query(
        query="Data Engineer",
        locations=["United Arab Emirates"],
        limit=10
    )
]

scraper.run(queries)

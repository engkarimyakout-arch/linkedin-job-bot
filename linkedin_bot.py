import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

message = """
🚀 GitHub Action Test

Hello Karim!

This message was sent from GitHub's cloud server.
"""

response = requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print(response.text)

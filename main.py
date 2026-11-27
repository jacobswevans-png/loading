import os
import requests
from datetime import datetime, timezone
from flask import Flask, send_from_directory

app = Flask(__name__)
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

visits = 0

@app.route("/")
def home():
    global visits

    response = send_from_directory(app.root_path, "index.html")

    if response.status_code == 200:
        visits += 1

        data = {
            "username": "Website Analytics",
            "allowed_mentions": {"parse": []},
            "embeds": [{
                "title": "New Website Visit",
                "color": 5793266,
                "fields": [
                    {
                        "name": "Website",
                        "value": "loading.up.railway.app"
                    },
                    {
                        "name": "Page",
                        "value": "/"
                    },
                    {
                        "name": "Status",
                        "value": "200 OK"
                    },
                    {
                        "name": "Visits Since Startup",
                        "value": str(visits)
                    }
                ],
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat(),
                "footer": {
                    "text": "Website Analytics"
                }
            }]
        }

        if WEBHOOK_URL:
            try:
                requests.post(
                    WEBHOOK_URL,
                    json=data,
                    timeout=3
                ).raise_for_status()
            except requests.RequestException:
                print("Webhook delivery failed.")

    return response

@app.route("/loading.gif")
def loading_gif():
    return send_from_directory(app.root_path, "loading.gif")

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8080))
    )

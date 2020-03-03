import os
import requests


def send_simple_message(amount, other_name):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxa290eb457da745fdad8b11f801694050.mailgun.org/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": "Nextagram Flask App <mailgun@sandboxa290eb457da745fdad8b11f801694050.mailgun.org >",
              "to": ["zeft.huisen@gmail.com"],
              "subject": f"{other_name} donated ${amount}",
              "text": "Testing some Mailgun awesomness!"})

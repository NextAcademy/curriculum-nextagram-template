import os
import requests


def send_simple_message(amount, receiving_name, name):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxa290eb457da745fdad8b11f801694050.mailgun.org/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": "Nextagram Flask App <mailgun@sandboxa290eb457da745fdad8b11f801694050.mailgun.org >",
              "to": ["zeft.huisen@gmail.com"],
              "subject": f"{name} donated ${amount} to {receiving_name}",
              "text": "Testing some Mailgun awesomness!"})

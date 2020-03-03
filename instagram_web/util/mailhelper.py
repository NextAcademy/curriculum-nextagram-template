import requests
import os

# url = "https://api.mailgun.net/vN/domainAbcdefg.mailgun.org"


def send_simple_message(amount, name):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox8305a785c9cf45bdaf8457fa68577b8f.mailgun.org/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": "Excited User mailgun@sandbox8305a785c9cf45bdaf8457fa68577b8f.mailgun.org",
              "to": ["haz.faizul@gmail.com"],
              "subject": f"Hello, ${amount} was just donated by {name}",
              "text": "Testing some Mailgun awesomness!"})

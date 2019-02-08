import os
import config
from flask import Flask
from models.base_model import db

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)
app.config.from_object(os.environ['APP_SETTINGS'])


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response

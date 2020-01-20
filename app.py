import os
import config
from flask import Flask, render_template
from models.base_model import db

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc


@app.route("/users/new")
def sign_up():
    return render_template('sign_up.html')

@app.route("/users/new/post", methods=['POST'])
def sign_up_post():
    return render_template('sign_up.html')

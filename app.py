import os
import config
from flask import Flask
from models.base_model import db
from config import Config
from authlib.integrations.flask_client import OAuth

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


oauth = OAuth()

oauth.register('google',
               client_id=Config.OAUTH_CLIENT_ID,
               client_secret=Config.OAUTH_CLIENT_SECRET,
               access_token_url='https://accounts.google.com/o/oauth2/token',
               access_token_params=None,
               refresh_token_url=None,
               authorize_url='https://accounts.google.com/o/oauth2/auth',
               api_base_url='https://www.googleapis.com/oauth2/v1/',
               client_kwargs={
                   'scope': 'https://www.googleapis.com/auth/userinfo.email',
                   'token_endpoint_auth_method': 'client_secret_basic',
                   'token_placement': 'header',
                   'prompt': 'consent'
               }
               )


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc

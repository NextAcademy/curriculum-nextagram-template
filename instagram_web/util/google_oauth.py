from authlib.flask.client import OAuth
import config
import os

if os.getenv('FLASK_ENV') == 'production':
    config = eval("config.ProductionConfig")
else:
    config = eval("config.DevelopmentConfig")

oauth = OAuth()

oauth.register('google',
               client_id=config.GOOGLE_CLIENT_ID,
               client_secret=config.GOOGLE_CLIENT_SECRET,
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

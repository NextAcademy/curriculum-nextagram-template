import braintree
import os
import config

from app import app
from flask import render_template
from models.user import User
from flask_assets import Environment, Bundle
from flask_login import LoginManager, current_user
from .util.assets import bundles
from instagram_web.helpers.google_oauth import oauth

assets = Environment(app)
assets.register(bundles)

login_manager = LoginManager(app)
oauth.init_app(app)

TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

gateway = braintree.BraintreeGateway(
   braintree.Configuration(
       braintree.Environment.Sandbox,
       merchant_id=app.config.get('BT_MERCHANT_ID'),
       public_key=app.config.get('BT_PUBLIC_KEY'),
       private_key=app.config.get('BT_PRIVATE_KEY')
   )
)

def generate_client_token():
   return gateway.client_token.generate()

def transact(options):
   return gateway.transaction.sale(options)

def find_transaction(id):
   return gateway.transaction.find(id)

from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.checkout.views import checkout_blueprint

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images" )
app.register_blueprint(checkout_blueprint, url_prefix="/checkout")

@login_manager.user_loader
def load_user(id):
    return User.get_or_none(id=id)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route("/")
def home():
    return render_template('home.html')



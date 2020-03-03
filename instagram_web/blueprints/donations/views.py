from instagram_web.util.gateway import gateway
from flask import Blueprint, render_template, request, redirect, url_for, flash, request
from flask_login import current_user, login_required
from models.donations import Donation
import os
from models.user import User
from models.user_images import Image
import requests

mg_domain = os.environ.get('MAILGUN_DOMAIN')
mg_api_key = os.environ.get('MAILGUN_API_KEY')


def send_simple_message(email):
    return requests.post(
        f"https://api.mailgun.net/v3/{mg_domain}/messages",
        auth=("api", f"{mg_api_key}"),
        data={"from": f"Excited User <mailgun@{mg_domain}>",
              "to": email,
              "subject": "Dono",
              "text": "Testing some Mailgun awesomness!"})


donations_blueprint = Blueprint(
    'donations', __name__, template_folder='templates')


@donations_blueprint.route('/<image_id>/new', methods=['GET'])
@login_required
def new(image_id):
    client_token = gateway.client_token.generate({
    })
    return render_template('donations/new.html', image_id=image_id, client_token=client_token)


@donations_blueprint.route('/<image_id>/create', methods=['POST'])
def create(image_id):
    amount = request.form.get('amount')
    payment_nonce = request.form.get('payment_nonce')
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": payment_nonce,
        "options": {
            "submit_for_settlement": True
        }
    })
    if not result.is_success:
        flash('dono did not work out.', 'warning')
        return redirect(request.referrer)

    dono = Donation(amount=amount, image_id=image_id)
    if dono.save():
        user = User.select().join(Image).where(Image.id == image_id)
        send_simple_message(user[0].email)
        flash(f'successfully donated {amount}', 'success')
        return redirect(url_for('users.index'))

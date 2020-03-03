from flask import Flask, Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required
from flask_login import current_user
from models.images import Image
from models.donations import Donation
from instagram_web.util.braintree import gateway
import requests
from config import Config
from models.user import User

donations_blueprint = Blueprint('donations',
                                __name__,
                                template_folder='templates')


def send_simple_message(email):
    return requests.post(
        f"{Config.MAILGUN_BASE_URL}/messages",
        auth=("api", Config.MAILGUN_API_KEY),
        data={"from": f"mailgun@{Config.MAILGUN_DOMAIN_NAME}",
              "to": [email],
              "subject": "Donation",
              "text": "You have received a donation to your image!"})


@donations_blueprint.route('/<image_id>/new', methods=['GET'])
@login_required
def new(image_id):
    image = Image.get_or_none(Image.id == image_id)

    if not image:
        flash('No image found', 'warning')
        return redirect(url_for('users.home'))

    client_token = gateway.client_token.generate()
    if not client_token:
        flash('Oh no', 'warning')
        return redirect(url_for('users.home'))

    return render_template('donations/new.html', image=image, client_token=client_token)


@donations_blueprint.route('/<image_id>/create', methods=['POST'])
@login_required
def create(image_id):
    nonce = request.form.get('payment_method_nonce')
    if not nonce:
        flash('invalid credit card details', 'warning')
        return redirect(url_for('users.index'))

    image = Image.get_or_none(Image.id == image_id)

    if not image:
        flash('No image found with the provided id', 'waning')
        return redirect(url_for('users.index'))

    amount = request.form.get('amount')

    if not amount:
        flash('No donation amount provided', 'warning')
        return redirect(url_for('users.index'))

    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        # "device_data": device_data_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })

    if not result.is_success:
        flash('Unable to complete transaction', 'warning')
        return redirect(request.referrer)

    donation = Donation(amount=amount, image_id=image.id,
                        user_id=current_user.id)

    if not donation.save():
        flash('Donation successful but error creating record', 'warning')
        return redirect(url_for('users.index'))

    flash(f'Donation successful. ${amount} donated', 'success')
    user = User.select().join(Image).where(Image.id == image_id)
    send_simple_message(user[0].email)
    return redirect(url_for('users.index'))

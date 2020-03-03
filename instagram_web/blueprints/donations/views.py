from instagram_web.util.gateway import gateway
from flask import Blueprint, render_template, request, redirect, url_for, flash, request
from flask_login import current_user, login_required
from models.donations import Donation


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
        flash('dono did not work out.')
        return redirect(request.referrer)

    dono = Donation(amount=amount, image_id=image_id)
    if not dono.save():
        flash('dono was successful. database not updated')

    return render_template('donations/new.html', payment_nonce=payment_nonce, result=result)

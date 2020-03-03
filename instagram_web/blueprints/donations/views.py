import peeweedbevolve
from flask import Blueprint, flash, Flask, render_template, request, flash, redirect, url_for, session
from models.user import User
from models.photos import Photos
from models.donation import Donation
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from instagram_web.util.s3_uploader import upload_file_to_s3
from instagram_web.util.braintree import gateway

donations_blueprint = Blueprint('donations',
                                __name__,
                                template_folder='templates')


@donations_blueprint.route('/<photo_id>/new', methods=['GET'])
def new(photo_id):
    image = Photos.get_or_none(Photos.id == photo_id)

    if not image:
        flash('No image found with id provided', 'warning')
        return redirect(request.referrer)

    client_token = gateway.client_token.generate()

    if not client_token:
        flash('Unable to obtain token', 'warning')
        return redirect(request.referrer)

    return render_template('donations/new.html', image=image, client_token=client_token)


@donations_blueprint.route('/<photo_id>', methods=['POST'])
def create(photo_id):
    nonce = request.form.get('payment_method_nonce')

    if not nonce:
        flash(f"Error with payment method nonce", 'warning')
        return redirect(url_for('users.show'))

    image = Photos.get_or_none(Photos.id == photo_id)

    if not image:
        flash(f"Could not find image with provided ID", 'warning')
        return redirect(url_for('users.show'))

    amount = request.form.get("amount")

    if not amount:
        flash(f"No donation provided", 'warning')
        return redirect(url_for('users.show'))

    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "options": {
            "submit_for_settlement": True
        }



    })

    if not result.is_success:
        flash('Unable to complete transaction', 'warning')

        return redirect(request.referrer)

    donation = Donation(amount=amount, photo_id=photo_id,
                        user_id=current_user.id)

    if not donation.save():
        flash('Dono successful but error recording', 'warning')
        return redirect(url_for('users.show'))

    flash('Successfully donation')
    return redirect(url_for('users.show'))

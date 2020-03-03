from flask import Flask, redirect, url_for, escape, request, Blueprint, render_template, request, flash
from models.userimages import UserImage
from models.user import User
from flask_login import login_required, current_user
from instagram_web.util.bthelper import gateway
from instagram_web.util.mailhelper import send_simple_message
from models.donation import Donation
import requests
import os

donations_blueprint = Blueprint('donations',
                                __name__,
                                template_folder='templates')


@donations_blueprint.route('/<image_id>/new', methods=["GET"])
@login_required
def new(image_id):
    image = UserImage.get_or_none(UserImage.id == image_id)

    if not image:
        flash(f"No Image was found with the provided ID")
        return redirect(url_for('users.index'))

# BELOW TAKEN FROM  from instagram_web.util.bthelper import gateway
    client_token = gateway.client_token.generate()
    # breakpoint()

    if not client_token:
        flash(f"Unable to obtain client token")
        return redirect(url_for('users.index'))

    return render_template('donations/new.html', image=image, client_token=client_token)


@donations_blueprint.route('/<image_id>', methods=["POST"])
@login_required
def create(image_id):
    nonce = request.form.get('payment_method_nonce')

    if not nonce:
        flash(f"Error with payment method nonce", 'warning')
        return redirect(url_for('users.index'))

    image = UserImage.get_or_none(UserImage.id == image_id)

    if not image:
        flash(f"Could not find image with provided ID", 'warning')
        return redirect(url_for('users.index'))

    amount = request.form.get("amount")

    if not amount:
        flash(f"No donation provided", "warning")
        return redirect(url_for('users.index'))

    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "options": {
            "submit_for_settlement": True
        }
    })

    if not result.is_success:
        flash(
            f"Error in gateway transaction", "warning")
        return redirect(request.referrer)

    donation = Donation(amount=amount, image_id=image.id,
                        user_id=current_user.id)
    #    ---- GET DONATOR NAME AND PASS TO EMAIL------
    donator = User.get_or_none(User.id == current_user.id)

    if not donation.save():
        flash(f"Donated succesfully but error creating a record in database", 'warning')
        return redirect(url_for('users.index'))

    flash(f"Donated: ${amount}", 'sucess')
    send_simple_message(amount=amount, name=donator.name)
    return redirect(url_for('users.index'))

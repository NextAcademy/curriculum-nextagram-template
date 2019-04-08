from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.user import User
from models.image import Image
from werkzeug.security import generate_password_hash
from flask_login import current_user
from werkzeug.utils import secure_filename
from instagram_web import gateway, generate_client_token, find_transaction, transact, TRANSACTION_SUCCESS_STATUSES
import re
import datetime
import os

checkout_blueprint = Blueprint('checkout',
                            __name__,
                            template_folder='templates')

# @checkout_blueprint.route('/payment', methods=['GET'])
# def payment():
#     ct = generate_client_token()
    

#     return render_template('checkout/payment.html', ct= ct)

@checkout_blueprint.route('/', methods=['GET'])
def index():
    return redirect(url_for('new_checkout'))

@checkout_blueprint.route('/new', methods=['GET'])
def new_checkout():
    client_token = generate_client_token()
    return render_template('checkout/new.html', client_token=client_token)

@checkout_blueprint.route('/<transaction_id>', methods=['GET'])
def show_checkout(transaction_id):
    transaction = find_transaction(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
        }
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
        }

    return render_template('checkout/show.html', transaction=transaction, result=result)

@checkout_blueprint.route('/checkout', methods=['POST'])
def create_checkout():
    result = transact({
        'amount': request.form['amount'],
        'payment_method_nonce': request.form['payment_method_nonce'],
        'options': {
            "submit_for_settlement": True
        }
    })

    if result.is_success or result.transaction:
        return redirect(url_for('checkout.show_checkout', transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('checkout.new_checkout'))
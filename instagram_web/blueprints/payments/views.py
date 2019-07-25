import os
from flask import Blueprint, render_template, request, redirect, url_for, session, escape, flash
from flask_login import current_user
from models.donation import Donation
from models.image import Image
from models.image import User
from instagram_web.util.braintree_helper import gateway
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


payments_blueprint = Blueprint('payments',
                            __name__,
                            template_folder='templates')


@payments_blueprint.route('/new/<id>', methods=['GET'])
def new(id):
    if not current_user.is_authenticated:
        flash("You are not logged in", "info")
        return redirect(url_for('sessions.new'))
    else:
        image = Image.get_by_id(id)
        token = gateway.client_token.generate()
        return render_template('payments/new.html', token=token, image=image)


@payments_blueprint.route('/payment', methods=['POST'])
def payment():
    image = Image.get_by_id(request.form.get('image'))
    user = User.get_by_id(image.user_id)
    amount = request.form.get('amount')
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": request.form.get('payment_method_nonce'),
        "options":{
            "submit_for_settlement": True
        }
    })
    message = Mail(
        from_email='keckkyle@gmail.com',
        to_emails='keckkyle@gmail.com',
        subject=f'{current_user.username} has donated to your photo',
        html_content=f'<strong>Congratulations!</strong><br>{current_user.username} has donated ${amount} to your photo. />')

    if result.is_success:
        donation = Donation(amount=amount, user_id=current_user.id, image_id=image.id)
        donation.save()
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            sg.send(message)
            flash(f"Thank you for your donation", 'success')
        except Exception as e:
            flash(f"Thank you for your donation - email failure", "info")
            flash(e, "danger")
        return redirect(url_for('images.show', id=image.id))
    else:
        flash("Payment fail", "danger")
        return redirect(url_for('payments.new', id=image.id))


@payments_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass    
    


@payments_blueprint.route('/', methods=["GET"])
def index():
    pass


@payments_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@payments_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass




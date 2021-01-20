from flask import Blueprint, flash, render_template,request,redirect,url_for,abort
from models.image import Image
from flask_login import login_required,current_user
from werkzeug.utils import secure_filename

import boto3, botocore
from config import S3_KEY, S3_SECRET, S3_BUCKET,S3_LOCATION

# -------------------- Day 5 - Payment & email -------------------- 
import braintree
import os
import peewee as pw
import requests
# from money.money import Money
# from money.currency import Currency
from decimal import *

from models.user import User
from werkzeug.security import check_password_hash
# -------------------- ---- End -------------------- 

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')

@images_blueprint.route('upload', methods=["GET"])
@login_required
def upload():
    return render_template('images/upload.html')

@images_blueprint.route('<int:id>/upload', methods=["POST"])
@login_required
def upload_to_s3(id):
    if id!=current_user.id:
        abort(403)

    s3 = boto3.client(
        's3',
        aws_access_key_id=S3_KEY,
        aws_secret_access_key=S3_SECRET
    )

    file = request.files["user_image"]
    image_path= current_user.name + "/images/user-images/"+ file.filename

    s3.upload_fileobj(
        file,
        S3_BUCKET,
        image_path,
        ExtraArgs={
            "ACL": "public-read",
            "ContentType": file.content_type
        }
    )
    file_loc = S3_LOCATION + image_path
    flash('Image uploaded successfully.')

    # create image instance and save to database
    image=Image(
        url=image_path,
        user=id
    )

    if image.save():
        flash("Image saved to database")
    else:
        flash("Unable to save image to database")
    return render_template('images/upload.html')


# -------------------- Day 5 - Payment -------------------- 
gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.getenv('BRAINTREE_MERCHANT_ID'),
        public_key=os.getenv('BRAINTREE_PUBLIC_KEY'),
        private_key=os.getenv('BRAINTREE_PRIVATE_KEY')
    )
)

@images_blueprint.route("<int:id>/payment-page-1",methods=["GET"])
@login_required
def new_payment(id):
    image_list = pw.prefetch(Image.select().where(Image.id==id),User)

    for image in image_list:
        owner=image.user.name
        image=image

    return render_template('images/payment.html',owner=owner,image=image,S3_LOCATION=S3_LOCATION)


@images_blueprint.route('<int:id>/payment-page-2', methods=["POST"])
@login_required
def braintree_payment(id):
    user=current_user
    donation = request.form['donation_amt']
    password = request.form['password']

    # Verify donor
    match = check_password_hash(user.password,password)
    if not match:
        flash('Incorrect password. Please try again.')
        return redirect(url_for('images.new_payment',id=id))

    token=gateway.client_token.generate()
    return render_template('images/bt-payment.html',token=token,donation=donation)


@images_blueprint.route("/payment/submit",methods=["POST"])
@login_required
def make_payment():
    nonce = request.form['nonce']

    # donation formatting for transaction
    donation = request.form['donation_amt']
    amount=''
    for char in donation[0:-1]:
        amount +=str(char)

    # Transaction
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "options": {
            "submit_for_settlement": True
        }
    })

    if result.is_success:
        flash('Donation received. Thank you.')
        send_simple_message(amount)


    else:
        for error in result.errors.deep_errors:
            flash(str(error.message))
        flash('Payment not successful. Please try again')
    return redirect(url_for('home'))

# -------------------- Day 5 Email -------------------- 

def send_simple_message(amount):
    # import mailgun keys
    domain = os.getenv('MAILGUN_DOMAIN_NAME')
    api = os.getenv('MAILGUN_API')


    return requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api",f"{api}"),
        data={
            "from": f"Excited User <mailgun@{domain}>",
            "to": ["tanjoanne128@gmail.com"],
            "subject": "Thank you for your donation",
            "text": f"Thank you for your donation of {amount}$! Love @NextAcademy"
        }
    )
# -------------------- Day 5 End -------------------- 
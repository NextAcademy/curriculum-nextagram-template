from flask import Blueprint, flash, render_template,request,redirect,url_for,abort
from models.image import Image
from flask_login import login_required,current_user
from werkzeug.utils import secure_filename

import boto3, botocore
from config import S3_KEY, S3_SECRET, S3_BUCKET,S3_LOCATION

# -------------------- Day 5 - Payment -------------------- 
import braintree
import os
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
gateway=braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.getenv('BRAINTREE_MERCHANT_ID'),
        public_key=os.getenv('BRAINTREE_PUBLIC_KEY'),
        private_key=os.getenv('BRAINTREE_PRIVATE_KEY')
    )
)

@images_blueprint.route("/payment",methods=["GET"])
@login_required
def new_payment():
    # customer_id=current_user.id
    token=gateway.client_token.generate()
    return render_template('images/payment.html',token=token)

@images_blueprint.route("/payment/submit",methods=["POST"])
def make_payment():
    nonce = request.form['nonce']

    # Test payment
    result = gateway.transaction.sale({
        "amount": "10.00",
        "payment_method_nonce": nonce,
        "options": {
            "submit_for_settlement": True
        }
    })

    if result.is_success:
        flash('Payment received')
        return redirect(url_for('home'))
    else:
        flash('Pyament not received. Please try again')
        return redirect(url_for('new_payment'))


# -------------------- ---- End -------------------- 

import peeweedbevolve
from app import app
from flask import render_template, request, url_for, redirect, flash, session, Flask
from flask_login import LoginManager,  login_user, current_user, logout_user
from instagram_web.blueprints.users.views import users_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from models.user import User, Images, Follows
from werkzeug.security import generate_password_hash, check_password_hash
from models.helpers import gateway
import braintree
from instagram_web.util.google_oauth import oauth
import config
from instagram_web.blueprints.login.view import login_blueprint
from instagram_web.blueprints.signup.view import signup_blueprint
from instagram_web.blueprints.home.view import home_blueprint
from instagram_web.blueprints.my_profile.view import myprofile_blueprint
from instagram_web.blueprints.other_profile.view import otherprofile_blueprint

# import boto3, botocore
import os

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(login_blueprint, url_prefix='/login')
app.register_blueprint(signup_blueprint, url_prefix='/signup')
app.register_blueprint(home_blueprint, url_prefix='/home')
app.register_blueprint(myprofile_blueprint, url_prefix='/my_profile')
app.register_blueprint(otherprofile_blueprint,url_prefix='/other_profile')

# # Login manager
# login_manager = LoginManager()
# login_manager.init_app(app)


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# user profile page
@app.route("/userpage", methods=["GET"])
def main_userpage():
    # user = User.get_by_id(user_id)
    return render_template("user_profile.html")

# feed wall
# @app.route("/feed", methods=["GET"])
# def home():
#     if (current_user.is_authenticated):
#         feed_images = Images.select().where(Images.user.in_(current_user.following())).order_by(Images.created_at.desc())
#         return render_template('home.html', feed_images = feed_images)
#     else:
#         return f'not login'

# @app.route("/signup", methods=["GET"])
# def signup():
#     return render_template("signup.html")


# @app.route("/signup", methods=["POST"])
# def create_signup():
#     username = request.form.get('username') 
#     password=request.form.get('password') 
#     email=request.form.get('email')
#     hashed_password = generate_password_hash(password)

#     name = User(
#         username = username,
#         email = email,
#         password = hashed_password
#     )
    
#     if name.save():
#         flash(f'Welcome {username}')
#         # session["user_id"] = user.id

#     # hashed_password = generate_password_hash(request.form.get('password'))
#     # name = User(username=request.form.get('username'), password=request.form.get(
#     #     'password'), email=request.form.get('email'))

#     name.save()
#     return redirect(url_for('signup'))


# @app.route("/signin")
# def signin():
#     return render_template("signin.html")

# Method to Login 1 :: Authenticate password and Session Login 
# @app.route("/signin", methods=["POST"])
# def signin():
#     username  = request.form['username']
#     password = request.form['password']
#     user = User.get_or_none(User.username == username)
#     if user and check_password_hash(user.password, password):
#         session["user_id"] = user.id
#     else:
#         flash('Either username or password is incorrect')
#     return redirect(url_for("signin"))

# # Method to Login 2 :: Login Manager
# # This callback is used to reload the user object from the user ID stored in the session
# @app.route("/userpage", methods=["GET"])
# def main_userpage():
#     # user = User.get_by_id(user_id)
#     return render_template("userpage.html")

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get_or_none(User.id == user_id)

# @app.route("/signin", methods=['POST', 'GET'])
# def signin():
#     # breakpoint()
#         username = request.form.get('username')
#         password_to_check = request.form.get('password')

#         user = User.get_or_none(User.username == username)

#         if not user:
#             flash('There is no one with that Username. Please check')
#             return render_template('signin.html')

#         hashed_password = user.password

#         if not check_password_hash(hashed_password, password_to_check):
#             flash('Incorrect password. Please try again.')
#             return render_template('signin.html')

#         login_user(user)
#         # flash(f"Welcome back {user.username}!")
#         return render_template('userpage.html')

# def page_not_found(e):
#   return render_template('404.html'), 404

# def create_app(config_filename):
#     app = Flask(__name__)
#     app.register_error_handler(404, page_not_found)
#     return app

@app.route("/logout", methods=["POST", "GET"])
def logout():
    # breakpoint()
    session.clear()
    if logout_user():
        # return redirect(url_for("home.index"))
        return render_template("signin.html")
    else:
        return redirect(url_for("home.index"))


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

# # edit username
@app.route("/userpage", methods=["POST", "GET"])
def edit_username():

    current_user.username = request.form.get("name")
    current_user.save()

    # return redirect(url_for('home'))
    return render_template('userpage.html')
    # key = os.environ.get('')

from models.helpers import upload_file_to_s3

# logic to send the file from the user’s computer directly to the bucket
@app.route("/profile_img", methods=["POST", "GET"])
def upload_file():
    
    # A
    if "user_file" not in request.files:
        return "No user_file key in request.files"

	# B
    file    = request.files["user_file"]

    """
        These attributes are also available

        file.filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype

    """

	# C.
    if file.filename == "":
        return "Please select a file"

	# D.
    if file:
        # file.filename = secure_filename(file.filename)
        output   	  = upload_file_to_s3(file, "hipster-bucket", acl="public-read")
        # return str(output)
        # breakpoint()
        current_user.picture = file.filename
        # breakpoint()
        current_user.save()
        return render_template('my_profile.html')

    else:
        return render_template('my_profile.html')

@app.route("/post_img", methods=["POST", "GET"])
def upload_postfile():

    # A
    if "user_file" not in request.files:
        return "No user_file key in request.files"

	# B
    file    = request.files["user_file"]

    """
        These attributes are also available

        file.filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype

    """

	# C.
    if file.filename == "":
        return "Please select a file"

	# D.
    if file:
        # file.filename = secure_filename(file.filename)
        # breakpoint()
        output   	  = upload_file_to_s3(file, "hipster-bucket", acl="public-read")
        # return str(output)
        # breakpoint()
        new_image = Images(user = current_user.id, image_url = file.filename)
        # breakpoint()
        new_image.save()
        return render_template('my_profile.html')

    else:
        return render_template('my_profile.html')

# ##test to upload to s3 bucket here
#let python turn into s3 and become user code
    # user_pic = request.files['user_file']
    # s3 = boto3.client(
    #     "s3",
    #     aws_access_key_id="AKIAWVM2KK4WA2CQDU64",
    #     aws_secret_access_key="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"
    # )
    # #uploading the pictures
    # s3.upload_fileobj(
    #     user_pic,
    #     "my-bucket-now",
    #     user_pic.filename,
    #     ExtraArgs={
    #         "ACL": 'public-read',
    #         "ContentType": user_pic.content_type
    #     }
    # )
    # # breakpoint()
    # # return redirect(url_for('home'))
    # return '{}{}'.format(os.environ.get("S3_LOCATION"), user_pic.filename)

# view other person profile page
# @app.route("/other_user/<username>", methods=["GET"])
# def view_othersProfile(username):
#     u = User.get_or_none(User.username == username)

#     return render_template("others_profile.html", user = u)


# @app.route("/other_user/<username>", methods=["POST"])
# def follow(username):
#     # breakpoint()
#     x = User.get_or_none(User.username == username)
#     # my_idols = User.select().join(Follows, on=(User.id == Follows.myidol_id)).where(Follows.myfan_id == current_user.id)

#     follow = Follows(myfan_id = current_user.id, myidol_id= x.id)
#     follow.save()
#     return redirect(url_for('others_profile'))
#     # return render_template("others_profile.html")


@app.route("/image/payment", methods=["GET"])
def donate():
   #generate token 
    client_token = gateway.client_token.generate()

    # return redirect(url_for('donate'))
    return render_template('donate.html', client_token = client_token)

TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

#gateway.transaction.find - 
@app.route('/checkouts/<transaction_id>', methods=['GET'])
def show_checkout(transaction_id):
    transaction = gateway.transaction.find(transaction_id)
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

    return render_template('showTransaction.html', transaction=transaction, result=result)

#gateway.transaction.sale - create transaction
@app.route("/image/checkout", methods=["POST"])
def checkout():
    result = gateway.transaction.sale({
        'amount': request.form['amount'],
        'payment_method_nonce': request.form['payment_method_nonce'],
        'options': {
            "submit_for_settlement": True
        }
    })

    if result.is_success or result.transaction:
        return redirect(url_for('show_checkout',transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('donate'))

oauth.init_app(app)

# google authorize login
@app.route('/google', methods=["GET"])
def authorize():
   token = oauth.google.authorize_access_token()

   if token:
       
       email = oauth.google.get(
           'https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
       user = User.get_or_none(User.email == email)
       if not user:
        # Add user into table
        # user = User(email= email, username= email, password="asdoiqwndoaisaoidjwoaw")
        # login user
           flash('Not registered to Google.')
           return redirect(url_for('signup'))
            #  return f'not a google user'
       else:
        #    login user
           flash(f'Welcome back to Nextagram {user.username}.')
           return redirect(url_for('google_login '))
            #  return f'a google user'

          

 
@app.route('/google_login', methods=["GET"])
def google_login():
   redirect_url = url_for('authorize', _external=True)
   return oauth.google.authorize_redirect(redirect_url)
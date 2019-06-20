import peeweedbevolve
from app import app
from flask import render_template, request, url_for, redirect, flash, session, Flask
from flask_login import LoginManager,  login_user, current_user
from instagram_web.blueprints.users.views import users_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
# from helpers import *
# import boto3, botocore
import os

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/", methods=["GET"])
def home():
    return render_template('home.html')


@app.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def create_signup():
    username = request.form.get('username') 
    password=request.form.get('password') 
    email=request.form.get('email')
    hashed_password = generate_password_hash(password)

    name = User(
        username = username,
        email = email,
        password = hashed_password
    )
    
    if name.save():
        flash(f'Welcome {username}')
        # session["user_id"] = user.id

    # hashed_password = generate_password_hash(request.form.get('password'))
    # name = User(username=request.form.get('username'), password=request.form.get(
    #     'password'), email=request.form.get('email'))

    name.save()
    return redirect(url_for('signup'))


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

# Method to Login 2 :: Login Manager
# This callback is used to reload the user object from the user ID stored in the session
@app.route("/userpage", methods=["GET"])
def main_userpage():
    # user = User.get_by_id(user_id)
    return render_template("userpage.html")

@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == user_id)

@app.route("/signin", methods=['POST', 'GET'])
def signin():
    # breakpoint()
        username = request.form.get('username')
        password_to_check = request.form.get('password')

        user = User.get_or_none(User.username == username)

        if not user:
            flash('There is no one with that Username. Please check')
            return render_template('signin.html')

        hashed_password = user.password

        if not check_password_hash(hashed_password, password_to_check):
            flash('Incorrect password. Please try again.')
            return render_template('signin.html')

        login_user(user)
        # flash(f"Welcome back {user.username}!")
        return render_template('userpage.html')

# def page_not_found(e):
#   return render_template('404.html'), 404

# def create_app(config_filename):
#     app = Flask(__name__)
#     app.register_error_handler(404, page_not_found)
#     return app

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
@app.route("/profile_img", methods=["POST"])
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
        output   	  = upload_file_to_s3(file, "my-bucket-now", acl="public-read")
        # return str(output)
        current_user.picture = request.form.get("picture")
        current_user.save()
        return redirect(url_for('userpage'))

    else:
        return redirect(url_for('home'))

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

# #POST profile picture to database
# @app.route("/profile_img", methods=["POST"])
# def profile_image():

#     #  picture = request.form.get("picture")
#     #  y = User(picture = picture)
#     #  y.save()
#     #  breakpoint() 

#     # upload to s3

   

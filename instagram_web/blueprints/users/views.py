from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.user import User
from werkzeug.security import generate_password_hash
from flask_login import current_user
from instagram_web.helpers.helpers import upload_file_to_s3, allowed_file
from werkzeug.utils import secure_filename
import re
from app import app
import datetime


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates/users')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    name = request.form['name']
    password = generate_password_hash(request.form['password'])
    email = request.form['email']
    username = request.form['username']
    user = User(name=name, password=password, email=email, username=username)
    if user.save():
        # Flash a message
        flash("Successfully created a user", "success")
        return redirect(url_for('home'))
    else:
        #Flash a error message
        # flash("Incorrect fields. Please try again.", "danger")
        # redirect back to this page (so they can fill in form again)
        return render_template('new.html', errors=user.errors)
    

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    user = User.get_by_id(id)
    return render_template('edit.html', id=current_user.id, user=user)


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_by_id(id)

    name = request.form.get('name')
    username = request.form.get('username')
    email = request.form.get('email')
    
    if current_user == user:
        if name:
            user.name = name
        if email:
            user.email = email
        if username:
            user.username = username

        if user.save():
            flash("Successfully updated user information.", "success")
            return redirect(url_for('home'))
        else:
            flash("Failed to update user information.", "danger")
            return redirect(url_for('edit', id=current_user.id))
    
    if user.update(recursive=True):
        flash("", "success")
        return redirect(url_for('store_list'))
    else:
        return redirect(url_for('edit', user = user))


# UPLOAD USER PIC Method

@users_blueprint.route('/<id>/upload', methods=['GET'])
def show_upload(id):    
    return render_template('uploadprofile.html')

@users_blueprint.route('/<id>/upload', methods=['POST'])
def upload(id):    
    user = User.get_by_id(id)
    if "user_file" not in request.files:
        flash("Please select a file to upload", "danger")

    file = request.files["user_file"]

    if file.filename == "":
        flash("Please choose a file that has a name", "danger")

    if file and allowed_file(file.filename):
        file.filename = secure_filename(str(id) + "_" + file.filename + str(datetime.datetime.now()))
        output = upload_file_to_s3(file, app.config["S3_BUCKET"])
        user.profile_image_path = output
        user.save()
        flash("Successfully uploaded profile image", "success")
        return redirect(url_for('home'))

    else:
        return redirect(url_for('home'))


# Profile page for current user
@users_blueprint.route('/<id>/profile', methods=['GET'])
def view_profile(id):
    user = User.get(User.id == id)

    
    username = request.form.get('username')
    email = request.form.get('email')
    name = request.form.get('name')

    if current_user == user:
        if name:
            user.name = name
        if email:
            user.email = email
        if username:
            user.username = username
    return render_template('profile.html',user = user)


# Direct users to the wall (All the users images)

@users_blueprint.route('/<id>/wall', methods=['GET'])
def view_wall(id):
    user = User.get(User.id == id)

    return render_template('wall.html',user = user)

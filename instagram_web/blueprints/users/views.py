from flask import Flask, Blueprint, render_template, request, flash, url_for, redirect
from models.user import User
from flask_login import current_user
from werkzeug.utils import secure_filename
from s3_uploader import upload_file_to_s3
from config import Config
from models.images import Image
from config import Config

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    user = User(username=username, email=email, password=password)
    if user.save():
        flash(f"Saved user: {user.username}")
        return redirect(url_for("users.new"))
    else:
        flash(f"Some error!")
        return render_template('users/new.html', errors=user.errors)


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    current_user.username = username
    if current_user.is_authenticated:
        return redirect(url_for('users.edit'))
    if not current_user.is_authenticated:
        return render_template('401.html'), 401


@users_blueprint.route('/', methods=["GET"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if not current_user.is_authenticated:
        return render_template('401.html'), 401


@users_blueprint.route('/edit', methods=["GET"])
def edit():
    return render_template('users/userpage.html')


@users_blueprint.route('/<id>/profile', methods=['GET'])
def profile(id):
    user = User.get(User.id == id)
    image_list = Image.select().where(Image.user_id == user.id)
    return render_template('users/profilepage.html',  image_list=image_list)


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_or_none(username=current_user.username)
    new_username = request.form.get("username")
    if new_username:
        user.username = new_username
    new_email = request.form.get("email")
    if new_email:
        user.email = new_email
    if user.save():
        flash("Saved!")
        return redirect(url_for("home"))
    else:
        return "error"


@users_blueprint.route('/upload', methods=['POST'])
def upload():
    # if not 'profile_image' in request.files:
    #     flash('No image has been provided', 'warning')
    #     return redirect(url_for('profile', id=current_user.id))

    file = request.files.get('user_file')

    if file:
        if not upload_file_to_s3(file):
            file.filename = secure_filename(file.filename)
            flash('Something wrong', 'warning')
            return redirect(url_for('users.profile', id=current_user.id))

        user = User.get_or_none(User.id == current_user.id)

        user.profile_image = file.filename

        user.save()
    else:
        flash("file can't be uploaded", 'warning')
        return redirect(url_for('users.profile', id=current_user.id))

    flash('Successfully updated')
    return redirect(url_for('home'))

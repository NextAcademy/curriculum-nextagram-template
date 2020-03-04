from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from models.user_images import Image
from werkzeug.security import generate_password_hash, check_password_hash
import re
import datetime
from flask_login import current_user, login_user, login_required
from werkzeug.utils import secure_filename
from helpers import upload_file_to_s3
from config import S3_BUCKET, S3_LOCATION


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/create', methods=['POST'])
def create():
    em = request.form.get('email')
    us = request.form.get('username')
    pa = request.form.get('password')

    if len(pa) > 6:
        if re.search(r'[A-Z]', pa) and re.search(r'[a-z]', pa) and re.search(r'\W', pa):
            hashed_pa = generate_password_hash(pa)
            new_user = User(email=em, username=us, password=hashed_pa)

            if new_user.save():
                login_user(new_user)
                return redirect(url_for('users.index'))
            else:
                return render_template('users/new.html', errors=new_user.errors)
        else:
            return render_template('users/new.html', errors='The password requires uppercase, lowercase and at least one special character')

    else:
        return render_template('users/new.html', errors='That password is too short!')


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get(User.username == username)
    image_list = Image.select().where(
        Image.user_id == user.id)
    return render_template("users/profile.html", username=username, user=user, image_list=image_list)


@users_blueprint.route('/', methods=["GET"])
def index():
    if current_user.is_authenticated:
        images = Image.select(Image, User).join(
            User).where(Image.user_id != current_user.id)
        return render_template('users/index.html', images=images)
    else:
        images = Image.select()
        return render_template('users/index.html', images=images)


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    if id == str(current_user.id):
        return render_template('users/edit.html')
    else:
        return "soz, but no access for u"


@users_blueprint.route('/<id>/update', methods=['POST'])
def update(id):
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.get_by_id(id)
    user.email = email
    user.username = username
    if len(password) > 0:
        if len(password) > 6:
            if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and re.search(r'\W', password):
                hashed_pass = generate_password_hash(password)
                user.password = hashed_pass
            else:
                return render_template('users/edit.html', errors='The password requires uppercase, lowercase and at least one special character')
        else:
            return render_template('users/edit.html', errors='That password is too short!')

    if user.save():
        flash('Updated successfully!')
        return redirect(url_for('users.edit', id=current_user.id))

    else:
        flash('failwhale')
        return render_template('users/edit.html')


@users_blueprint.route('/<id>/upload', methods=['POST'])
def upload(id):
    if "user_file" not in request.files:
        flash("No file was chosen! :O")
        return redirect(url_for('users.edit', id=id))
    file = request.files.get('user_file')
    file_name = secure_filename(file.filename)
    if file_name != '':
        user = User.get_by_id(current_user.id)
        error = str(upload_file_to_s3(file, S3_BUCKET))

        user.image = S3_LOCATION + file_name
        if user.save():
            return redirect(url_for('users.edit', id=id))
        else:
            return render_template('users/index.html', error=error)
    else:
        flash('File has no name!')
        return redirect(url_for('users.edit'))

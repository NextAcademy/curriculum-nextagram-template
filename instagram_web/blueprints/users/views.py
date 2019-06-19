from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_user
from instagram_web.util.helpers import upload_file_to_s3
from app import app

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/new', methods=['POST'])
def create():
    if len(request.form['password']) < 8:
        flash('Password too short!')
        return render_template('users/new.html', username=request.form['username'], email=request.form['email'])
    u = User(username = request.form['username'], email = request.form['email'], password = generate_password_hash(request.form['password']))
    if u.save():
        flash('New user created')
        login_user(u)
        return redirect(url_for('users.new'))
    else:
        return render_template('users/new.html', username=request.form['username'], email=request.form['email'])

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get_or_none(User.username == username)
    return render_template('users/profile.html', user = user)

@users_blueprint.route('/profile', methods=["GET"])
def own_profile():
    return render_template('users/profile.html', user = current_user)

@users_blueprint.route('/', methods=['POST'])
def signin():
        email = request.form['email']
        password = request.form['password']
        u = User.get_or_none(User.email == email)
        if u != None:
                flash(f'User found {u.username}')
                if check_password_hash(u.password, password):
                        flash('Password is a match!')
                        login_user(u)
                        return redirect(url_for('index'))
                else:
                        flash('But wrong password')
                        return render_template('home.html', email=request.form['email'])
        else:
                flash('No such user')
                return redirect(url_for('index'))
                


@users_blueprint.route('/', methods=["GET"])
def index():
    return render_template('home.html') #could be explore users though?


@users_blueprint.route('/edit', methods=['GET'])
def edit():
    return render_template('users/update.html')


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_or_none(User.id == current_user.id)
    if current_user.id==int(id) and check_password_hash(current_user.password, request.form['password_verification']):
        if request.form['email'] != '':
            user.email = request.form['email']
            flash('Email successfully changed')
        if request.form['username'] != '':
            user.username = request.form['username']
            flash('Username successfully changed')
        if request.form['password'] != '':
            user.password = generate_password_hash(request.form['password'])
            flash('Password successfully changed')
        user.save()
    else:
        flash('Incorrect password')
        return redirect(url_for('users.edit'))
    return redirect(url_for('users.own_profile'))

@users_blueprint.route('/profileimage', methods=['GET'])
def dp_edit():
    return render_template('users/avatarform.html')

@users_blueprint.route('/profileimage', methods=['POST'])
def dp_update():
    if "user_file" not in request.files:
        return "No user_file key in request.files"

    file = request.files["user_file"]

    if file.filename == "":
        return "Please select a file"

	# D.
    if file and current_user.is_authenticated:
    # if file and allowed_file(file.filename):
        # file.filename = secure_filename(file.filename)
        filename = "profile." + file.filename.rsplit('.', 1)[1]
        # output = upload_file_to_s3(file, app.config["S3_BUCKET"], filename=str(current_user.id)+'/'+filename)
        upload_file_to_s3(file, app.config["S3_BUCKET"], filename=str(current_user.id)+'/'+filename)
        current_user.profile_pic = filename
        current_user.save()
        return redirect(url_for('home'))
        #http://my-bucket-now.s3.amazonaws.com/Screenshot_168.png

    else:
        return redirect("/")

#this method is better off with a checkbox
# @users_blueprint.route('/update_privacy', methods=['POST'])
# def toggle_privacy():
#     if is_private:
#         current_user.is_private=False
#     else:
#         current_user.is_private=True
#     current_user.save()
#     return redirect("url_for('show', username = current_user.username)")

@users_blueprint.route('/make_public', methods=['POST'])
def make_public():
    current_user.is_private=False
    current_user.save()
    return redirect(url_for('users.own_profile'))

@users_blueprint.route('/make_private', methods=['POST'])
def make_private():
    current_user.is_private=True
    current_user.save()
    return redirect(url_for('users.own_profile'))
from flask import Blueprint, render_template, request, redirect, url_for, session, escape, flash
from flask_login import current_user, login_user
from models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from instagram_web.util.helpers import allowed_file, upload_file_to_s3


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    user = User(first_name = first_name, last_name = last_name, email = email, username = username, password = password)

    if user.save():
        login_user(user)
        flash("logged in", "success")
        return redirect(url_for('index'))
    else:
        for error in user.errors:
            flash(error, 'warning')
        return render_template('users/new.html')


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    if not current_user.is_authenticated:
        flash("You are not logged in", "info")
        return redirect(url_for('sessions.new'))
    else:
        user = User.get(User.username == username)
        return render_template('users/show.html', user = user)


@users_blueprint.route('/', methods=["GET"])
def index():
    pass


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    if not current_user.is_authenticated:
        return redirect(url_for('sessions.new'))
    else:
        user = User.get_by_id(id)
        if current_user == user:
            return render_template('users/edit.html', user=user)
        else:
            return redirect(url_for('index'))


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    new_password = request.form.get('new_password')
    old_password = request.form.get('old_password')

    update_user = User.get_by_id(id)
    check_password = check_password_hash(update_user.password, old_password)

    if not check_password:
        flash("Incorrect password", "warning")
        return redirect(url_for('users.edit', id=id))
    else:
        hashed_password = generate_password_hash(new_password)
        update_query = User.update(first_name=first_name, last_name = last_name, email = email, password = hashed_password).where(User.id == id)
        update_query.execute()
        return redirect(url_for('users.edit', id=id))





@users_blueprint.route('/<id>/profilephoto', methods=['POST'])
def upload_file(id):

    if 'user_file' not in request.files:
        return "No user_file key in request.files"
    
    file = request.files["user_file"]

    if file.filename == "":
        return "Please select a file"

    if file and allowed_file(file.filename):
        user = User.update(photo=file.filename).where(User.id == id)
        user.execute()
        upload_file_to_s3(file)
        return redirect(url_for('users.show', username = current_user.username))
    
    else: 
        return redirect(url_for('users.edit', id=id))
import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, escape, flash
from flask_login import current_user, login_user
from models.user import User
from models.fan_idol import FanIdol
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
        approved = FanIdol.get_or_none(FanIdol.fan==current_user.id,FanIdol.idol==user.id,FanIdol.approved==True)
        return render_template('users/show.html', user = user,approved=approved)


@users_blueprint.route('/', methods=["GET"])
def index():
    users = User.select().order_by(User.username.asc())
    text = "All users"
    return render_template('users/users.html', users = users,text=text)


@users_blueprint.route('/search', methods=["POST"])
def search():
    text = request.form.get('search')
    if text == '':
        text = "All users"
        users = User.select().order_by(User.username.asc())
    else:
        search = '%' + text + '%'
        text = "Usernames containing: " + text
        users = User.select().where(User.username ** search)
    
    return render_template('users/users.html', users = users, text = text)


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
    account_type = request.form.get('account_type')

    if new_password == '':
        new_password = old_password

    if account_type == 'private':
        account_type = True
    else:
        account_type = False

    update_user = User.get_by_id(id)
    check_password = check_password_hash(update_user.password, old_password)

    duplicate_email = User.get_or_none(User.email == email)

    if len(old_password) < 6:
        flash('Your password must be provided to make changes', 'danger')
        return redirect(url_for('users.edit', id=id))

    if str(duplicate_email.id) != id:
        flash('Provided email is already in use.', 'danger')
        return redirect(url_for('users.edit', id=id))

    if len(first_name) < 1:
        flash('Please provide a first name', 'warning')
        return redirect(url_for('users.edit', id=id))

    if len(last_name) < 1:
        flash('Please provide a last name', 'warning')
        return redirect(url_for('users.edit', id=id))

    if len(new_password) < 6:
        flash('Please provide a longer password', 'warning')
        return redirect(url_for('users.edit', id=id))

    if not check_password:
        flash("Incorrect password", "danger")
        return redirect(url_for('users.edit', id=id))
    else:
        hashed_password = generate_password_hash(new_password)
        update_query = User.update(first_name=first_name, last_name = last_name, email = email, password = hashed_password, updated_at = datetime.datetime.now(), private=account_type).where(User.id == id)
        update_query.execute()
        flash('User details updated', 'success')
        return redirect(url_for('users.show', username=update_user.username))



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
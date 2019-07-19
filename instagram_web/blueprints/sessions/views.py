from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from werkzeug.security import check_password_hash


sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates/sessions')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template("new.html")


@sessions_blueprint.route('/', methods=['POST'])
def create():
    password = request.form.get('password')
    username = request.form.get('username')
    user = User.get_or_none(User.username == username)
   
    if not user:
        flash("Username does not exist", "warning")
        return redirect(url_for('sessions.new'))
    
    check_password = check_password_hash(user.password, password)

    if not check_password:
        flash("Incorrect password", "warning")
        return redirect(url_for('sessions.new'))

    flash("logged in", "success")
    return redirect(url_for('sessions.new'))

    


@sessions_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@sessions_blueprint.route('/', methods=["GET"])
def index():
    return redirect(url_for('sessions.new'))


@sessions_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@sessions_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass

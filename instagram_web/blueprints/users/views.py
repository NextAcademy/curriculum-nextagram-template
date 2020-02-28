import peeweedbevolve
from flask import Blueprint, flash, Flask, render_template, request, flash, redirect, url_for, session
from models.user import User
from werkzeug.security import generate_password_hash

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/new/create', methods=['POST'])
def create():
    u_name = request.form.get("username")
    p_word = request.form.get("password")
    e_mail = request.form.get("email")

    c_user = User(name=u_name, password=p_word, email=e_mail)

    if c_user.save():
        flash("Sign Up success!")

        return redirect(url_for('users.new'))

    else:

        for error in c_user.errors:
            flash(error)
        return redirect(url_for('users.new'))


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():

    return "USERS"


# @users_blueprint.route('/')
# def login_status():
#     if User.name in session:
#         return 'Logged in as %s' % escape(session[User.name])
#     return 'You are not logged in'


@users_blueprint.route('/login', methods=['POST'])
def login():
    # if request.method == 'POST':
    #     session[User.name] = request.form.get("logUser")
    #     return redirect(url_for('users.login_status'))
    # login = request.form.get("logUser")
    # sessions['logStatus'] = login
    # sessions.modified = True
    pass


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass

from flask import Blueprint, render_template, request # flash, redirect, url_for
from werkzeug.security import generate_password_hash
from models.user import User


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    # COULD USE THE BELOW BUT NOT GOOD PRACTICE AS NOT CONTROLLING WHAT'S PASSED TO THE DB
    # data = request.form.to_dict()
    # new_user = User(data)

    # THE SIMPLE WAY IS SHOWN BELOW
    # name = request.form.get('name')
    # username = request.form.get('username')
    # email = request.form.get('email')
    # password = generate_password_hash(request.form.get('password'))
    
    # AND THIS IS MY CHOSEN METHOD AS IT LOOKS A BIT MORE FANCY :P
    u = request.form
    new_user = User(name=u.get('name'), email=u.get('email'), username=u.get('username'), password=generate_password_hash(u['password']))
    new_user.save()

    return render_template('users/new.html')


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass

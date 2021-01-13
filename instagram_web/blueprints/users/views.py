from flask import Blueprint, flash, render_template,request,redirect,url_for
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
    user = User(
        name=request.form['name'],
        email=request.form['email'],
        password=generate_password_hash(request.form['password']),
        address=request.form['address']
    )

    if user.save():
        flash("User created!")        
    else:
        flash("Unable to create user!")
    return redirect(url_for('users.new'))


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

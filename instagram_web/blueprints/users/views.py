from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.user import User


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates/users')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('startup_form.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    name = request.form['name']
    password = request.form['password']
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
        return render_template('startup_form.html', errors=user.errors)
    


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

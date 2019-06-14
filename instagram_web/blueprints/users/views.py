from flask import Flask, render_template, request,redirect, url_for, Blueprint,flash
from models.user import User

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/new', methods=['POST'])
def create():
    u = User(username = request.form['username'], email = request.form['email'], password = request.form['password'])
    if u.save():
        flash('New user created')
        return redirect(url_for('users.new'))
    else:
        return render_template('users/new.html', username=request.form['username'], email=request.form['email'])

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

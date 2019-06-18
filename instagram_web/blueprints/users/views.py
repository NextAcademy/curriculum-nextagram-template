from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_user

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
    if current_user.id==int(id) and check_password_hash(current_user.password, request.form['password_verification']):
        if request.form['email'] != '':
            current_user.email = request.form['email']
            flash('Email successfully changed')
        if request.form['username'] != '':
            current_user.username = request.form['username']
            flash('Username successfully changed')
        if request.form['password'] != '':
            current_user.password = generate_password_hash(request.form['password'])
            flash('Password successfully changed')
    else:
        flash('Incorrect password')
        return redirect(url_for('users.edit'))
    return render_template('home.html')

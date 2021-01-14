from flask import Blueprint, flash, render_template,request,redirect,url_for,session
from models.user import User
#-----------------------------------------------------------------
from werkzeug.security import check_password_hash
#-----------------------------------------------------------------

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

#-----------------------------------------------------------------
@users_blueprint.route('/login', methods=["GET"])
def login():
    return render_template('users/login.html')

@users_blueprint.route('/auth', methods=["POST"])
def authentication():
    username = request.form['name']
    password = request.form['password']

    try:
        user = User.get(name=username)
    except:
        flash('Username does not exist. Please try again.')
        return redirect(url_for('users.login'))

    db_password = user.password
    match = check_password_hash(db_password,password)

    if match:
        flash("User is logged in!")
        session["username"] = user.name
        return redirect(url_for('home'))
    else:
        flash("Incorrect password. Please try again.")
        return redirect(url_for('users.login'))

#-----------------------------------------------------------------


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    user = User(
        name=request.form['name'],
        email=request.form['email'],
        password=request.form['password']
    )

    if user.save():
        flash("User created!")
        return redirect(url_for('users.new'))
    else:
        flash("Unable to create user!")
        return render_template('users/new.html', errors=user.errors) 


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

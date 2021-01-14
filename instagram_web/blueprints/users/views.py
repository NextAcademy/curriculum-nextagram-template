from flask import Blueprint, flash, render_template,request,redirect,url_for,session
from models.user import User
#-----------------------------------------------------------------
from flask_login import login_user,login_required,logout_user
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
    # username=request.form['name'], password=request.form['password']
    username = request.form['name']
    password = request.form['password']

    try:
        user = User.get(name=username)
    except:
        flash('Username does not exist. Please try again.')
        return redirect(url_for('users.login'))

    login_user(user)
    flash('Logged in successfully.')
    return redirect(url_for('home'))

@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))
#-----------------------------------------------------------------




#------------------------------------------------------------

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

    # ------------ this part is similar to authentication() function---------
    # to see if can implement DRY
    if user.save():
        flash("User created!")
        username = user.name
        try:
            user = User.get(name=username)
        except:
            flash('Username does not exist. Please try again.')
            return redirect(url_for('users.login'))

        login_user(user)
        flash('Logged in successfully.')
    #--------------------------------------------------------------------------
        return redirect(url_for('home'))
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

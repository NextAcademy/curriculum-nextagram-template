from flask import Blueprint, flash, render_template,request,redirect,url_for,session,abort
from models.user import User
#---------------------DAY2--------------------------------------------
from flask_login import login_user,login_required,logout_user,current_user
#-----------------------END------------------------------------------

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

#---------------------DAY2--------------------------------------------
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
#-------------------------END----------------------------------------


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
    #--------------------------- END-----------------------------------------------
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

# ----------- DAY 3 -----------------------------------------------------------
@users_blueprint.route('/<int:id>/edit', methods=['GET'])
@login_required
def edit(id):
    if current_user.id != id:
        abort(403)
    else:
        return render_template('users/edit_user.html',id=id)

# Method for changing email
@users_blueprint.route('/<int:id>/update_email', methods=['POST'])
def update_username(id):
    pass


# ----------- END -------------------------------------------------------------


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass

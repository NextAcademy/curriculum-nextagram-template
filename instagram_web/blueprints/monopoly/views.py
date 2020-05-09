from flask import Blueprint, render_template, request, flash,  redirect, url_for
from models.mon_user import Mon_User


monopoly_blueprint = Blueprint(
    'monpoly', __name__, template_folder='templates')


@monopoly_blueprint.route('/')
def index():
    return render_template('monopoly/index1.html')


@monopoly_blueprint.route('/new')
def new():
    return render_template('monopoly/new.html')


@monopoly_blueprint.route('/create', methods=['POST'])
def create():
    name = request.form.get('username')
    password = request.form.get('password')

    new_user = Mon_User(name=name, password=password)
    if new_user.save():
        flash('success!', 'success')
        return redirect(url_for('monopoly.index'))

    else:
        flash('Did not succeed, try again.', 'danger')
        return render_template('monopoly/new.html')

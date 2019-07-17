from flask import Blueprint, render_template, redirect, url_for, request

sessions_blueprint = Blueprint(
    'sessions', __name__, template_folder='templates/sessions')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('new.html')


@sessions_blueprint.route('/', methods=['POST'])
def create():
    pass

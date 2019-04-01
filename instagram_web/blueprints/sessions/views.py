from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash


sessions_blueprint = Blueprint('sessions', #this blueprint is called sessions
                            __name__,
                            template_folder='templates')

@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')
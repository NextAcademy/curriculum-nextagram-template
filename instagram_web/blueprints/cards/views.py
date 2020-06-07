from flask import request, redirect, url_for, render_template, Blueprint
from models.cards import Card
import json
from flask_socketio import send, emit
from app import socketio
from flask_login import current_user
from models.user import User

cards_blueprint = Blueprint('cards', __name__, template_folder='templates')


@cards_blueprint.route('/new')
def new():
    render_template('cards/new.html')

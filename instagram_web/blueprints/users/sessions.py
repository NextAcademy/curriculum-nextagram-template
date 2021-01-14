from flask import Blueprint, flash, render_template,request,redirect,url_for
from models.user import User

# ---------- Not used at the moment ----------

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


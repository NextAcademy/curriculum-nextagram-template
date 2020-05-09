from flask import Blueprint, render_template, request, redirect, url_for

monopoly_blueprint = Blueprint(
    'monpoly', __name__, template_folder='templates')


@monopoly_blueprint.route('/')
def show():
    return render_template('monopoly/index1.html')

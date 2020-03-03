from flask import Blueprint, render_template, request, redirect, url_for, flash, request


donations_blueprint = Blueprint(
    'donations', __name__, template_folder='templates')


@donations_blueprint.route('/<image_id>/new', methods=['GET'])
def new(image_id):
    return render_template('donations/new.html', image_id=image_id)

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user
from models.user import User
from models.properties import Property
from werkzeug.utils import secure_filename
from config import S3_BUCKET, S3_LOCATION
from helpers import upload_file_to_s3

mon_prop_blueprint = Blueprint(
    'mon_prop', __name__, template_folder='templates')


@mon_prop_blueprint.route('/update')
def update():
    if current_user.username == 'Banker':
        properties = Property.select().order_by(Property.created_at)
        return render_template('mon_prop/update.html', properties=properties)
    else:
        flash('no access 4 u', 'danger')
        return redirect(url_for('monopoly.index'))


@mon_prop_blueprint.route('/edit', methods=['POST'])
def edit():
    if current_user.username == 'Banker':
        prop_name = request.form.get('prop_name')
        prop_price = request.form.get('price_input')
        prop = Property.get_or_none(Property.name == prop_name)
        if not prop:
            flash('no such property', 'danger')
            return redirect(request.referrer)

        prop.price = prop_price
        if prop.save():
            flash('saved successfully', 'success')
        else:
            flash('problem saving', 'warning')
        return redirect(request.referrer)
    else:
        flash('sorry, but you do not have access to this', 'warning')
        return redirect(url_for('monopoly.index'))


@mon_prop_blueprint.route('/new')
def new():
    if current_user.username == 'Banker':
        return render_template('mon_prop/new.html')
    else:
        flash('sorry, but you do not have access to that feature!', 'danger')
        return redirect(url_for('monopoly.index'))


@mon_prop_blueprint.route('/create', methods=['POST'])
def create():
    if current_user.username == 'Banker':
        name = request.form.get('name')
        house_price = request.form.get('house-price')
        category = request.form.get('category')
        if house_price == '':
            house_price = 0

        if "image-file" not in request.files:
            flash("No file was chosen! :O", 'warning')
            return redirect(request.referrer)
        file = request.files.get('image-file')
        file_name = secure_filename(file.filename)
        img_upload_err = str(upload_file_to_s3(file, S3_BUCKET))
        new_prop = Property(name=name, user_id=current_user.id,
                            house_price=house_price, category=category, image=file_name)
        if new_prop.save():
            flash('new property was saved', 'success')
            return redirect(url_for('mon_prop.new'))
        else:
            flash(f'failed, {img_upload_err}', 'danger')
            return redirect(request.referrer)

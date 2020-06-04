from flask import Blueprint, render_template, request, flash,  redirect, url_for
from flask_login import current_user, login_user, login_required
from models.user import User
from models.properties import Property
from models.activity_log import ActivityLog
from werkzeug.utils import secure_filename
from config import S3_BUCKET, S3_LOCATION
from helpers import upload_file_to_s3
from app import socketio
from flask_socketio import send, emit
import json


monopoly_blueprint = Blueprint(
    'monopoly', __name__, template_folder='templates')


def update_activities():
    activities = ActivityLog.select().order_by(
        ActivityLog.created_at.desc())
    activity_text = [x.text for x in activities]
    dictionary = {'activities': activity_text}
    data = json.dumps(dictionary)
    socketio.emit('activity_update', data)


def update_positions():
    users = User.select().where((User.monopoly > 0) & (
        User.username != 'Banker')).order_by(User.created_at.desc())
    user_positions = []
    locations = ['Go', 'Old Kent Road', 'Community Chest', 'Whitechapel Road', 'Income Tax', "King's Cross Station", 'The Angel Islington', 'Chance', 'Euston Road', 'Pentonville Road', 'Jail', 'Pall Mall', 'Electric Company', 'Whitehall', 'Northumberland Ave.', 'Marylebone Station', 'Bow Street', 'Community Chest 2', 'Marlborough Street',
                 'Vine Street', 'Free Parking', 'Strand', 'Chance 2', 'Fleet Street', 'Trafalgar Square', 'Fenchurch St. Station', 'Leicester Square', 'Coventry Street', 'Water Works', 'Piccadilly', 'Go to Jail!', 'Regent Street', 'Oxford Street', 'Community Chest 3', 'Bond Street', 'Liverpool St. Station', 'Chance 3', 'Park Lane', 'Supertax', 'Mayfair']

    for user in users:
        user_positions.append(
            f'{user.username} @ {locations[user.position]} | ${user.money}')
    socketio.emit('position_update', user_positions)


@socketio.on('connect')
def handle_connection():
    update_positions()
    update_activities()


def activity_create(txt):
    new_activity = ActivityLog(text=txt)
    new_activity.save()
    activities = ActivityLog.select()
    if len(activities) > 8:
        new_activities = ActivityLog.select().order_by(
            ActivityLog.created_at.desc()).limit(8)
        old_activities = ActivityLog.select().where(
            ActivityLog.id.not_in([activity.id for activity in new_activities]))
        for old_act in old_activities:
            old_act.delete_instance()
    update_activities()
    emit('money_update', current_user.money)
    update_positions()


def jail_free():
    current_user.jailed = -1
    current_user.doubles = 0
    current_user.save()


@monopoly_blueprint.route('/')
def index():
    if current_user.is_authenticated:
        users = User.select().where((User.monopoly > 0) & (User.username != 'Banker'))
        properties = Property.select()
        return render_template('monopoly/index1.html', properties=properties, users=users)

    else:
        flash('login is required', 'danger')
        return redirect(url_for('users.index'))


@monopoly_blueprint.route('/create')
def create():
    user = User.get_or_none(User.id == current_user.id)
    if user.monopoly > 0:
        user.monopoly = 0
    else:
        user.monopoly = 1

    if user.save():
        flash('updated successfully', 'success')

    else:
        flash('failwhale', 'danger')

    return redirect(request.referrer)


@socketio.on('roll')
def roll(data):
    roll_data = json.loads(data)
    roll_0 = roll_data['roll1']
    roll_1 = roll_data['roll2']
    jail_roll = int(roll_data['jail roll'])
    roll_sum = int(roll_0) + int(roll_1)
    text = f'{current_user.username} rolled {roll_0} & {roll_1}.'
    # executes if this is a roll from jail.
    if jail_roll > 0:
        if roll_0 == roll_1:
            jail_free()
            activity_create(f'{text} Thus escaping jail.')
        elif current_user.jailed == 2:
            current_user.money -= 50
            jail_free()
            activity_create(
                f'{text} And got out of jail by paying $50')
        else:
            current_user.jailed += 1
            activity_create(
                f'{text} Thus failing to get out of jail.')
            current_user.save()
            # early return to prevent position change.
            return
    else:
        activity_create(text)
        if roll_0 == roll_1:
            current_user.doubles += 1
        else:
            current_user.doubles = 0

    current_user.position += roll_sum
    current_user.save()

    if current_user.doubles == 3:
        current_user.position = 30

    current_user.save()

    if current_user.position > 39:
        current_user.position = current_user.position - 40
        current_user.money += 200

    if current_user.position == 30:
        current_user.position = 10
        current_user.jailed = 0
        current_user.doubles = 0

    if not current_user.save():
        flash('roll adding failed. Contact Shen.', 'danger')
        return redirect(url_for('users.index'))

    update_positions()


@monopoly_blueprint.route('/reset')
def reset():
    if current_user.is_authenticated and (current_user.username == 'Banker' or current_user.username == 'shennex'):
        banker = User.get_or_none(User.username == 'Banker')
        users = User.select().where((User.monopoly > 0) & (User.username != 'Banker'))
        for user in users:
            user.jailed = -1
            user.position = 0
            user.money = 1500
            user.doubles = 0
            user.save()

        properties = Property.select()
        for prop in properties:
            prop.houses = 0
            prop.mortgaged = False
            prop.user_id = banker.id
            prop.save()

        banker.money = 1000000
        banker.save()
        deletion = ActivityLog.delete().where(ActivityLog.text != '')
        deletion.execute()
        return redirect(request.referrer)
    else:
        flash('no access for u, soz', 'danger')
        return(redirect(url_for('users.index')))


@monopoly_blueprint.route('/jail-pay')
def jail_pay():
    if current_user.is_authenticated:
        current_user.money -= 50
        jail_free()
        if not current_user.save():
            flash('payment could not be done for some reason.', 'danger')
        else:
            activity_create(
                f'{current_user.username} payed $50 to get out of jail.')
    else:
        flash('need to be signed in to perform this action!', 'warning')

    return redirect(request.referrer)


@socketio.on('pay')
def pay(data):
    if current_user.is_authenticated:
        pay_data = json.loads(data)
        recipient_username = pay_data['recipient']
        amount = pay_data['amount']
        recipient = User.get_or_none(User.username == recipient_username)
        amount = int(amount)
        if amount > current_user.money:
            send('broke')
            return

        current_user.money -= amount
        recipient.money += amount

        if current_user.save() and recipient.save():
            activity_create(
                f'{current_user.username} payed ${amount} to {recipient_username}')
        else:
            print('failed saving at pay func.')


@monopoly_blueprint.route("/house", methods=['POST'])
def buy_house():
    return


@monopoly_blueprint.route('/new-property')
def new_property():
    if current_user.username == 'Banker':
        return render_template('monopoly/new-property.html')
    else:
        flash('sorry, but you do not have access to that feature!', 'danger')
        return redirect(url_for('monopoly.index'))


@monopoly_blueprint.route('/create-property', methods=['POST'])
def create_property():
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
            return redirect(url_for('monopoly.new_property'))
        else:
            flash(f'failed, {img_upload_err}', 'danger')
            return redirect(request.referrer)


@socketio.on('prop_request')
def prop_show():
    if current_user.is_authenticated:
        owned_props = Property.select().where(
            Property.user == current_user.id).order_by(Property.created_at.desc())
        prop_data = []
        for each in owned_props:
            image_url = each.image_url
            house_price = each.house_price
            houses = each.houses
            name = each.name
            prop_data.append({
                'name': name,
                'houses': houses,
                'house_price': house_price,
                'image_url': image_url
            })
        data = json.dumps(prop_data)
        emit('prop_response', data)


@socketio.on('house_buy')
def house_create(prop_name):
    if current_user.is_authenticated:
        current_prop = Property.get_or_none(Property.name == prop_name)
        if not current_prop:
            print('not prop')
            flash('No such property exists! Trouble. Contact shen.', 'warning')
            return redirect(url_for('users.index'))
        if current_prop.user_id != current_user.id:
            print('not user')
            flash('You are not authorized to do that', 'danger')
            return redirect(url_for('users.index'))

        if current_user.money < current_prop.house_price:
            print('broke')
            send('broke')
        else:
            current_user.money -= current_prop.house_price
            current_prop.houses += 1
            if not current_prop.save():
                print('prop did not save')

            if not current_user.save():
                print('user did not save')

            activity_create(
                f'{current_user.username} bought a house for {prop_name} | ${current_prop.house_price}')


@socketio.on('tester')
def tester():
    print('fuck')

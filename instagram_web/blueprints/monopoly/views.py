from flask import Blueprint, render_template, request, flash,  redirect, url_for
from flask_login import current_user, login_user, login_required
from models.user import User
from models.properties import Property
from models.activity_log import ActivityLog

monopoly_blueprint = Blueprint(
    'monopoly', __name__, template_folder='templates')


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


@monopoly_blueprint.route('/')
def index():
    if current_user.is_authenticated:
        users = User.select().where((User.monopoly > 0) & (User.username != 'Banker'))
        user_positions = []
        locations = ['Go', 'Old Kent Road', 'Community Chest', 'Whitechapel Road', 'Income Tax', "King's Cross Station", 'The Angel Islington', 'Chance', 'Euston Road', 'Pentonville Road', 'Jail', 'Pall Mall', 'Electric Company', 'Whitehall', 'Northumber Land Ave.', 'Marylebone Station', 'Bow Street', 'Community Chest 2', 'Marlborough Street',
                     'Vine Street', 'Free Parking', 'Strand', 'Chance 2', 'Fleet Street', 'Trafalgar Square', 'Fenchurch St. Station', 'Leicester Square', 'Coventry Street', 'Water Works', 'Picadilly', 'Go to Jail!', 'Regent Street', 'Oxford Street', 'Community Chest 3', 'Bond Street', 'Liverpool St Station', 'Chance 3', 'Park Lane', 'Supertax', 'Mayfair']

        for user in users:
            user_positions.append(
                f'{user.username} @ {locations[user.position]}')

        activities = ActivityLog.select().order_by(ActivityLog.created_at.desc())
        properties = Property.select()
        return render_template('monopoly/index1.html', user_positions=user_positions, properties=properties, activities=activities, users=users)

    else:
        flash('login is required', 'danger')
        return redirect(request.referrer)


# @monopoly_blueprint.route('/new')
# def new():
#     return render_template('users/new.html')


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


@monopoly_blueprint.route('/roll', methods=['POST'])
def roll():
    roll_0 = request.form.get('roll-0')
    roll_1 = request.form.get('roll-1')
    username = request.form.get('username')
    roll_sum = int(roll_0) + int(roll_1)
    current_user.position += roll_sum

    if current_user.position > 39:
        current_user.position = current_user.position - 40
        current_user.money += 200

    if current_user.position == 30:
        current_user.position = 10
        current_user.jailed = 0

    activity_create(
        f'{username} rolled {roll_0} and {roll_1}')

    if current_user.save():
        return redirect(request.referrer)
    else:
        flash('roll adding failed. Contact Shen.', 'danger')
        return redirect(request.referrer)


@monopoly_blueprint.route('/reset')
def reset():
    banker = User.get_or_none(User.username == 'Banker')
    users = User.select().where((User.monopoly > 0) & (User.username != 'Banker'))
    for user in users:
        user.jailed = -1
        user.position = 0
        user.money = 1500
        user.save()

    properties = Property.select()
    for prop in properties:
        prop.houses = 0
        prop.mortgaged = False
        prop.user_id = banker.id
        prop.save()

    deletion = ActivityLog.delete().where(ActivityLog.text != '')
    deletion.execute()
    return redirect(request.referrer)


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
        new_prop = Property(name=name, user_id=current_user.id)
        if new_prop.save():
            flash('new property was saved')
            return redirect(url_for('monopoly.new_property'))
        else:
            flash('failed for some reason')
            return redirect(request.referrer)


@monopoly_blueprint.route("/jail-add")
def jail_add():
    if current_user.is_authenticated:
        if current_user.jailed < 3:
            current_user.jailed += 1
            current_user.save()
            return redirect(request.referrer)
        else:
            flash("reached max number of turns", "danger")
            return redirect(request.referrer)


@monopoly_blueprint.route('/jail-free')
def jail_free():
    if current_user.is_authenticated:
        current_user.jailed = -1
        current_user.save()
        return redirect(request.referrer)
    else:
        flash('no access, soz', 'danger')
        return redirect(request.referrer)


@monopoly_blueprint.route('/pay')
def pay():
    if current_user.is_authenticated:
        payer_username = request.form.get('payer')
        recipient_username = request.form.get('recipient')
        amount = request.form.get('amount')

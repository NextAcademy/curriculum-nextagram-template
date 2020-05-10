from flask import Blueprint, render_template, request, flash,  redirect, url_for
from flask_login import current_user, login_user, login_required
from models.user import User


monopoly_blueprint = Blueprint(
    'monopoly', __name__, template_folder='templates')


@monopoly_blueprint.route('/')
def index():
    if current_user.is_authenticated:
        users = User.select().where(User.monopoly > 0)
        user_positions = []
        locations = ['Go', 'Old Kent Road', 'Community Chest', 'Whitechapel Road', 'Income Tax', "King's Cross Station", 'The Angel Islington', 'Chance', 'Euston Road', 'Pentonville Road', 'Jail', 'Pall Mall', 'Electric Company', 'Whitehall', 'Northumber Land Ave.', 'Marylebone Station', 'Bow Street', 'Community Chest 2', 'Marlborough Street',
                     'Vine Street', 'Free Parking', 'Strand', 'Chance 2', 'Fleet Street', 'Trafalgar Square', 'Fenchurch St. Station', 'Leicester Square', 'Coventry Street', 'Water Works', 'Picadilly', 'Go to Jail!', 'Regent Street', 'Oxford Street', 'Community Chest 3', 'Bond Street', 'Liverpool St Station', 'Chance 3', 'Park Lane', 'Supertax', 'Mayfair']
        for user in users:
            user_positions.append({user.username: locations[user.position]})
        return render_template('monopoly/index1.html', user_positions=user_positions)

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
    roll_value = request.form.get('roll-value')
    current_user.position += int(roll_value)
    if current_user.position > 39:
        current_user.position -= 40
    if current_user.save():
        return redirect(request.referrer)
    else:
        flash('roll adding failed. Contact Shen.', 'danger')
        return redirect(request.referrer)


@monopoly_blueprint.route('/reset')
def reset():
    users = User.select().where(User.monopoly > 0)
    for user in users:
        user.position = 0
        user.save()

    return redirect(request.referrer)

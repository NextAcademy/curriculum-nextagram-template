from flask import Blueprint, jsonify
from models.user import User

users_api_blueprint = Blueprint('users_api',
                                __name__,
                                template_folder='templates')


@users_api_blueprint.route('/', methods=['GET'])
def index():
    users = User.select()
    user_list = []
    for user in users:
        data = (user.__dict__)
        user_list.append(data['__data__'])

    return jsonify(user_list)

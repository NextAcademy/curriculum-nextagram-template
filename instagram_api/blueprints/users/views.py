from flask import Blueprint, jsonify
from models.user import User
from playhouse.shortcuts import model_to_dict


users_api_blueprint = Blueprint('users_api',
                                __name__,
                                template_folder='templates')


@users_api_blueprint.route('/', methods=['GET'])
def index():
    users = User.select()
    user_list = []
    for user in users:
        user = model_to_dict(user)
        user_list.append(user)
        # data = (user.__dict__)
        # user_list.append(data['__data__'])

    return jsonify(user_list)

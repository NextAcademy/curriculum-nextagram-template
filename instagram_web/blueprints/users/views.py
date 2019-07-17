from flask import Blueprint, render_template


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

@users_blueprint.route('/', methods=['POST'])
def create():
    email = request.form.get('email')
    full_name = request.form.get('full_name')
    username = request.form.get('username')
    password = request.form.get('password')

    


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass

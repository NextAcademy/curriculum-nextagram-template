from instagram_api.blueprints.users.views import users_api_blueprint
from app import app
from flask_cors import CORS

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##


app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')

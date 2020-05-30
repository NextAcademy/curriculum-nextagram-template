from flask_wtf.csrf import CSRFProtect
import os
import config
from flask import Flask
from models.base_model import db
from flask_socketio import SocketIO, emit

# import logging
# import redis
# import gevent
# from flask_sockets import Sockets

# REDIS_URL = os.environ['REDIS_URL']
# REDIS_CHAN = 'chat'

# app.debug = 'DEBUG' in os.environ

# sockets = Sockets(app)
# redis = redis.from_url(REDIS_URL)

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)
csrf = CSRFProtect(app)
socketio = SocketIO(app)


if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc


@socketio.on('message')
def handle_message(message):
    socketio.emit('message', message)

from app import app, socketio
import instagram_api
import instagram_web
import os

if __name__ == '__main__':
    if os.getenv('FLASK_ENV') == 'development':
        socketio.run(app)
    else:
        app.run()

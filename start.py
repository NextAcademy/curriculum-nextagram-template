from app import app, socketio
import instagram_api
import instagram_web

if __name__ == '__main__':
    socketio.run(app)

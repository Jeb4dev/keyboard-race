from app.app import app, settings, socketio

if __name__ == "__main__":
    socketio.run(app, port=8000, debug=settings.DEBUG)

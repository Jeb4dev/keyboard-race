from app.app import app, settings


if __name__ == "__main__":
    app.run(port=8000, debug=settings.DEBUG)
web: gunicorn -w 1 -b 0.0.0.0:$PORT --worker-class eventlet app.app:app
release: cd app; flask db upgrade

release: python migrate.py
web: gunicorn start:app --worker-class eventlet -w 1 module:app --preload 
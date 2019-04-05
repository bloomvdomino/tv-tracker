"""
gunicorn WSGI server configuration.
"""

bind = ':8000'
worker_class = 'gevent'

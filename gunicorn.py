"""
gunicorn WSGI server configuration.
"""

import os

port = os.environ.get("PORT", 8000)

bind = f"0:{port}"
worker_class = "gevent"

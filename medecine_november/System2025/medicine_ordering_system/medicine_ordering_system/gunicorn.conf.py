"""
Gunicorn configuration file for OnCare Medicine Ordering System
"""

import multiprocessing
import os

# Server socket
bind = os.environ.get('GUNICORN_BIND', "127.0.0.1:8000")
backlog = 2048

# Worker processes
workers = int(os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = os.environ.get('GUNICORN_WORKER_CLASS', 'sync')
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
graceful_timeout = 30

# Logging
accesslog = os.environ.get('GUNICORN_ACCESS_LOG', '-')
errorlog = os.environ.get('GUNICORN_ERROR_LOG', '-')
loglevel = os.environ.get('GUNICORN_LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'oncare_gunicorn'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (uncomment and configure if using SSL directly with Gunicorn)
# keyfile = '/path/to/keyfile'
# certfile = '/path/to/certfile'

# Preload application
preload_app = True

# Server hooks
def on_starting(server):
    """Called just before the master process is initialized."""
    server.log.info("Starting OnCare Medicine Ordering System")

def on_reload(server):
    """Called to recycle workers during a reload via SIGHUP."""
    server.log.info("Reloading OnCare Medicine Ordering System")

def when_ready(server):
    """Called just after the server is started."""
    server.log.info("OnCare Medicine Ordering System is ready. Spawning workers")

def on_exit(server):
    """Called just after exiting the master process."""
    server.log.info("Shutting down OnCare Medicine Ordering System")


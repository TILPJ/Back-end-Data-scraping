from .base import *
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = ["tilup-release-v1.herokuapp.com"]

STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = []

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES["default"].update(db_from_env)

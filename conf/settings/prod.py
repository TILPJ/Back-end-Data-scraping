from .base import *
import dj_database_url


DEBUG = False

ALLOWED_HOSTS = []

STATIC_ROOT = BASE_DIR / "static"

STATICFILES_DIRS = []

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# DATABASES = {
#     "default": {
#         "ENGINE": os.getenv("PROD_DATABASE_ENGINE"),
#         "NAME": os.getenv("PROD_DATABASE_NAME"),
#         "USER": os.getenv("PROD_DATABASE_USER"),
#         "PASSWORD": os.getenv("PROD_DATABASE_PASSWORD"),
#         "HOST": os.getenv("PROD_DATABASE_HOST"),
#         "PORT": os.getenv("PROD_DATABASE_PORT"),
#     }
# }


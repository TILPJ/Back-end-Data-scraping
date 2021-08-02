from .base import *
import dj_database_url


DEBUG = False

ALLOWED_HOSTS = ["tilup-release-v1.herokuapp.com"]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES["default"].update(db_from_env)


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

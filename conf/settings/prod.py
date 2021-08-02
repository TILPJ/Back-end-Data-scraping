from .base import *

DEBUG = False

ALLOWED_HOSTS = ["tilup.pythonanywhere.com"]

STATIC_ROOT = BASE_DIR / "static"

STATICFILES_DIRS = []

DATABASES = {
    "default": {
        "ENGINE": os.getenv("PROD_DATABASE_ENGINE"),
        "NAME": os.getenv("PROD_DATABASE_NAME"),
        "USER": os.getenv("PROD_DATABASE_USER"),
        "PASSWORD": os.getenv("PROD_DATABASE_PASSWORD"),
        "HOST": os.getenv("PROD_DATABASE_HOST"),
        "PORT": os.getenv("PROD_DATABASE_PORT"),
    }
}

from os import environ


class Config:

    SECRET_KEY = environ.get("SECRET_KEY")
    DEBUG = environ.get("DEBUG")
    DEVELOPMENT = environ.get("DEVELOPMENT")
    CSRF_ENABLED = True

    JSONIFY_PRETTYPRINT_REGULAR = False


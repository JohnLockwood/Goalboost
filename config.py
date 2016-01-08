import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Obviously this is reset in production, as are other sensitive passwords, etc.
    SECRET_KEY = os.environ.get("SECRET_KEY") or "TOP_SECRET_KEY"
    USER_PASSWORD_HASH_ROUNDS = 2000
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    DEBUG = False

    # Flask security configuration
    SECURITY_PASSWORD_HASH = os.environ.get("GOALBOOST_SECURITY_PASSWORD_HASH") or "pbkdf2_sha256"
    SECURITY_PASSWORD_SALT = os.environ.get("GOALBOOST_SECURITY_PASSWORD_SALT") or "SECRET" 
    SECURITY_REGISTERABLE = True
    SECURITY_EMAIL_SENDER =  os.environ.get("GOALBOOST_SECURITY_EMAIL_SENDER") or "someuser@example.com"
    SECURITY_POST_LOGOUT_VIEW = '/auth/logged_out' # defined in auth_controllers.py
    SECURITY_POST_LOGIN_VIEW = '/timer/user' # defined in auth_controllers.py

    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"

    WTF_CSRF_ENABLED = False

    # Mongo DB Configuration
    MONGODB_DB = os.environ.get("GOALBOOST_MONGO_DB") or "goalboost"
    MONGODB_HOST = os.environ.get("GOALBOOST_MONGO_HOST") or "localhost"
    MONGODB_PORT = os.environ.get("GOALBOOST_MONGO_PORT") or 27017
    MONGODB_USERNAME = os.environ.get("GOALBOOST_MONGO_USERNAME") or None
    MONGODB_PASSWORD = os.environ.get("GOALBOOST_MONGO_PASSWORD") or None

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SECURITY_SEND_REGISTER_EMAIL = False

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    USER_PASSWORD_HASH_ROUNDS = 150000
    # Mail configuration
    MAIL_SERVER = os.environ.get("GOALBOOST_MAIL_SERVER") or "smtp.example.com"
    MAIL_DEFAULT_SENDER = os.environ.get("GOALBOOST_MAIL_DEFAULT_SENDER") or "someuser@example.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("GOALBOOST_MAIL_USERNAME") or "codesolid"
    MAIL_PASSWORD = os.environ.get("GOALBOOST_MAIL_PASSWORD") or "secret"

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,

    "default": DevelopmentConfig
}
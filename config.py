import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "TOP_SECRET_KEY"
    USER_PASSWORD_HASH_ROUNDS = 2000
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    DEBUG = False

    # Flask security configuration
    SECURITY_PASSWORD_HASH = os.environ.get("GOALBOOST_SECURITY_PASSWORD_HASH") or "pbkdf2_sha256"
    SECURITY_PASSWORD_SALT = os.environ.get("GOALBOOST_SECURITY_PASSWORD_SALT") or "SECRET" 
    SECURITY_REGISTERABLE = True

    # Mail configuration - revisit
    MAIL_SERVER = os.environ.get("GOALBOOST_MAIL_SERVER") or "smtp.example.com"
    MAIL_DEFAULT_SENDER = os.environ.get("GOALBOOST_MAIL_DEFAULT_SENDER") or "someuser@example.com"
    SECURITY_EMAIL_SENDER =  os.environ.get("GOALBOOST_SECURITY_EMAIL_SENDER") or "someuser@example.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("GOALBOOST_MAIL_USERNAME") or "codesolid"
    MAIL_PASSWORD = os.environ.get("GOALBOOST_MAIL_PASSWORD") or "secret"

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True       
    SQLALCHEMY_DATABASE_URI = os.environ.get("GOALBOOST_DEV_DATABASE_URL") or \
        "mysql+pymysql://user:Password@localhost/dbname"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("GOALBOOST_TEST_DATABASE_URL") or \
        "mysql+pymysql://user:Password@localhost/dbname"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("GOALBOOST_DATABASE_URL") or \
        "mysql+pymysql://user:Password@localhost/dbname"
    USER_PASSWORD_HASH_ROUNDS = 150000


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,

    "default": DevelopmentConfig
}
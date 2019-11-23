class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:1@127.0.0.1:3306/test1'
    pool_pre_ping = True
    SECRET_KEY = '6c17d450a6ba5a8d929c9e4e4e3e9ac0'

    ### FLASK-SECURITY ###
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'bcrypt'

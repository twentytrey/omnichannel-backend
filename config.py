import os
import datetime
basedir=os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG=False
    TESTING=False
    CSRF_ENABLED=True
    SECRET_KEY='t#xbu+27*$6'
    ALLOWED_EXTENSIONS=set(['txt', 'pdf', 'csv', 'png', 'jpg', 'jpeg', 'gif'])
    JWT_BLACKLIST_ENABLED=True
    JWT_BLACKLIST_TOKEN_CHECKS=['access','refresh']
    JWT_ACCESS_TOKEN_EXPIRES=datetime.timedelta(days=20)
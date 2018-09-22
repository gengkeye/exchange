import os
import ldap
from django_auth_ldap.config import LDAPSearch

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'logs')


class Config:
    # Use it to encrypt or decrypt data
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = os.environ.get('SECRET_KEY', '2vym+ky!997d5kkcc64mnz06y1mmui3lut#(^wd=%s_qj$1%x')
    # How many line display every page, default 25

    REPO_URL = 'git@210.213.158.59:oldseven/jumpserver.git'

    # telegram bot
    TELE_USERNAME = 'OldsevenBot'
    TELE_TOKEN = '677765866:AAFrFCWkKVa878JIiXEgOv3lsgf4qEtZWu4'

    # Django security setting, if your disable debug model, you should setting that
    ALLOWED_HOSTS = ['*']

    # Development env open this, when error occur display the full process track, Production disable it
    DEBUG = False

    # DEBUG, INFO, WARNING, ERROR, CRITICAL can set. See https://docs.djangoproject.com/en/1.10/topics/logging/
    LOG_LEVEL = 'DEBUG'

    # mysql database
    DB_ENGINE = 'mysql'
    DB_NAME = 'exchange'
    DB_HOST = '127.0.0.1'
    DB_PORT = 3306
    DB_USER = 'jumpserver'
    DB_PASSWORD = 'QYoRb6wa4xVQi^fv'


    # Use Redis as broker for celery and web socket
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PASSWORD = ''
    BROKER_URL = 'redis://%(password)s%(host)s:%(port)s/3' % {
        'password': REDIS_PASSWORD,
        'host': REDIS_HOST,
        'port': REDIS_PORT,
    }

    # # Email SMTP setting, we only support smtp send mail
    # EMAIL_HOST = 'smtp.gmail.com'
    # EMAIL_PORT = 465
    # EMAIL_HOST_USER = 'dejiegeng@gmail.com'
    # EMAIL_HOST_PASSWORD = 'jlg117612'
    # EMAIL_USE_SSL = True  # If port is 465, set True
    # EMAIL_USE_TLS = False  # If port is 587, set True
    # EMAIL_SUBJECT_PREFIX = '[Jumpserver] '
    # SITE_URL = 'http://172.16.22.223:8080'

    # Api token expiration when create
    TOKEN_EXPIRATION = 3600

    # Session and csrf domain settings, If you deploy jumpserver,coco,luna standby,
    # So than share cookie, and you need use a same top-level domain name

    # SESSION_COOKIE_DOMAIN = '.jms.com'
    # CSRF_COOKIE_DOMAIN = '.jms.com'
    SESSION_COOKIE_AGE = 3600*24

    def __init__(self):
        pass

    def __getattr__(self, item):
        return None


class ProductionConfig(Config):
    # Email SMTP setting, we only support smtp send mail
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 465
    EMAIL_HOST_USER = 'dejiegeng@gmail.com'
    EMAIL_HOST_PASSWORD = 'jlg117612'
    EMAIL_USE_SSL = True  # If port is 465, set True
    EMAIL_USE_TLS = False  # If port is 587, set True
    EMAIL_SUBJECT_PREFIX = '[Jumpserver] '
    SITE_URL = 'http://172.16.22.223:8080'

config = {
    'production': ProductionConfig,
}

env = 'production'

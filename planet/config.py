# -*- coding: utf-8 -*-

DATABASE_URL = u"postgresql://planet:planet@localhost/planet"

class Config(object):
    DEBUG = True
    TESTING = False
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SERVER_NAME = u'192.168.33.10'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PAGE_SLICE = 25

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = u"postgresql://planet:planet@localhost/test"

config = {
    'default': DevelopmentConfig,
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
}

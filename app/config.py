import os

ENV = os.environ.get('ACHOO_DEBUG')

class Config(object):
    MSG = '(beta)'
    VERSION = '0.1'
    DEBUG = True if ENV == 'local' else False

import os

class Config():
	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True
	HOST = os.environ['HOST']
	SECRET_KEY = os.environ['SECRET_KEY']
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MONGO_URI = os.environ['MONGO_URI']

class Local(Config):
	DEBUG = True
	TESTING = True
	CSRF_ENABLED = False

class Staging(Config):
	DEBUG = False
	TESTING = True
	CSRF_ENABLED = True

class Production(Config):
	DEBUG = False
	CSRF_ENABLED = True
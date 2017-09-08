from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

db = None

def createDB(app):
	global db 
	if db == None:
		db = SQLAlchemy(app)
	return db
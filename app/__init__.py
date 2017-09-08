from flask import Flask
from app.urls import register_urls
from Exceptions.ExceptionHandler import SeException
from DBConnection.connection import createDB
from app.settings import os

## Registering Application
app = Flask(__name__)

##Registering Urls
register_urls(app)

## Loading Application configurations from settings
app.config.from_object(os.environ['APP_SETTINGS'])

##create db connection
createDB(app)

##register custom exception handler
@app.errorhandler(SeException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

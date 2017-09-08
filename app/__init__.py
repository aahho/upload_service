from flask import Flask, jsonify
from app.urls import register_urls
from app.exceptions import ApiBaseException
from app.settings import os

## Registering Application
app = Flask(__name__)

##Registering Urls
register_urls(app)

## Loading Application configurations from settings
app.config.from_object(os.environ['APP_SETTINGS'])

## For Handling Custom Api Exception
@app.errorhandler(ApiBaseException)
def handle_base_exception(error):
	response = jsonify(error.handle())
	response.status_code = error.status_code
	return response

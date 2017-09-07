from flask import Flask
from app.urls import register_urls
from app.settings import os

## Registering Application
app = Flask(__name__)

##Registering Urls
register_urls(app)

## Loading Application configurations from settings
app.config.from_object(os.environ['APP_SETTINGS'])

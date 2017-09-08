import os
from app import helpers

##Setting Base Directory
os.environ['BASE_DIR'] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

## Link to connect to the database
os.environ['DATABASE_URL'] = helpers.generate_database_url()

## Setting some new hashed secret key for application on reset
os.environ['SECRET_KEY'] = helpers.generate_hash_token()

## Validating On HOST
os.environ['HOST'] = helpers.getenv('HOST')

##
# Setting Up Environment to run application
##
host = helpers.getenv('APP_ENV')
if host == 'production':
	os.environ['APP_SETTINGS'] = 'app.config.Production'
elif host == 'staging':
	os.environ['APP_SETTINGS'] = 'app.config.Staging'
else:
	os.environ['APP_SETTINGS'] = 'app.config.Local'
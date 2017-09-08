from aws_s3.urls import aws_s3

## 
# Register all url blueprints
# @param blueprint_instance as app
##
def register_urls(app):
	## Blueprint for aws_s3
	app.register_blueprint(aws_s3)
from aws_s3 import validators, uploader
from app import response
from app.synchronizer.g_firebase.sync import push_to_firebase, update_upload

## Process New Upload
def process_upload(request):
	validators.validate_upload(request)
	result = uploader.upload(request)
	upload_firebase = push_to_firebase(result[0])
	return response.respond_with_list(200, result)
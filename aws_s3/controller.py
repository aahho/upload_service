from aws_s3 import validators, uploader
from app import response

## Process New Upload
def process_upload(request):
	validators.validate_upload(request)
	result = uploader.upload(request)
	return response.respond_with_list(200, result)
from aws_s3 import validators, uploader
from app import response
import json
from app.synchronizer.g_firebase.sync import push_to_firebase, update_upload

## Process New Upload
def process_upload(request):
	from transformers import UploadTransformer
	
	validators.validate_upload(request)
	result = uploader.upload(request)
	result, transformed = response.respond_with_transformed_list(200, result, UploadTransformer)
	upload_firebase = push_to_firebase(transformed[0])
	return result

def process_download(request):
	validators.validate_download(request)
	result = uploader.download(request)
	return response.respond_with_success(200, 'OKAY')
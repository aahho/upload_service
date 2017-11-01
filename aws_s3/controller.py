from aws_s3 import validators, uploader
from app import response
from app.synchronizer.g_firebase.sync import push_to_firebase, update_upload

## Process New Upload
def process_upload(request):
	from transformers import UploadTransformer
	
	validators.validate_upload(request)
	result = uploader.upload(request)
	upload_firebase = push_to_firebase(result[0])
	return response.respond_with_transformed_list(200, result, UploadTransformer)

def process_download(request):
	validators.validate_download(request)
	result = uploader.download(request)
	return response.respond_with_success(200, 'OKAY')
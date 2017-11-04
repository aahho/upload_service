import requests
from aws_s3.transformers import UploadTransformer

def update_upload(data):
	transformed = UploadTransformer.transform(data)
	transformed['tempLink'], transformed['selfLink'] = transformed['selfLink'], transformed['tempLink']
	response = requests.post("http://noodlestock.com:5000/manage/uploads/"+data['id'], json=transformed)
	return response.status_code
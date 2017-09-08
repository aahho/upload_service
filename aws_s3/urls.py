from flask import Blueprint
from app import response

aws_s3 = Blueprint('aws_s3', __name__, url_prefix='/upload')

@aws_s3.route('', methods=['GET'])
def get():
	return response.respond_with_success(200, 'Hello User!')
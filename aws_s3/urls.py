from flask import Blueprint, request, render_template, send_file, Response
from app.settings import os
import magic
from app import response
from aws_s3 import controller, helpers
import json

aws_s3 = Blueprint('aws_s3', __name__, 
	url_prefix='/service/s3', 
	static_url_path=os.environ['UPLOAD_FOLDER'],
	template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

@aws_s3.route('', methods=['GET'])
def get():
	return render_template('index.html')

@aws_s3.route('/static/<file_name>')
def view_file(file_name):
	file_path = os.path.join(os.environ['UPLOAD_FOLDER'], file_name).strip(' \t\r\n\0')
	mimetype = helpers.get_mime_from_file(file_path)
	
	file = helpers.load_file(file_path)
	response = Response(file, mimetype=mimetype)
	response.headers['Content-Type'] = mimetype
	# response.headers['Content-Disposition'] = 'attachment; filename='+file_path.split('/')[-1]
	
	return response

## For uploading new file on to aws
@aws_s3.route('/upload', methods=['POST'])
def upload():
	result = controller.process_upload(request)
	return result
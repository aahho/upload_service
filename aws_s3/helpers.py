from werkzeug.utils import secure_filename
import os, datetime, re, magic, math
from app import helpers

def fetch_file_details(file, temp_name):
	data = {
		'id' : str(helpers.generate_uuid()),
		'name' : get_name(file),
		'original_name' : get_original_name(file),
		'title' : get_title(file),
		'extension': get_extension(file),
		'content_type' : get_mime_type(file),
		'path' : get_path(temp_name),
		'size' : get_size(file)/(1000*1024)
	}
	data['temp_link'] = self_link(data)
	data['self_link'] = temp_link(temp_name)
	return data

def get_name(file):
	split = datetime.datetime.now().strftime("%c")+str(int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000))
	trim = re.sub('[\s+]', '', split)
	return re.sub(':', '', trim)+os.path.splitext(secure_filename(file.filename))[1]

def get_original_name(file):
	return secure_filename(file.filename)

def get_title(file):
	return os.path.splitext(secure_filename(file.filename))[0]

def get_extension(file):
	return os.path.splitext(secure_filename(file.filename))[1]

def get_mime_type(file):
	return file.content_type

def get_mime_from_file(file_path):
	mime = magic.Magic(mime=True)
	return mime.from_file(file_path)

def get_size(file):
	return len(file.read())

def get_current_month_and_year():
	return datetime.date.today().strftime("%B")+datetime.date.today().strftime("%Y")

def get_path(temp_name):
	return os.environ['UPLOAD_FOLDER']+'/'+temp_name

def temp_link(temp_name):
	return "http://"+helpers.getenv('HOST')+":5000/service/s3/static/"+temp_name

# def create_fresh_pool_format(data):
# 	return {
# 		'promise_id' : data['promiseId'],
# 		'expected_packet_count' : data['expectedSlice'],
# 		'data' : [
# 			{
# 				'start' : data['start'],
# 				'end' : data['end'],
# 				'current_loop_count' : data['currentLoopId']
# 			}
# 		]
# 	}

# def create_regular_pool_format(data):
# 	return {
# 		'start' : data['start'],
# 		'end' : data['end'],
# 		'current_loop_count' : data['currentLoopId'],
# 	}

def load_file(file):
	with open(file, 'r') as file:
		return file.read()

def get_bucket_directory():
	return 'production/'+get_current_month_and_year() if helpers.getenv('APP_ENV') == 'production' else 'testing/'+get_current_month_and_year()

def self_link(file_details):
	self_link = "https://s3.amazonaws.com/{0}/{1}/{2}".format(
		helpers.getenv('BUCKET_NAME'),
		get_bucket_directory(),
		file_details['name']
	)
	return self_link

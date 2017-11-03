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
		'size' : get_size(get_path(temp_name))
	}
	data['temp_link'] = self_link(data['name'])
	data['self_link'] = temp_link(temp_name)
	if data['extension'] in resizable_types():
		data['web_views'] = generate_web_view_links(get_extension(file))
		data['web_view_links'] = dict((label, self_link(data['web_views'][label]['name'])) for label in data['web_views'])
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

def resizable_types():
	return ['.png', '.jpg', '.jpeg']

def resizable_sizes():
	return [
		{
		'label' : 'mobile',
		'width' : 40,
		'height' : 40 
		},
		{
		'label' : 'thumbnail',
		'width' : 100,
		'height' : 100 
		},
		{
		'label' : 'medium',
		'width' : 640,
		'height' : 480 
		},
		{
		'label' : 'large',
		'width' : 1024,
		'height' : 768 
		}
	]

def generate_web_view_links(extension):
	sizes = resizable_sizes()
	links = {}
	for size in sizes:
		name = str(helpers.generate_uuid())+extension
		links[size['label']] = {'name' : name, 'width' : size['width'], 'height' : size['height']}
	return links

def get_mime_type(file):
	return file.content_type

def get_mime_from_file(file_path):
	mime = magic.Magic(mime=True)
	return mime.from_file(file_path)

def get_size(path):
	return os.stat(path).st_size

def get_current_month_and_year():
	return datetime.date.today().strftime("%B")+datetime.date.today().strftime("%Y")

def get_path(temp_name):
	return os.environ['UPLOAD_FOLDER']+'/'+temp_name

def temp_link(temp_name):
	host = helpers.getenv('HOST')
	if host == '127.0.0.1':
		host = '127.0.0.1:5000'
	return "http://"+host+"/service/s3/static/"+temp_name

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

def self_link(filename):
	self_link = "https://s3.amazonaws.com/{0}/{1}/{2}".format(
		helpers.getenv('BUCKET_NAME'),
		get_bucket_directory(),
		filename
	)
	return self_link

def resize_image(file_details):
	from PIL import Image
	from resizeimage import resizeimage

	try:
		file = open(file_details['path'], 'r')
		for label in file_details['web_views']:
			name = file_details['web_views'][label]['name']
			pil_image = Image.open(file, 'r')
			pil_image.thumbnail([file_details['web_views'][label]['width'], file_details['web_views'][label]['height']], Image.ANTIALIAS)
			pil_image.save(os.path.join(os.environ['UPLOAD_FOLDER'], name), pil_image.format)
			file_details['web_view_links'][label] = {'path' : get_path(name), 'name' : name}
		return file_details
	except Exception, e:
		print "--------- Came To Exception Image Resizer ________", file_details['path']
		return []

def apps_allowed():
	return ['noodlestock', 'fbase']
	
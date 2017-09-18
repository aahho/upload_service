from app.exceptions import MissingRequiredParameter, InvalidRequest
from werkzeug.utils import secure_filename
import json

##
# Validate New Upload Request and file formats
# @param request Object
##
def validate_upload(request):
	if not len(request.files):
		raise MissingRequiredParameter(params={'files'}, payload=(['hint','Please attach files.'],))
	files = request.files.getlist('files[]')
	for file in files:
		filename = secure_filename(file.filename)
		if '.' in filename and filename.rsplit('.', 1)[1].lower() in blocked_extension() :
			raise InvalidRequest(params={'upload'}, payload=(['hint','Requested file format not supported.'],))
	return True

##
# List of Blocked Extensions by server
##
def blocked_extension():
	return ['.exe', '.dll', '.deb', '.tar.gz']

##
# Validate File Chunks
# @param request Object
##
def validate_chunks(request):
	if 'files' not in request.files:
		raise MissingRequiredParameter(params={'files'}, payload=(['hint','Please attach files.'],))
	data = json.loads(json.dumps(request.form))
	if 'promiseId' in data and 'expectedSlice' in data and 'start' in data and 'end' in data and 'currentLoopId' in data:
		return True
	else:
		raise MissingRequiredParameter(payload=(['hint','Please send all fields.'],))
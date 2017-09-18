class ApiBaseException(Exception):
	message = 'We messed Up!'
	status_code = 500
	payload = ({'hint','Internal Server Error'},)
	error_code = 'AH_500'

	def __init__(self, message=None, status_code=None, payload=None, error_code=None):
		super(Exception, self).__init__()
		if message is not None:
			self.message = message
		if status_code is not None:
			self.status_code = status_code
		if payload is not None:
			self.payload = payload
		if error_code is not None:
			self.error_code = error_code

	def handle(self):
		response = {}
		response['data'] = self.message

		response['notification'] = {}
		response['notification'] = dict(self.payload or ())
		response['notification']['message'] = 'Failed to respond'
		response['notification']['type'] = 'failure'
		response['notification']['errorCode'] = self.error_code

		return response

class MissingRequiredParameter(ApiBaseException):
	status_code = 400
	error_code = 'AH_400'
	payload = (['hint','Please fill mandatory fields.'],)

	def __init__(self, params={}, payload=None):
		if payload is not None:
			self.payload = payload
		self.message = "Missing required parameters: %s" % ', '.join(params)

class ResourceDoesNotExist(ApiBaseException):
	status_code = 404
	message = "A resource with that ID no longer exists."
	error_code = 'AH_404'
	payload = (['hint','Resource Id/Uri no longer exists.'],)

class UnauthorizedRequest(ApiBaseException):
	status_code = 401
	message = "Unauthorized Request"
	error_code = 'AH_401'
	payload = (['hint','It lacks valid authentication credentials for the target resource.'],)

class InvalidRequest(ApiBaseException):
	status_code = 400
	error_code = 'AH_400'
	payload = (['hint','Request cannot be processed.'],)

	def __init__(self, params={}, payload=None):
		if payload is not None:
			self.payload = payload
		self.message = "Invalid request made for: %s" % ', '.join(params)
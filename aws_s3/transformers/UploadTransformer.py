def transform(data):
	result = {
		'id' : data['id'],
		'name' : data['name'],
		'extension' : data['extension'],
		'title' : data['original_name'],
		'selfLink' : data['self_link'],
		'tempLink' : data['temp_link'],
		'size' : data['size'],
		'mimeType' : data['content_type'],
		'webViewLinks' : data['web_view_links'] if 'web_view_links' in data else None
	}
	if result['webViewLinks'] is None:
		del result['webViewLinks']
	return result
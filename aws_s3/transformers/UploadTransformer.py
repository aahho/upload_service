def transform(data):
	result = {
		'id' : data['id'],
		'name' : data['name'],
		'extension' : data['extension'],
		'title' : data['original_name'],
		'selfLink' : data['self_link'],
		'tempLink' : data['temp_link'],
		'size' : data['size'],
		'mimeType' : data['content_type']
	}
	if 'web_view_links' in data:
		result['webViewLinks'] = data['web_view_links'],
	return result
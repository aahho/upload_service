from app.synchronizer.g_firebase import apis

def push_to_firebase(data):
	firebase = apis.FirebaseApi()
	upload = firebase.push_upload(data)
	return upload

def update_upload(data):
	firebase = apis.FirebaseApi()
	update = firebase.update_upload(data)
	return update
from app.synchronizer.g_firebase.sync import update_upload
import os

def sync_server(data):
	update = update_upload(data)
	if update:
		if os.path.exists(data['path']): os.remove(data['path'])
	return update

def remove_local_copy(data):
	if os.path.exists(data['path']): os.remove(data['path'])
	return True
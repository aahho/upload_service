from app.synchronizer.g_firebase.sync import update_upload as firebase_update
from app.synchronizer.noodlestock.sync import update_upload as noodlestock_update
import os

def sync_server(data):
	if data['app'] == 'fbase':
		update = firebase_update(data)
	if data['app'] == 'noodlestock':
		update = noodlestock_update(data)
		
	if update:
		if os.path.exists(data['path']): os.remove(data['path'])
	return update

def remove_local_copy(data):
	if os.path.exists(data['path']): os.remove(data['path'])
	return True
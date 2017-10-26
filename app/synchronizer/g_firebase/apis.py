from helpers import generate_firebase_config
from app.helpers import generate_uuid
import pyrebase

class FirebaseApi():

	def __init__(self):
		self.config = generate_firebase_config()
		self.firebase = pyrebase.initialize_app(self.config)
		self.auth = self.firebase.auth()
		self.db = self.firebase.database()

	def create_custom_token(self):
		return self.auth.create_custom_token(str(generate_uuid()))

	def signin_with_custom_token(self):
		return self.auth.sign_in_with_custom_token(self.create_custom_token())

	def push_upload(self, data):
		return self.db.child("/chat/uploads").child(data['id']).set(data)

	def get_uploads(self):
		return self.db.child("/chat/uploads").get(self.signin_with_custom_token()['idToken'])

	def update_upload(self, data):
		uploads = self.get_uploads()
		for upload in uploads.each():
			if data['id'] == upload.val()['id']:
				update = self.db.child("/chat/uploads").child(data['id']).update({"self_link": data['temp_link'], "temp_link": data['self_link']})
				if update:
					return True
		return False
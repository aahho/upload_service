from app import helpers

def generate_firebase_config():
	return {
		"apiKey" : helpers.getenv('firebase_api_key'),
		"authDomain" : helpers.getenv('firebase_auth_domain'),
		"databaseURL" : helpers.getenv('firebase_database_url'),
		"projectId" : helpers.getenv('firebase_project_id'),
		"storageBucket" : helpers.getenv('firebase_storage_bucket'),
		"serviceAccount" : helpers.getenv('firebase_service_account')
	}
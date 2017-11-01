from app import helpers
from app.synchronizer import helpers as sync_helper
import logging
import math
import mimetypes
from multiprocessing import Pool
import os
import copy_reg
import types

from boto.s3.connection import S3Connection
import boto3
from filechunkio import FileChunkIO

def _pickle_method(m):
	if m.im_self is None:
		return getattr, (m.im_class, m.im_func.func_name)
	else:
		return getattr, (m.im_self, m.im_func.func_name)
copy_reg.pickle(types.MethodType, _pickle_method)

class Apis(object):

	def __init__(self):
		self.access_key = helpers.getenv('AWS_ACCESS_KEY_ID')
		self.access_secret = helpers.getenv('AWS_ACCESS_KEY_SECRET')
		self.conn = S3Connection(self.access_key, self.access_secret)
		self.bucket_name = helpers.getenv('BUCKET_NAME')
		self.bucket_directory = 'production/'+helpers.get_current_month_and_year() if helpers.getenv('APP_ENV') == 'production' else 'testing/'+helpers.get_current_month_and_year()
		self.parallel_processes = 10

	def upload_large(self, file_details, guess_mimetype=True, force_download=False, policy="public-read"):
		import helpers as aws_helpers

		source_path = file_details['path']
		bucket = self.conn.get_bucket(self.bucket_name)
		keyname = self.bucket_directory+'/'+file_details['name']
		basic_headers = {
			"Content-Type":file_details['content_type'],
			"ACL": "public-read",
			# "Content-Disposition" : "attachment; filename=%s"% file_details['original_name']
		}
		if force_download:
			basic_headers["Content-Disposition"] = "attachment; filename=%s"% file_details['original_name']

		multipart = bucket.initiate_multipart_upload(keyname, headers=basic_headers)
		source_size = os.stat(source_path).st_size
		bytes_per_chunk = max(int(math.sqrt(5242880) * math.sqrt(source_size)), 5242880)
		chunk_amount = int(math.ceil(source_size / float(bytes_per_chunk)))
		pool = Pool(processes=self.parallel_processes)
		for i in range(chunk_amount):
			offset = i * bytes_per_chunk
			remaining_bytes = source_size - offset
			bytes = min([bytes_per_chunk, remaining_bytes])
			part_num = i + 1
			pool.apply_async(self._upload_part, [bucket, self.bucket_name, multipart, part_num, source_path, offset, bytes])
		pool.close()
		pool.join()
		if len(multipart.get_all_parts()) == chunk_amount:
			multipart.complete_upload()
			key = bucket.get_key(keyname)
			key.set_acl(policy)
			key.content_type = basic_headers['Content-Type']
			key.set_contents_from_filename(source_path, policy=policy, headers=basic_headers)
			if file_details['extension'] in aws_helpers.resizable_types():
				self.upload_resized(file_details)
			sync_helper.sync_server(file_details)
			print "FILE UPLOADED SUCESSFULLY"
			return True
		else:
			print "upload failed"
			multipart.cancel_upload()

	def _upload_part(self, bucket, bucketname, multipart, part_num, source_path, offset, bytes, amount_of_retries=10):
		def _upload(retries_left=amount_of_retries):
			try:
				logging.info('Start uploading part #%d ...' % part_num)
				with FileChunkIO(source_path, 'r', offset=offset, bytes=bytes) as fp:
					multipart.upload_part_from_file(fp=fp, part_num=part_num)
			except Exception, exc:
				if retries_left:
					_upload(retries_left=retries_left - 1)
				else:
					logging.info('... Failed uploading part #%d' % part_num)
					raise exc
			else:
				logging.info('... Uploaded part #%d' % part_num)
		_upload()

	def upload_resized(self, file_details, guess_mimetype=True, force_download=False, policy="public-read"):
		import helpers as aws_helpers
		details = aws_helpers.resize_image(file_details)
		original_path = file_details['path']
		original_name = file_details['name']
		for label in details['web_view_links']:
			file_details['path'] = details['web_view_links'][label]['path']
			file_details['name'] = details['web_view_links'][label]['name']
			new_upload = self.direct_upload(file_details)
			details['web_view_links'][label] = new_upload
			sync_helper.remove_local_copy(file_details)
		file_details['path'] = original_path
		file_details['name'] = original_name
		return True

	def direct_upload(self, file_details):
		import helpers as aws_helpers
		import boto3
		s3 = boto3.resource('s3', aws_access_key_id = self.access_key, aws_secret_access_key = self.access_secret)
		try:
			s3.Bucket(self.bucket_name).upload_file(
				file_details['path'], 
				self.bucket_directory+'/'+file_details['name'], 
				ExtraArgs = {
					'ACL': 'public-read', 
					'ContentType': file_details['content_type'],
					# 'ContentDisposition': 'attachment; filename=' + fileDetails['title'] + fileDetails['extension']
				}
			)
			return aws_helpers.self_link(file_details['name'])
		except Exception, e:
			print "Exception While Normal Upload"
			return True

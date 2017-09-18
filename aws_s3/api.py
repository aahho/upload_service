from app import helpers
import logging
import math
import mimetypes
from multiprocessing import Pool
import os
import copy_reg
import types

from boto.s3.connection import S3Connection
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
		self.parallel_processes = 4

	def upload_large(self, file_details, guess_mimetype=True, force_download=False, policy="public-read"):
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
			print "UPLOADED SUCCESSFULLY"
			multipart.complete_upload()
			key = bucket.get_key(keyname)
			key.set_acl(policy)
			key.content_type = basic_headers['Content-Type']
			key.set_contents_from_filename(source_path, policy=policy, headers=basic_headers)
		else:
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

	def direct_upload():
		pass
from aws_s3 import helpers
from app import helpers as common_helper
from aws_s3.api import Apis
from werkzeug.utils import secure_filename
import os
import threading

def upload(request):
	upload = Apis()
	files = request.files.getlist('files[]')
	if not os.path.isdir(os.environ['UPLOAD_FOLDER']):
		os.mkdir(os.environ['UPLOAD_FOLDER'])
	upload_response = []
	for file in files:
		name = str(common_helper.generate_uuid())+os.path.splitext(secure_filename(file.filename))[1]
		file.save(os.path.join(os.environ['UPLOAD_FOLDER'], name))
		file_details = helpers.fetch_file_details(file, name)
		threading.Thread(target = upload.upload_large, args=(file_details,)).start()
		upload_response.append(file_details)
	return upload_response
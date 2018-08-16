import json
import os
import uuid
import datetime
from django.shortcuts import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def upload(request):
	result = {'error': 1, 'message': '上传失败.'}
	files = request.FILES.get('file', None)
	type = request.GET.get('dir')
	if files:
		result = process_upload(files, type)
	return HttpResponse(json.dumps(result))


def is_suffix_allowed(type, file_suffix):
	suffix_allowed = {}
	suffix_allowed['image'] = ['jpg', 'jpeg', 'bmp', 'gif', 'png']
	suffix_allowed['flash'] = ['swf', 'flv']
	suffix_allowed['media'] = ['swf', 'flv', 'mp3', 'wav', 'wma', 'wmv', 'mid', 'avi', 'mpg', 'asf', 'rm', 'rmvb',
							   'mp4']
	suffix_allowed['file'] = ['doc', 'docx', 'xls', 'xlsx', 'ppt', 'htm', 'html', 'css', 'txt', 'zip', 'rar', 'pdf',
							  'java', 'c', 'py']
	return file_suffix in suffix_allowed[type]


def get_relative_file_path(type):
	today = datetime.datetime.today()
	relative_path = 'upload/%s/%s/%s' % (today.year, today.month, type)
	absolute_path = os.path.join(settings.MEDIA_ROOT, relative_path)
	if not os.path.exists(absolute_path):
		os.makedirs(absolute_path)
	return relative_path


def process_upload(files, type):
	file_types = ['image', 'flash', 'media', 'file']
	if type not in file_types:
		return {'error': 1, 'message': '上传类型不支持[必须是image,flash,media,file].'}
	file_suffix = files.name.split('.')[-1]
	if not is_suffix_allowed(type, file_suffix):
		return {'error': 1, 'message': '扩展名不支持,%s类型不支持扩展名%s.' % (type, file_suffix)}
	relative_path = get_relative_file_path(type)
	filename = str(uuid.uuid1()) + '.' + file_suffix
	basename = os.path.join(settings.MEDIA_ROOT, relative_path)
	file_full_path = os.path.join(basename, filename)
	file_url = settings.MEDIA_URL + relative_path + '/' + filename
	with open(file_full_path, 'wb') as f:
		if files.multiple_chunks() == False:
			f.write(files.file.read())
		else:
			for chunk in files.chunks():
				f.write(chunk)
	return {'error': 0, 'url': file_url}

from django.shortcuts import render
from django.db.models import Q
from repository import models
from utils.initialization import Initialization


# Create your views here.
def search_note(request):
	"""
	查找用户笔记
	:param request:
	:return:
	"""
	if request.method == 'GET':
		keyword = request.GET.get('keyword')
		tag = request.GET.get('tag', '0')
		sort = request.GET.get('sort', '0')
		sort_rule = {
			'0': 'create_time',
			'1': '-create_time',
		}
		sort_select = {
			'0': '按时间升序',
			'1': '按时间降序',
		}
		kwargs = {
			'keyword': keyword,
			'tag': tag,
			'sort': sort
		}
		if keyword:
			notes = models.Notes.objects.filter(
				Q(title__contains=keyword) | Q(summary__contains=keyword) | Q(content__contains=keyword)).filter(
				readlimit_id='1')
			if tag != '0':
				notes = notes.filter(notetag_id=tag)
			notes = notes.order_by(sort_rule[sort])
		else:
			notes = None
		tags = models.NoteTag.objects.all()
		data = Initialization(request, request.session.get('userid')).get_min()
		return render(request, 'search_note.html',
					  {'data': data, 'notes': notes, 'tags': tags, 'sort_select': sort_select, 'kwargs': kwargs})


def search_user(request):
	"""
	查找用户
	:param request:
	:return:
	"""
	if request.method == 'GET':
		keyword = request.GET.get('keyword')
		kwargs = {
			'keyword': keyword,
		}
		if keyword:
			users = models.UserInfo.objects.filter(Q(userid__contains=keyword) | Q(username__contains=keyword))
		else:
			users = None
		data = Initialization(request, request.session.get('userid')).get_min()
		return render(request, 'search_user.html', {'users': users, 'data': data, 'kwargs': kwargs})


def search_activity(request):
	if request.method == 'GET':
		keyword = request.GET.get('keyword')
		kwargs = {
			'keyword': keyword,
		}
		if keyword:
			activities = models.Activities.objects.filter(Q(activity_name__contains=keyword) | Q(activity_id__contains=keyword)|Q(activity_request__contains=keyword)|Q(place__contains=keyword))
		else:
			activities = None
		data = Initialization(request, request.session.get('userid')).get_min()
		return render(request, 'search_activity.html', {'data': data, 'activities': activities, 'kwargs': kwargs})

import json
from django.shortcuts import render, HttpResponse, redirect
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from repository import models
from utils.initialization import Initialization


# Create your views here.
def note_new(request):
	"""
	创建新笔记
	:param request:
	:return:
	"""
	if request.method == 'GET':
		data = Initialization(request, request.session.get('userid')).get_min()
		tags = models.NoteTag.objects.all()
		limits = models.ReadLimit.objects.all()
		return render(request, 'note_new.html', {'data': data, 'tags': tags, 'limits': limits})
	if request.method == 'POST':
		ret = {'status': 'fail', 'error': None}
		userid = request.session.get('userid')
		if userid:
			note_dict = {
				'title': request.POST.get('title'),
				'summary': request.POST.get('summary'),
				'notetag_id': request.POST.get('tag'),
				'readlimit_id': request.POST.get('limit'),
				'content': request.POST.get('content'),
				'note_user_id': userid
			}
			if note_dict['title'].isspace() or note_dict['title'] == '':
				ret['error'] = '标题不能为空.'
			elif note_dict['content'] == '':
				ret['error'] = '笔记内容不能为空.'
			else:
				try:
					with transaction.atomic():
						models.Notes.objects.create(**note_dict)
						ret['status'] = 'success'
				except Exception as e:
					ret['error'] = e.args
		else:
			ret['status'] = 'unauthorized'
		return HttpResponse(json.dumps(ret))


def note_detail(request, noteid):
	"""
	查看笔记详情
	:param request:
	:param noteid: 笔记id
	:return:
	"""
	if request.method == 'GET':
		is_author = False
		is_fond = False
		userid = request.session.get('userid')
		data = Initialization(request, request.session.get('userid')).get_min()
		note = models.Notes.objects.get(noteid=noteid)
		if userid == note.note_user_id:
			is_author = True
		fond = models.UserFondNotes.objects.filter(noteid_id=noteid, userid_id=userid)
		if fond:
			is_fond = True
		return render(request, 'note_detail.html',
					  {'data': data, 'note': note, 'is_author': is_author, 'is_fond': is_fond})


def note_edit(request, noteid):
	"""
	编辑笔记
	:param request:
	:param noteid: 笔记id
	:return:
	"""
	if request.method == 'GET':
		data = Initialization(request, request.session.get('userid')).get_min()
		note = models.Notes.objects.get(noteid=noteid)
		tags = models.NoteTag.objects.all()
		limits = models.ReadLimit.objects.all()
		if note.note_user_id == request.session.get('userid'):
			return render(request, 'note_edit.html', {'data': data, 'note': note, 'tags': tags, 'limits': limits})
		else:
			return redirect('/login/')
	if request.method == 'POST':
		ret = {'status': 'fail', 'error': None}
		userid = request.session.get('userid')
		if userid == request.POST.get('noteuser_id'):
			note_dict = {
				'title': request.POST.get('title'),
				'summary': request.POST.get('summary'),
				'notetag_id': request.POST.get('tag'),
				'readlimit_id': request.POST.get('limit'),
				'content': request.POST.get('content'),
				'note_user_id': userid,
				'last_edit_time': timezone.now()
			}
			if note_dict['title'].isspace() or note_dict['title'] == '':
				ret['error'] = '标题不能为空.'
			elif note_dict['content'] == '':
				ret['error'] = '笔记内容不能为空.'
			else:
				try:
					with transaction.atomic():
						models.Notes.objects.filter(noteid=request.POST.get('noteid')).update(**note_dict)
						ret['status'] = 'success'
				except Exception as e:
					ret['error'] = e.args
		else:
			ret['status'] = 'unauthorized'
		return HttpResponse(json.dumps(ret))


@csrf_exempt
def note_delete(request):
	"""
	删除笔记
	:param request:
	:return:
	"""
	if request.method == 'POST':
		ret = {'status': 'fail', 'error': None}
		noteid = request.POST.get('noteid')
		note = models.Notes.objects.get(noteid=noteid)
		if request.session.get('userid') == note.note_user_id:
			try:
				with transaction.atomic():
					models.Notes.objects.filter(noteid=noteid).delete()
					ret['status'] = 'success'
			except Exception as e:
				ret['error'] = e.args
		else:
			ret['status'] = 'unauthorized'
		return HttpResponse(json.dumps(ret))


@csrf_exempt
def fond(request):
	"""
	收藏笔记操作
	:param request:
	:return:
	"""
	if request.method == 'POST':
		ret = {'status': 'fail', 'error': None}
		noteid = request.POST.get('noteid')
		note_user = request.POST.get('userid')
		userid = request.session.get('userid')
		if userid:
			if userid == note_user:
				ret['error'] = '不能收藏自己的笔记.'
			else:
				try:
					with transaction.atomic():
						fond = models.UserFondNotes.objects.filter(noteid_id=noteid, userid_id=userid)
						if fond:
							ret['error'] = '已收藏笔记,重复操作.'
						else:
							models.UserFondNotes.objects.create(noteid_id=noteid, userid_id=userid)
							ret['status'] = 'success'
				except Exception as e:
					ret['error'] = e.args
		else:
			ret['status'] = 'unauthorized'
		return HttpResponse(json.dumps(ret))


@csrf_exempt
def cancel_fond(request):
	"""
	取消收藏笔记
	:param request:
	:return:
	"""
	if request.method == 'POST':
		ret = {'status': 'fail', 'error': None}
		noteid = request.POST.get('noteid')
		userid = request.session.get('userid')
		if userid:
			try:
				with transaction.atomic():
					models.UserFondNotes.objects.filter(noteid_id=noteid, userid_id=userid).delete()
					ret['status'] = 'success'
			except Exception as e:
				ret['error'] = e.args
		else:
			ret['status'] = 'unauthorized'
		return HttpResponse(json.dumps(ret))

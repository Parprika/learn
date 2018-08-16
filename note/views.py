import json
from django.shortcuts import render, HttpResponse
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from repository import models


# Create your views here.
def user_note(request, userid):
	if request.method == 'GET':
		note_obj = models.Notes.objects.filter(note_user=userid)
		user_obj = models.UserInfo.objects.filter(userid=userid).first()
		return render(request, 'user_note.html', {'note_obj': note_obj, 'user_obj': user_obj})


def note_new(request):
	"""
	创建新笔记
	:param request:
	:return:
	"""
	if request.method == 'GET':
		tag_obj = models.NoteTag.objects.all()
		limit_obj = models.ReadLimit.objects.all()
		return render(request, 'note_new.html', {'tag_obj': tag_obj, 'limit_obj': limit_obj})
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
						note_count = models.UserInfo.objects.get(userid=userid).notes_count
						models.UserInfo.objects.filter(userid=userid).update(notes_count=note_count + 1)
						ret['status'] = 'success'
						ret['userid'] = userid
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
		note_obj = models.Notes.objects.get(noteid=noteid)
		if userid == note_obj.note_user_id:
			is_author = True
		else:
			read_count = models.Notes.objects.get(noteid=noteid).read_count
			models.Notes.objects.filter(noteid=noteid).update(read_count=read_count + 1)
		fond_obj = models.UserFondNotes.objects.filter(noteid_id=noteid, userid_id=userid)
		if fond_obj:
			is_fond = True
		return render(request, 'note_detail.html', {'note_obj': note_obj, 'is_author': is_author, 'is_fond': is_fond})


def note_edit(request, noteid):
	"""
	编辑笔记
	:param request:
	:param noteid: 笔记id
	:return:
	"""
	if request.method == 'GET':
		note_obj = models.Notes.objects.get(noteid=noteid)
		tag_obj = models.NoteTag.objects.all()
		limit_obj = models.ReadLimit.objects.all()
		return render(request, 'note_edit.html', {'note_obj': note_obj, 'tag_obj': tag_obj, 'limit_obj': limit_obj})
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
						ret['userid'] = userid
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
		note_obj = models.Notes.objects.get(noteid=noteid)
		if request.session.get('userid') == note_obj.note_user_id:
			try:
				with transaction.atomic():
					models.Notes.objects.filter(noteid=noteid).delete()
					note_count = models.UserInfo.objects.get(userid=note_obj.note_user_id).notes_count
					models.UserInfo.objects.filter(userid=note_obj.note_user_id).update(notes_count=note_count - 1)
					ret['status'] = 'success'
			except Exception as e:
				ret['error'] = e.args
		else:
			ret['status'] = 'unauthorized'
		return HttpResponse(json.dumps(ret))


def note_explore(request):
	"""
	查找用户笔记
	:param request:
	:return:
	"""
	if request.method == 'GET':
		keyword = request.GET.get('keyword')
		tag = request.GET.get('tag_id', '0')
		sort = request.GET.get('sort_by', '0')
		sort_rule = {
			'0': 'create_time',
			'1': '-create_time',
			'2': 'fond_count',
			'3': '-fond_count',
			'4': 'read_count',
			'5': '-read_count'
		}
		sort_select = {
			'0': '按时间升序',
			'1': '按时间降序',
			'2': '按收藏量升序',
			'3': '按收藏量降序',
			'4': '按阅读量升序',
			'5': '按阅读量降序'
		}
		kwargs = {
			'keyword': keyword,
			'tag_id': tag,
			'sort_by': sort
		}
		if keyword:
			note_obj = models.Notes.objects.filter(
				Q(title__contains=keyword) | Q(summary__contains=keyword) | Q(content__contains=keyword)).filter(
				readlimit_id='1')
		else:
			note_obj = models.Notes.objects.filter(readlimit_id='1')
		if tag != '0':
			note_obj = note_obj.filter(notetag_id=tag)
		note_obj = note_obj.order_by(sort_rule[sort])
		tag_obj = models.NoteTag.objects.all()
		return render(request, 'note_explore.html',
					  {'note_obj': note_obj, 'tag_obj': tag_obj, 'sort_select': sort_select, 'kwargs': kwargs})


def user_fond_note(request, userid):
	"""
	查看收藏笔记
	:param request:
	:param userid: 用户学号
	:return:
	"""
	note_obj = models.UserFondNotes.objects.filter(userid_id=userid).order_by('-fond_time')
	user_obj = models.UserInfo.objects.get(userid=userid)
	return render(request, 'note_fond.html', {'note_obj': note_obj, 'user': user_obj})


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
						fond_obj = models.UserFondNotes.objects.filter(noteid_id=noteid, userid_id=userid)
						if fond_obj:
							ret['error'] = '已收藏笔记,重复操作.'
						else:
							models.UserFondNotes.objects.create(noteid_id=noteid, userid_id=userid)
							note_fond_count = models.Notes.objects.get(noteid=noteid).fond_count
							models.Notes.objects.filter(noteid=noteid).update(fond_count=note_fond_count + 1)
							user_fond_count = models.UserInfo.objects.get(userid=userid).fond_notes_count
							models.UserInfo.objects.filter(userid=userid).update(fond_notes_count=user_fond_count + 1)
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
		note_user = request.POST.get('userid')
		userid = request.session.get('userid')
		if userid:
			try:
				with transaction.atomic():
					models.UserFondNotes.objects.filter(noteid_id=noteid, userid_id=userid).delete()
					note_fond_count = models.Notes.objects.get(noteid=noteid).fond_count
					models.Notes.objects.filter(noteid=noteid).update(fond_count=note_fond_count - 1)
					user_fond_count = models.UserInfo.objects.get(userid=userid).fond_notes_count
					models.UserInfo.objects.filter(userid=userid).update(fond_notes_count=user_fond_count - 1)
					ret['status'] = 'success'
			except Exception as e:
				ret['error'] = e.args
		else:
			ret['status'] = 'unauthorized'
		return HttpResponse(json.dumps(ret))

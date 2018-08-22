import json
from django.shortcuts import render, HttpResponse, redirect
from repository import models
from utils.initialization import Initialization


# Create your views here.
def login(request):
	if request.method == 'GET':
		return render(request, 'login.html')
	elif request.method == 'POST':
		error = {'status': True, 'error_message': None}
		userid = request.POST.get('userid')
		password = request.POST.get('password')
		if userid and password:
			userinfo = models.UserInfo.objects.filter(userid=userid, password=password).first()
			if not userinfo:
				error['error_message'] = '学号或密码错误,请重试.'
			else:
				error['status'] = False
				request.session['userid'] = userid
				request.session['username'] = userinfo.username
		elif userid == '':
			error['error_message'] = '学号不能为空,请重试.'
		elif password == '':
			error['error_message'] = '密码不能为空,请重试.'
		return HttpResponse(json.dumps(error))


def register(request):
	if request.method == 'GET':
		return render(request, 'register.html')
	elif request.method == 'POST':
		error = {'status': True, 'error_message': None}
		information_dict = {
			'userid': request.POST.get('userid'),
			'username': request.POST.get('username'),
			'gender': request.POST.get('gender'),
			'major': request.POST.get('major'),
			'password': request.POST.get('password')
		}
		if information_dict['userid'].isspace() or information_dict['username'].isspace() or information_dict[
			'gender'].isspace() or information_dict['major'].isspace() or information_dict['password'].isspace() or \
				information_dict['userid'] == '' or information_dict['username'] == '' or information_dict[
			'gender'] == '' or information_dict['major'] == '' or information_dict['password'] == '':
			error['error_message'] = '信息不完整.'
		elif not information_dict['gender'] == '男' and not information_dict['gender'] == '女':
			error['error_message'] = '性别只能是"男"或"女".'
		else:
			userinfo = models.UserInfo.objects.filter(userid=information_dict['userid'])
			if userinfo:
				error['error_message'] = '帐号已被注册.'
			else:
				error['status'] = False
				userinfo = models.UserInfo.objects.create(**information_dict)
				request.session['userid'] = userinfo.userid
				request.session['username'] = userinfo.username
		return HttpResponse(json.dumps(error))


def logout(request):
	del request.session['userid']
	del request.session['username']
	return redirect('/login/')


def index(request):
	if request.method == 'GET':
		data = Initialization(request, request.session.get('userid')).get_min()
		return render(request, 'index.html', {'data': data})


def user_note(request, userid):
	if request.method == 'GET':
		data = Initialization(request, userid).get_all()
		if userid == request.session.get('userid'):
			notes = models.Notes.objects.filter(note_user=userid)
		else:
			notes = models.Notes.objects.filter(note_user=userid, readlimit='1')
		return render(request, 'user_note.html', {'data': data, 'notes': notes})


def user_fond(request, userid):
	if request.method == 'GET':
		data = Initialization(request, userid).get_all()
		notes = models.UserFondNotes.objects.filter(userid=userid)
		return render(request, 'note_fond.html', {'data': data, 'notes': notes})


def user_follows(request, userid):
	if request.method == 'GET':
		data = Initialization(request, userid).get_all()
		follows = models.UserFans.objects.filter(follower=userid)
		return render(request, 'follows.html', {'data': data, 'follows': follows})


def user_fans(request, userid):
	if request.method == 'GET':
		data = Initialization(request, userid).get_all()
		fans = models.UserFans.objects.filter(user=userid)
		return render(request, 'fans.html', {'data': data, 'fans': fans})


def user_activity(request, userid):
	if request.method == 'GET':
		data = Initialization(request, userid).get_all()
		activities = models.ActivityMembers.objects.filter(member=userid)
		return render(request, 'user_activity.html', {'data': data, 'activities': activities})

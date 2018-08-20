import json
from django.shortcuts import render, HttpResponse, redirect
from utils.qzsystem import QZSystem
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
			qz = QZSystem(userid, password)
			if not qz.login():
				error['error_message'] = '学号或密码错误,请重试.'
			else:
				error['status'] = False
				userinfo = models.UserInfo.objects.filter(userid=userid).first()
				if not userinfo:
					information_list = qz.get_information()
					information_dict = {
						'userid': information_list[7],
						'username': information_list[0],
						'gender': information_list[1],
						'institute': information_list[3],
						'major': information_list[4],
						'native_place': information_list[2]
					}
					request.session['userid'] = userid
					request.session['username'] = information_dict['username']
					# print(information_dict)
					models.UserInfo.objects.create(**information_dict)
				request.session['userid'] = userid
				request.session['username'] = userinfo.username
		elif userid == '':
			error['error_message'] = '学号不能为空,请重试.'
		elif password == '':
			error['error_message'] = '密码不能为空,请重试.'
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

def user_group(request, userid):
	if request.method == 'GET':
		data = Initialization(request, userid).get_all()
		groups = models.GroupMembers.objects.filter(member=userid)
		return render(request, 'user_group.html', {'data': data, 'groups': groups})

def user_activity(request, userid):
	if request.method == 'GET':
		data = Initialization(request, userid).get_all()
		return render(request, 'user_group.html', {'data': data})


def message(request, userid):
	if request.method == 'GET':
		data = Initialization(request, userid).get_min()
		return render(request, 'index.html', {'data': data})


def notice(request, userid):
	if request.method == 'GET':
		data = Initialization(request, userid).get_min()
		return render(request, 'index.html', {'data': data})

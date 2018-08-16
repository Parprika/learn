import json
from django.shortcuts import render, redirect, HttpResponse
from utils.qzsystem import QZSystem
from repository import models


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
				request.session['userid'] = userid
				request.session['password'] = password
				userinfo = models.UserInfo.objects.filter(userid=userid)
				if userinfo:
					pass
				else:
					information_list = qz.get_information()
					information_dict = {
						'userid': information_list[7],
						'username': information_list[0],
						'gender': information_list[1],
						'institute': information_list[3],
						'major': information_list[4],
						'native_place': information_list[2]
					}
					# print(information_dict)
					models.UserInfo.objects.create(**information_dict)
		elif userid == '':
			error['error_message'] = '学号不能为空,请重试.'
		elif password == '':
			error['error_message'] = '密码不能为空,请重试.'
		return HttpResponse(json.dumps(error))


def index(request):
	if request.method == 'GET':
		userid = request.session.get('userid')
		password = request.session.get('password')
		if userid and password:
			userinfo = models.UserInfo.objects.filter(userid=userid)
			if userinfo:
				return render(request, 'index.html', {'userinfo': userinfo, 'userid': userid})
			else:
				return redirect('/login/')
		else:
			return redirect('/login/')

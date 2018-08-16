import json
from django.shortcuts import render, HttpResponse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from repository import models


# Create your views here.
def follows(request, userid):
	"""
	获取关注人
	:param request:
	:param userid: 用户学号
	:return:
	"""
	if request.method == 'GET':
		follows_obj = models.UserFans.objects.filter(follower=userid).order_by('-follow_time')
		user_obj = models.UserInfo.objects.filter(userid=userid).first()
		return render(request, 'follows.html', {'follows_obj': follows_obj, 'user_obj': user_obj})


def fans(request, userid):
	"""
	获取粉丝
	:param request:
	:param userid: 用户学号
	:return:
	"""
	if request.method == 'GET':
		fans_obj = models.UserFans.objects.filter(user=userid).order_by('-follow_time')
		user_obj = models.UserInfo.objects.filter(userid=userid).first()
		return render(request, 'fans.html', {'fans_obj': fans_obj, 'user_obj': user_obj})


def search(request):
	"""
	按学号或姓名进行模糊搜索
	:param request:
	:return:
	"""
	if request.method == 'POST':
		ret = {
			'status': True,
			'count': 0,
			'data': None
		}
		user_list = []
		keyword = request.POST.get('keyword')
		if request.POST.get('select') == 'userid':
			user_obj = models.UserInfo.objects.filter(userid__contains=keyword)
		elif request.POST.get('select') == 'username':
			user_obj = models.UserInfo.objects.filter(username__contains=keyword)
		if user_obj:
			for user in user_obj:
				user_dict = {
					'userid': user.userid,
					'username': user.username,
					'gender': user.gender,
					'institute': user.institute,
					'major': user.major,
					'is_followed': False
				}
				relationship_obj = models.UserFans.objects.filter(user=user.userid,
																  follower=request.session.get('userid'))
				if relationship_obj:
					user_dict['is_followed'] = True
				user_list.append(user_dict)
			ret['count'] = len(user_list)
			ret['data'] = user_list
		else:
			ret['status'] = False
		return HttpResponse(json.dumps(ret))


@csrf_exempt
def follow(request):
	"""
	关注用户操作
	:param request:
	:return:
	"""
	if request.method == 'POST':
		ret = {'status': 'success', 'data': None}
		userid = request.session.get('userid')
		if userid:
			followid = request.POST.get('followid')
			if userid == followid:
				ret['status'] = 'fail'
				ret['data'] = '不能关注自己.'
			else:
				try:
					with transaction.atomic():
						follow_obj = models.UserFans.objects.filter(user_id=followid, follower_id=userid)
						if follow_obj:
							ret['status'] = 'fail'
							ret['data'] = '已关注,重复操作.'
						else:
							models.UserFans.objects.create(user_id=followid, follower_id=userid)
							fans_count = models.UserInfo.objects.get(userid=followid).fans_count
							models.UserInfo.objects.filter(userid=followid).update(fans_count=fans_count + 1)
							follow_count = models.UserInfo.objects.get(userid=userid).follow_count
							models.UserInfo.objects.filter(userid=userid).update(follow_count=follow_count + 1)
				except Exception as e:
					ret['status'] = 'fail'
					ret['data'] = e.args
		else:
			ret['status'] = 'unauthorized'
		return HttpResponse(json.dumps(ret))


@csrf_exempt
def cancel_follow(request):
	"""
	取消关注操作
	:param request:
	:return:
	"""
	if request.method == 'POST':
		ret = {'status': 'success', 'data': None}
		userid = request.session.get('userid')
		if userid:
			followid = request.POST.get('followid')
			try:
				with transaction.atomic():
					models.UserFans.objects.filter(user_id=followid, follower_id=userid).delete()
					fans_count = models.UserInfo.objects.get(userid=followid).fans_count
					models.UserInfo.objects.filter(userid=followid).update(fans_count=fans_count - 1)
					follow_count = models.UserInfo.objects.get(userid=userid).follow_count
					models.UserInfo.objects.filter(userid=userid).update(follow_count=follow_count - 1)
			except Exception as e:
				ret['status'] = 'fail'
				ret['data'] = e.args
		return HttpResponse(json.dumps(ret))

import json
from django.shortcuts import HttpResponse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from repository import models


@csrf_exempt
def follow(request):
	"""
	关注用户操作
	:param request:
	:return:
	"""
	if request.method == 'POST':
		ret = {'status': 'fail', 'data': None}
		userid = request.session.get('userid')
		if userid:
			followid = request.POST.get('followid')
			if userid == followid:
				ret['data'] = '非法操作.'
			else:
				follow = models.UserFans.objects.filter(user_id=followid, follower_id=userid)
				if follow:
					ret['status'] = 'success'
				else:
					try:
						with transaction.atomic():
							models.UserFans.objects.create(user_id=followid, follower_id=userid)
							fans_count = models.UserInfo.objects.get(userid=followid).fans_count
							models.UserInfo.objects.filter(userid=followid).update(fans_count=fans_count + 1)
							follow_count = models.UserInfo.objects.get(userid=userid).follow_count
							models.UserInfo.objects.filter(userid=userid).update(follow_count=follow_count + 1)
							ret['status'] = 'success'
					except Exception as e:
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
		ret = {'status': 'fail', 'data': None}
		userid = request.session.get('userid')
		if userid:
			followid = request.POST.get('followid')
			if userid == followid:
				ret['data'] = '非法操作.'
			else:
				try:
					with transaction.atomic():
						models.UserFans.objects.filter(user_id=followid, follower_id=userid).delete()
						fans_count = models.UserInfo.objects.get(userid=followid).fans_count
						models.UserInfo.objects.filter(userid=followid).update(fans_count=fans_count - 1)
						follow_count = models.UserInfo.objects.get(userid=userid).follow_count
						models.UserInfo.objects.filter(userid=userid).update(follow_count=follow_count - 1)
						ret['status'] = 'success'
				except Exception as e:
					ret['data'] = e.args
		else:
			ret['status'] = 'unauthorized'
		return HttpResponse(json.dumps(ret))

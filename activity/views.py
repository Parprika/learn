import json
from django.shortcuts import render, HttpResponse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from repository import models
from utils.initialization import Initialization


# Create your views here.
def activity_new(request):
	"""
	创建新活动
	:param request:
	:return:
	"""
	if request.method == 'GET':
		data = Initialization(request, request.session.get('userid')).get_min()
		activity_tags = models.ActivityTag.objects.all()
		return render(request, 'activity_new.html', {'data': data, 'activity_tags': activity_tags})
	if request.method == 'POST':
		ret = {'status': 'fail', 'error': None}
		userid = request.session.get('userid')
		if userid:
			activity_dict = {
				'activity_name': request.POST.get('activity_name'),
				'activity_request': request.POST.get('activity_content'),
				'start_time': request.POST.get('start_time'),
				'end_time': request.POST.get('end_time'),
				'place': request.POST.get('activity_place'),
				'activity_tag_id': request.POST.get('activity_tag'),
				'leader_id': userid
			}
			if activity_dict['activity_name'].isspace() or activity_dict['activity_name'] == "":
				ret['error'] = '活动名称不能为空.'
			elif activity_dict['activity_request'].isspace() or activity_dict['activity_request'] == "":
				ret['error'] = '活动要求不能为空.'
			elif activity_dict['start_time'] == "":
				ret['error'] = '开始时间不能为空.'
			elif activity_dict['end_time'] == "":
				ret['error'] = '结束时间不能为空.'
			elif activity_dict['start_time'] > activity_dict['end_time']:
				ret['error'] = '活动时间不合法.'
			elif activity_dict['place'].isspace() or activity_dict['place'] == "":
				ret['error'] = '活动地点不能为空.'
			else:
				try:
					with transaction.atomic():
						activity = models.Activities.objects.create(**activity_dict)
						models.ActivityMembers.objects.create(activity_id=activity.activity_id, member_id=userid,
															  identity=1)
						ret['status'] = 'success'
						ret['activity'] = activity.activity_id
				except Exception as e:
					ret['error'] = e.args
		else:
			ret['status'] = 'unauthorized'
		return HttpResponse(json.dumps(ret))


def activity_detail(request, activity_id):
	"""
	查看活动详情
	:param request:
	:param groupid:
	:return:
	"""
	is_leader = False
	is_in = False
	is_end = False
	data = Initialization(request, request.session.get('userid')).get_min()
	signs = models.ActivitySign.objects.filter(activity_id=activity_id).order_by('-time')
	activity = models.Activities.objects.get(activity_id=activity_id)
	members = models.ActivityMembers.objects.filter(activity=activity_id)
	if members.filter(member=request.session.get('userid')):
		is_in = True
	if request.session.get('userid') == activity.leader_id:
		is_leader = True
	if activity.status == 1:
		is_end = True
	return render(request, 'activity_detail.html', {
		'data': data, 'activity': activity, 'members': members, 'signs': signs, 'is_leader': is_leader, 'is_in': is_in,
		'is_end': is_end
	})


@csrf_exempt
def end_activity(request):
	"""
	结束活动
	:param request:
	:return:
	"""
	if request.method == 'POST':
		ret = {'status': 'fail', 'error': None}
		activity_id = request.POST.get('activity')
		activity = models.Activities.objects.filter(activity_id=activity_id).first()
		userid = request.session.get('userid')
		if userid:
			if userid == activity.leader_id:
				models.Activities.objects.filter(activity_id=activity_id).update(status=1)
				ret['status'] = 'success'
			else:
				ret['error'] = '权限不足.'
		else:
			ret['status'] = 'unauthorized'
		return HttpResponse(json.dumps(ret))


@csrf_exempt
def join_activity(request):
	"""
	参加活动
	:param request:
	:return:
	"""
	if request.method == 'POST':
		ret = {'status': 'fail', 'error': None}
		activity_id = request.POST.get('activity')
		userid = request.session.get('userid')
		is_in = models.ActivityMembers.objects.filter(activity_id=activity_id, member_id=userid)
		if userid:
			if is_in:
				ret['error'] = '已加入该活动.'
			else:
				models.ActivityMembers.objects.create(activity_id=activity_id, member_id=userid)
				ret['status'] = 'success'
		else:
			ret['status'] = 'unauthorized'
		return HttpResponse(json.dumps(ret))


@csrf_exempt
def quit_activity(request):
	"""
	退出活动
	:param request:
	:return:
	"""
	if request.method == 'POST':
		ret = {'status': 'fail', 'error': None}
		activity_id = request.POST.get('activity')
		userid = request.session.get('userid')
		is_in = models.ActivityMembers.objects.filter(activity_id=activity_id, member_id=userid)
		if userid:
			if is_in:
				models.ActivityMembers.objects.filter(activity_id=activity_id, member_id=userid).delete()
				ret['status'] = 'success'
			else:
				ret['error'] = '未加入该活动.'
		else:
			ret['status'] = 'unauthorized'
		return HttpResponse(json.dumps(ret))


def sign(request, activity_id):
	"""
	活动打卡
	:param request:
	:param activity_id:
	:return:
	"""
	if request.method == 'GET':
		data = Initialization(request, request.session.get('userid'))
		return render(request, 'activity_sign.html', {'activity': activity_id, 'data': data})
	if request.method == 'POST':
		ret = {'status': 'fail', 'error': None}
		userid = request.session.get('userid')
		is_in = models.ActivityMembers.objects.filter(activity_id=activity_id, member_id=userid)
		if userid:
			content = request.POST.get('content')
			if content == "":
				ret['error'] = '打卡内容不能为空.'
			elif is_in:
				models.ActivitySign.objects.create(activity_id=activity_id, user_id=userid, content=content)
				ret['status'] = 'success'
			else:
				ret['error'] = '未加入该活动.'
		else:
			ret['status'] = 'unauthorized'
		return HttpResponse(json.dumps(ret))


def members(request, activity_id):
	"""
	活动参与者
	:param request:
	:param activity_id:
	:return:
	"""
	is_leader = False
	is_in = False
	is_end = False
	data = Initialization(request, request.session.get('userid')).get_min()
	members = models.ActivityMembers.objects.filter(activity_id=activity_id).order_by('-add_time')
	activity = models.Activities.objects.get(activity_id=activity_id)
	if members.filter(member=request.session.get('userid')):
		is_in = True
	if request.session.get('userid') == activity.leader_id:
		is_leader = True
	if activity.status == 1:
		is_end = True
	return render(request, 'activity_members.html', {
		'data': data, 'activity': activity, 'members': members, 'is_leader': is_leader, 'is_in': is_in,
		'is_end': is_end
	})

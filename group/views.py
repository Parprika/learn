import json
from django.shortcuts import render, HttpResponse
from django.db import transaction
from repository import models
from utils.initialization import Initialization


# Create your views here.
def group_new(request):
	"""
	创建新小组
	:param request:
	:return:
	"""
	if request.method == 'GET':
		data = Initialization(request, request.session.get('userid'))
		group_tags = models.GroupTag.objects.all()
		return render(request, 'group_new.html', {'data': data, 'group_tags': group_tags})
	if request.method == 'POST':
		ret = {'status': 'fail', 'error': None}
		userid = request.session.get('userid')
		if userid:
			group_dict = {
				'group_name': request.POST.get('group_name'),
				'introduction': request.POST.get('introduction'),
				'grouptag_id': request.POST.get('group_tag'),
				'group_owner_id': userid
			}
			if group_dict['group_name'].isspace() or group_dict['group_name'] == "":
				ret['error'] = '小组组名不能为空.'
			# else:
			# 	try:
			# 		with transaction.atomic():
			# 			group = models.Groups.objects.create(**group_dict)
			# 			group_count = models.UserInfo.objects.get(userid=userid).groups_count
			# 			models.UserInfo.objects.filter(userid=userid).update(groups_count=group_count + 1)
			# 			models.GroupMembers.objects.create(group=group, member_id=userid, identity_id='2')
			# 			ret['status'] = 'success'
			# 			ret['group'] = group.groupid
			# 	except Exception as e:
			# 		ret['error'] = e.args
		else:
			ret['status'] = 'unauthorized'
		return HttpResponse(json.dumps(ret))


def group_detail(request, groupid):
	"""
	查看小组详情
	:param request:
	:param groupid: 小组id
	:return:
	"""
	data = Initialization(request, request.session.get('userid'))
	group = models.Groups.objects.get(groupid=groupid)
	members = models.GroupMembers.objects.filter(group=groupid)
	activity = models.Activities.objects.filter(group=groupid, status='1').first()
	if members.filter(member=request.session.get('userid')):
		is_in = True
	else:
		is_in = False
	if request.session.get('userid') == group.group_owner_id:
		is_creator = True
	else:
		is_creator = False
	return render(request, 'group_detail.html', {'data': data, 'group': group, 'members': members, 'activity': activity, 'is_creator': is_creator, 'is_in': is_in})

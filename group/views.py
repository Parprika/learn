import json
from django.shortcuts import render, HttpResponse
from django.db import transaction
from repository import models


# Create your views here.
def user_group(request, userid):
	user_group_obj = models.Groups.objects.filter(group_owner_id=userid)
	group_obj = models.GroupMembers.objects.filter(member=userid)
	user_obj = models.UserInfo.objects.get(userid=userid)
	return render(request, 'user_group.html', {'user_group_obj': user_group_obj, 'group_obj': group_obj, 'user_obj': user_obj})


def group_new(request):
	"""
	创建新小组
	:param request:
	:return:
	"""
	if request.method == 'GET':
		group_tag_obj = models.GroupTag.objects.all()
		return render(request, 'group_new.html', {'group_tag_obj': group_tag_obj})
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
			if group_dict['group_name'] == "":
				ret['error'] = '小组组名不能为空.'
			try:
				with transaction.atomic():
					models.Groups.objects.create(**group_dict)
					group_count = models.UserInfo.objects.get(userid=userid).groups_count
					models.UserInfo.objects.filter(userid=userid).update(groups_count=group_count + 1)
					ret['status'] = 'success'
					ret['userid'] = userid
			except Exception as e:
				ret['error'] = e.args
		else:
			ret['status'] = 'group_tag'
		return HttpResponse(json.dumps(ret))


def group_detail(request, groupid):
	"""
	查看小组详情
	:param request:
	:param groupid: 小组id
	:return:
	"""
	group_obj = models.Groups.objects.get(groupid=groupid)
	member_obj = models.GroupMembers.objects.filter(group=groupid)
	if member_obj.filter(member=request.session.get('userid')):
		is_in = True
	else:
		is_in = False
	if request.session.get('userid') == group_obj.group_owner_id:
		is_creator = True
	else:
		is_creator = False
	return render(request, 'group_detail.html', {'group_obj': group_obj, 'member_obj': member_obj, 'is_creator': is_creator, 'is_in': is_in})

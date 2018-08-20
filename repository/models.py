from django.db import models


# Create your models here.
class UserInfo(models.Model):
	"""
	用户信息
	"""
	userid = models.CharField(primary_key=True, max_length=32, verbose_name='学号')
	username = models.CharField(max_length=32, verbose_name='姓名')
	gender = models.CharField(max_length=32, verbose_name='性别')
	institute = models.CharField(max_length=32, verbose_name='所属学院')
	major = models.CharField(max_length=32, verbose_name='专业')
	native_place = models.CharField(max_length=32, verbose_name='籍贯')
	follow_count = models.IntegerField(default=0, verbose_name='关注数')
	fans_count = models.IntegerField(default=0, verbose_name='粉丝数')
	notes_count = models.IntegerField(default=0, verbose_name='笔记数量')
	fond_notes_count = models.IntegerField(default=0, verbose_name='收藏笔记数量')
	groups_count = models.IntegerField(default=0, verbose_name='小组数量')


class UserFans(models.Model):
	"""
	互粉关系
	"""
	relationship_id = models.BigAutoField(primary_key=True)
	user = models.ForeignKey(to='UserInfo', to_field='userid', on_delete='CASCADE', related_name='users',
							 verbose_name='用户')
	follower = models.ForeignKey(to='UserInfo', to_field='userid', on_delete='CASCADE', related_name='followers',
								 verbose_name='粉丝')
	follow_time = models.DateTimeField(auto_now_add=True, verbose_name='关注时间')


class Notes(models.Model):
	"""
	笔记
	"""
	noteid = models.BigAutoField(primary_key=True)
	title = models.CharField(max_length=64, verbose_name='标题')
	summary = models.CharField(max_length=128, null=True, verbose_name='简介')
	content = models.TextField(verbose_name='正文')
	fond_count = models.IntegerField(default=0, verbose_name='收藏量')
	read_count = models.IntegerField(default=0, verbose_name='阅读量')
	create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
	last_edit_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
	notetag = models.ForeignKey(to='NoteTag', to_field='notetag_id', default='1', on_delete='CASCADE',
								verbose_name='笔记标签')
	readlimit = models.ForeignKey(to='ReadLimit', to_field='limitid', default='1', on_delete='CASCADE',
								  verbose_name='阅读权限')
	note_user = models.ForeignKey(to='UserInfo', to_field='userid', on_delete='CASCADE', verbose_name='作者')


class NoteTag(models.Model):
	"""
	笔记标签
	"""
	notetag_id = models.BigAutoField(primary_key=True)
	notetag_name = models.CharField(max_length=32, verbose_name='笔记标签')


class ReadLimit(models.Model):
	"""
	笔记阅读权限
	"""
	limitid = models.BigAutoField(primary_key=True)
	limit_type = models.CharField(max_length=32, verbose_name='阅读权限')


class UserFondNotes(models.Model):
	"""
	用户收藏
	"""
	fondid = models.BigAutoField(primary_key=True)
	userid = models.ForeignKey(to='UserInfo', to_field='userid', on_delete='CASCADE', verbose_name='学号')
	noteid = models.ForeignKey(to='Notes', to_field='noteid', on_delete='CASCADE', verbose_name='笔记')
	fond_time = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')


class Groups(models.Model):
	"""
	小组
	"""
	groupid = models.BigAutoField(primary_key=True)
	group_name = models.CharField(max_length=32, verbose_name='小组组名')
	introduction = models.CharField(max_length=128, null=True, verbose_name='小组简介')
	group_owner = models.ForeignKey(to='UserInfo', to_field='userid', on_delete='CASCADE', verbose_name='创建者')
	member_count = models.IntegerField(default=1, verbose_name='组员数量')
	member_limit = models.IntegerField(default=50, verbose_name='组员上限')
	integral = models.IntegerField(default=0, verbose_name='小组积分')
	activities_count = models.IntegerField(default=1, verbose_name='历史小组活动数量')
	grouptag = models.ForeignKey(to='GroupTag', to_field='grouptag_id', on_delete='CASCADE', verbose_name='小组标签')
	create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class GroupTag(models.Model):
	"""
	小组标签
	"""
	grouptag_id = models.BigAutoField(primary_key=True)
	grouptag_name = models.CharField(max_length=32, verbose_name='小组标签')


class GroupMembers(models.Model):
	"""
	小组成员
	"""
	relationship_id = models.BigAutoField(primary_key=True)
	group = models.ForeignKey(to='Groups', to_field='groupid', on_delete='CASCADE', verbose_name='小组')
	member = models.ForeignKey(to='UserInfo', to_field='userid', on_delete='CASCADE', verbose_name='成员')
	identity = models.ForeignKey(to='MemberIdentity', to_field='identity_id', default='1', on_delete='CASCADE',
								 verbose_name='身份')
	integral = models.IntegerField(default=0, verbose_name='获得积分')
	add_time = models.DateTimeField(auto_now_add=True, verbose_name='加入时间')


class MemberIdentity(models.Model):
	identity_id = models.BigAutoField(primary_key=True)
	identity_name = models.CharField(max_length=32, verbose_name='身份')


class GroupRequest(models.Model):
	"""
	小组申请
	"""
	request_id = models.BigAutoField(primary_key=True)
	initiator = models.ForeignKey(to='UserInfo', to_field='userid', on_delete='CASCADE', related_name='applicant',
								  verbose_name='发起人')
	target_user = models.ForeignKey(to='UserInfo', to_field='userid', on_delete='CASCADE', related_name='target',
									verbose_name='对象')
	target_group = models.CharField(max_length=32, verbose_name='目标小组')
	request_type = models.ForeignKey(to='RequestType', to_field='request_id', on_delete='CASCADE', verbose_name='请求类型')
	request_status = models.ForeignKey(to='RequestStatus', to_field='status_id', on_delete='CASCADE',
									   verbose_name='请求状态')
	request_time = models.DateTimeField(auto_now_add=True, verbose_name='申请时间')


class RequestType(models.Model):
	"""
	申请类型
	"""
	request_id = models.BigAutoField(primary_key=True)
	request_name = models.CharField(max_length=32, verbose_name='请求类型')


class RequestStatus(models.Model):
	"""
	申请状态
	"""
	status_id = models.BigAutoField(primary_key=True)
	status_name = models.CharField(max_length=32, verbose_name='请求状态')


class Activities(models.Model):
	"""
	小组活动
	"""
	activity_id = models.BigAutoField(primary_key=True)
	activity_request = models.TextField(verbose_name='活动内容')
	start_time = models.DateTimeField(verbose_name='开始时间')
	end_time = models.DateTimeField(verbose_name='结束时间')
	place = models.CharField(max_length=128, verbose_name='活动地点')
	sign_count = models.IntegerField(default=0, verbose_name='打卡数量')
	group = models.ForeignKey(to='Groups', to_field='groupid', on_delete='CASCADE', verbose_name='所属小组')
	status = models.ForeignKey(to='ActivityStatus', to_field='status_id', on_delete='CASCADE', verbose_name='活动状态')


class ActivityStatus(models.Model):
	"""
	活动状态
	"""
	status_id = models.BigAutoField(primary_key=True)
	status_name = models.CharField(max_length=32, verbose_name='活动状态')


class ActivitySign(models.Model):
	"""
	活动打卡
	"""
	sign_id = models.BigAutoField(primary_key=True)
	user = models.ForeignKey(to='UserInfo', to_field='userid', on_delete='CASCADE', verbose_name='打卡人')
	activity = models.ForeignKey(to='Activities', to_field='activity_id', on_delete='CASCADE', verbose_name='活动')
	content = models.TextField(verbose_name='打卡内容')
	time = models.DateTimeField(auto_now_add=True, verbose_name='打卡时间')


class Notices(models.Model):
	"""
	通知
	"""
	notice_id = models.BigAutoField(primary_key=True)
	to_user = models.ForeignKey(to='UserInfo', to_field='userid', on_delete='CASCADE', verbose_name='接收者')
	content = models.CharField(max_length=255, verbose_name='通知内容')
	notice_time = models.DateTimeField(auto_now_add=True, verbose_name='通知时间')
	status = models.ForeignKey(to='NoticeStatus', to_field='status_id', on_delete='CASCADE', verbose_name='通知状态')


class NoticeStatus(models.Model):
	"""
	通知状态
	"""
	status_id = models.BigAutoField(primary_key=True)
	status_name = models.CharField(max_length=32, verbose_name='通知状态')

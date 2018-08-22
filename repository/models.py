from django.db import models


# Create your models here.
class UserInfo(models.Model):
	"""
	用户信息
	"""
	userid = models.CharField(primary_key=True, max_length=32, verbose_name='学号')
	username = models.CharField(max_length=32, verbose_name='姓名')
	password = models.CharField(max_length=32, verbose_name='密码')
	gender = models.CharField(max_length=32, verbose_name='性别')
	major = models.CharField(max_length=32, verbose_name='专业')


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


class Activities(models.Model):
	"""
	活动
	"""
	activity_id = models.BigAutoField(primary_key=True)
	activity_name = models.CharField(max_length=32, verbose_name='活动名称')
	activity_request = models.TextField(verbose_name='活动内容')
	start_time = models.DateTimeField(verbose_name='开始时间')
	end_time = models.DateTimeField(verbose_name='结束时间')
	place = models.CharField(max_length=128, verbose_name='活动地点')
	leader = models.ForeignKey(to='UserInfo', to_field='userid', on_delete='CASCADE', verbose_name='发起人')
	activity_tag = models.ForeignKey(to='ActivityTag', to_field='tag_id', on_delete='CASCADE', verbose_name='活动标签')
	status = models.IntegerField(default=0, verbose_name='活动状态')  # 0表示未结束,1表示已结束


class ActivityTag(models.Model):
	"""
	活动标签
	"""
	tag_id = models.BigAutoField(primary_key=True)
	tag_name = models.CharField(max_length=32, verbose_name='活动标签')


class ActivityMembers(models.Model):
	"""
	活动成员
	"""
	relationship_id = models.BigAutoField(primary_key=True)
	activity = models.ForeignKey(to='Activities', to_field='activity_id', on_delete='CASCADE', verbose_name='活动')
	member = models.ForeignKey(to='UserInfo', to_field='userid', on_delete='CASCADE', verbose_name='成员')
	identity = models.IntegerField(default=0, verbose_name='身份')  # 0表示参加者,1表示组织者
	add_time = models.DateTimeField(auto_now_add=True, verbose_name='加入时间')


class ActivitySign(models.Model):
	"""
	活动打卡
	"""
	sign_id = models.BigAutoField(primary_key=True)
	user = models.ForeignKey(to='UserInfo', to_field='userid', on_delete='CASCADE', verbose_name='打卡人')
	activity = models.ForeignKey(to='Activities', to_field='activity_id', on_delete='CASCADE', verbose_name='活动')
	content = models.TextField(verbose_name='打卡内容')
	time = models.DateTimeField(auto_now_add=True, verbose_name='打卡时间')

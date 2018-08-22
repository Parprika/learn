from repository import models


class Initialization:
	def __init__(self, request, target_id):
		self.target_id = target_id
		self.userid = request.session.get('userid')
		self.username = request.session.get('username')

	def get_info(self):
		info_obj = models.UserInfo.objects.get(userid=self.target_id)
		return info_obj

	def get_note_count(self):
		if self.userid == self.target_id:
			note_count = models.Notes.objects.filter(note_user=self.target_id).count()
		else:
			note_count = models.Notes.objects.filter(note_user=self.target_id, readlimit='1').count()
		return note_count

	def get_fond_count(self):
		fond_count = models.UserFondNotes.objects.filter(userid=self.target_id).count()
		return fond_count

	def get_follow_count(self):
		follow_count = models.UserFans.objects.filter(follower_id=self.target_id).count()
		return follow_count

	def get_fans_count(self):
		fans_count = models.UserFans.objects.filter(user_id=self.target_id).count()
		return fans_count

	def get_activity_count(self):
		activity_count = models.ActivityMembers.objects.filter(member=self.target_id).count()
		return activity_count

	def get_relationship(self):
		if self.userid == self.target_id:
			relationship = 'self'  # 自己
		else:
			fans = models.UserFans.objects.filter(user=self.userid, follower=self.target_id)
			follow = models.UserFans.objects.filter(user=self.target_id, follower=self.userid)
			if fans and follow:  # 相互关注
				relationship = 'friend'
			elif follow:  # 当前用户已关注
				relationship = 'follow'
			else:
				relationship = 'not_follow'
		return relationship

	def get_min(self):
		ret = {
			'userid': self.userid,
			'username': self.username,
			'note_count': self.get_note_count(),
		}
		return ret

	def get_all(self):
		ret = {
			'userid': self.userid,
			'username': self.username,
			'note_count': self.get_note_count(),
			'fond_count': self.get_fond_count(),
			'follow_count': self.get_follow_count(),
			'fans_count': self.get_fans_count(),
			'activity_count': self.get_activity_count(),
			'relationship': self.get_relationship(),
			'info': self.get_info(),
		}
		return ret

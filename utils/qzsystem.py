import re
import urllib.request
import urllib.parse
import http.cookiejar
from pyquery import PyQuery as pq


class QZSystem:
	"""
	登录教务系统
	"""
	LOGIN_URL = 'http://jwxt.gdufe.edu.cn/jsxsd/xk/LoginToXkLdap'
	MAIN_URL = 'http://jwxt.gdufe.edu.cn/jsxsd/framework/xsMain.jsp'
	INFORMATION_URL = 'http://jwxt.gdufe.edu.cn/jsxsd/grxx/xsxx?Ves632DSdyV=NEW_XSD_XJCJ'
	HEADERS = {
		'Accept':
			'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Language':
			'zh-CN,zh;q=0.9,en;q=0.8',
		'Connection':
			'keep-alive',
		'Content-Type':
			'application/x-www-form-urlencoded',
		'User-Agent':
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
	}

	def __init__(self, username, password):
		self.cookie = http.cookiejar.CookieJar()
		self.handler = urllib.request.HTTPCookieProcessor(self.cookie)
		self.opener = urllib.request.build_opener(self.handler)
		self.username = username
		self.password = password

	def login(self):
		POST_DATA = {'USERNAME': self.username, 'PASSWORD': self.password}
		DATA = urllib.parse.urlencode(POST_DATA).encode('utf-8')
		request = urllib.request.Request(self.LOGIN_URL, DATA, self.HEADERS)
		try:
			response = self.opener.open(request)
			result = response.read().decode('utf-8')
		except Exception:
			return False
		return True

	def get_information(self):
		response = self.opener.open(self.INFORMATION_URL)
		doc = pq(response.read().decode('utf-8'))
		message_list = []
		name = doc('tr:nth-child(4) td:nth-child(2)').text()
		gender = doc('tr:nth-child(4) td:nth-child(4)').text()
		address = doc('tr:nth-child(7) td:nth-child(2)').text()
		message_list.append(name)
		message_list.append(gender)
		message_list.append(address)
		items = doc('tr:nth-child(3) td').items()
		for item in items:
			context = item.text()
			context = re.search('(.*?)：(.*)', context, re.S)
			message_list.append(context.group(2))
		return message_list

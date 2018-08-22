# learn
基于Python3.6和Django2.0的笔记分享和活动组织系统.

## 主要功能
-登录,注册,注销登录功能.
-关注模块:可对感兴趣的用户添加关注,同事也可以取消关注
-笔记模块:对个人笔记增删改操作,查阅用户笔记可添加收藏,笔记编辑使用kindeditor.
-活动模块:组织新活动以及管理活动,用户可通过搜索加入或退出活动;加入活动后可在当前活动中打卡分享.
-搜索模块:支持笔记,用户,活动全局全文搜索

## 运行
修改learn/settings 修改数据库(mysql)配置,如下:

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'learn',
		'USER': 'root',
		'PASSWORD': None,
		'HOST': '127.0.0.1',
		'PORT': '3306',
	}
}


## 创建数据库
数据库models统一在repository/models中
创建本地mysql数据库,然后终端下执行(manage.py同级目录):
python manage.py makemigrations
python manage.py migrate
注:笔记标签(NoteTag)与活动标签(ActivityTag)需要自己提前录入数据,笔记阅读权限(ReadLimit)设置为:{'1': '所有人', '2': '仅自己'}


## 创建超级用户
终端下执行:
python manage.py createsuperuser

## 开始运行
python manage.py runserver
浏览器打开:http://127.0.0.1:8000/login/ 开始运行

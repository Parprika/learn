from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def filter_all(keyword, type, dict):
	if keyword:
		if type == 'tag_obj_id':
			arg1 = dict.get('tag_id', '0')
			arg2 = dict.get('sort_by', '0')
			if not arg1 or arg1 == '0':
				ret = '<a class="active" href="/note/explore/?keyword=%s&tag_id=0&sort_by=%s">全部</a>' % (keyword, arg2)
			else:
				ret = '<a href="/note/explore/?keyword=%s&tag_id=0&sort_by=%s">全部</a>' % (keyword, arg2)
		else:
			arg1 = dict.get('sort_by', '0')
			arg2 = dict.get('tag_id', '0')
			if not arg1 or arg1 == '0':
				ret = '<a class="active" href="/note/explore/?keyword=%s&tag_id=%s&sort_by=0">全部</a>' % (keyword, arg2)
			else:
				ret = '<a href="/note/explore/?keyword=%s&tag_id=%s&sort_by=0">全部</a>' % (keyword, arg2)
	else:
		if type == 'tag_obj_id':
			arg1 = dict.get('tag_id', '0')
			arg2 = dict.get('sort_by', '0')
			if not arg1 or arg1 == '0':
				ret = '<a class="active" href="/note/explore/?tag_id=0&sort_by=%s">全部</a>' % arg2
			else:
				ret = '<a href="/note/explore/?tag_id=0&sort_by=%s">全部</a>' % arg2
		else:
			arg1 = dict.get('sort_by', '0')
			arg2 = dict.get('tag_id', '0')
			if not arg1 or arg1 == '0':
				ret = '<a class="active" href="/note/explore/?tag_id=%s&sort_by=0">全部</a>' % arg2
			else:
				ret = '<a href="/note/explore/?tag_id=%s&sort_by=0">全部</a>' % arg2
	return mark_safe(ret)


@register.simple_tag
def filter_tag(keyword, tag_obj, dict):
	ret = []
	for tag in tag_obj:
		if keyword:
			if tag.notetag_id == int(dict.get('tag_id', '0')):
				temp = '<a class="active" href="/note/explore/?keyword=%s&tag_id=%s&sort_by=%s">%s</a>' % (
					keyword, tag.notetag_id, dict.get('sort_by', '0'), tag.notetag_name)
			else:
				temp = '<a href="/note/explore/?keyword=%s&tag_id=%s&sort_by=%s">%s</a>' % (
					keyword, tag.notetag_id, dict.get('sort_by', '0'), tag.notetag_name)
		else:
			if tag.notetag_id == int(dict.get('tag_id', '0')):
				temp = '<a class="active" href="/note/explore/?tag_id=%s&sort_by=%s">%s</a>' % (
					tag.notetag_id, dict.get('sort_by', '0'), tag.notetag_name)
			else:
				temp = '<a href="/note/explore/?tag_id=%s&sort_by=%s">%s</a>' % (
					tag.notetag_id, dict.get('sort_by', '0'), tag.notetag_name)
		ret.append(temp)
	return mark_safe(''.join(ret))


@register.simple_tag
def filter_sort(keyword, sort_select, dict):
	ret = []
	for key, value in sort_select.items():
		if keyword:
			if key == dict.get('sort_by', '0'):
				temp = '<a class="active" href="/note/explore/?keyword=%s&tag_id=%s&sort_by=%s">%s</a>' % (
				keyword, dict.get('tag_id', '0'), key, value)
			else:
				temp = '<a href="/note/explore/?keyword=%s&tag_id=%s&sort_by=%s">%s</a>' % (
					keyword, dict.get('tag_id', '0'), key, value)
		else:
			if key == dict.get('sort_by', '0'):
				temp = '<a class="active" href="/note/explore/?tag_id=%s&sort_by=%s">%s</a>' % (
				dict.get('tag_id', '0'), key, value)
			else:
				temp = '<a href="/note/explore/?tag_id=%s&sort_by=%s">%s</a>' % (
					dict.get('tag_id', '0'), key, value)
		ret.append(temp)
	return mark_safe(''.join(ret))

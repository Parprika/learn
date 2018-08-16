from django.utils.safestring import mark_safe


class Paging:
	"""
	分页功能
	"""
	def __init__(self, current, data_count, count_per_page=10, page_count=11):
		self.current = current
		self.data_count = data_count
		self.count_per_page = count_per_page
		self.page_count = page_count

	@property
	def start(self):
		return (self.current - 1) * self.count_per_page

	@property
	def end(self):
		return self.current * self.count_per_page

	@property
	def all(self):
		x, y = divmod(self.data_count, self.count_per_page)
		if y:
			x += 1
		return x

	def get_paging(self, url):
		paging_list = []
		if self.all < self.page_count:
			start = 1
			end = self.all + 1
		else:
			if self.current <= (self.page_count + 1) / 2:
				start = 1
				end = self.page_count + 1
			else:
				start = self.current - (self.page_count - 1) / 2
				end = self.current + (self.page_count + 1) / 2
				if (self.current + (self.page_count - 1) / 2) > self.all:
					start = self.all - self.page_count + 1
					end = self.all + 1
		if self.current == 1:
			previous = '<a class="previous" href="javascript:void(0);">上一页</a>'
		else:
			previous = '<a class="previous" href="%s?p=%s">上一页</a>' % (url, self.current - 1)
		paging_list.append(previous)
		for i in range(int(start), int(end)):
			if i == self.current:
				page = '<a class="page active" href="%s?p=%s">%s</a>' % (url, i, i)
			else:
				page = '<a class="page" href="%s?p=%s">%s</a>' % (url, i, i)
			paging_list.append(page)
		if self.current == self.all:
			next = '<a class="next" href="javascript:void(0);">下一页</a>'
		else:
			next = '<a class="next" href="%s?p=%s">下一页</a>' % (url, self.current + 1)
		paging_list.append(next)
		jump = """
		<input type='text'/><a class='jump' onclick='jump(this, "%s?p=");'>跳转</a>
		<script>
			function jump(ths, url) {
				var val = ths.previousSibling.value;
				location.href = url + val;
			}
		</script>
		""" % (url,)
		paging_list.append(jump)
		paging = ''.join(paging_list)
		paging = mark_safe(paging)
		return paging

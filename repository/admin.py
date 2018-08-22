from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from repository import models

# Register your models here.
admin.site.register(models.UserInfo)
# admin.site.register(models.Notes)
admin.site.register(models.NoteTag)
admin.site.register(models.UserFans)
admin.site.register(models.ReadLimit)
admin.site.register(models.UserFondNotes)
admin.site.register(models.Activities)
admin.site.register(models.ActivitySign)
admin.site.register(models.ActivityMembers)
admin.site.register(models.ActivityTag)


@admin.register(models.Notes)
class NotesAdmin(admin.ModelAdmin):
	class Media:
		js = (
			'/static/kindeditor/kindeditor-all.js',
			'/static/kindeditor/lang/zh-CN.js',
			'/static/kindeditor/config.js',
		)

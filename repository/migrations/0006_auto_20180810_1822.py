# Generated by Django 2.0.5 on 2018-08-10 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0005_auto_20180810_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='notetag',
            field=models.ForeignKey(default='1', on_delete='CASCADE', to='repository.NoteTag', verbose_name='笔记标签'),
        ),
        migrations.AlterField(
            model_name='notes',
            name='readlimit',
            field=models.ForeignKey(default='1', on_delete='CASCADE', to='repository.ReadLimit', verbose_name='阅读权限'),
        ),
    ]

# Generated by Django 2.0.5 on 2018-08-13 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0006_auto_20180810_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfans',
            name='follow_time',
            field=models.DateTimeField(auto_now_add=True, default='2018-08-13 12:46:24.932631', verbose_name='关注时间'),
            preserve_default=False,
        ),
    ]

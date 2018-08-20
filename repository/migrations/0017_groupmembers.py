# Generated by Django 2.0.5 on 2018-08-18 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0016_auto_20180818_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupMembers',
            fields=[
                ('relationship_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('integral', models.IntegerField(default=0, verbose_name='获得积分')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('group', models.ForeignKey(on_delete='CASCADE', to='repository.Groups', verbose_name='小组')),
                ('identity', models.ForeignKey(default='1', on_delete='CASCADE', to='repository.MemberIdentity', verbose_name='身份')),
                ('member', models.ForeignKey(on_delete='CASCADE', to='repository.UserInfo', verbose_name='成员')),
            ],
        ),
    ]

# Generated by Django 2.0.5 on 2018-08-09 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('noteid', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128, verbose_name='标题')),
                ('summary', models.CharField(max_length=255, verbose_name='简介')),
                ('content', models.TextField(verbose_name='正文')),
                ('fond_count', models.IntegerField(default=0, verbose_name='收藏量')),
                ('read_count', models.IntegerField(default=0, verbose_name='阅读量')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('last_edit_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
        ),
        migrations.CreateModel(
            name='NoteTag',
            fields=[
                ('notetag_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('notetag_name', models.CharField(max_length=32, verbose_name='笔记标签')),
            ],
        ),
        migrations.CreateModel(
            name='ReadLimit',
            fields=[
                ('limitid', models.BigAutoField(primary_key=True, serialize=False)),
                ('limit_type', models.CharField(max_length=32, verbose_name='阅读权限')),
            ],
        ),
        migrations.CreateModel(
            name='UserFans',
            fields=[
                ('relationship_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('is_special', models.BooleanField(default='False', verbose_name='特别关注')),
            ],
        ),
        migrations.CreateModel(
            name='UserFondNotes',
            fields=[
                ('fondid', models.BigAutoField(primary_key=True, serialize=False)),
                ('fond_time', models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')),
                ('noteid', models.ForeignKey(on_delete='CASCADE', to='repository.Notes', verbose_name='笔记')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('userid', models.CharField(max_length=32, primary_key=True, serialize=False, verbose_name='学号')),
                ('username', models.CharField(max_length=32, verbose_name='姓名')),
                ('gender', models.CharField(max_length=32, verbose_name='性别')),
                ('institute', models.CharField(max_length=32, verbose_name='所属学院')),
                ('major', models.CharField(max_length=32, verbose_name='专业')),
                ('native_place', models.CharField(max_length=32, verbose_name='籍贯')),
                ('follow_count', models.IntegerField(default=0, verbose_name='关注数')),
                ('fans_count', models.IntegerField(default=0, verbose_name='粉丝数')),
                ('notes_count', models.IntegerField(default=0, verbose_name='笔记数量')),
                ('fond_notes_count', models.IntegerField(default=0, verbose_name='收藏笔记数量')),
            ],
        ),
        migrations.CreateModel(
            name='UserTag',
            fields=[
                ('usertag_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('usertag_name', models.CharField(max_length=32, verbose_name='用户标签')),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='usertag',
            field=models.ManyToManyField(to='repository.UserTag', verbose_name='用户标签'),
        ),
        migrations.AddField(
            model_name='userfondnotes',
            name='userid',
            field=models.ForeignKey(on_delete='CASCADE', to='repository.UserInfo', verbose_name='学号'),
        ),
        migrations.AddField(
            model_name='userfans',
            name='follower',
            field=models.ForeignKey(on_delete='CASCADE', related_name='followers', to='repository.UserInfo', verbose_name='粉丝'),
        ),
        migrations.AddField(
            model_name='userfans',
            name='user',
            field=models.ForeignKey(on_delete='CASCADE', related_name='users', to='repository.UserInfo', verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='notes',
            name='note_user',
            field=models.ForeignKey(on_delete='CASCADE', to='repository.UserInfo', verbose_name='作者'),
        ),
        migrations.AddField(
            model_name='notes',
            name='notetag',
            field=models.ManyToManyField(to='repository.NoteTag', verbose_name='笔记标签'),
        ),
        migrations.AddField(
            model_name='notes',
            name='readlimit',
            field=models.ForeignKey(on_delete='CASCADE', to='repository.ReadLimit', verbose_name='阅读权限'),
        ),
    ]

# Generated by Django 2.0.5 on 2018-08-16 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0013_remove_userfans_is_special'),
    ]

    operations = [
        migrations.AddField(
            model_name='activities',
            name='place',
            field=models.CharField(default='线上', max_length=128, verbose_name='活动地点'),
            preserve_default=False,
        ),
    ]

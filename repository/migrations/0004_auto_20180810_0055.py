# Generated by Django 2.0.5 on 2018-08-09 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0003_auto_20180810_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='content',
            field=models.TextField(verbose_name='正文'),
        ),
    ]

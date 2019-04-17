# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-04-11 12:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.CharField(default='/static/img/header.jpg', max_length=200, verbose_name='用户头像'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='用户密码'),
        ),
    ]

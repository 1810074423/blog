# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-04-10 09:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='文章主键')),
                ('title', models.CharField(max_length=50, verbose_name='文章标题')),
                ('content', models.TextField(verbose_name='文章内容')),
                ('publish_time', models.DateTimeField(auto_now_add=True, verbose_name='文章发表时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='文章修改时间')),
                ('count', models.IntegerField(default=0, verbose_name='点击量')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='用户主键')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='用户名称')),
                ('nickname', models.CharField(max_length=50, verbose_name='用户昵称')),
                ('password', models.CharField(blank=True, max_length=12, null=True, verbose_name='用户密码')),
                ('age', models.IntegerField(default=18, verbose_name='用户年龄')),
                ('gender', models.CharField(default='男', max_length=50, verbose_name='用户性别')),
                ('birthday', models.DateTimeField(auto_now_add=True, verbose_name='用户生日')),
                ('login_time', models.DateTimeField(auto_now=True, verbose_name='登陆时间')),
                ('avatar', models.CharField(default='/static/blog/img/header.jpg', max_length=200, verbose_name='用户头像')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.User'),
        ),
    ]

from django.db import models
# from tinymce.models import HTMLField
# content = HTMLField()
from DjangoUeditor.models import UEditorField
content = UEditorField()


class User(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='用户主键')
    username = models.CharField(max_length=50, unique=True, verbose_name='用户名称')
    nickname = models.CharField(max_length=50, verbose_name='用户昵称')
    password = models.CharField(max_length=50, null=True, blank=True, verbose_name='用户密码')
    age = models.IntegerField(default=18, verbose_name='用户年龄')
    gender = models.CharField(max_length=50, default='男', verbose_name='用户性别')
    birthday = models.DateTimeField(auto_now_add=True, verbose_name='用户生日')
    login_time = models.DateTimeField(auto_now=True, verbose_name='登陆时间')
    # avatar = models.CharField(max_length=200, default='/static/img/header.jpg', verbose_name='用户头像')
    avatar = models.ImageField(upload_to='static/img/upload', default='/static/img/header.jpg', verbose_name="用户头像")

    class Meta:
        ordering = ['id']
        verbose_name = '用户'

    def __str__(self):
        return self.username


class Article(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='文章主键')
    title = models.CharField(max_length=50, verbose_name='文章标题')
    # content = HTMLField(verbose_name='文章内容')
    content = UEditorField(verbose_name='文章内容')
    publish_time = models.DateTimeField(auto_now_add=True, verbose_name='文章发表时间')
    modify_time = models.DateTimeField(auto_now=True, verbose_name='文章修改时间')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    count = models.IntegerField(default=0, verbose_name='点击量')

    class Meta:
        ordering = ['id']
        verbose_name = '文章'

    def __str__(self):
        return self.title

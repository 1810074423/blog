from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import JsonResponse
from . import models
from . import utils
from .utils import require_login
import uuid
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.core.cache import cache
from io import BytesIO
from . import cache_util


@require_POST
@csrf_exempt
def check_user(request):
    username = request.POST['username']
    try:
        models.User.objects.get(username=username)
        return JsonResponse({"msg": "该用户已存在，请重新注册", "issuccess": False})
    except:
        return JsonResponse({'msg': "用户名可用", "issuccess": True})


def code(request):
    img, msg = utils.create_code()
    file = BytesIO()
    img.save(file, "PNG")
    request.session["code"] = msg
    return HttpResponse(file.getvalue(), 'image/png')


def index(request):
    articles = cache_util.get_all_article()
    return render(request, "blog/index.html", {"articles": articles})


def login(request):
    if request.method == 'GET':
        return render(request, 'blog/login.html', {})
    elif request.method == "POST":
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()
        password = utils.pwd_by_hmac(password)
        code = request.POST["code"].strip()
        msg = request.session["code"]
        if msg.lower() != code.lower():
            return render(request, "blog/login.html", {"msg": "验证码有误！！"})

        try:
            user = models.User.objects.get(username=username)
            if password == user.password:
                request.session['login_user'] = user
                return render(request, 'blog/user_detail.html', {'msg': '登录成功！！'})
        except Exception as e:
            print("异常错误：", e)
            return render(request, 'blog/login.html', {'msg': '登录失败，请重新登录！'})


def login_out(request):
    try:
        del request.session['login_user']
        return render(request, 'blog/index.html', {})
    except:
        return render(request, 'blog/index.html', {})


def register(request):
    if request.method == 'GET':
        return render(request, 'blog/register.html', {'msg': '请认真填写如下内容'})
    elif request.method == "POST":
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()
        password1 = request.POST['password1'].strip()
        nickname = request.POST['nickname'].strip()
        if username == '':
            return render(request, 'blog/register.html', {'msg': '用户名不能为空'})
        if nickname == '':
            return render(request, 'blog/register.html', {'msg': '昵称不能为空'})
        if len(password) < 6:
            return render(request, 'blog/register.html', {'msg': '密码不能小于6位'})
        if password != password1:
            return render(request, 'blog/register.html', {'msg': '两次密码不一致，请重新注册！'})
        users = models.User.objects.filter(username=username)
        if len(users) > 0:
            return render(request, 'blog/register.html', {'msg': '用户名已存在！'})
        try:
            password = utils.pwd_by_hmac(password)
            user = models.User(username=username, password=password, nickname=nickname)
            user.save()
            return render(request, 'blog/login.html', {'msg': '注册成功，请登录！！'})
        except Exception as e:
            print("异常错误：", e)
            return render(request, 'blog/register.html', {'msg': '注册失败，请重新注册！'})


@require_login
def user_list(request):
    users = models.User.objects.all()
    return render(request, 'blog/user_list.html', {'users': users})


@require_login
def user_delete(request, u_id):
    try:
        user = models.User.objects.get(pk=u_id)
        user.delete()
    except Exception as e:
        print("删除用户错误：", e)
    finally:
        return redirect(reverse('blog:user_list'))


@require_login
def user_update(request, u_id):
    user = models.User.objects.get(id=u_id)
    if request.method == "GET":
        return render(request, 'blog/user_update.html', {'user': user})
    else:
        nickname = request.POST['nickname']
        age = request.POST['age']
        gender = request.POST['gender']
        avatar = request.FILES.get("avatar", "/static/img/header.jpg")
        # path = 'static/img/' + uuid.uuid4().hex + avatar.name
        # with open(path, "wb") as f_w:
        #     for file in avatar.chunks():
        #         f_w.write(file)
        # path = '/' + path
        user = models.User.objects.get(pk=u_id)
        user.avatar = avatar
        user.nickname = nickname
        user.age = age
        user.gender = gender
        try:
            user.save()
            request.session["login_user"] = user
            return redirect(reverse("blog:user_detail"))
        except Exception as e:
            print("异常错误：", e)
            return render(request, "blog/user_update.html", {"user": user, "msg": "修改失败，请重新修改！"})


@require_login
def user_detail(request):
    return render(request, 'blog/user_detail.html', {})


@require_login
def change_pwd(request):
    try:
        user = request.session['login_user']
    except:
        return render(request, 'blog/login.html', {'msg': "请先登录系统"})
    if request.method == 'GET':
        return render(request, 'blog/change_pwd.html', {})
    else:
        old_password = request.POST['old_password'].strip()
        new_password = request.POST['new_password'].strip()
        new1_password = request.POST['new1_password'].strip()
        old_password = utils.pwd_by_hmac(old_password)
        if user.password != old_password:
            return render(request, 'blog/change_pwd.html', {'msg': '原密码输入错误，请再次输入'})
        if len(new_password) < 6:
            return render(request, 'blog/change_pwd.html', {'msg': '密码不能小于6位'})
        if new_password != new1_password:
            return render(request, 'blog/change_pwd.html', {'msg': '两次密码不一致，请重新输入！'})
        try:
            user.password = utils.pwd_by_hmac(new_password)
            user.save()
            request.session["login_user"] = user
            return redirect(reverse('blog:login'), {'msg': '注册成功，请登录！！'})
        except Exception as e:
            print("异常错误：", e)
            return render(request, 'blog/register.html', {'msg': '注册失败，请重新注册！'})


@require_login
def article_list(request):
    articles = models.Article.objects.all()
    return render(request, "blog/article_list.html", {"articles": articles})


@require_login
def article_add(request):
    if request.method == 'GET':
        return render(request, 'blog/article_add.html', {})
    elif request.method == 'POST':
        title = request.POST['title'].strip()
        content = request.POST['content'].strip()
        author = request.session["login_user"]

        if title == "":
            return render(request, 'blog/article_add.html', {"msg": "文章标题不能为空"})
        if len(title) > 100:
            return render(request, 'blog/article_add.html', {"msg": "标题过长"})
        if content == "":
            return render(request, 'blog/article_add.html', {"msg": "文章内容不能为空"})
        article = models.Article(title=title, content=content, author=author)
        try:
            article.save()
            return redirect(reverse("blog:article_detail", kwargs={"a_id": article.id}))
        except:
            return render(request, "blog/article_add.html", {"msg": "文章添加失败，请重新添加！！"})


@require_login
def article_delete(request, a_id):
    try:
        article = models.Article.objects.get(pk=a_id)
        article.delete()
    except Exception as e:
        print("删除用户错误：", e)
    finally:
        return redirect(reverse('blog:article_list'))


@require_login
def article_update(request, a_id):
    article = models.Article.objects.get(pk=a_id)
    if request.method == 'GET':
        return render(request, 'blog/article_update.html', {"article": article})
    else:
        title = request.POST["title"].strip()
        content = request.POST['content'].strip()
        if title == '':
            return render(request, 'blog/article_update.html', {"msg": '文章标题不能为空！'})
        if len(title) > 50:
            return render(request, 'blog/article_update.html', {"msg": '文章标题过长！'})
        if content == '':
            return render(request, 'blog/article_update.html', {"msg": '文章内容不能为空！'})
        try:
            article.title = title
            article.content = content
            article.save()
            return redirect(reverse("blog:article_detail", kwargs={"a_id": article.id}))
        except Exception as e:
            print("异常错误，错误是", e)
            return redirect(reverse("blog:article_detail", kwargs={"a_id": article.id}))


@require_login
def article_self(request):
    # 查询登录用户的所有文章
    login_user = request.session["login_user"]
    articles = models.Article.objects.filter(author=login_user)
    return render(request, "blog/article_self.html", {"articles": articles})


def article_detail(request, a_id):
    article = models.Article.objects.get(id=a_id)
    article.count += 1
    article.save()
    return render(request, "blog/article_detail.html", {"article": article})

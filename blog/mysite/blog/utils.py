from django.shortcuts import render
from django.conf import settings
import hashlib
import hmac
import random
import string
from PIL import Image,ImageDraw,ImageFont,ImageFilter


def get_random_char(count=4):
    ran = string.ascii_lowercase + string.ascii_uppercase + string.digits
    char = ''
    for i in range(count):
        char += random.choice(ran)
    return char


def get_random_color():
    return random.randint(200,255), random.randint(200,255), random.randint(200,255)


def create_code():
    img = Image.new('RGB', (120,30), (94,86,125))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', 25)
    code = get_random_char()
    for t in range(4):
        draw.text((30*t+5, 0), code[t], get_random_color(), font)
    for _ in range(random.randint(0, 50)):
        draw.point((random.randint(0, 120), random.randint(0, 30)),fill=get_random_color())
    return img, code


def require_login(fn):
    def inner(request, *args, **kwargs):
        login_user = request.session.get('login_user', None)
        if login_user is not None:
            return fn(request, *args, **kwargs)
        else:
            return render(request, "blog/login.html",{"msg": "请先登录系统！"})
    return inner


def pwd_by_hashlib(password):
    md5 = hashlib.md5(password.encode("utf-8"))
    md5.update(settings.SALT.encode("utf-8"))
    return md5.hexdigest()


def pwd_by_hmac(password):
    return hmac.new(settings.SALT.encode("utf-8"), password.encode("utf-8"), "MD5").hexdigest()


if __name__ == '__main__':
    # print(pwd_by_hashlib("123456"))
    print(pwd_by_hmac("123456"))

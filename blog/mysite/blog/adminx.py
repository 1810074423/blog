import xadmin
from .models import User, Article
from xadmin import views


class UserAdmin(object):
    list_display = ["username", "nickname", "age", "gender", "password"]
    list_filter = ["age", "nickname"]
    list_per_page = 5


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "博客管理系统后台"
    site_footer = "2018@qikuedu.com"
    menu_style = "accordion"


xadmin.site.register(views.CommAdminView,GlobalSettings)

xadmin.site.register(views.BaseAdminView, BaseSetting)


xadmin.site.register(User, UserAdmin)
xadmin.site.register(Article)









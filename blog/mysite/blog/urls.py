from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^login_out/$', views.login_out, name='login_out'),
    url(r'^register/$', views.register, name='register'),
    url(r'^user_list/$', views.user_list, name='user_list'),
    url(r'^(?P<u_id>\d+)/user_delete/$', views.user_delete, name='user_delete'),
    url(r'^user_update/(?P<u_id>\d+)/$', views.user_update, name='user_update'),
    url(r'^user_detail/$', views.user_detail, name='user_detail'),
    url(r'^change_pwd/$', views.change_pwd, name='change_pwd'),

    url(r'^article_list/$', views.article_list, name='article_list'),
    url(r'^article_add/$', views.article_add, name='article_add'),
    url(r"^article_self/$", views.article_self, name="article_self"),
    url(r'^article_delete/(?P<a_id>\d+)/$', views.article_delete, name='article_delete'),
    url(r'^article_update/(?P<a_id>\d+)/$', views.article_update, name='article_update'),
    url(r'^article_detail/(?P<a_id>\d+)/$', views.article_detail, name='article_detail'),

    url(r"^code/$", views.code, name="code"),
    url(r'^check_user/$', views.check_user, name="check_user"),
]

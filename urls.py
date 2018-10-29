from django.conf.urls import url
from . import views

urlpatterns = [
		url(r'home/$', views.home, name="home"),
		url(r'auth_login/$', views.authlogin, name='login'),
        url(r'register/$', views.register, name='register'),
		url(r'mvouchar/$', views.mvouchar, name='mvouchar'),
		url(r'duplicate/$', views.all_duplicates, name='duplicate'),
		url(r'report/$', views.all_reports, name='report'),
		url(r'login/$', views.login, name='login'),
		url(r'profile/$', views.user_profile, name='profile'),
		url(r'logout/$', views.logout, name='logout'),
		url(r'jsondata/$', views.mvouchar, name='jsondata'),
]

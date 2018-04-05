# accounts/urls.py
from django.conf.urls import url
from django.urls import re_path

from . import views


urlpatterns = [
     url(r'^signup/$', views.signup, name='signup'),
     url(r'^my_account/$', views.UserUpdateView.as_view(), name='my_account'),
     url(r'^users/$', views.UserList.as_view(), name='users'),
]

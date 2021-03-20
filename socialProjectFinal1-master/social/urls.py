"""social_testt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path,include
from django_private_chat import urls as django_private_chat_urls
from django.contrib.auth.views import LogoutView
from . import views
app_name = 'social'
urlpatterns = [
    path('',views.index),
    path('social/register/',views.register,name="register"),
    path('social/login/',views.login,name="login"),
    path('social/home/',views.home,name="home"),
    re_path(r'^social/trustable/(?P<id_user>[0-9]+)/$', views.trustable,name="trustable"),
    path('social/logout/', LogoutView.as_view(), name="logout"),
    re_path(r'^social/resolved/(?P<id_user>[0-9]+)/$',views.resolved, name="is_resolved"),
    re_path(r'^social/unresolved/(?P<id_user>[0-9]+)/$',views.unresolved, name="unresolved"), 
    re_path(r'^social/untrustable/(?P<id_user>[0-9]+)/$', views.untrustable,name="untrustable"),
    path('social/create/', views.create,name = "create"),
    path('social/post/',views.post,name= "post"),
    path('social/addPost/', views.addPost, name= "addPost")
   
]

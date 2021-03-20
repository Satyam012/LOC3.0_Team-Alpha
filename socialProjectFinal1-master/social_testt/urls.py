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
from django.conf import settings
from django.conf.urls.static import static
from social import views as my_views
#from django_private_chat import views as chat_views
#anonymity issue fixed. Now fix the url in templates from dialogs/username to dialogs/user_id/ (notice / at end) in dialogs.html and make dialogs/username views raise http404
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^dialogs/(?P<username>[0-9]+)/$',my_views.myDialogListView.as_view(),name='mydialogs_detail'),#username is now user id
    re_path(r'^', include('django_private_chat.urls')),
    path('',include('social.urls')),
]
if settings.DEBUG: #Not for production code
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
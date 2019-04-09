"""usug URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url, patterns
from django.contrib import admin
from applications.app.views import *
from django.views.generic import TemplateView
import notifications


urlpatterns = [
    url('^inbox/notifications/', include('notifications.urls', namespace='notifications')),
    url(r'^chaining/', include('smart_selects.urls')),

    url(r'^notifications/$', Notifications_list.as_view(), name='tze_notifications_list_all'),
# Home url
    url(r'^home/', HomeView.as_view(), name="home"),

# Director url    
    url(r'^director/', include('applications.director.urls')),

# Engineering urls
    url(r'^engineering/', include('applications.engineering.urls')),

# Accountants url
    url(r'^accountants/', include('applications.accountants.urls')),

# tza url
    url(r'^tza/', include('applications.tza.urls')),

# hzm url
    url(r'^hzm/', include('applications.hzm.urls')),

# admin url
    url(r'^admin/', include('applications.admin1.urls')),

# uta url
    url(r'^uta/', include('applications.uta.urls')),

# User, Servant, Admin login and logout url
    url(r'^$', Login.as_view(), name="login"),
    url(r'^logout/$', 'applications.app.views.Logout', name="logout"),
    #url(r'^request/$', TemplateView.as_view(template_name="huselt.html")),
    url(r'^request/$', HandahErh.as_view()),

    url(r'^captcha/', include('captcha.urls')),
    
# Django admin url
    url(r'^base_admin/', include(admin.site.urls)),


    url(r'^messages/', include('django_messages.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG is False:   #if DEBUG is True it will be served automatically
    urlpatterns += patterns('',
            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
from django.conf.urls import url
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
	url(r'report/$', TailanView.as_view(), name = 'report'),
	url(r'report/(?P<pk>[0-9]+)/$', YearTailanView.as_view(), name = 'report'),
	url(r'report/(?P<bid>[0-9]+)/(?P<year>[0-9]+)/(?P<pk>[0-9]+)/$', export, name = 'report'),
]
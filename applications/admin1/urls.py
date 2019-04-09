from django.conf.urls import url
from applications.admin1.views import *
# Admin url
urlpatterns = [

	url(r'^$', Admin.as_view(), name = 'admin'),
	url(r'^employee/create/$', EmployeeCreate.as_view(), name = 'employee-create'),
	url(r'^employee/update/(?P<pk>[0-9]+)/$', EmployeeUpdate.as_view(), name = 'employee-update'),
	url(r'^tasag/create/$', TasagCreate.as_view(), name = 'tasag-create'),
	url(r'^tushaal/create/$', TushaalCreate.as_view(), name = 'tushaal-create'),

]
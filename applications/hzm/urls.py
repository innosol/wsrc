from django.conf.urls import url
from .views import *
#from applications.accountants.view import Report
urlpatterns = [
	url(r'^$', Home.as_view(), name="home_hzm"),
	

    ##### hzm mergejilten urls
	url(r'^huseltuud/$', HZM_Huselt_list.as_view(), name='hzm huselt check'),
    url(r'^tz_huseltuud/delgerengui/(?P<huselt_id>\d+)/$', HZM_tz_huselt_delgerengui.as_view(), name='hzm_tz_huselt_delgerengui'),
    url(r'^sent_material/(?P<burdel_history_id>\d+)/(?P<material_number>\d+)/$', HZM_TZ_Sent_materialView.as_view(), name = 'hzm_sent_material_show'),
    url(r'^tz_huseltuud/check/(?P<burdel_history_id>\d+)/(?P<material_number>\d+)/$', HZM_TZ_Material_check.as_view(), name = 'hzm_material_check'),
    url(r'^tz_huseltuud/check_finish_hzm/(?P<huselt_id>\d+)/$', TZ_huselt_check_finish_hzm.as_view(), name = 'huselt_check_finish_hzm'),


	##### baiguullaga menu urls
    url(r'^baiguullaga/$', HZM_BaiguullagaaView.as_view()),
    url(r'^baiguullaga/(?P<baiguullaga_id>\d+)/$', HZM_Baiguullaga_delgerengui.as_view(), name='hzm_baiguullaga_delgerengui'),

    #### hunii noots menu urls
    url(r'^ajiltan/$', HZM_AjiltanView.as_view()),
    url(r'^ajiltan/(?P<id>\d+)/$', HZM_Ajiltan_delgerengui.as_view(), name='hzm_ajiltan_delgerengui'),

    #### tonoggggg tohooromj menu urls
    url(r'^tohooromj/$', HZM_TohooromjjView.as_view()),

    #### tz gerchilgee menu urls
    url(r'^tz_gerchilgee_list/$', HZM_TZ_gerchilgee_listView.as_view(), name = 'hzm_tz_gerchilgee_list'),
    url(r'^tz_gerchilgee_delgerengui/(?P<tz_gerchilgee_id>\d+)/$', HZM_TZ_gerchilgee_delgerenguiView.as_view(), name = 'hzm_tz_gerchilgee_delgerengui'),

]
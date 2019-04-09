# coding:utf-8
from django.conf.urls import url
from .views import *
#from applications.accountants.view import Report
urlpatterns = [
	url(r'^$', Home.as_view(), name="home_uta"),
	url(r'^report/$', Report.as_view(), name="uta_report"),
	url(r'^report/(?P<org>[0-9]+)/$', ReportOrg.as_view(), name="uta_report"),
	url(r'^sez/$', CheckSezView.as_view(), name = 'check_sez'),
    url(r'^tolov/$', tolov, name = 'tolov'),
    url(r'^sez/list/(?P<org>[0-9]+)/(?P<id>[0-9]+)$', CheckListView.as_view(), name="check_list"),

    ##### Судалгаа
    url(r'^sudalgaa/list/$', SudalgaaList.as_view(), name = 'sudalgaa_list'),
    url(r'^sudalgaa/list/(?P<id>[0-9]+)/$', SudalgaaSelf.as_view(), name = 'sudalgaa_self'),
    url(r'^sudalgaa/(?P<org_id>[0-9]+)/(?P<id>[0-9]+)/(?P<table_id>[0-9]+)/$', sudalgaa_husnegt, name = 'sudalgaa_husnegt'),
    url(r'^sudalgaa/tolov/huleen_avah/(?P<id>[0-9]+)/$', SudalgaaSelf.sudalgaa_tolov_huleen_avah, name = 'sudalgaa_tolov_huleen_avah'),
    url(r'^sudalgaa/tolov/butsaah/(?P<id>[0-9]+)/$', SudalgaaSelf.sudalgaa_tolov_butsaah, name = 'sudalgaa_tolov_butsaah'),
    url(r'^sudalgaa/message/(?P<id>[0-9]+)/$', MessageView.as_view(), name = 'message_uta'),

	##### uta darga urls
	url(r'^huseltuud_huvaarilah/$', UTA_darga_huselt_huvaarilalt_list.as_view(), name='uta darga huselt huvaarilah'),
    url(r'^huselt_huvaarilah/(?P<huselt_id>\d+)/$', TZ_huselt_uta_huvaarilah.as_view(), name='uta huselt huvaarilah'),


    ##### uta mergejilten urls
	url(r'^huseltuud/$', UTA_Huselt_list.as_view(), name='uta huselt check'),
    url(r'^tz_huseltuud/delgerengui/(?P<huselt_id>\d+)/$', UTA_tz_huselt_delgerengui.as_view(), name='uta_tz_huselt_delgerengui'),
    url(r'^sent_material/(?P<burdel_history_id>\d+)/(?P<material_number>\d+)/$', UTA_TZ_Sent_materialView.as_view(), name = 'uta_sent_material_show'),
    url(r'^tz_huseltuud/check_finish_uta/(?P<huselt_id>\d+)/$', TZ_huselt_check_finish_uta.as_view(), name = 'huselt_check_finish_uta'),
    url(r'^tz_huseltuud/check/(?P<burdel_history_id>\d+)/(?P<material_number>\d+)/$', UTA_TZ_Material_check.as_view(), name = 'uta_material_check'),
    

	##### baiguullaga menu urls
    url(r'^baiguullaga/$', UTA_BaiguullagaaView.as_view()),
    url(r'^baiguullaga/(?P<baiguullaga_id>\d+)/$', UTA_Baiguullaga_delgerengui.as_view(), name='uta_baiguullaga_delgerengui'),

    #### hunii noots menu urls
    url(r'^ajiltan/$', UTA_AjiltanView.as_view()),
    url(r'^ajiltan/(?P<id>\d+)/$', UTA_Ajiltan_delgerengui.as_view(), name='uta_ajiltan_delgerengui'),

    #### tonoggggg tohooromj menu urls
    url(r'^tohooromj/$', UTA_TohooromjjView.as_view()),

    #### tz gerchilgee menu urls
    url(r'^tz_gerchilgee_list/$', UTA_TZ_gerchilgee_listView.as_view(), name = 'uta_tz_gerchilgee_list'),
    url(r'^tz_gerchilgee_delgerengui/(?P<tz_gerchilgee_id>\d+)/$', UTA_TZ_gerchilgee_delgerenguiView.as_view(), name = 'uta_tz_gerchilgee_delgerengui'),

    url(r'^gshu/$', UTA_gshutailanView.as_view(), name = 'uta_gshu_menu'),

]
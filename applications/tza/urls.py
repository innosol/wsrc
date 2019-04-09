from django.conf.urls import url
from applications.tza.views import *
from applications.engineering.views import BaiguullagaaView, TZE_baig_medeelel_list, TZE_zasag_tod_list, TZE_hangagch_baig_list, TZE_tatvar_tod_list, TZE_audit_dugnelt_list, TZE_norm_standart_list, TZE_huuli_durem_list, TZE_us_ashigluulah_zovshoorol_list, TZE_sanhuu_tailan_list, TZE_oron_toonii_schema, TZE_SEZ_sudalgaa
from applications.engineering.views import EmployeeView, TZE_Ajiltan_all_list, TZE_Ajiltan_udirdah_list, TZE_Ajiltan_engineer_list, TZE_Ajiltan_mergejliin_list, TZE_Ajiltan_busad_list, TZE_alba_tasag_list
from applications.engineering.views import TohooromjjView, Tohooromj_Gunii_Hudag_list, Tohooromj_Usan_San_list, Tohooromj_Nasos_list, Tohooromj_Lab_list, Tohooromj_Sh_Suljee_list, Tohooromj_Ts_Baiguulamj_list, Tohooromj_Water_Car_list, Tohooromj_Bohir_Car_list, Tohooromj_Us_Damjuulah_list, Tohooromj_Us_Tugeeh_list, Tohooromj_Tonog_Tohooromj_list, TZE_hariutsaj_barilguud_list, Us_hangamjiin_schema_zurag_list
# Admin url
urlpatterns = [
# tza url
    url(r'^$', TzaHome.as_view(), name="home_tza"),
    url(r'^agree/(?P<iid>[0-9]+)/$', Handah_erh_huselt_list.agree, name="agree"),
    url(r'^email/sending/employee/(?P<id>[0-9]+)/$', request_email, name = 'email'),
    url(r'^email/sending/employee/remove/(?P<id>[0-9]+)/$', remove_email, name = 'email_remove'),
    ###### tur zuur ashiglagdah urls
    url(r'^tz_shuud_olgoh_list/$', TZ_shuud_olgolt_listView.as_view(), name='tz shuud olgoh list'),
    url(r'^tz_shuud_olgoh_list/tz_olgolt/(?P<baiguullaga_id>\d+)/$', TZ_shuud_olgoh.as_view(), name = 'tz shuud olgoh'),
    url(r'^tz_shuud_olgoh_list/show_gerchilgee/(?P<baiguullaga_id>\d+)/$', Show_gerchilgee.as_view(), name = 'show gerchilgee'),
    url(r'^add_baiguullaga/$', Add_baiguullaga.as_view(), name='add new baiguullaga'),

    ###### tza darga urls
    url(r'^huseltuud_huvaarilah/$', Tza_darga_huselt_huvaarilalt_list.as_view(), name='tza darga huselt huvaarilah'),
    url(r'^huselt_huvaarilah/(?P<huselt_id>\d+)/$', TZ_huselt_huvaarilah.as_view(), name='huselt huvaarilah'),
    url(r'^huselt_hurliin_tov/(?P<huselt_id>\d+)/$', TZ_huselt_hural_tovloh.as_view(), name='huseltiin hural tovloh'),
    url(r'^huselt_ajliin_heseg_date_tov/(?P<huselt_id>\d+)/$', Ajliin_heseg_date_tovloh.as_view(), name='ajliin heseg date tovloh'),
    url(r'^handah_erh_huselt_list/$', Handah_erh_huselt_list.as_view(), name='handah erh huselt list'),
    url(r'^handah_erh/tze/(?P<tze_id>\d+)/$', Handah_erh_baig_delgerengui.as_view(), name='handah_erh_baig_delgerengui'),


    
    url(r'^tz_huselt_delgerengui/detail/(?P<id>\d+)/$', TZ_huselt_delgerengui.as_view(), name='tz_huselt_detail_delgerengui'),

    ###### tza  mergejilten urls
    url(r'^huseltuud/$', Tza_Huselt_list.as_view(), name='huselt check'),
    url(r'^tz_huseltuud/check/(?P<burdel_history_id>\d+)/(?P<material_number>\d+)/$', TZA_TZ_Material_check.as_view(), name = 'tza_material_check'),
    url(r'^tz_huseltuud/check_finish_tza/(?P<huselt_id>\d+)/$', TZ_huselt_check_finish_tza.as_view(), name = 'huselt_check_finish_tza'),
    url(r'^tz_huseltuud/hurliin_shiidver_saving/(?P<huselt_id>\d+)/$', Hurliin_shiidver_saving.as_view(), name = 'hurliin_shiidver_saving'),
    url(r'^tz_huseltuud/delgerengui/(?P<huselt_id>\d+)/$', Tza_huselt_delgerengui.as_view(), name='tza_huselt_delgerengui'),
    url(r'^sent_material/(?P<burdel_history_id>\d+)/(?P<material_number>\d+)/$', TZA_TZ_Sent_materialView.as_view(), name = 'tza_sent_material_show'),
    
    ###### baiguullaga menu urls
    url(r'^baiguullaga/$', tzaBaiguullagaaView.as_view()),
    url(r'^baiguullaga/(?P<baiguullaga_id>\d+)/$', TZA_Baiguullaga_delgerengui.as_view(), name='baiguullaga_delgerengui'),

    url(r'^tze/profile/view/(?P<tze_id>\d+)/$', TZE_profileView.as_view(), name='baiguullaga_profile'),
    url(r'^tze/profile/medeelel_list/(?P<tze_id>\d+)/$', TZE_profile_baig_medeelel_list.as_view(), name = 'tze_baig_medeelel_list'),
    url(r'^tze/profile/zasag_tod/view/(?P<tze_id>\d+)/$', TZE_profile_zasag_tod_list.as_view(), name = 'tze_zasag_tod_list'),
    url(r'^tze/profile/hangagch_baig/view/(?P<tze_id>\d+)/$', TZE_profile_hangagch_baig_list.as_view(), name = 'tze_hangagch_baig_list'),
    url(r'^tze/profile/tatvar_tod/view/(?P<tze_id>\d+)/$', TZE_profile_tatvar_tod_list.as_view(), name = 'tze_tatvar_tod_list'),
    url(r'^tze/profile/audit_dugnelt/view/(?P<tze_id>\d+)/$', TZE_profile_audit_dugnelt_list.as_view(), name = 'tze_audit_dugnelt_list'),
    url(r'^tze/profile/norm_standart/view/(?P<tze_id>\d+)/$', TZE_profile_norm_standart_list.as_view(), name = 'tze_norm_standart_list'),
    url(r'^tze/profile/huuli_durem/view/(?P<tze_id>\d+)/$', TZE_profile_huuli_durem_list.as_view(), name = 'tze_huuli_durem_list'),
    url(r'^tze/profile/ajliin_bair_dugnelt/view/(?P<tze_id>\d+)/$', TZE_profile_ajliin_bair_dugnelt_list.as_view(), name = 'tze_ajliin_bair_dugnelt_list'),
    url(r'^tze/profile/uildver_tech_schema/view/(?P<tze_id>\d+)/$', TZE_profile_uildver_tech_schema_list.as_view(), name = 'tze_uildver_tech_schema_list'),
    url(r'^tze/profile/us_ashigluulah_zovshoorol/view/(?P<tze_id>\d+)/$', TZE_profile_us_ashigluulah_zovshoorol_list.as_view(), name = 'tze_us_ashigluulah_zovshoorol_list'),
    url(r'^tze/profile/sanhuu_tailan/view/(?P<tze_id>\d+)/$', TZE_profile_sanhuu_tailan_list.as_view(), name = 'tze_sanhuu_tailan_list'),
    url(r'^tze/profile/oron_toonii_schema/view/(?P<tze_id>\d+)/$', TZE_profile_oron_toonii_schema.as_view(), name = 'tze_oron_toonii_schema_list'),
    url(r'^tze/profile/sez_sudalgaa/view/(?P<tze_id>\d+)/$', TZE_profile_SEZ_sudalgaa.as_view(), name = 'tze_sez_sudalgaa_list'),

    url(r'^tze/profile/medeelel_list/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_baig_medeelel_list.as_view(), name = 'tze_baig_medeelel_list'),
    url(r'^tze/profile/zasag_tod/view/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_zasag_tod_list.as_view(), name = 'tze_zasag_tod_list'),
    url(r'^tze/profile/hangagch_baig/view/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_hangagch_baig_list.as_view(), name = 'tze_hangagch_baig_list'),
    url(r'^tze/profile/tatvar_tod/view/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_tatvar_tod_list.as_view(), name = 'tze_tatvar_tod_list'),
    url(r'^tze/profile/audit_dugnelt/view/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_audit_dugnelt_list.as_view(), name = 'tze_audit_dugnelt_list'),
    url(r'^tze/profile/norm_standart/view/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_norm_standart_list.as_view(), name = 'tze_norm_standart_list'),
    url(r'^tze/profile/huuli_durem/view/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_huuli_durem_list.as_view(), name = 'tze_huuli_durem_list'),
    url(r'^tze/profile/ajliin_bair_dugnelt/view/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_ajliin_bair_dugnelt_list.as_view(), name = 'tze_ajliin_bair_dugnelt_list'),
    url(r'^tze/profile/uildver_tech_schema/view/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_uildver_tech_schema_list.as_view(), name = 'tze_uildver_tech_schema_list'),
    url(r'^tze/profile/us_ashigluulah_zovshoorol/view/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_us_ashigluulah_zovshoorol_list.as_view(), name = 'tze_us_ashigluulah_zovshoorol_list'),
    url(r'^tze/profile/sanhuu_tailan/view/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_sanhuu_tailan_list.as_view(), name = 'tze_sanhuu_tailan_list'),
    url(r'^tze/profile/oron_toonii_schema/view/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_oron_toonii_schema.as_view(), name = 'tze_oron_toonii_schema_list'),
    url(r'^tze/profile/sez_sudalgaa/view/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_SEZ_sudalgaa.as_view(), name = 'tze_sez_sudalgaa_list'),












    ###### hunii noots menu
    url(r'^ajiltan/$', tzaAjiltanView.as_view()),
    url(r'^ajiltan/(?P<id>\d+)/$', TZA_Ajiltan_delgerengui.as_view(), name='tza_ajiltan_delgerengui'),
    url(r'^ajiltan/(?P<id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZA_Ajiltan_delgerengui.as_view(), name='tza_ajiltan_delgerengui'),

    url(r'^baiguullaga/profile/ajiltan/(?P<tze_id>\d+)/$', TZE_profile_hunii_nootsView.as_view(), name = 'ajiltan'),
    url(r'^baiguullaga/profile/employee_all_list/(?P<tze_id>\d+)/$', TZE_profile_Ajiltan_all_list.as_view(), name = 'tze_ajiltan_all_list'),
    url(r'^baiguullaga/profile/employee_udirdah_list/(?P<tze_id>\d+)/$', TZE_profile_Ajiltan_udirdah_list.as_view(), name = 'tze_ajiltan_udirdah_list'),
    url(r'^baiguullaga/profile/employee_engineer_list/(?P<tze_id>\d+)/$', TZE_profile_Ajiltan_engineer_list.as_view(), name = 'tze_ajiltan_engineer_list'),
    url(r'^baiguullaga/profile/employee_mergejil_list/(?P<tze_id>\d+)/$', TZE_profile_Ajiltan_mergejliin_list.as_view(), name = 'tze_ajiltan_mergejil_list'),
    url(r'^baiguullaga/profile/employee_busad_list/(?P<tze_id>\d+)/$', TZE_profile_Ajiltan_busad_list.as_view(), name = 'tze_ajiltan_busad_list'),
    url(r'^baiguullaga/profile/employee_alba_tasag_list/(?P<tze_id>\d+)/$', TZE_profile_alba_tasag_list.as_view(), name = 'tze_ajiltan_alba_tasag_list'),


    url(r'^baiguullaga/profile/employee_all_list/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_Ajiltan_all_list.as_view(), name = 'tze_ajiltan_all_list'),
    url(r'^baiguullaga/profile/employee_udirdah_list/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_Ajiltan_udirdah_list.as_view(), name = 'tze_ajiltan_udirdah_list'),
    url(r'^baiguullaga/profile/employee_engineer_list/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_Ajiltan_engineer_list.as_view(), name = 'tze_ajiltan_engineer_list'),
    url(r'^baiguullaga/profile/employee_mergejil_list/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_Ajiltan_mergejliin_list.as_view(), name = 'tze_ajiltan_mergejil_list'),
    url(r'^baiguullaga/profile/employee_busad_list/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_Ajiltan_busad_list.as_view(), name = 'tze_ajiltan_busad_list'),
    url(r'^baiguullaga/profile/employee_alba_tasag_list/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_alba_tasag_list.as_view(), name = 'tze_ajiltan_alba_tasag_list'),

    ##### tonog tohooromj menu
    url(r'^tohooromj/$', TZA_TohooromjjView.as_view(), name='tza_tohooromj_menu'),

    url(r'^tohooromj/gunii_hudag_list/$', TZA_Gunii_Hudag_list.as_view(), name = 'tza_gunii_hudag_list'),
    url(r'^tohooromj/usan_san_list/$', TZA_Usan_San_list.as_view(), name = 'tza_usan_san_list'),
    url(r'^tohooromj/nasos_list/$', TZA_Nasos_list.as_view(), name = 'tza_nasos_list'),
    url(r'^tohooromj/lab_list/$', TZA_Lab_list.as_view(), name = 'tza_lab_list'),
    url(r'^tohooromj/sh_suljee_list/$', TZA_Sh_Suljee_list.as_view(), name = 'tza_sh_suljee_list'),
    url(r'^tohooromj/ts_baiguulamj_list/$', TZA_Ts_Baiguulamj_list.as_view(), name = 'tza_ts_baig_list'),
    url(r'^tohooromj/us_tugeeh_list/$', TZA_Us_Tugeeh_list.as_view(), name = 'tza_us_tugeeh_list'),
    url(r'^tohooromj/us_damjuulah_list/$', TZA_Us_Damjuulah_list.as_view(), name = 'tza_us_damjuulah_list'),

    url(r'^tohooromj/water_car_list/$', TZA_Water_Car_list.as_view(), name = 'tza_water_car_list'),
    url(r'^tohooromj/bohir_car_list/$', TZA_Bohir_Car_list.as_view(), name = 'tza_bohir_car_list'),
    url(r'^tohooromj/tonog_tohooromj_list/$', TZA_Tonog_Tohooromj_list.as_view(), name = 'tza_tonog_tohooromj_list'),
    url(r'^tohooromj/abb_list/$', TZA_ABB_list.as_view(), name = 'tza_hariutsaj_barilguud_list'),
    url(r'^tohooromj/us_hangamj_list/$', TZA_Us_hangamjiin_schema_zurag_list.as_view(), name = 'tza_us_hangamj_schema_list'),

    
    url(r'^tohooromj/bb/approve/$', TZA_BB_approveView.as_view(), name = 'tza_bb_approve'),
    url(r'^tohooromj/car/approve/$', TZA_Car_approveView.as_view(), name = 'tza_car_approve'),
    url(r'^tohooromj/abb/approve/$', TZA_ABB_approveView.as_view(), name = 'tza_abb_approve'),
    url(r'^tohooromj/equipment/approve/$', TZA_equipment_approveView.as_view(), name = 'tza_equipment_approve'),

    url(r'^tohooromj/bb/disapprove/$', TZA_BB_disapproveView.as_view(), name = 'tza_bb_disapprove'),
    url(r'^tohooromj/car/disapprove/$', TZA_Car_disapproveView.as_view(), name = 'tza_car_disapprove'),
    url(r'^tohooromj/abb/disapprove/$', TZA_ABB_disapproveView.as_view(), name = 'tza_abb_disapprove'),
    url(r'^tohooromj/equipment/disapprove/$', TZA_equipment_disapproveView.as_view(), name = 'tza_equipment_disapprove'),

    url(r'^tohooromj/bb/update_many/tze/$', TZA_BB_tze_updateView.as_view(), name = 'tza_bb_update_tze_many'),
    url(r'^tohooromj/car/update_many/tze/$', TZA_Car_tze_updateView.as_view(), name = 'tza_car_update_tze_many'),
    url(r'^tohooromj/abb/update_many/tze/$', TZA_ABB_tze_updateView.as_view(), name = 'tza_abb_update_tze_many'),
    url(r'^tohooromj/equipment/update_many/tze/$', TZA_Equipment_tze_updateView.as_view(), name = 'tza_equipment_update_tze_many'),

    url(r'^baiguullaga/profile/tohooromj/(?P<tze_id>\d+)/$', TZE_profile_tonog_tohooromjView.as_view(),name = 'tohooromj_menu'),

    url(r'^baiguullaga/profile/tohooromj_gunii_hudag_list/(?P<tze_id>\d+)/$', TZE_profile_Gunii_Hudag_list.as_view(), name = 'tze_gunii_hudag_list'),
    url(r'^baiguullaga/profile/tohooromj_usan_san_list/(?P<tze_id>\d+)/$', TZE_profile_Usan_San_list.as_view(), name = 'tze_usan_san_list'),
    url(r'^baiguullaga/profile/tohooromj_nasos_list/(?P<tze_id>\d+)/$', TZE_profile_Nasos_list.as_view(), name = 'tze_nasos_list'),
    url(r'^baiguullaga/profile/tohooromj_lab_list/(?P<tze_id>\d+)/$', TZE_profile_Lab_list.as_view(), name = 'tze_lab_list'),
    url(r'^baiguullaga/profile/tohooromj_sh_suljee_list/(?P<tze_id>\d+)/$', TZE_profile_Sh_Suljee_list.as_view(), name = 'tze_sh_suljee_list'),
    url(r'^baiguullaga/profile/tohooromj_ts_baig_list/(?P<tze_id>\d+)/$', TZE_profile_Ts_Baiguulamj_list.as_view(), name = 'tze_ts_baig_list'),

    url(r'^baiguullaga/profile/tohooromj_water_car_list/(?P<tze_id>\d+)/$', TZE_profile_Water_Car_list.as_view(), name = 'tze_water_car_list'),
    url(r'^baiguullaga/profile/tohooromj_bohir_car_list/(?P<tze_id>\d+)/$', TZE_profile_Bohir_Car_list.as_view(), name = 'tze_bohir_car_list'),
    url(r'^baiguullaga/profile/tohooromj_us_damjuulah_list/(?P<tze_id>\d+)/$', TZE_profile_Us_Damjuulah_list.as_view(), name = 'tze_us_damjuulah_list'),
    url(r'^baiguullaga/profile/tohooromj_us_tugeeh_list/(?P<tze_id>\d+)/$', TZE_profile_Us_Tugeeh_list.as_view(), name = 'tze_us_tugeeh_list'),
    url(r'^baiguullaga/profile/tohooromj_tonog_tohooromj_list/(?P<tze_id>\d+)/$', TZE_profile_Tonog_Tohooromj_list.as_view(), name = 'tze_tonog_tohooromj_list'),
    url(r'^baiguullaga/profile/tze_hariutsaj_barilguud_list/(?P<tze_id>\d+)/$', TZE_profile_ABB_list.as_view(), name = 'tze_hariutsaj_barilguud_list'),
    url(r'^baiguullaga/profile/tohooromj_us_hangamj_list/(?P<tze_id>\d+)/$', TZE_profile_us_hangamj_schema_zurag_list.as_view(), name = 'tze_us_hangamj_schema_list'),


    url(r'^baiguullaga/profile/tohooromj_gunii_hudag_list/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_Gunii_Hudag_list.as_view(), name = 'tze_gunii_hudag_list'),
    url(r'^baiguullaga/profile/tohooromj_usan_san_list/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_Usan_San_list.as_view(), name = 'tze_usan_san_list'),
    url(r'^baiguullaga/profile/tohooromj_nasos_list/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_Nasos_list.as_view(), name = 'tze_nasos_list'),
    url(r'^baiguullaga/profile/tohooromj_lab_list/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_Lab_list.as_view(), name = 'tze_lab_list'),
    url(r'^baiguullaga/profile/tohooromj_sh_suljee_list/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_Sh_Suljee_list.as_view(), name = 'tze_sh_suljee_list'),
    url(r'^baiguullaga/profile/tohooromj_ts_baig_list/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_Ts_Baiguulamj_list.as_view(), name = 'tze_ts_baig_list'),

    url(r'^baiguullaga/profile/tohooromj_water_car_list/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_Water_Car_list.as_view(), name = 'tze_water_car_list'),
    url(r'^baiguullaga/profile/tohooromj_bohir_car_list/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_Bohir_Car_list.as_view(), name = 'tze_bohir_car_list'),
    url(r'^baiguullaga/profile/tohooromj_us_damjuulah_list/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_Us_Damjuulah_list.as_view(), name = 'tze_us_damjuulah_list'),
    url(r'^baiguullaga/profile/tohooromj_us_tugeeh_list/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_Us_Tugeeh_list.as_view(), name = 'tze_us_tugeeh_list'),
    url(r'^baiguullaga/profile/tohooromj_tonog_tohooromj_list/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_Tonog_Tohooromj_list.as_view(), name = 'tze_tonog_tohooromj_list'),
    url(r'^baiguullaga/profile/tze_hariutsaj_barilguud_list/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_ABB_list.as_view(), name = 'tze_hariutsaj_barilguud_list'),
    url(r'^baiguullaga/profile/tohooromj_us_hangamj_list/(?P<tze_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_profile_us_hangamj_schema_zurag_list.as_view(), name = 'tze_us_hangamj_schema_list'),

    
    url(r'^bb/tze/update/(?P<pk>\d+)/$', BB_tze_update.as_view(), name = 'bb_tze_update'),
    url(r'^car/tze/update/(?P<pk>\d+)/$', Car_tze_update.as_view(), name = 'car_tze_update'),
    url(r'^abb/tze/update/(?P<pk>\d+)/$', ABB_tze_update.as_view(), name = 'abb_tze_update'),





    ##### tz gerchilgee menu
    url(r'^tz_gerchilgee_list/$', TZA_TZ_gerchilgee_listView.as_view(), name = 'tza_tz_gerchilgee_list'),
    url(r'^tz_gerchilgee_delgerengui/(?P<tz_gerchilgee_id>\d+)/$', TZA_TZ_gerchilgee_delgerenguiView.as_view(), name = 'tza_tz_gerchilgee_delgerengui'),
    url(r'^tz_gerchilgee_tolov_change/(?P<tz_gerchilgee_id>\d+)/$', TZA_TZ_gerchilgee_tolov_change.as_view(), name = 'tza_tz_gerchilgee_tolov_change'),
    url(r'^tz_gerchilgee/sungah/(?P<tz_gerchilgee_id>\d+)/$', TZA_TZ_gerchilgee_sungah.as_view(), name = 'tza_tz_gerchilgee_sungah'),
    url(r'^tz_gerchilgee/insert/huulbar/(?P<tz_gerchilgee_id>\d+)/$', TZA_TZ_gerchilgee_huulbar_insert.as_view(), name = 'tza_tz_gerchilgee_huulbar_insert'),

    

    ##### ua tailan menu
    url(r'^uatailan/$', tzauatailan_menu.as_view(), name='tza_ua_tailan_menu'),
    url(r'^uatailan/uatailan_list$', tzauatailan_ListView.as_view(), name = 'tza_ua_tailan_list'),
    url(r'^uatailan/water_shinjilgee/$', TZA_water_shinjilgee_listView.as_view(), name='tza_water_shinjilgee_list'),
    url(r'^uatailan/bohir_shinjilgee/$', TZA_bohir_shinjilgee_listView.as_view(), name='tza_bohir_shinjilgee_list'),
    
    url(r'^uatailan/materials/(?P<pk>\d+)/$', tzauatailan_material_listView.as_view(), name = 'ua_tailan_material_list'),

    url(r'^uatailan/materials/husnegt1/(?P<pk>\d+)/$', TZA_UAT_hudag.as_view(), name = 'tza_ua_tailan_husnegt1'),
    url(r'^uatailan/materials/husnegt2_tsevershuuleh/(?P<pk>\d+)/$', TZA_UAT_tsevershuuleh.as_view(), name = 'tza_ua_tailan_tsevershuuleh'),
    url(r'^uatailan/materials/husnegt2_usansan/(?P<pk>\d+)/$', TZA_UAT_usansan.as_view(), name = 'tza_ua_tailan_usansan'),
    url(r'^uatailan/materials/husnegt2_nasosStants/(?P<pk>\d+)/$', TZA_UAT_tsever_us_nasosStants.as_view(), name = 'tza_ua_tailan_nasosstants'),
    url(r'^uatailan/materials/husnegt2_lab/(?P<pk>\d+)/$', TZA_UAT_tsever_us_lab.as_view(), name = 'tza_ua_tailan_lab'),
    url(r'^uatailan/materials/husnegt6/(?P<pk>\d+)/$', TZA_UAT_tsever_us_sh_suljee.as_view(), name = 'tza_ua_tailan_tsever_usnii_shugam'),
    url(r'^uatailan/materials/husnegt7/(?P<pk>\d+)/$', TZA_UAT_abb.as_view(), name = 'tza_ua_tailan_abb'),
    url(r'^uatailan/materials/husnegt8/(?P<pk>\d+)/$', TZA_UAT_us_dulaan_damjuulah_tov.as_view(), name = 'tza_ua_tailan_us_dulaan_damjuulah'),
    url(r'^uatailan/materials/husnegt9/(?P<pk>\d+)/$', TZA_UAT_bohir_us_sh_suljee.as_view(), name = 'tza_ua_tailan_bohir_usnii_shugam'),
    url(r'^uatailan/materials/husnegt10/(?P<pk>\d+)/$', TZA_UAT_tseverleh.as_view(), name = 'tza_ua_tailan_tseverleh'),
    url(r'^uatailan/materials/husnegt10_bohir_nasos/(?P<pk>\d+)/$', TZA_UAT_bohir_us_nasosStants.as_view(), name = 'tza_ua_tailan_husnegt10_bohir_nasos'),
    url(r'^uatailan/materials/husnegt11/(?P<pk>\d+)/$', TZA_UAT_us_tugeeh_bar.as_view(), name = 'tza_ua_tailan_us_tugeeh_bair'),
    url(r'^uatailan/materials/husnegt12/(?P<pk>\d+)/$', TZA_UAT_water_car.as_view(), name = 'tza_ua_tailan_water_car'),
    url(r'^uatailan/materials/husnegt13/(?P<pk>\d+)/$', TZA_UAT_bohir_car.as_view(), name = 'tza_ua_tailan_bohir_car'),
    url(r'^uatailan/materials/husnegt15/(?P<pk>\d+)/$', TZA_UAT_hunii_noots.as_view(), name = 'tza_ua_tailan_ajiltan'),


    url(r'^uatailan/create/$', UAT_create, name='tzes_uatailan_create'),
    url(r'^uatailan/negtgel/$', UAT_negtgel, name='tzes_uatailan_negtgel'),




    url(r'^gshu/$', tzagshutailanView.as_view(), name='tza_gshu_tailan_menu'),
    url(r'^gshu_tailan/check/(?P<gshu_id>\d+)/$', TZA_gshu_check_View.as_view(), name='tza_gshu_check'),
    url(r'^gshu/create/$', GSHU_tailan_create, name='tzes_gshu_tailan_create'),






    url(r'^export/excel/uatailan/(?P<pk>\d+)/$', UaTailanHorvuuleh , name = 'uatailanhorvuuleh'),
    url(r'^negtgel/$', tzaNegtgelView.as_view()),
    url(r'^export/excel/negtgel/$', UaTailanNegtgelHorvuuleh , name = 'uatailannegtgelhorvuuleh'),
    
    #url(r'^baiguullaga_huvaarilalt/(?P<baiguullaga_id>\d+)/$', Baig_huvaarilalt_update.as_view()),
    url(r'^export/excel/gshu/$', GshuTailanHorvuuleh , name = 'gshutailanhorvuuleh'),

    url(r'^export/excel/bb/$', BBHorvuuleh , name = 'bbhorvuuleh'),
    url(r'^export/excel/car/$', CarHorvuuleh , name = 'carhorvuuleh'),
    url(r'^export/excel/tonog/$', TonogHorvuuleh , name = 'tonoghorvuuleh'),
    url(r'^export/excel/ajiltan/$', AjiltanHorvuuleh , name = 'ajiltanhorvuuleh'),
    


    #url(r'^city/(?P<id>\d+)/$', city, name = 'city_ajax'),
    #url(r'^district/(?P<city_id>\d+)/(?P<district_id>\d+)/$', district, name = 'district_ajax'),
    #url(r'^husnegt/1/$', Husnegt1View.as_view()),
    #url(r'^husnegt/2/$', Husnegt2View.as_view()),
    #url(r'^husnegt/3/$', Husnegt3View.as_view()),
    #url(r'^husnegt/4/$', Husnegt4View.as_view()),
    #url(r'^husnegt/5/$', Husnegt5View.as_view()),
    #url(r'^uatailan/1/$', uatailan1View.as_view()),
    #url(r'^uatailan/2/$', uatailan2View.as_view()),
    #url(r'^uatailan/3/$', uatailan3View.as_view()),
    #url(r'^uatailan/4/$', uatailan4View.as_view()),
    #url(r'^uatailan/6/$', uatailan6View.as_view()),
    #url(r'^uatailan/7/$', uatailan7View.as_view()),
    #url(r'^uatailan/8/$', uatailan8View.as_view()),
    #url(r'^uatailan/9/$', uatailan9View.as_view()),
    #url(r'^uatailan/10/$', uatailan10View.as_view()),
    #url(r'^uatailan/11/$', uatailan11View.as_view()),
    #url(r'^uatailan/12/$', uatailan12View.as_view()),
    #url(r'^uatailan/13/$', uatailan13View.as_view()),
    #url(r'^uatailan/14/$', uatailan14View.as_view()),
]
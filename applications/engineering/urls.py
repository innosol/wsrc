from django.conf.urls import url, include
from applications.engineering.views import *
from django.views.generic import TemplateView
import django.views.defaults

urlpatterns = [
    url(r'^chaining/', include('smart_selects.urls')),
    #### tz zovshoorol menu
    url(r'^tz_tables/$', Tusgai_zovshoorolView.as_view(), name='tusgai zovshoorol huselt menu'),
    url(r'^tz_huseltuud/delgerengui/(?P<huselt_id>\d+)/$', TZE_huselt_delgerengui.as_view(), name='tze_tz_huselt_delgerengui'),
    url(r'^tz_gerchilgee_delgerengui/(?P<tz_gerchilgee_id>\d+)/$', TZE_TZ_gerchilgee_delgerengui.as_view(), name = 'tze_tz_gerchilgee_delgerengui'),
    url(r'^material_choose_2/(?P<huselt_id>\d+)/$', TZ_material2_chooseView.as_view(), name = 'material_choose 2'),
    url(r'^material_choose_3/(?P<huselt_id>\d+)/$', TZ_material3_chooseView.as_view(), name = 'material_choose 3'),
    url(r'^material_choose_4/(?P<huselt_id>\d+)/$', TZ_material4_chooseView.as_view(), name = 'material_choose 4'),
    url(r'^material_choose_5/(?P<huselt_id>\d+)/$', TZ_material5_chooseView.as_view(), name = 'material_choose 5'),
    url(r'^material_choose_6/(?P<huselt_id>\d+)/$', TZ_material6_chooseView.as_view(), name = 'material_choose 6'),
    url(r'^material_choose_7/(?P<huselt_id>\d+)/$', TZ_material7_chooseView.as_view(), name = 'material_choose 7'),
    url(r'^material_choose_8/(?P<huselt_id>\d+)/$', TZ_material8_chooseView.as_view(), name = 'material_choose 8'),
    url(r'^material_choose_9/(?P<huselt_id>\d+)/$', TZ_material9_chooseView.as_view(), name = 'material_choose 9'),
    url(r'^material_choose_10/(?P<huselt_id>\d+)/$', TZ_material10_chooseView.as_view(), name = 'material_choose 10'),
    url(r'^material_choose_11/(?P<huselt_id>\d+)/$', TZ_material11_chooseView.as_view(), name = 'material_choose 11'),
    url(r'^material_choose_12/(?P<huselt_id>\d+)/$', TZ_material12_chooseView.as_view(), name = 'material_choose 12'),
    url(r'^material_choose_13/(?P<huselt_id>\d+)/$', TZ_material13_chooseView.as_view(), name = 'material_choose 13'),
    url(r'^material_choose_14/(?P<huselt_id>\d+)/$', TZ_material14_chooseView.as_view(), name = 'material_choose 14'),
    url(r'^material_choose_15/(?P<huselt_id>\d+)/$', TZ_material15_chooseView.as_view(), name = 'material_choose 15'),
    url(r'^material_choose_16/(?P<huselt_id>\d+)/(?P<material_number>\d+)/$', TZ_material16_chooseView.as_view(), name = 'material_choose 16'),
    url(r'^sent_material/(?P<burdel_history_id>\d+)/(?P<material_number>\d+)/$', Sent_materialView.as_view(), name = 'sent_material_show'),
    url(r'^tz_huselt_ilgeeh/(?P<huselt_id>\d+)/$', TZ_tze_huselt_ilgeeh.as_view(), name = 'tze_tz_huselt_ilgeeh'),
    url(r'^tz_huselt_tsutslah/(?P<huselt_id>\d+)/$', TZ_tze_huselt_tsutslah.as_view(), name = 'tze_tz_huselt_tsutslah'),
    url(r'^tz_huselt_gargah/$', TZ_huselt_new.as_view(), name = 'tze_tz_huselt_new'),
    url(r'^tz_huselt_zaalt_edit/(?P<burdel_id>\d+)/$', TZ_huselt_zaalt_edit.as_view(), name = 'tze_tz_huselt_zaalt_edit'),
    url(r'^tz_huselt_show_material/(?P<burdel_id>\d+)/(?P<material_number>\d+)/$', Show_materialView.as_view(), name = 'burduulj baigaa material show'),

    url(r'^tusgai_zovshoorol/insert/form/zasag_tod/$', TZ_Zasag_tod_FormView.as_view(), name = 'zasag_tod_insert_tz'),
    url(r'^tusgai_zovshoorol/insert/form/han_baig/$', TZ_Hangagch_baig_FormView.as_view(), name = 'han_baig_insert_tz'),
    url(r'^tusgai_zovshoorol/insert/form/tax_tod/$', TZ_Tax_tod_FormView.as_view(), name = 'tax_tod_insert_tz'),
    url(r'^tusgai_zovshoorol/insert/form/audit_dugnelt/$', TZ_Audit_dugnelt_FormView.as_view(), name = 'audit_dugnelt_insert_tz'),
    url(r'^tusgai_zovshoorol/insert/form/norm_standart/$', TZ_Norm_standart_FormView.as_view(), name = 'norm_standart_insert_tz'),
    url(r'^tusgai_zovshoorol/insert/form/us_zovshoorol/$', TZ_Us_zovshoorol_FormView.as_view(), name = 'us_zovshoorol_insert_tz'),
    url(r'^tusgai_zovshoorol/insert/form/sanhuu_tailan/$', TZ_Sanhuu_tailan_FormView.as_view(), name = 'sanhuu_tailan_insert_tz'),
    url(r'^tusgai_zovshoorol/insert/form/hariutssan_barilguud/$', TZ_Hariutssan_barilguud_FormView.as_view(), name = 'hariutssan_barilguud_insert_tz'),
    url(r'^tusgai_zovshoorol/insert/form/oron_too_schema/$', TZ_Oron_too_schema_FormView.as_view(), name = 'oron_too_schema_insert_tz'),
    url(r'^tusgai_zovshoorol/insert/form/uildver_tech_schema/$', TZ_Uildver_tech_schema_FormView.as_view(), name = 'uildver_tech_schema_insert_tz'),
    url(r'^tusgai_zovshoorol/insert/form/mheg_dugnelt/$', TZ_MHEG_dugnelt_FormView.as_view(), name = 'MHEG_dugnelt_insert_tz'),
    url(r'^tusgai_zovshoorol/insert/form/ajliin_bair_dugnelt/$', TZ_Ajliin_bair_dugnelt_FormView.as_view(), name = 'ajliin_bair_dugnelt_insert_tz'),
    url(r'^tusgai_zovshoorol/insert/form/us_shinjilgee/(?P<burdel_id>\d+)/$', TZ_material_water_shijilgee.as_view(), name = 'tz_huselt_us_shijilgee_insert'),
    url(r'^tusgai_zovshoorol/insert/form/bohir_shinjilgee/(?P<burdel_id>\d+)/$', TZ_material_bohir_shinjilgee.as_view(), name = 'tz_huselt_bohir_shijilgee_insert'),

    url(r'^tusgai_zovshoorol/update/form/us_shinjilgee/(?P<burdel_id>\d+)/$', TZ_water_shinjilgee_update.as_view(), name = 'tz_huselt_us_shijilgee_update'),
    url(r'^tusgai_zovshoorol/update/form/bohir_shinjilgee/(?P<burdel_id>\d+)/$', TZ_bohir_shinjilgee_update.as_view(), name = 'tz_huselt_bohir_shijilgee_update'),

    url(r'^tusgai_zovshoorol/detail/form/bohir_shinjilgee/(?P<id>\d+)/$', TZ_bohir_shinjilgee_delgerengui.as_view(), name = 'tz_huselt_bohir_shijilgee_delgerengui'),
    
    url(r'^tusgai_zovshoorol/insert/form/hudag/(?P<huselt_id>\d+)/$', TZ_hudag_formView.as_view(), name = 'tz_hudag_insert'),
    url(r'^tusgai_zovshoorol/insert/form/usansan/(?P<huselt_id>\d+)/$', TZ_usansan_formView.as_view(), name = 'tz_usansan_insert'),
    url(r'^tusgai_zovshoorol/insert/form/nasos_stants/(?P<huselt_id>\d+)/$', TZ_nasosStants_formView.as_view(), name = 'tz_nasosStants_insert'),
    url(r'^tusgai_zovshoorol/insert/form/lab/(?P<huselt_id>\d+)/$', TZ_lab_formView.as_view(), name = 'tz_lab_insert'),
    url(r'^tusgai_zovshoorol/insert/form/abb/(?P<huselt_id>\d+)/$', TZ_abb_formView.as_view(), name = 'tz_abb_insert'),
    url(r'^tusgai_zovshoorol/insert/form/us_dulaan_damjuulah/(?P<huselt_id>\d+)/$', TZ_us_damjuulah_formView.as_view(), name = 'tz_us_dulaan_damjuulah_insert'),
    url(r'^tusgai_zovshoorol/insert/form/sh_suljee/(?P<huselt_id>\d+)/$', TZ_sh_suljee_formView.as_view(), name = 'tz_sh_suljee_insert'),
    url(r'^tusgai_zovshoorol/insert/form/ts_baig/(?P<huselt_id>\d+)/$', TZ_ts_baig_formView.as_view(), name = 'tz_ts_baig_insert'),
    url(r'^tusgai_zovshoorol/insert/form/us_tugeeh/(?P<huselt_id>\d+)/$', TZ_us_tugeeh_formView.as_view(), name = 'tz_us_tugeeh_insert'),
    url(r'^tusgai_zovshoorol/insert/form/water_car/(?P<huselt_id>\d+)/$', TZ_water_car_formView.as_view(), name = 'tz_water_car_insert'),
    url(r'^tusgai_zovshoorol/insert/form/bohir_car/(?P<huselt_id>\d+)/$', TZ_bohir_car_formView.as_view(), name = 'tz_bohir_car_insert'),

    url(r'^tusgai_zovshoorol/insert/form/norm_standard/(?P<huselt_id>\d+)/$', TZ_standard_formView.as_view(), name = 'tz_norm_standart_insert'),
    url(r'^tusgai_zovshoorol/insert/form/huuli_durem/(?P<huselt_id>\d+)/$', TZ_huuli_durem_formView.as_view(), name = 'tz_huuli_durem_insert'),
    url(r'^tusgai_zovshoorol/insert/form/oron_too/(?P<huselt_id>\d+)/$', TZ_oron_too_schema_formView.as_view(), name = 'tz_oron_too_insert'),
    url(r'^tusgai_zovshoorol/insert/form/equipment/(?P<huselt_id>\d+)/$', TZ_equipment_formView.as_view(), name = 'tz_equipment_insert'),


    



    
    

    #### handah erh
    url(r'^handah_erh_list/$', Handah_erhView.as_view(), name='tze_handah_erh_menu'),
    url(r'^handah_erh/change/engineer/$', Engineer_user_change.as_view(), name='tze_engineer_user_change'),
    url(r'^handah_erh/change/account/$', Account_user_change.as_view(), name='tze_account_user_change'),
    url(r'^handah_erh/remove/engineer/$', Engineer_user_remove.as_view(), name='tze_engineer_user_remove'),
    url(r'^handah_erh/remove/account/$', Account_user_remove.as_view(), name='tze_account_user_remove'),
    


    #### baiguullaga
    url(r'^baiguullaga/$',BaiguullagaaView.as_view(), name='baiguullaga_menu'),

    url(r'^organization/update/$', OrgUpdateView.as_view(), name="org_update"),
    url(r'^baiguullaga/insert/form/zasag_tod/$', Zasag_tod_FormView.as_view(), name = 'zasag_tod_insert'),
    url(r'^baiguullaga/insert/form/han_baig/$', Hangagch_baig_FormView.as_view(), name = 'han_baig_insert'),
    url(r'^baiguullaga/insert/form/tax_tod/$', Tax_tod_FormView.as_view(), name = 'tax_tod_insert'),
    url(r'^baiguullaga/insert/form/audit_dugnelt/$', Audit_dugnelt_FormView.as_view(), name = 'audit_dugnelt_insert'),
    url(r'^baiguullaga/insert/form/norm_standart/$', Norm_standart_FormView.as_view(), name = 'norm_standart_insert'),
    url(r'^baiguullaga/insert/form/huuli_durem/$', Huuli_durem_FormView.as_view(), name = 'tze_huuli_durem_insert'),
    url(r'^baiguullaga/insert/form/us_zovshoorol/$', Us_zovshoorol_FormView.as_view(), name = 'us_zovshoorol_insert'),
    url(r'^baiguullaga/insert/form/sanhuu_tailan/$', Sanhuu_tailan_FormView.as_view(), name = 'sanhuu_tailan_insert'),
    url(r'^baiguullaga/insert/form/hariutssan_barilguud/$', Hariutssan_barilguud_FormView.as_view(), name = 'hariutssan_barilguud_insert'),
    url(r'^baiguullaga/insert/form/oron_too_schema/$', Oron_too_schema_FormView.as_view(), name = 'oron_too_schema_insert'),
    url(r'^baiguullaga/insert/form/ajliin_bair_dugnelt/$', Ajliin_bair_dugnelt_FormView.as_view(), name = 'ajliin_bair_dugnelt_insert'),
    url(r'^baiguullaga/insert/form/uildver_tech_schema/$', Uildver_tech_schema_FormView.as_view(), name = 'uildver_tech_schema_insert'),

    url(r'^tze_baig_medeelel_list/$', TZE_baig_medeelel_list.as_view(), name = 'tze_baig_medeelel_list'),
    url(r'^tze_zasag_tod_list/$', TZE_zasag_tod_list.as_view(), name = 'tze_zasag_tod_list'),
    url(r'^tze_hangagch_baig_list/$', TZE_hangagch_baig_list.as_view(), name = 'tze_hangagch_baig_list'),
    url(r'^tze_tatvar_tod_list/$', TZE_tatvar_tod_list.as_view(), name = 'tze_tatvar_tod_list'),
    url(r'^tze_audit_dugnelt_list/$', TZE_audit_dugnelt_list.as_view(), name = 'tze_audit_dugnelt_list'),
    url(r'^tze_norm_standart_list/$', TZE_norm_standart_list.as_view(), name = 'tze_norm_standart_list'),
    url(r'^tze_huuli_durem_list/$', TZE_huuli_durem_list.as_view(), name = 'tze_huuli_durem_list'),
    url(r'^tze_us_zuvshoorol_list/$', TZE_us_ashigluulah_zovshoorol_list.as_view(), name = 'tze_us_ashigluulah_zovshoorol_list'),
    url(r'^tze_sanhuu_tailan_list/$', TZE_sanhuu_tailan_list.as_view(), name = 'tze_sanhuu_tailan_list'),
    url(r'^tze_oron_toonii_schema_list/$', TZE_oron_toonii_schema.as_view(), name = 'tze_oron_toonii_schema_list'),
    url(r'^tze_sez_sudalgaa_list/$', TZE_SEZ_sudalgaa.as_view(), name = 'tze_sez_sudalgaa_list'),
    url(r'^ajliin_bair_dugnelt/list/$', TZE_ajliin_bair_dugnelt_list.as_view(), name = 'tze_ajliin_bair_dugnelt_list'),
    url(r'^uildver_tech_schema/list/$', TZE_uildver_tech_schema_list.as_view(), name = 'tze_uildver_tech_schema_list'),
    

    url(r'^zdt/delete/(?P<id>\d+)/$', Zasag_tod_DeleteView.as_view(), name = 'zasag_tod_delete'),
    url(r'^han/delete/(?P<id>\d+)/$', Hangagch_baig_DeleteView.as_view(), name = 'han_baig_delete'),
    url(r'^tax/delete/(?P<id>\d+)/$', Tax_tod_DeleteView.as_view(), name = 'tax_tod_delete'),
    url(r'^audit/delete/(?P<id>\d+)/$', Audit_dugnelt_DeleteView.as_view(), name = 'audit_dugnelt_delete'),
    url(r'^norm/delete/(?P<id>\d+)/$', Norm_standart_DeleteView.as_view(), name = 'norm_standart_delete'),
    url(r'^huuli_durem/delete/(?P<id>\d+)/$', TZE_huuli_durem_delete.as_view(), name = 'tze_huuli_durem_delete'),
    url(r'^us_zovshoorol/delete/(?P<id>\d+)/$', Us_zovshoorol_DeleteView.as_view(), name = 'us_zovshoorol_delete'),
    url(r'^sanhuu_balance/delete/(?P<id>\d+)/$', Sanhuu_tailan_DeleteView.as_view(), name = 'sanhuu_tailan_delete'),
    url(r'^abb/delete/(?P<id>\d+)/$', Hariutssan_barilguud_DeleteView.as_view(), name = 'hariutssan_barilguud_delete'),
    url(r'^oron_too_schema/delete/(?P<id>\d+)/$', Oron_too_schema_DeleteView.as_view(), name = 'oron_too_schema_delete'),
    url(r'^ajliin_bair_dugnelt/delete/(?P<id>\d+)/$', Ajliin_bair_dugnelt_DeleteView.as_view(), name = 'ajliin_bair_dugnelt_delete'),
    url(r'^uildver_tech_schema/delete/(?P<id>\d+)/$', Uildver_tech_schema_deleteView.as_view(), name = 'uildver_tech_schema_delete'),


    #### hunii noots
    url(r'^ajiltan/$', EmployeeView.as_view(), name = 'ajiltan'),
    url(r'^employee/$', Ajiltan_createView.as_view(), name = 'ajiltan_create'),
    url(r'^ajiltan/(?P<id>\d+)/$', AjiltanUpdateView.as_view(), name = 'ajiltan_update'),
    url(r'^ajiltan/delete/(?P<id>\d+)/$', TZE_AjiltanDeleteView.as_view(), name = 'tze_ajiltan_delete'),
    url(r'^employee/detail/(?P<id>\d+)/$', TZE_Ajiltan_delgerengui.as_view(), name = 'tze_ajiltan_delgerengui'),
    url(r'^employee/detail/(?P<id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', TZE_Ajiltan_delgerengui.as_view(), name='tze_ajiltan_delgerengui'),

    url(r'^employee_all_list/$', TZE_Ajiltan_all_list.as_view(), name = 'tze_ajiltan_all_list'),
    url(r'^employee_udirdah_list/$', TZE_Ajiltan_udirdah_list.as_view(), name = 'tze_ajiltan_udirdah_list'),
    url(r'^employee_engineer_list/$', TZE_Ajiltan_engineer_list.as_view(), name = 'tze_ajiltan_engineer_list'),
    url(r'^employee_mergejil_list/$', TZE_Ajiltan_mergejliin_list.as_view(), name = 'tze_ajiltan_mergejil_list'),
    url(r'^employee_busad_list/$', TZE_Ajiltan_busad_list.as_view(), name = 'tze_ajiltan_busad_list'),
    url(r'^employee_alba_tasag_insert/$', TZE_alba_tasag_insert.as_view(), name = 'tze_alba_tasag_insert'),
    url(r'^employee_alba_tasag_/update/(?P<id>\d+)/$', TZE_alba_tasag_update.as_view(), name='tze_alba_tasag_update'),
    url(r'^employee_alba_tasag_/delete/(?P<id>\d+)/$', TZE_alba_tasag_delete.as_view(), name='tze_alba_tasag_delete'),
    url(r'^employee_alba_tasag_list/$', TZE_alba_tasag_list.as_view(), name = 'tze_ajiltan_alba_tasag_list'),
    url(r'^employee_alban_tushaal_list/(?P<id>\d+)/$', TZE_alban_tushaal_list.as_view(), name='tze_alban_tushaal_list'),
    url(r'^employee_alban_tushaal_edit/(?P<id>\d+)/$', TZE_alban_tushaal_edit.as_view(), name='tze_alban_tushaal_edit'),
    url(r'^employee_alba_tasag/ajilchid_list/(?P<id>\d+)/$', TZE_alba_tasgiin_ajilchid_list.as_view(), name='tze_alba_tasgiin_ajilchid_list'),
    
    #url(r'^engineering/ajiltan/delete/(?P<id>\d+)/$', 'applications.engineering.views.delete_ajiltan', name ="ajiltan_delete"),
    


    #### tonog tohooromj
    url(r'^tohooromj/$', TohooromjjView.as_view(),name = 'tohooromj_menu'),
    url(r'^tohooromj_davtan/$', TemplateView.as_view(template_name="tohooromj_davtan.html")),

    url(r'^tohooromj/bb/(?P<id>\d+)/$', BB_deleteView.as_view(), name = 'tze_bb_delete'),
    url(r'^tohooromj/car/(?P<id>\d+)/$', Car_deleteView.as_view(), name = 'tze_car_delete'),
    url(r'^tohooromj/equipment/(?P<id>\d+)/$', Equipment_deleteView.as_view(), name = 'tze_equipment_delete'),
    url(r'^tohooromj/us_hangamj_schema/(?P<id>\d+)/$', Us_hangamj_deleteView.as_view(), name = 'tze_us_hangamj_schema_delete'),


    url(r'^tohooromj_gunii_hudag_list/$', Tohooromj_Gunii_Hudag_list.as_view(), name = 'tze_gunii_hudag_list'),
    url(r'^tohooromj_usan_san_list/$', Tohooromj_Usan_San_list.as_view(), name = 'tze_usan_san_list'),
    url(r'^tohooromj_nasos_list/$', Tohooromj_Nasos_list.as_view(), name = 'tze_nasos_list'),
    url(r'^tohooromj_lab_list/$', Tohooromj_Lab_list.as_view(), name = 'tze_lab_list'),
    url(r'^tohooromj_sh_suljee_list/$', Tohooromj_Sh_Suljee_list.as_view(), name = 'tze_sh_suljee_list'),
    url(r'^tohooromj_ts_baig_list/$', Tohooromj_Ts_Baiguulamj_list.as_view(), name = 'tze_ts_baig_list'),

    url(r'^tohooromj_water_car_list/$', Tohooromj_Water_Car_list.as_view(), name = 'tze_water_car_list'),
    url(r'^tohooromj_bohir_car_list/$', Tohooromj_Bohir_Car_list.as_view(), name = 'tze_bohir_car_list'),
    url(r'^tohooromj_us_damjuulah_list/$', Tohooromj_Us_Damjuulah_list.as_view(), name = 'tze_us_damjuulah_list'),
    url(r'^tohooromj_us_tugeeh_list/$', Tohooromj_Us_Tugeeh_list.as_view(), name = 'tze_us_tugeeh_list'),
    url(r'^tohooromj_tonog_tohooromj_list/$', Tohooromj_Tonog_Tohooromj_list.as_view(), name = 'tze_tonog_tohooromj_list'),
    url(r'^tze_hariutsaj_barilguud_list/$', TZE_hariutsaj_barilguud_list.as_view(), name = 'tze_hariutsaj_barilguud_list'),
    url(r'^tohooromj_us_hangamj_list/$', Us_hangamjiin_schema_zurag_list.as_view(), name = 'tze_us_hangamj_schema_list'),

    url(r'^tohooromj_gunii_hudag/delgerengui/(?P<id>\d+)/$', Tohooromj_Gunii_Hudag_delgerengui.as_view(), name = 'tze_gunii_hudag_delgerengui'),
    url(r'^tohooromj_usan_san/delgerengui/(?P<id>\d+)/$', Tohooromj_Usan_San_delgerengui.as_view(), name = 'tze_usan_san_delgerengui'),
    url(r'^tohooromj_nasos/delgerengui/(?P<id>\d+)/$', Tohooromj_NasosStants_delgerengui.as_view(), name = 'tze_nasosStants_delgerengui'),
    url(r'^tohooromj_lab/delgerengui/(?P<id>\d+)/$', Tohooromj_Lab_delgerengui.as_view(), name = 'tze_lab_delgerengui'),
    url(r'^tohooromj_sh_suljee/delgerengui/(?P<id>\d+)/$', Tohooromj_Sh_Suljee_delgerengui.as_view(), name = 'tze_sh_suljee_delgerengui'),
    url(r'^tohooromj_ts_baig/delgerengui/(?P<id>\d+)/$', Tohooromj_Ts_Baiguulamj_delgerengui.as_view(), name = 'tze_ts_baig_delgerengui'),
    url(r'^tohooromj_water_car/delgerengui/(?P<id>\d+)/$', Tohooromj_Water_Car_delgerengui.as_view(), name = 'tze_water_car_delgerengui'),
    url(r'^tohooromj_bohir_car/delgerengui/(?P<id>\d+)/$', Tohooromj_Bohir_Car_delgerengui.as_view(), name = 'tze_bohir_car_delgerengui'),
    url(r'^tohooromj_us_damjuulah/delgerengui/(?P<id>\d+)/$', Tohooromj_Us_Damjuulah_delgerengui.as_view(), name = 'tze_us_damjuulah_delgerengui'),
    url(r'^tohooromj_us_tugeeh/delgerengui/(?P<id>\d+)/$', Tohooromj_Us_Tugeeh_delgerengui.as_view(), name = 'tze_us_tugeeh_delgerengui'),
    url(r'^tohooromj_tonog_tohooromj/delgerengui/(?P<id>\d+)/$', Tohooromj_Tonog_Tohooromj_delgerengui.as_view(), name = 'tze_tonog_tohooromj_delgerengui'),
    url(r'^tohooromj_abb/delgerengui/(?P<id>\d+)/$', Tohooromj_ABB_delgerengui.as_view(), name = 'tze_abb_delgerengui'),


    url(r'^tohooromj_gunii_hudag/delgerengui/(?P<id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', Tohooromj_Gunii_Hudag_delgerengui.as_view(), name = 'tze_gunii_hudag_delgerengui'),
    url(r'^tohooromj_usan_san/delgerengui/(?P<id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', Tohooromj_Usan_San_delgerengui.as_view(), name = 'tze_usan_san_delgerengui'),
    url(r'^tohooromj_nasos/delgerengui/(?P<id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', Tohooromj_NasosStants_delgerengui.as_view(), name = 'tze_nasosStants_delgerengui'),
    url(r'^tohooromj_lab/delgerengui/(?P<id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', Tohooromj_Lab_delgerengui.as_view(), name = 'tze_lab_delgerengui'),
    url(r'^tohooromj_sh_suljee/delgerengui/(?P<id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', Tohooromj_Sh_Suljee_delgerengui.as_view(), name = 'tze_sh_suljee_delgerengui'),
    url(r'^tohooromj_ts_baig/delgerengui/(?P<id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', Tohooromj_Ts_Baiguulamj_delgerengui.as_view(), name = 'tze_ts_baig_delgerengui'),
    url(r'^tohooromj_water_car/delgerengui/(?P<id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', Tohooromj_Water_Car_delgerengui.as_view(), name = 'tze_water_car_delgerengui'),
    url(r'^tohooromj_bohir_car/delgerengui/(?P<id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', Tohooromj_Bohir_Car_delgerengui.as_view(), name = 'tze_bohir_car_delgerengui'),
    url(r'^tohooromj_us_damjuulah/delgerengui/(?P<id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', Tohooromj_Us_Damjuulah_delgerengui.as_view(), name = 'tze_us_damjuulah_delgerengui'),
    url(r'^tohooromj_us_tugeeh/delgerengui/(?P<id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', Tohooromj_Us_Tugeeh_delgerengui.as_view(), name = 'tze_us_tugeeh_delgerengui'),
    url(r'^tohooromj_tonog_tohooromj/delgerengui/(?P<id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', Tohooromj_Tonog_Tohooromj_delgerengui.as_view(), name = 'tze_tonog_tohooromj_delgerengui'),
    url(r'^tohooromj_abb/delgerengui/(?P<id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', Tohooromj_ABB_delgerengui.as_view(), name = 'tze_abb_delgerengui'),

    
    url(r'^tohooromj/lab/shinjilgee/(?P<id>\d+)/$', Tohooromj_Lab_shinjilgee_list.as_view(), name = 'tze_lab_shinjilgee_list'),

    url(r'^tonog_tohooromj/insert/form/hudag_zurag/$', HudagZuragFormView.as_view(), name = 'hudag_zurag_insert'),
    url(r'^tonog_tohooromj/insert/form/hudag/$', HudagFormView.as_view(), name = 'hudag_insert'),
    url(r'^tonog_tohooromj/insert/form/nasos/$', NasosStantsFormView.as_view(), name = 'nasos_stants_insert'),
    url(r'^tonog_tohooromj/insert/form/lab/$', LabFormView.as_view(), name = 'lab_insert'),
    url(r'^tonog_tohooromj/insert/form/shugam_suljee/$', ShugamSuljeeFormView.as_view(), name = 'shugam_insert'),
    url(r'^tonog_tohooromj/insert/form/tseverleh_baiguulamj/$', TseverlehBaiguulamjFormView.as_view(), name = 'ts_baiguulamj_insert'),
    url(r'^tonog_tohooromj/insert/form/usan_san/$', UsanSanFormView.as_view(), name = 'usansan_insert'),
    url(r'^tonog_tohooromj/insert/form/us_damjuulah_bair/$', UsDamjuulahBairFormView.as_view(), name = 'us_damjuulah_insert'),
    url(r'^tonog_tohooromj/insert/form/us_tugeeh_bair/$', UsTugeehBairFormView.as_view(), name = 'us_tugeeh_insert'),
    url(r'^tonog_tohooromj/insert/form/water_car/$', WaterCarFormView.as_view(), name = 'car_insert'),
    url(r'^tonog_tohooromj/insert/form/bohir_car/$', BohirCarFormView.as_view(), name = 'bohircar_insert'),
    url(r'^tonog_tohooromj/insert/form/equipment/$', EquipmentFormView.as_view(), name = 'tonog_insert'),

    
    url(r'^tonog_tohooromj/edit/usan_san_wash/(?P<id>\d+)/$', UsanSan_UgaalgaFormView.as_view(), name='tze_usan_san_wash_edit'),
    url(r'^tonog_tohooromj/list/usan_san_wash/(?P<id>\d+)/$', UsanSan_UgaalgaListView.as_view(), name='tze_usan_san_wash_list'),
    url(r'^tonog_tohooromj/edit/us_tugeeh_wash/(?P<id>\d+)/$', UsTugeehB_Sav_ugaalgaFormView.as_view(), name='tze_us_tugeeh_wash_edit'),

    url(r'^tonog_tohooromj/insert/form/hudag/(?P<pk>\d+)/$', HudagUpdateView.as_view(), name = 'hudag_insert'),
    url(r'^tonog_tohooromj/insert/form/usan_san/(?P<pk>\d+)/$', UsansanUpdateView.as_view(), name = 'usansan_insert'),
    url(r'^tonog_tohooromj/insert/form/nasos/(?P<pk>\d+)/$', NasosUpdateView.as_view(), name = 'nasos_insert'),
    url(r'^tonog_tohooromj/insert/form/lab/(?P<pk>\d+)/$', LabUpdateView.as_view(), name = 'lab_insert'),
    url(r'^tonog_tohooromj/insert/form/shugam_suljee/(?P<pk>\d+)/$', SuljeeUpdateView.as_view(), name = 'shugam_insert'),
    url(r'^tonog_tohooromj/insert/form/tseverleh_baiguulamj/(?P<pk>\d+)/$', Ts_baiguulamjUpdateView.as_view(), name = 'ts_baiguulamj_insert'),
    url(r'^tonog_tohooromj/insert/form/water_car/(?P<pk>\d+)/$', WatercarUpdateView.as_view(), name = 'car_insert'),
    url(r'^tonog_tohooromj/insert/form/bohir_car/(?P<pk>\d+)/$', BohircarUpdateView.as_view(), name = 'bohircar_insert'),
    url(r'^tonog_tohooromj/insert/form/us_damjuulah_bair/(?P<pk>\d+)/$', UsdamjuulahUpdateView.as_view(), name = 'us_damjuulah_insert'),
    url(r'^tonog_tohooromj/insert/form/us_tugeeh_bair/(?P<pk>\d+)/$', UstugeehUpdateView.as_view(), name = 'us_tugeeh_insert'),
    url(r'^tonog_tohooromj/insert/form/equipment/(?P<pk>\d+)/$', EquipmentUpdateView.as_view(), name = 'tonog_insert'),



    #### UA tailan
    url(r'^uamedee/$', uamedeeView.as_view(), name="tze_uamedee_menu"),
    
    url(r'^uamedee/tze_ua_tailan_list/$', UATailan_listView.as_view(), name="tze_ua_tailan_list"),
    url(r'^uamedee/water_analysis_list/$', Water_analysis_listView.as_view(), name="tze_water_analysis_list"),
    url(r'^uamedee/bohir_analysis_list/$', Bohir_analysis_listView.as_view(), name="tze_bohir_analysis_list"),

    url(r'^uamedee/insert/bohir_analysis/$', Bohir_analysis_formView.as_view(), name="tze_bohir_analysis_insert"),
    url(r'^uamedee/insert/savlasan_water_analysis/$', UA_water_analysis_insert.as_view(), name="tze_water_analysis_insert"),

    url(r'^uamedee/delgerengui/savlasan_water_analysis/(?P<pk>\d+)/$', UA_water_analysis_delgerengui.as_view(), name = 'tze_ua_water_analysis_delgerengui'),
    url(r'^uamedee/delgerengui/bohir_water_analysis/(?P<pk>\d+)/$', BohirWater_analysis_delgerengui.as_view(), name = 'tze_bohir_water_analysis_delgerengui'),
    

    #url(r'^uamedee/(?P<pk>\d+)/$', uamedeeView.as_view(), name = 'uamedee'),
    url(r'^wateranalysis/delete/(?P<id>\d+)/$', 'applications.engineering.views.waterAnalysisDelete'),
    url(r'^bohiranalysis/delete/(?P<id>\d+)/$', 'applications.engineering.views.bohirAnalysisDelete'),
    url(r'^water_update/(?P<pk>\d+)/$', WaterAnalysisUpdateView.as_view(), name = 'water_update'),
    url(r'^bohir_update/(?P<pk>\d+)/$', BohirAnalysisUpdateView.as_view(), name = 'bohir_update'),

    url(r'^uatailan/1/$', UAT_hudag_sudalgaa.as_view()),
    url(r'^uatailan/2/$', UAT_tsevershuuleh.as_view()),
    url(r'^uatailan/3/$', UAT_usansan.as_view()),
    url(r'^uatailan/4/$', UAT_tsever_us_nasosStants.as_view()),
    url(r'^uatailan/5/$', UAT_tsever_us_lab.as_view()),
    url(r'^uatailan/6/$', UAT_tsever_us_sh_suljee.as_view()),
    url(r'^uatailan/7/$', UAT_abb.as_view()),
    url(r'^uatailan/8/$', UAT_us_dulaan_damjuulah.as_view()),
    url(r'^uatailan/9/$', UAT_bohir_us_sh_suljee.as_view()),
    url(r'^uatailan/10/$', UAT_tseverleh.as_view()),
    url(r'^uatailan/11/$', UAT_bohir_us_nasosStants.as_view()),
    url(r'^uatailan/12/$', UAT_us_tugeeh.as_view()),
    url(r'^uatailan/13/$', UAT_water_car.as_view()),
    url(r'^uatailan/14/$', UAT_bohir_car.as_view()),
    url(r'^uatailan/15/$', UAT_hunii_noots.as_view()),

    

    #### sanhuugiin medee

    #### sanhuugiin tailan

    #### gshu tailan
    url(r'^gshu_tailan/$', GSHU_tailan.as_view(), name='gshu_tailan'),
    url(r'^gshu_tailan/insert/(?P<gshu_id>\d+)/$', GSHU_insertBase.as_view(), name='gshu_insert'),
    url(r'^gshu_tailan/materials/(?P<gshu_id>\d+)/$', GSHU_tailan_materials_view.as_view(), name='gshu_materials_view'),


    
    url(r'^notifications/read/$', tze_notifications_set_read, name='tze-set-notifications-read'),
    
    
    
    
    #### busad
    
    
    
    

    #url(r'^husnegt/1/$', Husnegt1View.as_view()),
    #url(r'^husnegt/2/$', Husnegt2View.as_view()),
    #url(r'^husnegt/3/$', Husnegt3View.as_view()),
    #url(r'^husnegt/4/$', Husnegt4View.as_view()),
    #url(r'^husnegt/5/$', Husnegt5View.as_view()),
    
    url(r'^404/$', django.views.defaults.page_not_found, ),
    url(r'^filtering/employee/name/$', nameFilter, name = 'employee_name_filter' ),
    url(r'^export/sh_suljees/$', Horvuuleh , name = 'horvuuleh'),
    
    ]


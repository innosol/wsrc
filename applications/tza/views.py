# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group
from django.views.generic import FormView, View, TemplateView, UpdateView, ListView
from django.views.generic.edit import BaseFormView
from applications.app.views import LoginRequired, create_tailan
from applications.app.models import *
from applications.app.forms import *
from applications.tza.forms import *
from applications.engineering.forms import EmptyForm
from applications.engineering.filters import *
from applications.tza.filters import *
from applications.engineering.views import e_mail_sending, E_mail_sending_thread, Tohooromj_ABB_delgerengui, TZE_TZ_gerchilgee_delgerengui, Sent_materialView
from applications.engineering.views import Base_Ajax_FormView, Tohooromj_Gunii_Hudag_delgerengui ,Tohooromj_Usan_San_delgerengui ,Tohooromj_NasosStants_delgerengui ,Tohooromj_Lab_delgerengui ,Tohooromj_Sh_Suljee_delgerengui ,Tohooromj_Ts_Baiguulamj_delgerengui ,Tohooromj_Us_Tugeeh_delgerengui ,Tohooromj_Us_Damjuulah_delgerengui ,Tohooromj_Water_Car_delgerengui ,Tohooromj_Bohir_Car_delgerengui ,Tohooromj_Tonog_Tohooromj_delgerengui, TZE_Ajiltan_delgerengui
import datetime
import jsonpickle
import json
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from applications.app.models import *
import datetime
import xlsxwriter
import StringIO
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
import random
import string
import smtplib
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.template import loader, RequestContext
from django.db.models import Min
from .filters import TZE_tza_darga_filter, TZE_tza_mergejilten_filter, TZE_search, Ajiltan_filter
from notifications.signals import notify



class TzaHome(LoginRequired, TemplateView):
	perm_code_names = ['tza_mergejilten_permission']
	template_name = 'tzahome.html'

class Base_List_FilterView(object):
	filter_class = None
	def get_filter(self, filter_class = None):
		if filter_class is None:
			filter_class = self.get_filter_class()
		return filter_class(**self.get_filter_kwargs())
	def get_filter_kwargs(self):
		kwargs = {
			'data': self.request.GET
		}
		return kwargs
	def get_filter_class(self):
		return self.filter_class
	def get_mergejilten_tzes(self):
		tzes_for_ajiltan = TZE.objects.none()
		if self.user.is_tza_alba():
			if self.user.has_tza_darga_permission():
				tzes_for_ajiltan = TZE.objects.filter(status=True)
			else:
				rel_baigs = Rel_baig_zz_ajilchid.objects.filter(tza_mergejilten = self.user.user_id)
				tze_ids_for_ajiltan = []
				for i in rel_baigs:
					tze_ids_for_ajiltan.append(i.tze.id)
				tzes_for_ajiltan = TZE.objects.filter(id__in = tze_ids_for_ajiltan, status = True)
		elif self.user.is_uta_alba():
			if self.user.has_uta_darga_permission():
				tzes_for_ajiltan = TZE.objects.filter(status=True)
			else:
				rel_baigs = Rel_baig_zz_ajilchid.objects.filter(uta_mergejilten = self.user.user_id)
				tze_ids_for_ajiltan = []
				for i in rel_baigs:
					tze_ids_for_ajiltan.append(i.tze.id)
				tzes_for_ajiltan = TZE.objects.filter(id__in = tze_ids_for_ajiltan, status = True)
		elif self.user.is_hzm_alba():
			tzes_for_ajiltan = TZE.objects.filter(status=True)

		return tzes_for_ajiltan
	def get_user_objects(self, queryset):
		tzes_for_ajiltan = self.get_mergejilten_tzes()
		queryset = queryset.filter(tze = tzes_for_ajiltan)
		return queryset

class Base_FilterView(object):
	filter_class = None
	def get_filter(self, filter_class = None):
		if filter_class is None:
			filter_class = self.get_filter_class()
		return filter_class(**self.get_filter_kwargs())
	def get_filter_kwargs(self):
		kwargs = {
			'data': self.request.GET
		}
		return kwargs
	def get_filter_class(self):
		return self.filter_class

''' tur zuuriin views'''

class TZ_shuud_olgolt_listView(LoginRequired, TemplateView):
	perm_code_names = ['tza_tur_zuur_permission']

	template_name = 'tza/tz_olgolt_tur_zuur/tz_shuud_olgolt.html'

	def get_context_data(self, **kwargs):
		context = super(TZ_shuud_olgolt_listView, self).get_context_data(**kwargs)
		context['org'] = TZE.objects.filter(status=True)
		cert_org_dic = {}
		for o in context['org']:
			cert_org_dic[o.id] = Certificate.objects.filter(tze = o, status = True)
		context['cert_org_dic'] = cert_org_dic
		return context

class TZ_shuud_olgoh(Base_Ajax_FormView):
	perm_code_names = ['tza_tur_zuur_permission']
	template_name = 'tza/tz_olgolt_tur_zuur/form_div_htmls/TZ_shuud_olgoh_div.html'
	success_url = reverse_lazy('tz shuud olgoh list')
	form_class = Certificate_giving_Form
	
	def get_form_kwargs(self):
		kwargs = super(TZ_shuud_olgoh, self).get_form_kwargs()
		tz_choices = TZ.objects.all()
		kwargs['tz_choices'] = tz_choices
		return kwargs

	def dispatch(self, request, *args, **kwargs):
		self._b_id = self.kwargs['baiguullaga_id']
		self._tze = get_object_or_404(TZE, id = self._b_id)
		return super(TZ_shuud_olgoh, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(TZ_shuud_olgoh, self).get_context_data(**kwargs)
		context['baiguullaga_id'] = self._b_id
		return context

	def form_valid(self, form):
		new_tz_certificate = form.save(commit = False)
		new_tz_certificate.tze = self._tze
		new_tz_certificate.begin_time = timezone.now()
		new_tz_certificate.created_by = self.user
		new_tz_certificate.status = True
		new_tz_certificate.change_tolov_to_olgogdson()

		tz_ids = form.cleaned_data.get("tz_id")
		new_tz_certificate.tz_id.clear()
		for i in tz_ids:
			new_tz_certificate.tz_id.add(i)

		#new_tz_certificate.history_writing()
		messages.success(self.request, 'Амжилттай хадгаллаа.')
		return super(TZ_shuud_olgoh, self).form_valid(form)


class Show_gerchilgee(LoginRequired, TemplateView):
	perm_code_names = ['tza_tur_zuur_permission']
	template_name = 'tza/tz_olgolt_tur_zuur/delgerengui_div_htmls/show_gerchilgee.html'

	def dispatch(self, request, *args, **kwargs):
		self._b_id = self.kwargs['baiguullaga_id']
		return super(Show_gerchilgee, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(Show_gerchilgee, self).get_context_data(**kwargs)
		context['certs'] = Certificate.objects.filter(tze = self._b_id, status = True)
		tze = TZE.objects.get(id = self._b_id)
		context['tze'] = tze
		return context

class Add_baiguullaga(Base_Ajax_FormView):
	perm_code_names = ['tza_tur_zuur_permission']
	form_class = TZEForm
	template_name='tza/tz_olgolt_tur_zuur/form_div_htmls/add_baiguullaga_div.html'
	success_url = reverse_lazy('tz shuud olgoh list')
	def form_valid(self, form):
		a=form.save()
		#request_email(self.request, id=a['baiguullaga'].id)
		id=a['baiguullaga'].id
		tze = TZE.objects.get(id=id)
		user = Ajiltan.objects.get(baiguullaga = tze)
		u_zahiral = User(user_id = user, username = a['baiguullaga'].reg_num, is_active = True)
		u_zahiral.set_password('12345')
		u_zahiral.save()
		b = TZE_Users_bind(tze = tze, user_zahiral = u_zahiral, status = True)
		b.save()
		
		group_tze = Group.objects.filter(name__icontains="тзэ")
		u_zahiral.groups = group_tze

		create_tailan(a['baiguullaga'])
		return super(Add_baiguullaga, self).form_valid(form)

''' tur zuuriin views '''

class History_View(object):
	def dispatch(self, request, *args, **kwargs):
		tze_id = kwargs['tze_id']
		self.tze = get_object_or_404(TZE, id=tze_id)

		if 'year' in kwargs and 'month' in kwargs and 'day' in kwargs and 'hour' in kwargs and 'minute' in kwargs:
			self.is_history = True
			self.history_date = datetime.datetime(int(kwargs['year']),int(kwargs['month']), int(kwargs['day']), int(kwargs['hour']), int(kwargs['minute']))
		else:
			self.is_history = False
		return super(History_View, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(History_View, self).get_context_data(**kwargs)
		if self.is_history:
			context['history_date'] = self.history_date
		context['is_history'] = self.is_history
		return context


class TZE_profileView(LoginRequired, TemplateView, Base_FilterView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	filter_class = DateFilter
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			self.user = User.objects.get(id = request.user.id)
			if ZZ.objects.filter(id = self.user.user_id.baiguullaga.id):
				self.baiguullaga = ZZ.objects.get(id = self.user.user_id.baiguullaga.id)
				if self.user.user_id.tasag.dep_name == u'Үнэ тарифын алба':
					self.template_name = 'uta/baiguullaga/baiguullaga_profile.html'
				elif  self.user.user_id.tasag.dep_name == u'Тусгай зөвшөөрлийн алба':
					self.template_name = 'tza/baiguullaga/baiguullaga_profile.html'
				elif  self.user.user_id.tasag.dep_name == u'Эрх зүй, мэдээлэл, захиргааны алба':
					self.template_name = 'hzm/baiguullaga/baiguullaga_profile.html'
		tze_id = kwargs['tze_id']
		self.tze = get_object_or_404(TZE, id=tze_id)
		return super(TZE_profileView, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		years = []
		context = super(TZE_profileView, self).get_context_data(**kwargs)
		for i in range(3):
			years.append(int(timezone.now().year)-(i+1))
		context['years'] = years

		object1 = ZDTodorhoilolt.objects.filter(tze = self.tze)
		object2 = HangagchBaiguullaga.objects.filter(tze = self.tze)
		object3 = TaxTodorhoilolt.objects.filter(tze = self.tze)
		object4 = AuditDugnelt.objects.filter(tze = self.tze)
		object5 = NormStandart.objects.filter(tze = self.tze)
		object6 = Baig_huuli_durem.objects.filter(tze = self.tze)
		object7 = UsZuvshuurul.objects.filter(tze = self.tze)
		object8 = SanhuuTailan.objects.filter(tze = self.tze)
		object10 = OronTooniiSchema.objects.filter(tze = self.tze)
		object11 = AjliinBair.objects.filter(tze = self.tze)
		object12 = UildverTechnology.objects.filter(tze= self.tze)

		date_filter_obj = self.get_filter()
		context['filter_form'] = date_filter_obj
		if self.request.GET.get('date') or self.request.GET.get('time'):
			if date_filter_obj.is_valid():
				date = date_filter_obj.cleaned_data['date']
				time = date_filter_obj.cleaned_data['time']
				if not date_filter_obj.cleaned_data['time']:
					time = datetime.time(23, 59)
				date_time = datetime.datetime.combine(date, time)
				context['zasag_count'] = len(ZDTodorhoilolt.get_history_queryset_with_status(object1, date_time, status=True))
				context['hangagch_count'] = len(HangagchBaiguullaga.get_history_queryset_with_status(object2, date_time, status=True))
				context['tax_tod_count'] = len(TaxTodorhoilolt.get_history_queryset_with_status(object3, date_time, status=True))
				context['audit_count'] = len(AuditDugnelt.get_history_queryset_with_status(object4, date_time, status=True))
				context['norm_standart_count'] = len(NormStandart.get_history_queryset_with_status(object5, date_time, status=True))
				context['huuli_durem_count'] = len(Baig_huuli_durem.get_history_queryset_with_status(object6, date_time, status=True))
				context['us_zovshoorol_count'] = len(UsZuvshuurul.get_history_queryset_with_status(object7, date_time, status=True))
				context['sanhuu_tailan_count'] = len(SanhuuTailan.get_history_queryset_with_status(object8, date_time, status=True))
				context['oron_toonii_schema_count'] = len(OronTooniiSchema.get_history_queryset_with_status(object10, date_time, status=True))
				context['ajliin_bair_dugnelt_count'] = len(AjliinBair.get_history_queryset_with_status(object11, date_time, status=True))
				context['uildver_tech_schema_count'] = len(UildverTechnology.get_history_queryset_with_status(object12, date_time, status=True))


				context['url0'] = reverse_lazy('tze_baig_medeelel_list', kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				context['url1'] = reverse_lazy('tze_zasag_tod_list', kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				context['url2'] = reverse_lazy('tze_hangagch_baig_list', kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				context['url3'] = reverse_lazy('tze_tatvar_tod_list', kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				context['url4'] = reverse_lazy('tze_audit_dugnelt_list', kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				context['url5'] = reverse_lazy('tze_norm_standart_list', kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				context['url6'] = reverse_lazy('tze_huuli_durem_list', kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				context['url7'] = reverse_lazy('tze_us_ashigluulah_zovshoorol_list', kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				context['url8'] = reverse_lazy('tze_sanhuu_tailan_list', kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				context['url9'] = reverse_lazy('tze_oron_toonii_schema_list', kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				context['url10'] = reverse_lazy('tze_sez_sudalgaa_list', kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				context['url_ajliin_bair_dugnelt_list'] = reverse_lazy('tze_ajliin_bair_dugnelt_list', kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				context['url_uildver_tech_schema_list'] = reverse_lazy('tze_uildver_tech_schema_list', kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})

				context['tze'] = self.tze.get_history_object(date_time)
				context['history_date'] = date_time
			
		else:
			context['zasag_count'] = object1.filter(status=True).count()
			context['hangagch_count'] = object2.filter(status=True).count()
			context['tax_tod_count'] = object3.filter(status=True).count()
			context['audit_count'] = object4.filter(status=True).count()
			context['norm_standart_count'] = object5.filter(status=True).count()
			context['huuli_durem_count'] = object6.filter(status=True).count()
			context['us_zovshoorol_count'] = object7.filter(status=True).count()
			context['sanhuu_tailan_count'] = object8.filter(status=True).count()
			context['oron_toonii_schema_count'] = object10.filter(status=True).count()
			context['ajliin_bair_dugnelt_count'] = object11.filter(status=True).count()
			context['uildver_tech_schema_count'] = object12.filter(status=True).count()

			context['url0'] = reverse_lazy('tze_baig_medeelel_list', kwargs={'tze_id': self.tze.id})
			context['url1'] = reverse_lazy('tze_zasag_tod_list', kwargs={'tze_id': self.tze.id})
			context['url2'] = reverse_lazy('tze_hangagch_baig_list', kwargs={'tze_id': self.tze.id})
			context['url3'] = reverse_lazy('tze_tatvar_tod_list', kwargs={'tze_id': self.tze.id})
			context['url4'] = reverse_lazy('tze_audit_dugnelt_list', kwargs={'tze_id': self.tze.id})
			context['url5'] = reverse_lazy('tze_norm_standart_list', kwargs={'tze_id': self.tze.id})
			context['url6'] = reverse_lazy('tze_huuli_durem_list', kwargs={'tze_id': self.tze.id})
			context['url7'] = reverse_lazy('tze_us_ashigluulah_zovshoorol_list', kwargs={'tze_id': self.tze.id})
			context['url8'] = reverse_lazy('tze_sanhuu_tailan_list', kwargs={'tze_id': self.tze.id})
			context['url9'] = reverse_lazy('tze_oron_toonii_schema_list', kwargs={'tze_id': self.tze.id})
			context['url10'] = reverse_lazy('tze_sez_sudalgaa_list', kwargs={'tze_id': self.tze.id})
			context['url_ajliin_bair_dugnelt_list'] = reverse_lazy('tze_ajliin_bair_dugnelt_list', kwargs={'tze_id': self.tze.id})
			context['url_uildver_tech_schema_list'] = reverse_lazy('tze_uildver_tech_schema_list', kwargs={'tze_id': self.tze.id})

			context['tze'] = self.tze

		return context
class TZE_profile_baig_medeelel_list(LoginRequired, History_View, TemplateView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/baiguullaga/list_htmls/tze_baiguullaga_delgerengui.html'
	def get_context_data(self, **kwargs):
		context=super(TZE_profile_baig_medeelel_list, self).get_context_data(**kwargs)
		if self.is_history:
			context['tze'] = self.tze.get_history_object(self.history_date)
		return context
class TZE_profile_zasag_tod_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'baiguullaga/list_htmls/tze_zasag_tod_list.html'
	def get_queryset(self):
		queryset = ZDTodorhoilolt.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = ZDTodorhoilolt.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset
class TZE_profile_hangagch_baig_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tze_baiguullaga_menu_view']
	template_name = 'baiguullaga/list_htmls/tze_hangagch_baigs_list.html'
	def get_queryset(self):
		queryset = HangagchBaiguullaga.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = HangagchBaiguullaga.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset
class TZE_profile_tatvar_tod_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'baiguullaga/list_htmls/tze_tax_tod_list.html'
	def get_queryset(self):
		queryset = TaxTodorhoilolt.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = TaxTodorhoilolt.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset
class TZE_profile_audit_dugnelt_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'baiguullaga/list_htmls/tze_audit_dugnelt_list.html'
	def get_queryset(self):
		queryset = AuditDugnelt.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = AuditDugnelt.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset
class TZE_profile_norm_standart_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'baiguullaga/list_htmls/tze_norm_standart_list.html'
	def get_queryset(self):
		queryset = NormStandart.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = NormStandart.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset
class TZE_profile_huuli_durem_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'baiguullaga/list_htmls/tze_huuli_juram_list.html'
	def get_queryset(self):
		queryset = Baig_huuli_durem.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = Baig_huuli_durem.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset
		return queryset
class TZE_profile_ajliin_bair_dugnelt_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'baiguullaga/list_htmls/tze_ajliin_bair_dugnelt_list.html'
	def get_queryset(self):
		queryset = AjliinBair.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = AjliinBair.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset
		return queryset
class TZE_profile_uildver_tech_schema_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'baiguullaga/list_htmls/tze_uildver_tech_schema_list.html'
	def get_queryset(self):
		queryset = UildverTechnology.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = UildverTechnology.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset
		return queryset
class TZE_profile_us_ashigluulah_zovshoorol_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'baiguullaga/list_htmls/tze_us_zovshoorol_list.html'
	def get_queryset(self):
		queryset = UsZuvshuurul.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = UsZuvshuurul.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset
class TZE_profile_sanhuu_tailan_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'baiguullaga/list_htmls/tze_sanhuu_tailan_list.html'
	def get_queryset(self):
		queryset = SanhuuTailan.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = SanhuuTailan.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset
class TZE_profile_oron_toonii_schema(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'baiguullaga/list_htmls/tze_oron_toonii_schema_list.html'
	def get_queryset(self):
		queryset = OronTooniiSchema.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = OronTooniiSchema.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset
class TZE_profile_SEZ_sudalgaa(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'baiguullaga/list_htmls/sanhuu_sudalgaa.html'
	def get_queryset(self):
		queryset = SanhuuTailan.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = SanhuuTailan.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset


class TZE_profile_tonog_tohooromjView(LoginRequired, TemplateView, Base_FilterView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	filter_class = DateFilter
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			self.user = User.objects.get(id = request.user.id)
			if ZZ.objects.filter(id = self.user.user_id.baiguullaga.id):
				self.baiguullaga = ZZ.objects.get(id = self.user.user_id.baiguullaga.id)
				if self.user.user_id.tasag.dep_name == u'Үнэ тарифын алба':
					self.template_name = 'uta/tonog_tohooromj/baiguullaga_tonog_tohooromj_list.html'
				elif  self.user.user_id.tasag.dep_name == u'Тусгай зөвшөөрлийн алба':
					self.template_name = 'tza/tonog_tohooromj/baiguullaga_tonog_tohooromj_list.html'
				elif  self.user.user_id.tasag.dep_name == u'Эрх зүй, мэдээлэл, захиргааны алба':
					self.template_name = 'hzm/tonog_tohooromj/baiguullaga_tonog_tohooromj_list.html'
		tze_id = kwargs['tze_id']
		self.tze = get_object_or_404(TZE, id=tze_id)
		return super(TZE_profile_tonog_tohooromjView, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(TZE_profile_tonog_tohooromjView, self).get_context_data(**kwargs)

		object2 = Hudag.objects.filter(tze = self.tze)
		object3 = UsanSan.objects.filter(tze = self.tze)
		object4 = NasosStants.objects.filter(tze = self.tze)
		object5 = Lab.objects.filter(tze = self.tze)
		object6 = Sh_suljee.objects.filter(tze = self.tze)
		object7 = Ts_baiguulamj.objects.filter(tze = self.tze)

		object9 = WaterCar.objects.filter(tze = self.tze)
		object10 = BohirCar.objects.filter(tze = self.tze)
		object11 = UsDamjuulahBair.objects.filter(tze = self.tze)
		object12 = UsTugeehBair.objects.filter(tze = self.tze)
		object13 = Equipment.objects.filter(tze = self.tze)
		object14 = ABB.objects.filter(tze = self.tze)
		object15 = HudagNegtsgesenBairshliinZurag.objects.filter(tze = self.tze)

		date_filter_obj = self.get_filter()
		context['filter_form'] = date_filter_obj
		if self.request.GET.get('date') or self.request.GET.get('time'):
			if date_filter_obj.is_valid():
				date = date_filter_obj.cleaned_data['date']
				time = date_filter_obj.cleaned_data['time']
				if not date_filter_obj.cleaned_data['time']:
					time = datetime.time(23, 59)
				date_time = datetime.datetime.combine(date, time)

				context['object_list'] = Hudag.get_history_queryset_with_status(object2, date_time, status=True)

				context['hudag_count'] = len(Hudag.get_history_queryset_with_status(object2, date_time, status=True))
				context['usansan_count'] = len(UsanSan.get_history_queryset_with_status(object3, date_time, status=True))
				context['nasos_count'] = len(NasosStants.get_history_queryset_with_status(object4, date_time, status=True))
				context['lab_count'] = len(Lab.get_history_queryset_with_status(object5, date_time, status=True))
				context['sh_suljee_count'] = len(Sh_suljee.get_history_queryset_with_status(object6, date_time, status=True))
				context['ts_baig_count'] = len(Ts_baiguulamj.get_history_queryset_with_status(object7, date_time, status=True))

				context['water_car_count'] = len(WaterCar.get_history_queryset_with_status(object9, date_time, status=True))
				context['bohir_car_count'] = len(BohirCar.get_history_queryset_with_status(object10, date_time, status=True))
				context['us_damjuulah_count'] = len(UsDamjuulahBair.get_history_queryset_with_status(object11, date_time, status=True))
				context['us_tugeeh_count'] = len(UsTugeehBair.get_history_queryset_with_status(object12, date_time, status=True))
				context['equipment_count'] = len(Equipment.get_history_queryset_with_status(object13, date_time, status=True))
				context['hariutsaj_barilguud_count'] = len(ABB.get_history_queryset_with_status(object14, date_time, status=True))
				context['us_hangamj_schema_count'] = len(HudagNegtsgesenBairshliinZurag.get_history_queryset_with_status(object15, date_time, status=True))


				url_hudag_list = reverse_lazy('tze_gunii_hudag_list' , kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				url_usansan_list = reverse_lazy('tze_usan_san_list' , kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				url_nasos_list = reverse_lazy('tze_nasos_list' , kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				url_lab_list = reverse_lazy('tze_lab_list' , kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				url_sh_suljee_list = reverse_lazy('tze_sh_suljee_list' , kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				url_ts_baig_list = reverse_lazy('tze_ts_baig_list' , kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})

				url_water_car_list = reverse_lazy('tze_water_car_list' , kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				url_bohir_car_list = reverse_lazy('tze_bohir_car_list' , kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				url_us_damjuulah_list = reverse_lazy('tze_us_damjuulah_list' , kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				url_us_tugeeh_list = reverse_lazy('tze_us_tugeeh_list' , kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				url_equipment_list = reverse_lazy('tze_tonog_tohooromj_list' , kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				url_abb_list = reverse_lazy('tze_hariutsaj_barilguud_list' , kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				url_us_hangamj_schema_list = reverse_lazy('tze_us_hangamj_schema_list' , kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})

				context['tze'] = self.tze.get_history_object(date_time)
				context['history_date'] = date_time

				
		else:
			context['object_list'] = object2

			context['hudag_count'] = object2.filter(status=True).count()
			context['usansan_count'] = object3.filter(status=True).count()
			context['nasos_count'] = object4.filter(status=True).count()
			context['lab_count'] = object5.filter(status=True).count()
			context['sh_suljee_count'] = object6.filter(status=True).count()
			context['ts_baig_count'] = object7.filter(status=True).count()

			context['water_car_count'] = object9.filter(status=True).count()
			context['bohir_car_count'] = object10.filter(status=True).count()
			context['us_damjuulah_count'] = object11.filter(status=True).count()
			context['us_tugeeh_count'] = object12.filter(status=True).count()
			context['equipment_count'] = object13.filter(status=True).count()
			context['hariutsaj_barilguud_count'] = object14.filter(status=True).count()
			context['us_hangamj_schema_count'] = object15.filter(status=True).count()


			url_hudag_list = reverse_lazy('tze_gunii_hudag_list' , kwargs={'tze_id': self.tze.id})
			url_usansan_list = reverse_lazy('tze_usan_san_list' , kwargs={'tze_id': self.tze.id})
			url_nasos_list = reverse_lazy('tze_nasos_list' , kwargs={'tze_id': self.tze.id})
			url_lab_list = reverse_lazy('tze_lab_list' , kwargs={'tze_id': self.tze.id})
			url_sh_suljee_list = reverse_lazy('tze_sh_suljee_list' , kwargs={'tze_id': self.tze.id})
			url_ts_baig_list = reverse_lazy('tze_ts_baig_list' , kwargs={'tze_id': self.tze.id})

			url_water_car_list = reverse_lazy('tze_water_car_list' , kwargs={'tze_id': self.tze.id})
			url_bohir_car_list = reverse_lazy('tze_bohir_car_list' , kwargs={'tze_id': self.tze.id})
			url_us_damjuulah_list = reverse_lazy('tze_us_damjuulah_list' , kwargs={'tze_id': self.tze.id})
			url_us_tugeeh_list = reverse_lazy('tze_us_tugeeh_list' , kwargs={'tze_id': self.tze.id})
			url_equipment_list = reverse_lazy('tze_tonog_tohooromj_list' , kwargs={'tze_id': self.tze.id})
			url_abb_list = reverse_lazy('tze_hariutsaj_barilguud_list' , kwargs={'tze_id': self.tze.id})
			url_us_hangamj_schema_list = reverse_lazy('tze_us_hangamj_schema_list' , kwargs={'tze_id': self.tze.id})

			context['tze'] = self.tze

			


		context['url_hudag_list'] = url_hudag_list
		context['url_usansan_list'] = url_usansan_list
		context['url_nasos_list'] = url_nasos_list
		context['url_lab_list'] = url_lab_list
		context['url_sh_suljee_list'] = url_sh_suljee_list
		context['url_ts_baig_list'] = url_ts_baig_list

		context['url_water_car_list'] = url_water_car_list
		context['url_bohir_car_list'] = url_bohir_car_list
		context['url_us_damjuulah_list'] = url_us_damjuulah_list
		context['url_us_tugeeh_list'] = url_us_tugeeh_list
		context['url_equipment_list'] = url_equipment_list
		context['url_abb_list'] = url_abb_list
		context['url_us_hangamj_schema_list'] = url_us_hangamj_schema_list
		return context

class TZE_profile_Gunii_Hudag_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_gunii_hudag_list.html'
	def get_queryset(self):
		queryset = Hudag.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = Hudag.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset
class TZE_profile_Usan_San_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_usan_san_list.html'
	def get_queryset(self):
		queryset = UsanSan.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = UsanSan.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset
class TZE_profile_Nasos_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_nasos_list.html'
	def get_queryset(self):
		queryset = NasosStants.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = NasosStants.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset
class TZE_profile_Lab_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_lab_list.html'
	def get_queryset(self):
		queryset = Lab.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = Lab.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset
class TZE_profile_Sh_Suljee_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_sh_suljee_list.html'
	def get_queryset(self):
		queryset = Sh_suljee.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = Sh_suljee.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset
class TZE_profile_Ts_Baiguulamj_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_ts_baiguulamj_list.html'
	def get_queryset(self):
		queryset = Ts_baiguulamj.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = Ts_baiguulamj.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset
class TZE_profile_Us_Tugeeh_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_us_tugeeh_list.html'
	def get_queryset(self):
		queryset = UsTugeehBair.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = UsTugeehBair.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset
class TZE_profile_Us_Damjuulah_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_us_damjuulah_list.html'
	def get_queryset(self):
		queryset = UsDamjuulahBair.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = UsDamjuulahBair.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset

class TZE_profile_ABB_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_abb_list.html'
	def get_queryset(self):
		queryset = ABB.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = ABB.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset
class TZE_profile_us_hangamj_schema_zurag_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_us_hangamj_schema_list.html'
	def get_queryset(self):
		queryset = HudagNegtsgesenBairshliinZurag.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = HudagNegtsgesenBairshliinZurag.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset
class TZE_profile_Water_Car_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_water_car_list.html'
	def get_queryset(self):
		queryset = WaterCar.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = WaterCar.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset
class TZE_profile_Bohir_Car_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_bohir_car_list.html'
	def get_queryset(self):
		queryset = BohirCar.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = BohirCar.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset
class TZE_profile_Tonog_Tohooromj_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_tonog_tohooromj_list.html'
	def get_queryset(self):
		queryset = Equipment.objects.filter(tze = self.tze)
		if self.is_history:
			queryset = Equipment.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset




class TZE_profile_hunii_nootsView(LoginRequired, TemplateView, Base_FilterView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	filter_class = DateFilter
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			self.user = User.objects.get(id = request.user.id)
			if ZZ.objects.filter(id = self.user.user_id.baiguullaga.id):
				self.baiguullaga = ZZ.objects.get(id = self.user.user_id.baiguullaga.id)
				if self.user.user_id.tasag.dep_name == u'Үнэ тарифын алба':
					self.template_name = 'uta/hunii_noots/baiguullaga_employee_list.html'
				elif  self.user.user_id.tasag.dep_name == u'Тусгай зөвшөөрлийн алба':
					self.template_name = 'tza/hunii_noots/baiguullaga_employee_list.html'
				elif  self.user.user_id.tasag.dep_name == u'Эрх зүй, мэдээлэл, захиргааны алба':
					self.template_name = 'hzm/hunii_noots/baiguullaga_employee_list.html'
		tze_id = kwargs['tze_id']
		self.tze = get_object_or_404(TZE, id=tze_id)
		return super(TZE_profile_hunii_nootsView, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(TZE_profile_hunii_nootsView, self).get_context_data(**kwargs)
		ajiltan = Ajiltan.objects.filter(baiguullaga = self.tze)

		date_filter_obj = self.get_filter()
		context['filter_form'] = date_filter_obj
		if self.request.GET.get('date') or self.request.GET.get('time'):
			if date_filter_obj.is_valid():
				date = date_filter_obj.cleaned_data['date']
				time = date_filter_obj.cleaned_data['time']
				if not date_filter_obj.cleaned_data['time']:
					time = datetime.time(23, 59)
				date_time = datetime.datetime.combine(date, time)

				context['object_list'] = Ajiltan.get_history_queryset_with_status(ajiltan, date_time, status=True)
				context['niit_ajiltan_count'] = len(Ajiltan.get_history_queryset_with_status(ajiltan, date_time, status=True))
				context['udirdah_ajiltan_count'] = len(Ajiltan.get_history_queryset_with_status_and_zereg(ajiltan, date_time, status=True, zereg=u'Удирдах ажилтан'))
				context['engineer_ajiltan_count'] = len(Ajiltan.get_history_queryset_with_status_and_zereg(ajiltan, date_time, status=True, zereg=u'Инженер техникийн ажилтан'))
				context['mergejliin_ajiltan_count'] = len(Ajiltan.get_history_queryset_with_status_and_zereg(ajiltan, date_time, status=True, zereg=u'Мэргэжлийн ажилтан'))
				context['busad_ajiltan_count'] = len(Ajiltan.get_history_queryset_with_status_and_zereg(ajiltan, date_time, status=True, zereg=u'Бусад'))

				url0 = reverse_lazy('tze_ajiltan_alba_tasag_list', kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				url1 = reverse_lazy('tze_ajiltan_all_list', kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				url2 = reverse_lazy('tze_ajiltan_udirdah_list', kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				url3 = reverse_lazy('tze_ajiltan_engineer_list', kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				url4 = reverse_lazy('tze_ajiltan_mergejil_list', kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})
				url5 = reverse_lazy('tze_ajiltan_busad_list', kwargs={'tze_id': self.tze.id,'year': date_time.year, 'month': date_time.month, 'day': date_time.day, 'hour':date_time.hour, 'minute': date_time.minute})

				context['tze'] = self.tze.get_history_object(date_time)
				context['history_date'] = date_time
				context['is_history'] = True
		else:
			context['object_list'] = ajiltan.filter(status=True)
			context['niit_ajiltan_count'] = ajiltan.filter(status=True).count()
			context['udirdah_ajiltan_count'] = ajiltan.filter(zereg=u'Удирдах ажилтан', status=True).count()
			context['engineer_ajiltan_count'] = ajiltan.filter(zereg=u'Инженер техникийн ажилтан', status=True).count()
			context['mergejliin_ajiltan_count'] = ajiltan.filter(zereg=u'Мэргэжлийн ажилтан', status=True).count()
			context['busad_ajiltan_count'] = ajiltan.filter(zereg=u'Бусад', status=True).count()

			url0 = reverse_lazy('tze_ajiltan_alba_tasag_list', kwargs={'tze_id': self.tze.id})
			url1 = reverse_lazy('tze_ajiltan_all_list', kwargs={'tze_id': self.tze.id})
			url2 = reverse_lazy('tze_ajiltan_udirdah_list', kwargs={'tze_id': self.tze.id})
			url3 = reverse_lazy('tze_ajiltan_engineer_list', kwargs={'tze_id': self.tze.id})
			url4 = reverse_lazy('tze_ajiltan_mergejil_list', kwargs={'tze_id': self.tze.id})
			url5 = reverse_lazy('tze_ajiltan_busad_list', kwargs={'tze_id': self.tze.id})

			context['tze'] = self.tze

		context['url0'] = url0
		context['url1'] = url1
		context['url2'] = url2
		context['url3'] = url3
		context['url4'] = url4
		context['url5'] = url5

		return context

class TZE_profile_Ajiltan_all_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'employee/list_htmls/tze_ajiltan_list.html'
	list_header=u"Нийт ажилчдын жагсаалт"
	def get_queryset(self):
		queryset = Ajiltan.objects.filter(baiguullaga = self.tze)
		if self.is_history:
			queryset = Ajiltan.get_history_queryset_with_status(queryset, self.history_date, status=True)
		else:
			queryset = queryset.filter(status = True)
		return queryset
	def get_context_data(self, **kwargs):
		context = super(TZE_profile_Ajiltan_all_list,self).get_context_data(**kwargs)
		context['list_header'] = self.list_header
		return context
class TZE_profile_Ajiltan_udirdah_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'employee/list_htmls/tze_ajiltan_list.html'
	list_header=u"Удирдах ажилчдын жагсаалт"
	def get_queryset(self):
		queryset = Ajiltan.objects.filter(baiguullaga = self.tze)
		if self.is_history:
			queryset = Ajiltan.get_history_queryset_with_status_and_zereg(queryset, self.history_date, status=True, zereg=u'Удирдах ажилтан')
		else:
			queryset = queryset.filter(status = True, zereg = u'Удирдах ажилтан')
		return queryset
	def get_context_data(self, **kwargs):
		context = super(TZE_profile_Ajiltan_udirdah_list,self).get_context_data(**kwargs)
		context['list_header'] = self.list_header
		return context
class TZE_profile_Ajiltan_engineer_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'employee/list_htmls/tze_ajiltan_list.html'
	list_header="Инженер техникийн ажилчдын жагсаалт"
	def get_queryset(self):
		queryset = Ajiltan.objects.filter(baiguullaga = self.tze)
		if self.is_history:
			queryset = Ajiltan.get_history_queryset_with_status_and_zereg(queryset, self.history_date, status=True, zereg=u'Инженер техникийн ажилтан')
		else:
			queryset = queryset.filter(status = True, zereg = u'Инженер техникийн ажилтан')
		return queryset
	def get_context_data(self, **kwargs):
		context = super(TZE_profile_Ajiltan_engineer_list,self).get_context_data(**kwargs)
		context['list_header'] = self.list_header
		return context
class TZE_profile_Ajiltan_mergejliin_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'employee/list_htmls/tze_ajiltan_list.html'
	list_header="Мэргэжлийн ажилчдын жагсаалт"
	def get_queryset(self):
		queryset = Ajiltan.objects.filter(baiguullaga = self.tze)
		if self.is_history:
			queryset = Ajiltan.get_history_queryset_with_status_and_zereg(queryset, self.history_date, status=True, zereg=u'Мэргэжлийн ажилтан')
		else:
			queryset = queryset.filter(status = True, zereg = u'Мэргэжлийн ажилтан')
		return queryset
	def get_context_data(self, **kwargs):
		context = super(TZE_profile_Ajiltan_mergejliin_list,self).get_context_data(**kwargs)
		context['list_header'] = self.list_header
		return context
class TZE_profile_Ajiltan_busad_list(LoginRequired, History_View, ListView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'employee/list_htmls/tze_ajiltan_list.html'
	list_header="Бусад ажилчдын жагсаалт"
	def get_queryset(self):
		queryset = Ajiltan.objects.filter(baiguullaga = self.tze)
		if self.is_history:
			queryset = Ajiltan.get_history_queryset_with_status_and_zereg(queryset, self.history_date, status=True, zereg=u'Бусад')
		else:
			queryset = queryset.filter(status = True, zereg = u'Бусад')
		return queryset
	def get_context_data(self, **kwargs):
		context = super(TZE_profile_Ajiltan_busad_list,self).get_context_data(**kwargs)
		context['list_header'] = self.list_header
		return context
class TZE_profile_alba_tasag_list(LoginRequired, History_View, TemplateView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'employee/list_htmls/tze_ajiltan_alba_tasag_list.html'

	def get_context_data(self, **kwargs):
		context = super(TZE_profile_alba_tasag_list, self).get_context_data(**kwargs)
		tasguud = Tasag.objects.filter(baiguullaga = self.tze)
		if self.is_history:
			context['object_list'] = Tasag.get_history_queryset_with_status(tasguud, self.history_date, status=True)
		else:
			context['object_list'] = tasguud.filter(status = True)
		return context

''' TZA darga views START'''
class Tza_darga_huselt_huvaarilalt_list(LoginRequired, ListView, Base_List_FilterView):
	perm_code_names = ['tza_darga_permission']
	context_object_name="tz_huselts"
	template_name = "tza/tz_huselt_huvaarilah/tza_darga_huselt_huvaarilah.html"
	filter_class = TZ_huselt_huvaarilah_tza_filter
	def get_context_data(self, **kwargs):
		context = super(Tza_darga_huselt_huvaarilalt_list, self).get_context_data(**kwargs)
		context['filter_form'] = self.get_filter()
		return context
	def get_queryset(self):
		#material_huleen_avsan = get_object_or_404(TZ_huselt_yavts, yavts_name=u'Бичиг баримтыг хүлээн авсан')
		queryset = TZ_Huselt.objects.exclude(yavts=u'Материал бүрдүүлэлт').exclude(yavts=u'Буцаагдсан') #| TZ_Huselt.objects.filter(hzm_checked_OK = True, yavts = material_huleen_avsan)
		exclude_id_list=[]
		for i in queryset:
			burdel_history = Burdel_history.objects.filter(tz_huselt = i).order_by('-ilgeesen_datetime').first()
			if burdel_history:
				if burdel_history.hzm_check_finished == False:
					exclude_id_list.append(i.id)

		for i in exclude_id_list:
			queryset = queryset.exclude(id = i)
		queryset = self.filter(queryset)
		return queryset
	def filter(self, queryset):
		return queryset

class TZ_huselt_huvaarilah(Base_Ajax_FormView):
	perm_code_names = ['tza_darga_permission']
	form_class = TZ_huselt_tza_huvaarilahForm
	template_name = "tza/tz_huselt_huvaarilah/form_div_htmls/tz_huselt_huvaarilah_div.html"
	success_url = reverse_lazy('tza darga huselt huvaarilah')

	def dispatch(self, request, *args, **kwargs):
		self._huselt_id = self.kwargs['huselt_id']
		self._huselt = get_object_or_404(TZ_Huselt, id=self._huselt_id)
		return super(TZ_huselt_huvaarilah, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(TZ_huselt_huvaarilah, self).get_context_data(**kwargs)
		context['huselt_id'] = self._huselt_id
		context['tz_huselt'] = self._huselt
		return context
	def form_valid(self, form):
		tza_mergejilten_user = get_object_or_404(User, user_id = form.cleaned_data['tza_mergejilten'])

		self._huselt.tza_mergejilten = form.cleaned_data['tza_mergejilten']
		self._huselt.save()

		notify.send(self._huselt.tze, recipient=tza_mergejilten_user, verb=self._huselt.tze.org_name + ' ' + self._huselt.tze.org_type + u' илгээсэн ТЗ хүсэлтийг таньд хуваарилалаа.', url_data = reverse_lazy('huselt check'))

		messages.success(self.request, 'Амжилттай хадгаллаа.')
		return super(TZ_huselt_huvaarilah, self).form_valid(form)


class TZ_huselt_hural_tovloh(TZ_huselt_huvaarilah):
	perm_code_names = ['tza_darga_permission']
	form_class = TZ_huselt_hural_tovlohForm
	template_name = "tza/tz_huselt_huvaarilah/form_div_htmls/tz_huselt_hural_tovloh_div.html"

	def form_valid(self, form):
		self._huselt.hurliin_date = form.cleaned_data['hural_date']
		self._huselt.save()
		messages.success(self.request, 'Амжилттай хадгаллаа.')
		return HttpResponseRedirect(self.get_success_url())

class Ajliin_heseg_date_tovloh(TZ_huselt_huvaarilah):
	perm_code_names = ['tza_darga_permission']
	form_class = Ajliin_heseg_date_tovlohForm
	template_name = "tza/tz_huselt_huvaarilah/form_div_htmls/ajliin_heseg_date_tovloh_div.html"

	def form_valid(self, form):
		self._huselt.ajliin_heseg_date = form.cleaned_data['date']
		self._huselt.save()
		messages.success(self.request, 'Амжилттай хадгаллаа.')
		return HttpResponseRedirect(self.get_success_url())

class Handah_erh_huselt_list(LoginRequired, TemplateView):
	perm_code_names = ['tza_darga_permission']
	template_name='tza/handah_erh_huselt/handah_erh_huselt_list.html'
	
	def get_context_data(self, **kwargs):
		context = super(Handah_erh_huselt_list, self).get_context_data(**kwargs)
		l = []
		for u in User.objects.all():
			l.append(u.user_id.baiguullaga.id)
		
		paginator1 = Paginator(TZE.objects.exclude(id__in = set(l)), 10)
		page1 = self.request.GET.get('page')
		try:
			context['tze'] = paginator1.page(page1)
		except PageNotAnInteger:
			context['tze'] = paginator1.page(1)
		except EmptyPage:
			context['tze'] = paginator1.page(paginator1.num_pages)
		return context

	@staticmethod
	def agree(request, iid = 0):
		request_email(request, iid)
		return HttpResponseRedirect('/tza/handah_erh_huselt_list/')
class Handah_erh_baig_delgerengui(LoginRequired, TemplateView):
	perm_code_names = ['tza_darga_permission']
	template_name = 'tza/handah_erh_huselt/handah_erh_huselt_baig_delgerengui.html'
	def get_context_data(self, **kwargs):
		context = super(Handah_erh_baig_delgerengui, self).get_context_data(**kwargs)
		tze_id = kwargs['tze_id']
		context['baig'] = get_object_or_404(TZE, id=tze_id)
		context['zahiral'] = Ajiltan.objects.get(baiguullaga = context['baig'])
		return context

class TZ_huselt_delgerengui(LoginRequired, TemplateView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tz_huselt_huvaarilah/delgerengui_div_htmls/tz_huselt_delgerengui.html'

	def dispatch(self, request, *args, **kwargs):
		obj_id = kwargs['id']
		self.obj = get_object_or_404(TZ_Huselt, id = obj_id)
		return super(TZ_huselt_delgerengui, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(TZ_huselt_delgerengui, self).get_context_data(**kwargs)
		context['tz_huselt'] = self.obj

		return context
''' TZA darga views END'''

''' ТZA mergejilten views START '''
class Tza_Huselt_list(LoginRequired, ListView, Base_List_FilterView): # tusgai zovshoorliin huseltiin shalgah list
	perm_code_names = ['tza_mergejilten_permission']
	template_name = 'tza/tz_huselt_shalgah/tza_huselt_shalgah.html'
	context_object_name="tz_huseltuud"
	filter_class = TZ_huselt_tza_filter
	def get_context_data(self, **kwargs):
		context = super(Tza_Huselt_list, self).get_context_data(**kwargs)
		context['filter_form'] = self.get_filter()
		return context
	def get_queryset(self):
		queryset = TZ_Huselt.objects.filter(tza_mergejilten = self.user.user_id).exclude(yavts=u'Материал бүрдүүлэлт').exclude(yavts=u'Буцаагдсан')
		queryset = self.filter(queryset)
		return queryset
	def filter(self, queryset):
		return queryset

class Tza_huselt_delgerengui(LoginRequired, TemplateView):
	perm_code_names = ['tza_mergejilten_permission']
	template_name = 'tza/tz_huselt_shalgah/tza_huselt_delgerengui.html'

	def dispatch(self, request, *args, **kwargs):
		huselt_id = self.kwargs['huselt_id']
		self.obj = get_object_or_404(TZ_Huselt, id = huselt_id)
		return super(Tza_huselt_delgerengui, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(Tza_huselt_delgerengui, self).get_context_data(**kwargs)
		context['h'] = self.obj
		context['warnings'] = TZ_anhaaruulga.objects.filter(tz_huselt = context['h'])
		context['burdel_histories'] = Burdel_history.objects.filter(tz_huselt = context['h']).order_by('-ilgeesen_datetime')
		context['burdel_history'] = context['burdel_histories'].first()
		context['tz_huselt_medegdels'] = TZ_medegdel.objects.filter(tz_huselt = context['h'])
		return context

class TZA_TZ_Material_check(LoginRequired, FormView):
	perm_code_names = ['tza_mergejilten_permission']
	template_name = 'tza/tz_huselt_shalgah/form_div_htmls/material_check.html'
	form_class = Material_check_form

	def dispatch(self, request, *args, **kwargs):
		self.burdel_history = get_object_or_404(Burdel_history, id = self.kwargs['burdel_history_id'])
		self._material_number = self.kwargs['material_number']
		self.view_url = self.get_view_url(self.burdel_history.id, self._material_number)

		return super(TZA_TZ_Material_check, self).dispatch(request, *args, **kwargs)
	def get_view_url(self, burdel_history_id, material_number):
		return reverse_lazy('tza_material_check', kwargs={'burdel_history_id': burdel_history_id, 'material_number':material_number})

	def get_context_data(self, **kwargs):
		context = super(TZA_TZ_Material_check, self).get_context_data(**kwargs)
		context['material'] = get_object_or_404(TZ_material, material_number = self._material_number)
		return context


	def form_valid(self, form):
		material = get_object_or_404(TZ_material, material_number = self._material_number)
		m = self.burdel_history.materialiud_list.get(material = material)
		
		
		if form.cleaned_data['status'] == 'zovshoorson':
			m.change_status_to_zovshoorson(timezone.now(), self.user)
		elif form.cleaned_data['status'] == 'hangaltgui':
			m.tatgalzsan_tailbar = form.cleaned_data['tailbar']
			m.change_status_to_hangaltgui(timezone.now(), self.user)

		return super(TZA_TZ_Material_check, self).form_valid(form)

	def get_success_url(self):
		self.success_url = reverse_lazy('tza_huselt_delgerengui', kwargs={'huselt_id': self.burdel_history.tz_huselt.id})
		return super(TZA_TZ_Material_check, self).get_success_url()
class TZA_TZ_Sent_materialView(Sent_materialView):
	perm_code_names = ['tza_mergejilten_permission']
	def get_material_check_url(self):
		return reverse_lazy('tza_material_check', kwargs = {'burdel_history_id': self.burdel_history.id, 'material_number': self._material_number})

class TZ_huselt_check_finish_tza(Base_Ajax_FormView):
	perm_code_names = ['tza_mergejilten_permission']
	template_name = 'tza/tz_huselt_shalgah/form_div_htmls/tz_huselt_check.html'
	form_class = ShalgajDuussanForm
	success_url = '/tza/huseltuud/'

	def dispatch(self, request, *args, **kwargs):
		self._huselt_id = self.kwargs['huselt_id']
		self._tz_huselt = get_object_or_404(TZ_Huselt, id=self._huselt_id)
		return super(TZ_huselt_check_finish_tza, self).dispatch(request, *args, **kwargs)
	def get(self, request, *args, **kwargs):
		self.view_url = reverse_lazy('huselt_check_finish_tza', kwargs={'huselt_id': self._huselt_id})
		return super(TZ_huselt_check_finish_tza, self).get(request, *args, **kwargs)
	def post(self, request, *args, **kwargs):
		self.view_url = reverse_lazy('huselt_check_finish_tza', kwargs={'huselt_id': self._huselt_id})
		return super(TZ_huselt_check_finish_tza, self).post(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(TZ_huselt_check_finish_tza, self).get_context_data(**kwargs)
		context['huselt_id'] = self._huselt_id
		context['tz_huselt'] = self._tz_huselt
		return context

	def form_valid(self, form):
		burdel_history = Burdel_history.objects.filter(tz_huselt = self._tz_huselt).order_by('-ilgeesen_datetime').first()
		burdel_history.tza_check_finished = True # tza shalgaj duussan. Huselt butsaagdah esehiig materialiudiin status yamar baihaas shaltgaalna
		burdel_history.save()
		if burdel_history.uta_check_finished == True and burdel_history.hzm_check_finished == True:
			
			if burdel_history.is_all_zovshoorson():
				self._tz_huselt.change_yavts_to_bichig_barimt_OK()

				burdel_history.now_checking = False
				burdel_history.save()

				messages.success(self.request, 'Амжилттай хадгаллаа. Бичиг баримтуудыг хүлээн авсан.')
			else:
				self._tz_huselt.change_yavts_to_butsaagdsan()

				burdel_history.now_checking = False
				burdel_history.save()

				self._tz_huselt.burdel.material_butsaah_function()
				messages.success(self.request, 'Амжилттай хадгаллаа. Бичиг баримтууд буцаагдсан.')
		else:
			messages.success(self.request, 'Амжилттай хадгаллаа. Тусгай зөвшөөрлийн хүсэлтийг шалгаж дууслаа.')
		return super(TZ_huselt_check_finish_tza, self).form_valid(form)


class Hurliin_shiidver_saving(Base_Ajax_FormView):
	perm_code_names = ['tza_mergejilten_permission']
	template_name = 'tza/tz_huselt_shalgah/form_div_htmls/hurliin_shiidver_saving.html'
	form_class = Hurliin_shiidver_Form
	success_url = '/tza/huseltuud/'

	def get_form_kwargs(self):
		kwargs = super(Hurliin_shiidver_saving, self).get_form_kwargs()
		burdel_history = Burdel_history.objects.filter(tz_huselt = self.tz_huselt).order_by('-ilgeesen_datetime').first()
		tz_choices = burdel_history.tz.all()
		kwargs['tz_choices'] = tz_choices
		return kwargs

	def dispatch(self, request, *args, **kwargs):
		huselt_id = self.kwargs['huselt_id']
		self.tz_huselt = get_object_or_404(TZ_Huselt, id = huselt_id)
		return super(Hurliin_shiidver_saving, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(Hurliin_shiidver_saving, self).get_context_data(**kwargs)
		context['huselt_id'] = self.tz_huselt.id
		context['tz_huselt'] = self.tz_huselt
		return context


	def form_valid(self, form):
		if form.cleaned_data['shiidver'] == '1':

			new_tz_certificate = form.save(commit = False)
			new_tz_certificate.tze = self.tz_huselt.tze
			new_tz_certificate.begin_time = timezone.now()
			new_tz_certificate.created_by = self.user
			new_tz_certificate.status = True
			new_tz_certificate.save()

			tz_ids = form.cleaned_data.get("tz_id")
			new_tz_certificate.tz_id.clear()
			for i in tz_ids:
				new_tz_certificate.tz_id.add(i)

			self.tz_huselt.change_yavts_to_tz_olgoson()

			messages.success(self.request, 'Хурлын шийдвэрийг амжилттай хадгаллаа. Тусгай зөвшөөрлийн гэрчилгээг үүсгэсэн.')
		else:
			self.tz_huselt.change_yavts_to_tz_olgoogui()
			messages.success(self.request, 'Хурлын шийдвэрийг амжилттай хадгаллаа. Хүсэлтийг цуцалсан.')
		return super(Hurliin_shiidver_saving, self).form_valid(form)




''' TZA mergejilten views END '''

"""    TZA baiguullaga  menu deer ashiglagdaj baigaa viewuud  START  """

class tzaBaiguullagaaView(LoginRequired, FormView):
	perm_code_names = ['tza_mergejilten_permission']
	form_class = Baiguullaga_huvaarilalt_tza_Form
	template_name = "tza/baiguullaga/baiguullaga.html"
	success_url = '/tza/baiguullaga/'
	def get_user_objects(self):	# hereglegchid hamaaraltai objectuudiig get
		objects = TZE.objects.filter(status = True)
		if not self.user.has_tza_darga_permission():
			rel_baigs = Rel_baig_zz_ajilchid.objects.filter(tza_mergejilten = self.user.user_id)
			tzes_for_ajiltan = []
			for i in rel_baigs:
				tzes_for_ajiltan.append(i.tze.id)
			objects = objects.filter(id__in = tzes_for_ajiltan)
		return objects
	def get_filter_class(self):
		if self.user.has_tza_darga_permission():
			filter_class = TZE_tza_darga_filter
		else:
			filter_class = TZE_tza_mergejilten_filter
		return filter_class
	def get_filtered_objects(self, queryset):
		if self.user.has_tza_darga_permission():
			city = self.request.GET.get('city')
			district = self.request.GET.get('district')
			khoroo = self.request.GET.get('khoroo')
			tza_mergejilten = self.request.GET.get('tza_mergejilten')
			tz_list = self.request.GET.getlist('tz')
			if city:
				queryset = queryset.filter(city = city)
			if district:
				queryset = queryset.filter(district = district)
			if khoroo:
				queryset = queryset.filter(khoroo = khoroo)
			if tza_mergejilten:
				rel_baigs_filtered = Rel_baig_zz_ajilchid.objects.filter(tza_mergejilten = tza_mergejilten)
				tzes_for_ajiltan = []
				for i in rel_baigs_filtered:
					tzes_for_ajiltan.append(i.tze.id)
				queryset = queryset.filter(id__in = tzes_for_ajiltan)
			if tz_list:
				cert_queryset = Certificate.objects.filter(status = True)
				for tz in tz_list:
					cert_queryset = cert_queryset.filter(tz_id = tz)
				tzes_with_cert = []
				for i in cert_queryset:
					tzes_with_cert.append(i.tze.id)
				queryset = queryset.filter(id__in = tzes_with_cert)
		else:
			city = self.request.GET.get('city')
			district = self.request.GET.get('district')
			khoroo = self.request.GET.get('khoroo')
			tz_list = self.request.GET.getlist('tz')
			if city:
				queryset = queryset.filter(city = city)
			if district:
				queryset = queryset.filter(district = district)
			if khoroo:
				queryset = queryset.filter(khoroo = khoroo)
			if tz_list:
				cert_queryset = Certificate.objects.filter(status = True)
				for tz in tz_list:
					cert_queryset = cert_queryset.filter(tz_id = tz)
				tzes_with_cert = []
				for i in cert_queryset:
					tzes_with_cert.append(i.tze.id)
				queryset = queryset.filter(id__in = tzes_with_cert)
		return queryset

	def get_context_data(self, **kwargs):
		context = super(tzaBaiguullagaaView, self).get_context_data(**kwargs)
		objects = self.get_user_objects()
		filter_class = self.get_filter_class()
		filter_form = filter_class(self.request.GET)
		search_form = TZE_search(self.request.GET)
		context['filter_form'] = filter_form
		context['search_form'] = search_form
		if self.request.GET.get('search'):
			search = self.request.GET.get('search')
			context['baig'] = objects.filter(org_name__icontains = search) | objects.filter(reg_num = search) | objects.filter(ubd = search)
		else:
			context['baig'] = self.get_filtered_objects(queryset = objects)

		return context
	def form_valid(self, form):
		baig_ids = self.request.POST.getlist('chosen_baigs')
		all_baigs = TZE.objects.filter(status = True)
		#print "baig_ids: ", baig_ids
		for i in baig_ids:
			baig = all_baigs.get(id = i)
			r, created = Rel_baig_zz_ajilchid.objects.get_or_create(tze = baig)
			r.tza_mergejilten = form.cleaned_data['tza_mergejilten']
			r.created_by = self.user
			r.status = True
			r.save()
			#r.save_and_history_writing()
		messages.success(self.request, 'Амжилттай хадгаллаа.')
		return super(tzaBaiguullagaaView, self).form_valid(form)

class TZA_Baiguullaga_delgerengui(LoginRequired, TemplateView):
	perm_code_names = ['tza_mergejilten_permission']
	template_name = 'tza/baiguullaga/delgerengui_div_htmls/tza_baiguullaga_delgerengui.html'
	def dispatch(self, request, *args, **kwargs):
		baig_id = kwargs['baiguullaga_id']
		self._object = get_object_or_404(TZE, id = baig_id)
		return super(TZA_Baiguullaga_delgerengui, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(TZA_Baiguullaga_delgerengui, self).get_context_data(**kwargs)
		context['baig'] = self._object
		context['cert'] = Certificate.objects.filter(tze = self._object, status = True)
		return context

"""    TZA baiguullaga  menu deer ashiglagdaj baigaa viewuud  END  """


"""    TZA hunii noots  menu deer ashiglagdaj baigaa viewuud  START  """
class tzaAjiltanView(LoginRequired, TemplateView, Base_List_FilterView):
	perm_code_names = ['tza_mergejilten_permission']
	template_name = "tza/hunii_noots/ajiltan.html"
	filter_class = Ajiltan_filter

	def filter(self, queryset):
		f_zereg = self.request.GET.get('zereg')
		f_alban_tushaal = self.request.GET.get('alban_tushaal')
		if f_zereg:
			queryset = queryset.filter(zereg = f_zereg)
		if f_alban_tushaal:
			alban_tushaals = AlbanTushaal.objects.filter(position_name__icontains = f_alban_tushaal, status=True)
			queryset = queryset.filter(alban_tushaal = alban_tushaals)

		return queryset
	def get_context_data(self, **kwargs):
		context = super(tzaAjiltanView, self).get_context_data(**kwargs)
		context['filter_form'] = self.get_filter()

		tze_baig = self.request.GET.get('tze_baig')

		baigs = self.get_mergejilten_tzes()
		if tze_baig:
			baigs = baigs.filter(org_name__icontains = tze_baig)
		filtered_ajiltans = self.filter(Ajiltan.objects.filter(baiguullaga = baigs, status = True))
		context['ajiltan'] = filtered_ajiltans
		return context

class TZA_Ajiltan_delgerengui(TZE_Ajiltan_delgerengui):
	perm_code_names = ['tza_mergejilten_permission']

"""    TZA hunii noots  menu deer ashiglagdaj baigaa viewuud  END  """



"""    TZA tonog tohooromj menu deer ashiglagdaj baigaa viewuud  START  """

class TZA_TohooromjjView(LoginRequired, TemplateView, Base_List_FilterView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = "tza/tonog_tohooromj/tohooromj.html"
	
	def get_context_data(self, **kwargs):
		context = super(TZA_TohooromjjView, self).get_context_data(**kwargs)

		object2 = self.get_user_objects(Hudag.objects.filter(status=True))
		object3 = self.get_user_objects(UsanSan.objects.filter(status=True))
		object4 = self.get_user_objects(NasosStants.objects.filter(status=True))
		object5 = self.get_user_objects(Lab.objects.filter(status=True))
		object6 = self.get_user_objects(Sh_suljee.objects.filter(status=True))
		object7 = self.get_user_objects(Ts_baiguulamj.objects.filter(status=True))

		object9 = self.get_user_objects(WaterCar.objects.filter(status=True))
		object10 = self.get_user_objects(BohirCar.objects.filter(status=True))
		object11 = self.get_user_objects(UsDamjuulahBair.objects.filter(status=True))
		object12 = self.get_user_objects(UsTugeehBair.objects.filter(status=True))
		object13 = self.get_user_objects(Equipment.objects.filter(status=True))
		object14 = self.get_user_objects(ABB.objects.filter(status=True))
		object15 = self.get_user_objects(HudagNegtsgesenBairshliinZurag.objects.filter(status=True))


		context['hudag_count'] = object2.count()
		context['usansan_count'] = object3.count()
		context['nasos_count'] = object4.count()
		context['lab_count'] = object5.count()
		context['sh_suljee_count'] = object6.count()
		context['ts_baig_count'] = object7.count()

		context['water_car_count'] = object9.count()
		context['bohir_car_count'] = object10.count()
		context['us_damjuulah_count'] = object11.count()
		context['us_tugeeh_count'] = object12.count()
		context['equipment_count'] = object13.count()
		context['hariutsaj_barilguud_count'] = object14.count()
		context['us_hangamj_schema_count'] = object15.count()
		context['object_list'] = object2


		url_hudag_list = reverse_lazy('tza_gunii_hudag_list')
		url_usansan_list = reverse_lazy('tza_usan_san_list')
		url_nasos_list = reverse_lazy('tza_nasos_list')
		url_lab_list = reverse_lazy('tza_lab_list')
		url_sh_suljee_list = reverse_lazy('tza_sh_suljee_list')
		url_ts_baig_list = reverse_lazy('tza_ts_baig_list')

		url_water_car_list = reverse_lazy('tza_water_car_list')
		url_bohir_car_list = reverse_lazy('tza_bohir_car_list')
		url_us_damjuulah_list = reverse_lazy('tza_us_damjuulah_list')
		url_us_tugeeh_list = reverse_lazy('tza_us_tugeeh_list')
		url_equipment_list = reverse_lazy('tza_tonog_tohooromj_list')
		url_abb_list = reverse_lazy('tza_hariutsaj_barilguud_list')
		url_us_hangamj_schema_list = reverse_lazy('tza_us_hangamj_schema_list')

		context['url_hudag_list'] = url_hudag_list
		context['url_usansan_list'] = url_usansan_list
		context['url_nasos_list'] = url_nasos_list
		context['url_lab_list'] = url_lab_list
		context['url_sh_suljee_list'] = url_sh_suljee_list
		context['url_ts_baig_list'] = url_ts_baig_list

		context['url_water_car_list'] = url_water_car_list
		context['url_bohir_car_list'] = url_bohir_car_list
		context['url_us_damjuulah_list'] = url_us_damjuulah_list
		context['url_us_tugeeh_list'] = url_us_tugeeh_list
		context['url_equipment_list'] = url_equipment_list
		context['url_abb_list'] = url_abb_list
		context['url_us_hangamj_schema_list'] = url_us_hangamj_schema_list

		return context
class TZA_Gunii_Hudag_list(LoginRequired, ListView, Base_List_FilterView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_gunii_hudag_list.html'
	queryset = Hudag.objects.filter(status = True)
	filter_class = Hudag_filter
	def get_context_data(self, **kwargs):
		context = super(TZA_Gunii_Hudag_list, self).get_context_data(**kwargs)
		context['filter_form'] = self.get_filter()
		return context
	def get_queryset(self):
		queryset = super(TZA_Gunii_Hudag_list, self).get_queryset()
		queryset = self.get_user_objects(queryset)
		queryset = self.filter(queryset)
		return queryset
	def filter(self, queryset):
		city = self.request.GET.get('city')
		district = self.request.GET.get('district')
		khoroo = self.request.GET.get('khoroo')
		if city:
			queryset = queryset.filter(city=city)
		if district:
			queryset = queryset.filter(district=district)
		if khoroo:
			queryset = queryset.filter(khoroo=khoroo)
		return queryset
	
class TZA_Usan_San_list(LoginRequired, ListView, Base_List_FilterView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_usan_san_list.html'
	queryset = UsanSan.objects.filter(status = True)
	filter_class = UsanSan_filter
	def get_context_data(self, **kwargs):
		context = super(TZA_Usan_San_list, self).get_context_data(**kwargs)
		context['filter_form'] = self.get_filter()
		return context
	def get_queryset(self):
		queryset = super(TZA_Usan_San_list, self).get_queryset()
		queryset = self.get_user_objects(queryset = queryset)
		queryset = self.filter(queryset)
		return queryset
	def filter(self, queryset):
		city = self.request.GET.get('city')
		district = self.request.GET.get('district')
		khoroo = self.request.GET.get('khoroo')
		if city:
			queryset = queryset.filter(city=city)
		if district:
			queryset = queryset.filter(district=district)
		if khoroo:
			queryset = queryset.filter(khoroo=khoroo)
		return queryset
class TZA_Nasos_list(LoginRequired, ListView, Base_List_FilterView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_nasos_list.html'
	queryset = NasosStants.objects.filter(status = True)
	filter_class = NasosStants_filter
	def get_context_data(self, **kwargs):
		context = super(TZA_Nasos_list, self).get_context_data(**kwargs)
		context['filter_form'] = self.get_filter()
		return context
	def get_queryset(self):
		queryset = super(TZA_Nasos_list, self).get_queryset()
		queryset = self.get_user_objects(queryset = queryset)
		queryset = self.filter(queryset)
		return queryset
	def filter(self, queryset):
		city = self.request.GET.get('city')
		district = self.request.GET.get('district')
		khoroo = self.request.GET.get('khoroo')
		if city:
			queryset = queryset.filter(city=city)
		if district:
			queryset = queryset.filter(district=district)
		if khoroo:
			queryset = queryset.filter(khoroo=khoroo)
		return queryset
class TZA_Lab_list(LoginRequired, ListView, Base_List_FilterView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_lab_list.html'
	queryset = Lab.objects.filter(status = True)
	filter_class = Lab_filter
	def get_context_data(self, **kwargs):
		context = super(TZA_Lab_list, self).get_context_data(**kwargs)
		context['filter_form'] = self.get_filter()
		return context
	def get_queryset(self):
		queryset = super(TZA_Lab_list, self).get_queryset()
		queryset = self.get_user_objects(queryset = queryset)
		queryset = self.filter(queryset)
		return queryset
	def filter(self, queryset):
		torol = self.request.GET.get('torol')
		if torol:
			queryset = queryset.filter(torol = torol)
		return queryset
class TZA_Sh_Suljee_list(LoginRequired, ListView, Base_List_FilterView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_sh_suljee_list.html'
	queryset = Sh_suljee.objects.filter(status = True)
	filter_class = Sh_suljee_filter
	def get_context_data(self, **kwargs):
		context=super(TZA_Sh_Suljee_list, self).get_context_data(**kwargs)
		context['filter_form'] = self.get_filter()
		return context
	def get_queryset(self):
		queryset = super(TZA_Sh_Suljee_list, self).get_queryset()
		queryset = self.get_user_objects(queryset = queryset)
		queryset = self.filter(queryset)
		return queryset
	def filter(self, queryset):
		shugam_helber = self.request.GET.get('shugam_helber')
		if shugam_helber:
			queryset = queryset.filter(shugam_helber = shugam_helber)
		return queryset
class TZA_Ts_Baiguulamj_list(LoginRequired, ListView, Base_List_FilterView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_ts_baiguulamj_list.html'
	queryset = Ts_baiguulamj.objects.filter(status = True)
	filter_class = Ajiltan_filter
	def get_context_data(self, **kwargs):
		context = super(TZA_Ts_Baiguulamj_list, self).get_context_data(**kwargs)
		context['filter_form'] = self.get_filter()
		return context
	def get_queryset(self):
		queryset = super(TZA_Ts_Baiguulamj_list, self).get_queryset()
		queryset = self.get_user_objects(queryset = queryset)
		queryset = self.filter(queryset)
		return queryset
	def filter(self, queryset):
		return queryset
class TZA_Us_Tugeeh_list(LoginRequired, ListView, Base_List_FilterView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_us_tugeeh_list.html'
	queryset = UsTugeehBair.objects.filter(status = True)
	filter_class = UsTugeehBair_filter
	def get_context_data(self, **kwargs):
		context = super(TZA_Us_Tugeeh_list, self).get_context_data(**kwargs)
		context['filter_form'] = self.get_filter()
		return context
	def get_queryset(self):
		queryset = super(TZA_Us_Tugeeh_list, self).get_queryset()
		queryset = self.get_user_objects(queryset = queryset)
		queryset = self.filter(queryset)
		return queryset
	def filter(self, queryset):
		city = self.request.GET.get('city')
		district = self.request.GET.get('district')
		khoroo = self.request.GET.get('khoroo')
		if city:
			queryset = queryset.filter(city=city)
		if district:
			queryset = queryset.filter(district=district)
		if khoroo:
			queryset = queryset.filter(khoroo=khoroo)
		return queryset
class TZA_Us_Damjuulah_list(LoginRequired, ListView, Base_List_FilterView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_us_damjuulah_list.html'
	queryset = UsDamjuulahBair.objects.filter(status = True)
	filter_class = Ajiltan_filter
	def get_context_data(self, **kwargs):
		context = super(TZA_Us_Damjuulah_list, self).get_context_data(**kwargs)
		context['filter_form'] = self.get_filter()
		return context
	def get_queryset(self):
		queryset = super(TZA_Us_Damjuulah_list, self).get_queryset()
		queryset = self.get_user_objects(queryset = queryset)
		queryset = self.filter(queryset)
		return queryset
	def filter(self, queryset):
		return queryset

class TZA_Water_Car_list(LoginRequired, ListView, Base_List_FilterView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_water_car_list.html'
	queryset = WaterCar.objects.filter(status = True)
	filter_class = Ajiltan_filter
	def get_context_data(self, **kwargs):
		context = super(TZA_Water_Car_list, self).get_context_data(**kwargs)
		context['filter_form'] = self.get_filter()
		return context
	def get_queryset(self):
		queryset = super(TZA_Water_Car_list, self).get_queryset()
		queryset = self.get_user_objects(queryset = queryset)
		queryset = self.filter(queryset)
		return queryset
	def filter(self, queryset):
		return queryset
class TZA_Bohir_Car_list(LoginRequired, ListView, Base_List_FilterView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_bohir_car_list.html'
	queryset = BohirCar.objects.filter(status = True)
	filter_class = Ajiltan_filter
	def get_context_data(self, **kwargs):
		context = super(TZA_Bohir_Car_list, self).get_context_data(**kwargs)
		context['filter_form'] = self.get_filter()
		return context
	def get_queryset(self):
		queryset = super(TZA_Bohir_Car_list, self).get_queryset()
		queryset = self.get_user_objects(queryset = queryset)
		queryset = self.filter(queryset)
		return queryset
	def filter(self, queryset):
		return queryset
class TZA_Tonog_Tohooromj_list(LoginRequired, ListView, Base_List_FilterView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_tonog_tohooromj_list.html'
	queryset = Equipment.objects.filter(status = True)
	filter_class = Ajiltan_filter
	def get_context_data(self, **kwargs):
		context = super(TZA_Tonog_Tohooromj_list, self).get_context_data(**kwargs)
		context['filter_form'] = self.get_filter()
		return context
	def get_queryset(self):
		queryset = super(TZA_Tonog_Tohooromj_list, self).get_queryset()
		queryset = self.get_user_objects(queryset = queryset)
		queryset = self.filter(queryset)
		return queryset
	def filter(self, queryset):
		return queryset
class TZA_ABB_list(LoginRequired, ListView, Base_List_FilterView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_abb_list.html'
	queryset = ABB.objects.filter(status = True)
	filter_class = Ajiltan_filter
	def get_context_data(self, **kwargs):
		context = super(TZA_ABB_list, self).get_context_data(**kwargs)
		context['filter_form'] = self.get_filter()
		return context
	def get_queryset(self):
		queryset = super(TZA_ABB_list, self).get_queryset()
		queryset = self.get_user_objects(queryset = queryset)
		queryset = self.filter(queryset)
		return queryset
	def filter(self, queryset):
		return queryset
class TZA_Us_hangamjiin_schema_zurag_list(LoginRequired, ListView, Base_List_FilterView):
	perm_code_names = ['tza_mergejilten_permission', 'uta_mergejilten_permission', 'hzm_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/list_htmls/tza_us_hangamj_schema_list.html'
	queryset = HudagNegtsgesenBairshliinZurag.objects.filter(status = True)
	filter_class = Ajiltan_filter
	def get_context_data(self, **kwargs):
		context = super(TZA_Us_hangamjiin_schema_zurag_list, self).get_context_data(**kwargs)
		context['filter_form'] = self.get_filter()
		return context
	def get_queryset(self):
		queryset = super(TZA_Us_hangamjiin_schema_zurag_list, self).get_queryset()
		queryset = self.get_user_objects(queryset = queryset)
		queryset = self.filter(queryset)
		return queryset
	def filter(self, queryset):
		return queryset

class TZA_BB_approveView(Base_Ajax_FormView):
	perm_code_names = ['tza_mergejilten_permission']
	form_class=EmptyForm
	template_name = 'tza/tonog_tohooromj/form_div_htmls/bb_approve.html'
	success_url=reverse_lazy('tza_tohooromj_menu')
	view_url = reverse_lazy('tza_bb_approve')
	object_class=BB
	def form_valid(self, form):
		chosen_obj_ids = self.request.POST.getlist('chosen_objs')
		#print chosen_obj_ids
		chosen_bbs = self.object_class.objects.filter(id__in=chosen_obj_ids)
		for bb in chosen_bbs:
			bb.approved = True
			bb.save()
		return super(TZA_BB_approveView, self).form_valid(form)
class TZA_Car_approveView(TZA_BB_approveView):
	template_name = 'tza/tonog_tohooromj/form_div_htmls/car_approve.html'
	view_url = reverse_lazy('tza_car_approve')
	object_class = Car
class TZA_ABB_approveView(TZA_BB_approveView):
	template_name = 'tza/tonog_tohooromj/form_div_htmls/abb_approve.html'
	view_url = reverse_lazy('tza_abb_approve')
	object_class = ABB
class TZA_equipment_approveView(TZA_BB_approveView):
	template_name = 'tza/tonog_tohooromj/form_div_htmls/equipment_approve.html'
	view_url = reverse_lazy('tza_equipment_approve')
	object_class = Equipment

class TZA_BB_disapproveView(Base_Ajax_FormView):
	perm_code_names = ['tza_mergejilten_permission']
	form_class=EmptyForm
	template_name = 'tza/tonog_tohooromj/form_div_htmls/bb_disapprove.html'
	success_url=reverse_lazy('tza_tohooromj_menu')
	view_url = reverse_lazy('tza_bb_approve')
	object_class=BB
	def form_valid(self, form):
		chosen_obj_ids = self.request.POST.getlist('chosen_objs')
		#print chosen_obj_ids
		chosen_bbs = self.object_class.objects.filter(id__in=chosen_obj_ids)
		for bb in chosen_bbs:
			bb.approved = False
			bb.save()
		return super(TZA_BB_disapproveView, self).form_valid(form)
class TZA_Car_disapproveView(TZA_BB_disapproveView):
	template_name = 'tza/tonog_tohooromj/form_div_htmls/car_disapprove.html'
	view_url = reverse_lazy('tza_car_disapprove')
	object_class = Car
class TZA_ABB_disapproveView(TZA_BB_disapproveView):
	template_name = 'tza/tonog_tohooromj/form_div_htmls/abb_disapprove.html'
	view_url = reverse_lazy('tza_abb_disapprove')
	object_class = ABB
class TZA_equipment_disapproveView(TZA_BB_disapproveView):
	template_name = 'tza/tonog_tohooromj/form_div_htmls/equipment_disapprove.html'
	view_url = reverse_lazy('tza_equipment_disapprove')
	object_class = Equipment


class TZA_BB_tze_updateView(Base_Ajax_FormView):
	perm_code_names = ['tza_mergejilten_permission']
	form_class=BB_tze_update_form
	template_name = 'tza/tonog_tohooromj/form_div_htmls/car_tze_update_many.html'
	success_url=reverse_lazy('tza_tohooromj_menu')
	view_url = reverse_lazy('tza_bb_update_tze_many')
	object_class=BB
	def form_valid(self, form):
		tze = form.cleaned_data['tze']
		chosen_obj_ids = self.request.POST.getlist('chosen_objs')
		#print chosen_obj_ids
		chosen_bbs = self.object_class.objects.filter(id__in=chosen_obj_ids)
		for bb in chosen_bbs:
			bb.tze = tze
			bb.save()
		return super(TZA_BB_tze_updateView, self).form_valid(form)
class TZA_Car_tze_updateView(TZA_BB_tze_updateView):
	form_class=Car_tze_update_form
	view_url = reverse_lazy('tza_car_update_tze_many')
	object_class=Car
class TZA_ABB_tze_updateView(TZA_BB_tze_updateView):
	form_class=ABB_tze_update_form
	view_url = reverse_lazy('tza_abb_update_tze_many')
	object_class=ABB
class TZA_Equipment_tze_updateView(TZA_BB_tze_updateView):
	form_class=Equipment_tze_update_form
	view_url = reverse_lazy('tza_equipment_update_tze_many')
	object_class=Equipment


"""    TZA tonog tohooromj menu deer ashiglagdaj baigaa viewuud  END  """


"""    TZA TZ gerchilgee  menu deer ashiglagdaj baigaa viewuud  START  """

class TZA_TZ_gerchilgee_listView(LoginRequired, ListView, Base_List_FilterView):
	perm_code_names = ['tza_mergejilten_permission']
	template_name = 'tza/tusgai_zovshoorol/tza_tz_gerchilgee_list.html'
	queryset = Certificate.objects.filter(status = True)
	filter_class = TZ_Gerchilgee_filter
	def get_context_data(self, **kwargs):
		context = super(TZA_TZ_gerchilgee_listView, self).get_context_data(**kwargs)
		context['filter_form'] = self.get_filter()

		return context
	def get_queryset(self):
		queryset = super(TZA_TZ_gerchilgee_listView, self).get_queryset()
		queryset = self.get_user_objects(queryset = queryset)
		queryset = self.filter(queryset)
		return queryset
	def filter(self, queryset):
		tze_baig = self.request.GET.get('tze_baig')
		tz_list = self.request.GET.getlist('tz')

		baigs = self.get_mergejilten_tzes()
		if tze_baig:
			baigs = baigs.filter(org_name__icontains = tze_baig)
			queryset = queryset.filter(tze = baigs)
		if tz_list:
			for tz in tz_list:
				queryset = queryset.filter(tz_id = tz)

		return queryset

class TZA_TZ_gerchilgee_delgerenguiView(TZE_TZ_gerchilgee_delgerengui):
	perm_code_names = ['tza_mergejilten_permission']
	

class TZA_TZ_gerchilgee_tolov_change(Base_Ajax_FormView):
	perm_code_names = ['tza_mergejilten_permission']
	template_name = 'tza/tusgai_zovshoorol/form_div_htmls/tz_gerchilgee_tolov_change_div.html'
	form_class = TZ_gerchilgee_change_tolov
	success_url = reverse_lazy('tza_tz_gerchilgee_list')
	def dispatch(self, request, *args, **kwargs):
		object_id = kwargs['tz_gerchilgee_id']
		self._object = get_object_or_404(Certificate, id = object_id)
		return super(TZA_TZ_gerchilgee_tolov_change, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(TZA_TZ_gerchilgee_tolov_change, self).get_context_data(**kwargs)
		context['certificate'] = self._object
		return context
	def form_valid(self, form):
		self._object.tolov = form.cleaned_data['tolov']
		self._object.save()
		messages.success(self.request, 'Амжилттай хадгаллаа.')
		return super(TZA_TZ_gerchilgee_tolov_change, self).form_valid(form)
class TZA_TZ_gerchilgee_sungah(LoginRequired, UpdateView):
	perm_code_names = ['tza_mergejilten_permission']
	template_name = 'tza/tusgai_zovshoorol/form_div_htmls/tz_gerchilgee_sungah_div.html'
	form_class = TZ_gerchilgee_sungah_Form
	success_url = reverse_lazy('tza_tz_gerchilgee_list')
	pk_url_kwarg = 'tz_gerchilgee_id'
	context_object_name = 'certificate'
	model=Certificate
	def form_valid(self, form):
		if form.has_changed():
			sungalt = Certificate_sungalt(certificate = self.object, ognoo = timezone.now())
			sungalt.save()

			messages.success(self.request, 'Амжилттай хадгаллаа.')
		messages.success(self.request, 'Форм өөрчлөгдөөгүй байна.')
		return super(TZA_TZ_gerchilgee_sungah, self).form_valid(form)

class TZA_TZ_gerchilgee_huulbar_insert(LoginRequired, UpdateView):
	perm_code_names = ['tza_mergejilten_permission']
	template_name = 'tza/tusgai_zovshoorol/form_div_htmls/tz_gerchilgee_huulbar_insert.html'
	form_class = Certificate_huulbar_insert_Form
	success_url = reverse_lazy('tza_tz_gerchilgee_list')
	pk_url_kwarg = 'tz_gerchilgee_id'
	context_object_name = 'certificate'
	model=Certificate

"""    TZA TZ gerchilgee  menu deer ashiglagdaj baigaa viewuud  END  """


class tzauatailan_menu(LoginRequired, ListView):
	perm_code_names = ['tza_mergejilten_permission']
	template_name = "tza/uatailan/uatailan.html"
	def get_queryset(self):
		queryset = UATailan.objects.filter(status = True)
		return queryset
	def get_context_data(self, **kwargs):
		context = super(tzauatailan_menu, self).get_context_data(**kwargs)
		context['water'] = AnalysisWater.objects.filter(status= True)
		context['bohir'] = AnalysisBohir.objects.filter(status=True)
		return context
class tzauatailan_ListView(tzauatailan_menu):
	template_name = "tza/uatailan/list_htmls/ua_tailan_list.html"
class tzauatailan_material_listView(LoginRequired,TemplateView):
	perm_code_names = ['tza_mergejilten_permission']
	template_name = "tza/uatailan/ua_tailan_material_list.html"
	def get_context_data(self, **kwargs):
		context = super(tzauatailan_material_listView, self).get_context_data(**kwargs)
		obj_id = kwargs['pk']
		obj = get_object_or_404(UATailan, id = obj_id)
		context['obj'] = obj
		return context
class TZA_water_shinjilgee_listView(LoginRequired, ListView, Base_List_FilterView):
	perm_code_names = ['tza_mergejilten_permission']
	template_name = "tza/uatailan/water_shinjilgee_list.html"
	filter_class = Analysis_water_filter
	def get_queryset(self):
		queryset = AnalysisWater.objects.filter(status = True)
		queryset = self.get_user_objects(queryset = queryset)
		queryset = self.filter(queryset)
		return queryset
	def get_context_data(self, **kwargs):
		context = super(TZA_water_shinjilgee_listView, self).get_context_data(**kwargs)
		names_dic = {}
		delgerengui_urls_dic = {}
		for i in context['object_list']:
 			if Analysis_undnii_us.objects.filter(id= i.id):
 				names_dic[i.id] = u'Ундны усны шинжилгээ'
 				delgerengui_urls_dic[i.id] = reverse_lazy('tze_undnii_water_analysis_delgerengui', kwargs={'pk': i.id})
	 		elif Analysis_savlasan_us.objects.filter(id= i.id):
	 			names_dic[i.id]= u'Савласан усны шинжилгээ'
	 			delgerengui_urls_dic[i.id] = reverse_lazy('tze_savlasan_water_analysis_delgerengui', kwargs={'pk': i.id})

		context['names_dic'] = names_dic
		context['delgerengui_urls_dic'] = delgerengui_urls_dic
		context['filter_form'] = self.get_filter()
		return context
	def filter(self, queryset):
		tze_baig = self.request.GET.get('tze_baig')

		baigs = self.get_mergejilten_tzes()
		if tze_baig:
			baigs = baigs.filter(org_name__icontains = tze_baig)
			queryset = queryset.filter(tze = baigs)

		return queryset
class TZA_bohir_shinjilgee_listView(LoginRequired, ListView, Base_List_FilterView):
	perm_code_names = ['tza_mergejilten_permission']
	template_name = "tza/uatailan/bohir_shinjilgee_list.html"
	filter_class = AnalysisBohir_filter
	def get_queryset(self):
		queryset = AnalysisBohir.objects.filter(status = True)
		queryset = self.get_user_objects(queryset = queryset)
		queryset = self.filter(queryset)
		return queryset
		return qs
	def get_context_data(self, **kwargs):
		context = super(TZA_bohir_shinjilgee_listView,self).get_context_data(**kwargs)
		context['filter_form'] = self.get_filter()
		return context
	def filter(self, queryset):
		tze_baig = self.request.GET.get('tze_baig')

		baigs = self.get_mergejilten_tzes()
		if tze_baig:
			baigs = baigs.filter(org_name__icontains = tze_baig)
			queryset = queryset.filter(tze = baigs)

		return queryset

class TZA_UAT_hudag(LoginRequired, ListView):
	perm_code_names = ['tza_mergejilten_permission']
	template_name = "uatailan/gunii_hudag_sudalgaa.html"
	def dispatch(self, request, *args, **kwargs):
		obj_id = kwargs['pk']
		self.obj = get_object_or_404(UATailan, id = obj_id)
		return super(TZA_UAT_hudag, self).dispatch(request, *args, **kwargs)
	def get(self, request, *args, **kwargs):
		self.baiguullaga = self.obj.tze
		return super(TZA_UAT_hudag, self).get(request, *args, **kwargs)
	def get_queryset(self):
		hudag_queryset = self.obj.gunii_hudags.hudags.all()
		dummy_obj = Hudag()
		queryset = dummy_obj.get_history_queryset(hudag_queryset, self.obj.tailan_date)
		return queryset
	def get_context_data(self, **kwargs):
		context=super(TZA_UAT_hudag, self).get_context_data(**kwargs)
		context['is_history']=True
		context['history_date']=self.obj.tailan_date
		return context
class TZA_UAT_tsevershuuleh(TZA_UAT_hudag):
	template_name = "uatailan/tsevershuuleh_sudalgaa.html"
	def get_queryset(self):
		obj_queryset = self.obj.tsevershuuleh.tsevershuuleh.all()
		dummy_obj = Ts_baiguulamj()
		queryset = dummy_obj.get_history_queryset(obj_queryset, self.obj.tailan_date)
		return queryset
	#def get_context_data(self, **kwargs):
	#	context = super(TZA_uatailan2_tsevershuulehView, self).get_context_data(**kwargs)
	#	context['tohooromj_count'] = 
class TZA_UAT_usansan(TZA_UAT_hudag):
	template_name = "uatailan/usansan_sudalgaa.html"
	def get_queryset(self):
		obj_queryset = self.obj.usansan.usan_sans.all()
		dummy_obj = UsanSan()
		queryset = dummy_obj.get_history_queryset(obj_queryset, self.obj.tailan_date)
		return queryset
class TZA_UAT_tsever_us_nasosStants(TZA_UAT_hudag):
	template_name = "uatailan/tsever_us_nasos_stants_sudalgaa.html"
	def get_queryset(self):
		obj_queryset = self.obj.tsever_nasos_stants.nasos_stantss.all()
		dummy_obj = NasosStants()
		queryset = dummy_obj.get_history_queryset(obj_queryset, self.obj.tailan_date)
		return queryset
class TZA_UAT_tsever_us_lab(TZA_UAT_hudag):
	template_name = "uatailan/tsever_us_lab_sudalgaa.html"
	def get_queryset(self):
		obj_queryset = self.obj.lab.labs.all()
		dummy_obj = Lab()
		queryset = dummy_obj.get_history_queryset(obj_queryset, self.obj.tailan_date)
		return queryset
class TZA_UAT_tsever_us_sh_suljee(TZA_UAT_hudag):
	template_name = "uatailan/tsever_us_sh_suljee.html"
	def get_queryset(self):
		obj_queryset = self.obj.tsever_usnii_shugam.sh_suljees.all()
		dummy_obj = Sh_suljee()
		queryset = dummy_obj.get_history_queryset(obj_queryset, self.obj.tailan_date)
		return queryset
class TZA_UAT_bohir_us_sh_suljee(TZA_UAT_hudag):
	template_name = "uatailan/bohir_us_sh_suljee_sudalgaa.html"
	def get_queryset(self):
		obj_queryset = self.obj.bohir_usnii_shugam.sh_suljees.all()
		dummy_obj = Sh_suljee()
		queryset = dummy_obj.get_history_queryset(obj_queryset, self.obj.tailan_date)
		return queryset
class TZA_UAT_abb(TZA_UAT_hudag):
	template_name = "uatailan/abb_sudalgaa.html"
	def get_queryset(self):
		obj_queryset = self.obj.abb.abbs.all()
		dummy_obj = ABB()
		queryset = dummy_obj.get_history_queryset(obj_queryset, self.obj.tailan_date)
		return queryset
class TZA_UAT_us_tugeeh_bar(TZA_UAT_hudag):
	template_name = "uatailan/us_tugeeh_bair_sudalgaa.html"
	def get_queryset(self):
		obj_queryset = self.obj.us_tugeeh.us_tugeeh_bairs.all()
		dummy_obj = UsTugeehBair()
		queryset = dummy_obj.get_history_queryset(obj_queryset, self.obj.tailan_date)
		return queryset
class TZA_UAT_tseverleh(TZA_UAT_hudag):
	template_name = "uatailan/tseverleh_sudalgaa.html"
	def get_queryset(self):
		obj_queryset = self.obj.tseverleh.tseverleh.all()
		dummy_obj = Ts_baiguulamj()
		queryset = dummy_obj.get_history_queryset(obj_queryset, self.obj.tailan_date)
		return queryset
class TZA_UAT_bohir_us_nasosStants(TZA_UAT_hudag):
	template_name = "uatailan/bohir_us_nasos_stants_sudalgaa.html"
	def get_queryset(self):
		obj_queryset = self.obj.bohir_nasos_stants.nasos_stantss.all()
		dummy_obj = NasosStants()
		queryset = dummy_obj.get_history_queryset(obj_queryset, self.obj.tailan_date)
		return queryset
class TZA_UAT_water_car(TZA_UAT_hudag):
	template_name = "uatailan/water_car_sudalgaa.html"
	def get_queryset(self):
		obj_queryset = self.obj.water_car.water_cars.all()
		dummy_obj = WaterCar()
		queryset = dummy_obj.get_history_queryset(obj_queryset, self.obj.tailan_date)
		return queryset
class TZA_UAT_bohir_car(TZA_UAT_hudag):
	template_name = "uatailan/bohir_car_sudalgaa.html"
	def get_queryset(self):
		obj_queryset = self.obj.bohir_car.bohir_cars.all()
		dummy_obj = BohirCar()
		queryset = dummy_obj.get_history_queryset(obj_queryset, self.obj.tailan_date)
		return queryset
class TZA_UAT_us_dulaan_damjuulah_tov(TZA_UAT_hudag):
	template_name = "uatailan/us_dulaan_damjuulah_tov_sudalgaa.html"
	def get_queryset(self):
		obj_queryset = self.obj.us_damjuulah_tov.usDamjuulahBair.all()
		queryset = UsDamjuulahBair.get_history_queryset(obj_queryset, self.obj.tailan_date)
		return queryset
class TZA_UAT_hunii_noots(TZA_UAT_hudag):
	template_name = "uatailan/hunii_noots_sudalgaa.html"
	def get_queryset(self):
		obj_queryset = self.obj.ajiltans.ajiltans.all()
		queryset = Ajiltan.get_history_queryset(obj_queryset, self.obj.tailan_date)
		return queryset


def UAT_negtgel(request):
	tailan_ids = request.GET.getlist('chosen_tailans')
	print tailan_ids, "\n\n\n"
	if tailan_ids:
		tailans = UATailan.objects.filter(id__in = tailan_ids)

		response = HttpResponse(content_type='application/vnd.ms-excel')
		response['Content-Disposition'] = 'attachment; filename=UATailan.xlsx'

		output = StringIO.StringIO()
		workbook = xlsxwriter.Workbook(output)



		UATailan.export_to_excel(workbook, tailans)




		workbook.close()

		xlsx_data = output.getvalue()
		response.write(xlsx_data)
		return response		

	return HttpResponseRedirect(reverse_lazy('tza_ua_tailan_menu'))


def UAT_create(request):
	user = get_object_or_404(User, id=request.user.id)
	tze_queryset = TZE.objects.filter(status = True)

	total_created_tailan = 0
	for tze in tze_queryset:
		if tze.get_huchintei_certificates():
			tailan_this_year = UATailan.objects.filter(tze = tze, tailan_date__year = timezone.now().year)
			if not tailan_this_year:
				tailan_this_year = UATailan(tze = tze, tailan_date = timezone.now())
				tailan_this_year.status = True
				tailan_this_year.created_by = user

				tailan_this_year.generate_tailans()
				
				total_created_tailan = total_created_tailan + 1
	
	messages.success(request, 'Нийт {} тусгай зөвшөөрөл эзэмшигчид үйл ажиллагааны тайлан үүсгэлээ.'.format(total_created_tailan))
	return HttpResponseRedirect(reverse_lazy('tza_ua_tailan_menu'))


class BB_tze_update(LoginRequired, UpdateView):
	# neg objectiin tze update hiine
	perm_code_names = ['tza_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/form_div_htmls/bb_tze_update.html'
	form_class = BB_tze_update_form
	success_url = reverse_lazy('tza_tohooromj_menu')
	context_object_name = 'certificate'
	model=BB
	
class Car_tze_update(LoginRequired, UpdateView):
	# neg objectiin tze update hiine
	perm_code_names = ['tza_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/form_div_htmls/car_tze_update.html'
	form_class = Car_tze_update_form
	success_url = reverse_lazy('tza_tohooromj_menu')
	context_object_name = 'certificate'
	model=Car

class ABB_tze_update(LoginRequired, UpdateView):
	# neg objectiin tze update hiine
	perm_code_names = ['tza_mergejilten_permission']
	template_name = 'tza/tonog_tohooromj/form_div_htmls/abb_tze_update.html'
	form_class = ABB_tze_update_form
	success_url = reverse_lazy('tza_tohooromj_menu')
	context_object_name = 'certificate'
	model=ABB










class tzagshutailanView(LoginRequired, ListView, Base_List_FilterView):
	perm_code_names = ['tza_mergejilten_permission']
	template_name = "tza/gshu_tailan/gshu_tailan.html"
	filter_class = TZE_search_by_name
	def get_queryset(self):
		queryset = GShU.objects.filter(status = True).exclude(tolov=u'Мэдээлэл дутуу').exclude(tolov=u'Буцаасан')
		queryset = self.get_user_objects(queryset = queryset)
		queryset = self.filter(queryset)
		return queryset
	def get_context_data(self, **kwargs):
		context = super(tzagshutailanView,self).get_context_data(**kwargs)
		context['filter_form'] = self.get_filter()
		return context
	def filter(self, queryset):
		tze_baig_name = self.request.GET.get('search')
		if tze_baig_name:
			tze_queryset = self.get_mergejilten_tzes().filter(org_name__icontains = tze_baig_name)
			queryset = queryset.filter(tze = tze_queryset)
		return queryset
class TZA_gshu_check_View(Base_Ajax_FormView):
	perm_code_names = ['tza_mergejilten_permission']
	form_class = TZA_gshu_check_form
	template_name = 'tza/gshu_tailan/tza_gshu_check.html'
	header = "Гүйцэтгэлийн шалгуур үзүүлэлтийн тайлан"
	def dispatch(self, request, *args, **kwargs):
		gshu_id = kwargs['gshu_id']
		self.gshu = get_object_or_404(GShU, id=gshu_id)
		self.view_url = reverse_lazy('tza_gshu_check', kwargs={'gshu_id': gshu_id})
		return super(TZA_gshu_check_View, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(TZA_gshu_check_View, self).get_context_data(**kwargs)
		context['header'] = self.header
		return context
	def get_form_kwargs(self):
		kwargs = super(TZA_gshu_check_View, self).get_form_kwargs()
		if hasattr(self, 'gshu'):
			kwargs.update({'instance': self.gshu})
		return kwargs
	def form_valid(self, form):
		obj= form.save(commit=False)
		obj.status = True
		obj.created_by = self.user
		obj.save()
		return super(TZA_gshu_check_View, self).form_valid(form)
def GSHU_tailan_create(request):
	user = get_object_or_404(User, id=request.user.id)
	tze_queryset = TZE.objects.filter(status = True)

	total_created_gshu = 0
	for tze in tze_queryset:
		if tze.get_huchintei_certificates():
			gshu_this_year = GShU.objects.filter(tze = tze, tailan_date__year = timezone.now().year)
			if not gshu_this_year:
				gshu_this_year = GShU(tze = tze, tailan_date = timezone.now())
				gshu_this_year.status = True
				gshu_this_year.created_by = user
				num_list = tze.get_gshu_uzuulelt_num_list()
				for i in num_list:
					attr = "uzuulelt_{}".format(i)
					setattr(gshu_this_year, attr, True)
				gshu_this_year.save()
				
				total_created_gshu = total_created_gshu + 1
	
	messages.success(request, 'Нийт {} тусгай зөвшөөрөл эзэмшигчид ГШҮТ үүсгэлээ.'.format(total_created_gshu))
	return HttpResponseRedirect(reverse_lazy('tza_gshu_tailan_menu'))













class tzaNegtgelView(LoginRequired,TemplateView):
	perm_code_names = ['tza_mergejilten_permission']
	template_name = "tza/negtgel/negtgel.html"



def request_email(request, id = 0):
	#try:
	tze = TZE.objects.get(id=id)
	ajiltan = Ajiltan.objects.get(baiguullaga = tze)
	password = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
	e_mail_subject = "Бүртгэл амжилттай хийгдлээ"
	body = "Бүртгэл амжилттай хийгдлээ. Нууц үг: " + password
	thread = E_mail_sending_thread('wsrcmon@gmail.com', ajiltan.e_mail, e_mail_subject, body, 'QjErHKfS76KmRQBB')
	thread.start()
	print "thread started"
	u_zahiral = User(user_id = ajiltan, username = tze.reg_num, is_active = True)
	u_zahiral.set_password('12345')
	u_zahiral.save()
	b = TZE_Users_bind(tze = tze, user_zahiral = u_zahiral, status = True)
	b.save()
	
	group_tze = Group.objects.filter(name__icontains="тзэ")
	u_zahiral.groups = group_tze

	#except:
	#	print "request email error"
	return HttpResponseRedirect('/tza/')

def remove_email(request, id = 0):
	try:
		user = Ajiltan.objects.get(baiguullaga = TZE.objects.get(id=id))
		e_mail_subject = "Таны хүсэлт цуцлагдлаа"
		body = ""
		thread = E_mail_sending_thread('wsrcmon@gmail.com', user.e_mail, e_mail_subject, body, 'QjErHKfS76KmRQBB')
		thread.start()
		print "thread started"
		TZE.objects.get(id=id).delete()
	except:
		pass
	return HttpResponseRedirect('/tza/')


def BBHorvuuleh(request):
	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=NiitBarilgaBaiguulamj.xlsx'
	xlsx_data = BBHorvuulehToExcel()
	response.write(xlsx_data)
	return response

def BBHorvuulehToExcel():
	output = StringIO.StringIO()
	workbook = xlsxwriter.Workbook(output)
	worksheet1 = workbook.add_worksheet(u'Барилга байгууламжийн жагсаалт')
	worksheet1.set_column('A:J', 14)
	worksheet1.set_column('B:C', 20)
	title = workbook.add_format({
    	'bold': True,
    	'font_size': 14,
    	'align': 'center',
    	'valign': 'vcenter'
    	})
	title.set_text_wrap()
	header = workbook.add_format({
    	'bg_color': '#F7F7F7',
    	'color': 'black',
    	'align': 'center',
    	'valign': 'top',
    	'border': 1
    	})
    
	header.set_text_wrap()

	body = workbook.add_format({
		'border' : 1,
		'color': 'black',
    	'align': 'left',
    	'valign': 'middle'
		})
	body.set_text_wrap()
	bb= BB.objects.filter(status= True)
#   Хүснэгт 11
	title_text10 = u"Тусгай Зөвшөөрөл Эзэмшигчдийн барилга байгууламжийн товч жагсаалт"
	worksheet1.merge_range('B2:F2', title_text10, title)
	worksheet1.write('F3', u'Хүснэгт№1', header)
	worksheet1.merge_range('A4:A5', u'№', header)
	worksheet1.merge_range('B4:B5', u'Тусгай зөвшөөрөл эзэмшигч байгууллага', header)
	worksheet1.merge_range('C4:C5', u'Барилга байгууламжийн нэр', header)
	worksheet1.merge_range('D4:D5', u'Хүчин чадал', header)
	worksheet1.merge_range('E4:E5', u'Ашиглалтанд орсон огноо', header)
	worksheet1.merge_range('F4:F5', u'Тайлбар', header)
	
	tursh= u''

	if bb:
		for i in range(len(bb)):
			worksheet1.write('A%s' %(i+6), i+1, body)
		for iRow7, bbbb in enumerate(bb):
			tze1= TZE.objects.get(id= bbbb.tze_id)
			worksheet1.write(iRow7 + 5,1, tze1.org_name,  body)
			if Hudag.objects.filter(id= bbbb.id):
 				tursh = u'Худаг' 
	 		elif NasosStants.objects.filter(id= bbbb.id):
	 			tursh= u'Насос станц'
	 		elif Lab.objects.filter(id= bbbb.id):
	 			tursh= u'Лаборатори'
	 		elif Sh_suljee.objects.filter(id= bbbb.id):
	 			tursh= u'Шугам сүлжээ'
	 		elif UsanSan.objects.filter(id= bbbb.id):
	 			tursh= u'Усансан'
	 		elif UsTugeehBair.objects.filter(id= bbbb.id):
	 			tursh= u'Ус түгээх байр'
	 		elif UsDamjuulahBair.objects.filter(id= bbbb.id):
	 			tursh= u'Ус, дулаан дамжуулах төв'
	 		elif Ts_baiguulamj.objects.filter(id= bbbb.id):
	 			tursh= u'Цэвэрлэх байгууламж'
			worksheet1.write(iRow7 + 5,2, tursh ,  body)
			worksheet1.write(iRow7 + 5,3, bbbb.huchin_chadal, body)
			worksheet1.write(iRow7 + 5,4, bbbb.ashiglaltand_orson_ognoo.strftime('%d/%m/%Y'), body)
			worksheet1.write(iRow7 + 5,5, bbbb.tailbar, body)

	workbook.close()
	xlsx_data = output.getvalue()
	return xlsx_data

	
def CarHorvuuleh(request):
	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=NiitAvtomashin.xlsx'
	xlsx_data = CarHorvuulehToExcel()
	response.write(xlsx_data)
	return response

def CarHorvuulehToExcel():
	output = StringIO.StringIO()
	workbook = xlsxwriter.Workbook(output)
	worksheet1 = workbook.add_worksheet(u'Хүснэгт№1.')
	worksheet2 = workbook.add_worksheet(u'Хүснэгт№2.')
	worksheet1.set_column('A:J', 14)
	worksheet1.set_column(1,1, 20)
	worksheet2.set_column('A:J', 14)
	worksheet2.set_column(1,1, 20)
	title = workbook.add_format({
    	'bold': True,
    	'font_size': 14,
    	'align': 'center',
    	'valign': 'vcenter'
    	})
	title.set_text_wrap()
	header = workbook.add_format({
    	'bg_color': '#F7F7F7',
    	'color': 'black',
    	'align': 'center',
    	'valign': 'top',
    	'border': 1
    	})
    
	header.set_text_wrap()

	body = workbook.add_format({
		'border' : 1,
		'color': 'black',
    	'align': 'left',
    	'valign': 'middle'
		})
	body.set_text_wrap()
	watercar= WaterCar.objects.filter(status= True)
#   Хүснэгт 11
	title_text10 = u"Зөөврийн ус хангамжийн үйлчилгээ үзүүлдэг автомашины судалгаа"
	worksheet1.merge_range('B2:H2', title_text10, title)
	worksheet1.write('H3', u'Хүснэгт№1', header)
	worksheet1.merge_range('A4:A5', u'№', header)
	worksheet1.merge_range('B4:B5', u'Тусгай зөвшөөрөл эзэмшигч байгууллага', header)
	worksheet1.merge_range('C4:C5', u'Автомашины марк, улсын дугаар', header)
	worksheet1.merge_range('D4:D5', u'Хүчин чадал(тонн)', header)
	worksheet1.merge_range('E4:G4', u'Хэрэглэгчийн тоо', header)
	worksheet1.write('E5', u'ААНБ', header)
	worksheet1.write('F5', u'УТБ', header)
	worksheet1.write('G5', u'Хүн ам', header)
	worksheet1.merge_range('H4:H5', u'Борлуулсан усны хэмжээ(м3/хон)', header)
	if watercar:
		for i in range(len(watercar)):
			worksheet1.write('A%s' %(i+6), i+1, body)
		for iRow7, bbbb in enumerate(watercar):
			tze1= TZE.objects.get(id= bbbb.tze_id)
			worksheet1.write(iRow7 + 5,1, tze1.org_name,  body)
			worksheet1.write(iRow7 + 5,2, str(bbbb.mark)+' '+str(bbbb.no) ,  body)
			worksheet1.write(iRow7 + 5,3, bbbb.huchin_chadal, body)
			worksheet1.write(iRow7 + 5,4, bbbb.aanb_too, body)
			worksheet1.write(iRow7 + 5,5, bbbb.utb_too, body)
			worksheet1.write(iRow7 + 5,6, bbbb.hun_am_too, body)
			worksheet1.write(iRow7 + 5,7, bbbb.us, body)




	bohircar= BohirCar.objects.filter(status= True)
#   Хүснэгт 11
	title_text11 = u"Бохир ус зөөвөрлөх үйлчилгээ үзүүлдэг автомашины судалгаа"
	worksheet2.merge_range('B2:H2', title_text11, title)
	worksheet2.write('H3', u'Хүснэгт№2', header)
	worksheet2.merge_range('A4:A5', u'№', header)
	worksheet2.merge_range('B4:B5', u'Тусгай зөвшөөрөл эзэмшигч байгууллага', header)
	worksheet2.merge_range('C4:C5', u'Автомашины марк, улсын дугаар', header)
	worksheet2.merge_range('D4:D5', u'Хүчин чадал(тонн)', header)
	worksheet2.merge_range('E4:F4', u'Хэрэглэгчийн тоо', header)
	worksheet2.write('E5', u'Гэрээт', header)
	worksheet2.write('F5', u'Дуудлагын', header)
	worksheet2.merge_range('G4:G5', u'Зөөвөрлөсөн усны хэмжээ(м3/хон)', header)
	worksheet2.merge_range('H4:H5', u'Бохир ус нийлүүлэх цэгийн байршил', header)
	if bohircar:
		for i in range(len(bohircar)):
			worksheet2.write('A%s' %(i+6), i+1, body)
		for iRow8, bbbba in enumerate(bohircar):
			tze2= TZE.objects.get(id= bbbba.tze_id)
			worksheet2.write(iRow8 + 5,1, tze2.org_name,  body)
			worksheet2.write(iRow8 + 5,2, str(bbbba.mark)+' '+str(bbbba.no), body)
			worksheet2.write(iRow8 + 5,3, bbbba.huchin_chadal, body)
			worksheet2.write(iRow8 + 5,4, bbbba.gereet_too, body)
			worksheet2.write(iRow8 + 5,5, bbbba.duudlaga_too, body)
			worksheet2.write(iRow8 + 5,6, bbbba.us, body)
			worksheet2.write(iRow8 + 5,7, bbbba.niiluuleh_tseg, body)

	workbook.close()
	xlsx_data = output.getvalue()
	return xlsx_data

def TonogHorvuuleh(request):
	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=NiitTonogTohooromj.xlsx'
	xlsx_data = TonogHorvuulehToExcel()
	response.write(xlsx_data)
	return response

def TonogHorvuulehToExcel():
	output = StringIO.StringIO()
	workbook = xlsxwriter.Workbook(output)
	worksheet1 = workbook.add_worksheet(u'Хүснэгт№1')
	worksheet1.set_column('A:L', 14)
	worksheet1.set_column(1,1, 20)
	title = workbook.add_format({
    	'bold': True,
    	'font_size': 14,
    	'align': 'center',
    	'valign': 'vcenter'
    	})
	title.set_text_wrap()
	header = workbook.add_format({
    	'bg_color': '#F7F7F7',
    	'color': 'black',
    	'align': 'center',
    	'valign': 'top',
    	'border': 1
    	})
    
	header.set_text_wrap()

	body = workbook.add_format({
		'border' : 1,
		'color': 'black',
    	'align': 'left',
    	'valign': 'middle'
		})
	body.set_text_wrap()
	equipment= Equipment.objects.filter(status= True)
#   Хүснэгт 11
	title_text10 = u"Машин механизм, тоног төхөөрөмж, ажлын багаж хэрэгслийн жагсаалт"
	worksheet1.merge_range('A2:F2', title_text10, title)
	worksheet1.write('F3', u'Хүснэгт№1', header)
	worksheet1.merge_range('A4:A5', u'№', header)
	worksheet1.merge_range('B4:B5', u'Тусгай зөвшөөрөл эзэмшигч байгууллага', header)
	worksheet1.merge_range('C4:C5', u'Машин механизм, тоног төхөөрөмжийн нэр', header)
	worksheet1.merge_range('D4:D5', u'Машин механизм, тоног төхөөрөмжийн төрөл', header)
	worksheet1.merge_range('E4:E5', u'Тоо ширхэг', header)
	worksheet1.merge_range('F4:F5', u'Хүчин чадал', header)
	worksheet1.merge_range('G4:G5', u'Элэгдэлтийн чанар', header)
	worksheet1.merge_range('H4:H5', u'Ашиглалтанд орсон он', header)
	worksheet1.merge_range('I4:I5', u'Балансын үнэ', header)
	worksheet1.merge_range('J4:J5', u'Хуримтлагдсан элэгдэл', header)
	worksheet1.merge_range('K4:K5', u'Элэгдлийн хувь нэмэр', header)
	worksheet1.merge_range('L4:L5', u'Эх үүсвэр', header)
	if equipment:
		for i in range(len(equipment)):
			worksheet1.write('A%s' %(i+6), i+1, body)
		for iRow7, bbbb in enumerate(equipment):
			tze1= TZE.objects.get(id= bbbb.tze_id)
			worksheet1.write(iRow7 + 5,1, tze1.org_name,  body)
			worksheet1.write(iRow7 + 5,2, bbbb.name ,  body)
			worksheet1.write(iRow7 + 5,3, bbbb.torol_id, body)
			worksheet1.write(iRow7 + 5,4, bbbb.too, body)
			worksheet1.write(iRow7 + 5,5, bbbb.huchin_chadal, body)
			worksheet1.write(iRow7 + 5,6, bbbb.elegdliin_chanar, body)
			worksheet1.write(iRow7 + 5,7, bbbb.ashiglaltand_orson_ognoo, body)
			worksheet1.write(iRow7 + 5,8, bbbb.balans_une, body)
			worksheet1.write(iRow7 + 5,9, bbbb.hurimtlagdsan_elegdel, body)
			worksheet1.write(iRow7 + 5,10, bbbb.elegdel_huvi, body)
			worksheet1.write(iRow7 + 5,11, bbbb.eh_uusver, body)


	workbook.close()
	xlsx_data = output.getvalue()
	return xlsx_data

def AjiltanHorvuuleh(request):
	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Ajiltan.xlsx'
	xlsx_data = AjiltanHorvuulehToExcel()
	response.write(xlsx_data)
	return response

def AjiltanHorvuulehToExcel():
	output = StringIO.StringIO()
	workbook = xlsxwriter.Workbook(output)
	worksheet1 = workbook.add_worksheet(u'Хүснэгт№1')
	worksheet1.set_column('B:K', 14)
	title = workbook.add_format({
    	'bold': True,
    	'font_size': 14,
    	'align': 'center',
    	'valign': 'vcenter'
    	})
	title.set_text_wrap()
	header = workbook.add_format({
    	'bg_color': '#F7F7F7',
    	'color': 'black',
    	'align': 'center',
    	'valign': 'top',
    	'border': 1
    	})
    
	header.set_text_wrap()

	body = workbook.add_format({
		'border' : 1,
		'color': 'black',
    	'align': 'left',
    	'valign': 'middle'
		})
	body.set_text_wrap()
	ezem= TZE.objects.filter(status= True)
	for ezem in ezem:
		ajiltan= Ajiltan.objects.filter(baiguullaga= ezem.id, status= True)
		diplom= School.objects.filter(emp= ajiltan)
		mergejil= Job.objects.filter(emp=ajiltan)
		certificate= EngineeringCertificate.objects.filter(emp=ajiltan)
	#   Хүснэгт 11
		
		title_text12 = u"Хүний нөөцийн судалгаа"
		worksheet1.merge_range('B2:I2', title_text12, title)
		worksheet1.write('K3', u'Хүснэгт№12', header)
		worksheet1.merge_range('A4:A5', u'№', header)
		worksheet1.merge_range('B4:B5', u'Тусгай зөвшөөрөл эзэмшигч', header)
		worksheet1.merge_range('C4:C5', u'Овог', header)
		worksheet1.merge_range('D4:D5', u'Нэр', header)
		worksheet1.merge_range('E4:E5', u'Нас', header)
		worksheet1.merge_range('F4:F5', u'Хүйс', header)
		worksheet1.merge_range('G4:G5', u'Регистрийн дугаар', header)
		worksheet1.merge_range('H4:H5', u'Албан тушаал', header)
		worksheet1.merge_range('I4:I5', u'Мэргэжил', header)
		worksheet1.merge_range('J4:J5', u'Төгссөн сургууль', header)
		worksheet1.merge_range('K4:K5', u'Диплом, мэргэжлийн үнэмлэхний дугаар', header)
		turshilt =  u''
		turshilt1 = u''
		turshilt2 = u''
		
		if ajiltan:
			for i in range(len(ajiltan)):
				worksheet1.write('A%s' %(i+6), i+1, body)
			for iRow9, bbbbab in enumerate(ajiltan):
				tze1= TZE.objects.get(id= bbbbab.baiguullaga_id)
				worksheet1.write(iRow9 + 5,1, tze1.org_name,  body)
				worksheet1.write(iRow9 + 5,2, bbbbab.emp_lname ,  body)
				worksheet1.write(iRow9 + 5,3, bbbbab.emp_name, body)
				worksheet1.write(iRow9 + 5,4, bbbbab.nas, body)
				worksheet1.write(iRow9 + 5,5, bbbbab.gender, body)
				worksheet1.write(iRow9 + 5,6, bbbbab.emp_reg, body)
				positionn= AlbanTushaal.objects.get(id= bbbbab.position_id_id)
				pos= AlbanTushaalList.objects.get(id= positionn.position_name_id)
				worksheet1.write(iRow9 + 5,7, pos.name, body)
				worksheet1.write(iRow9 + 5,8, '', body)
				worksheet1.write(iRow9 + 5,9,'', body)
				worksheet1.write(iRow9 + 5,10,'', body)
				for cert in EngineeringCertificate.objects.filter(emp= bbbbab):
					turshilt2 = turshilt2 +'\n '+ str(cert.certificate_num)
				for school in School.objects.filter(emp= bbbbab):
					turshilt1 = turshilt1 +'\n '+ str(school.diplom_num)
					ih_surguuli= University.objects.filter(id= school.school_name_id)
					for ih in ih_surguuli:
						turshilt = turshilt +'\n ' +ih.university
				
	worksheet1.write(iRow9 + 5,8, turshilt, body)
	worksheet1.write(iRow9 + 5,9, turshilt1, body)
	worksheet1.write(iRow9 + 5,10, turshilt2, body)	
	workbook.close()
	xlsx_data = output.getvalue()
	return xlsx_data



def GshuTailanHorvuuleh(request):
	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=G_SH_U_tailan.xlsx'
	xlsx_data = GshuTailanHorvuulehToExcel()
	response.write(xlsx_data)
	return response

def GshuTailanHorvuulehToExcel():
	output = StringIO.StringIO()
	workbook = xlsxwriter.Workbook(output)
	worksheet1 = workbook.add_worksheet(u'ТЗА-д хамааралтай')
	worksheet2 = workbook.add_worksheet(u'ҮТА-нд хамааралтай')
	worksheet1.set_column('B:L', 24)
	worksheet2.set_column('B:L', 24)
	title = workbook.add_format({
    	'bold': True,
    	'font_size': 14,
    	'align': 'center',
    	'valign': 'vcenter'
    	})
	title.set_text_wrap()
	header = workbook.add_format({
    	'bg_color': '#F7F7F7',
    	'color': 'black',
    	'align': 'center',
    	'valign': 'top',
    	'border': 1
    	})
    
	header.set_text_wrap()

	body = workbook.add_format({
		'border' : 1,
		'color': 'black',
    	'align': 'left',
    	'valign':'top'
		})
	body.set_text_wrap()


	title_text10 = u"1.Үйлчилгээний хүртээмж"
	worksheet1.merge_range('A4:F4', title_text10, title)
	worksheet1.write('A5', u'№', header)
	worksheet1.merge_range('B5:C5', u'Гүйцэтгэлийн үзүүлэлт', header)
	worksheet1.merge_range('D5:E5', u'Тодорхойлолт', header)
	worksheet1.merge_range('F5:G5', u'Тооцох аргачлал', header)
	worksheet1.write('H5', u'Хугацаа', header)
	worksheet1.merge_range('A6:A10', u'1', body)
	worksheet1.merge_range('B6:C10', u'Баталгаат ундны усаар хангагдсан хүн амын эзлэх хувь(ТЗЭ-ийн үйлчилгээнд хамрагдсан хүн амын эзлэх хувь)', body)
	worksheet1.merge_range('D6:E10', u'Тухайн орон нутгийн хүн амын хэдэн хувь ТЗЭ байгууллагаар үйлчлүүлдэг, өөрөөр хэлбэл баталгаат ундны усаар хангагдаж байгааг илэрхийлнэ.', body)
	worksheet1.merge_range('F6:G10', u'PPasdws - Баталгаат ундны усаар хангагдсан хүн амын эзлэх хувь, % \n Pasdws - Тухайн орон нутагт ТЗЭ-ээр үйлчлүүлж буй хүн амын тоо, жилийн эцсээр \n Nmean - Тухайн орон нутгийн хүн амын тоо, жилийн эцсээр \n PPasdws = Pasdws/Nmean x 100%  ', body)
	worksheet1.merge_range('H6:H10', u'Хугацаа', body)

	title_text11 = u"2.Цэвэр ус олборлолт"
	worksheet1.merge_range('A12:F12', title_text11, title)
	worksheet1.write('A13', u'№', header)
	worksheet1.merge_range('B13:C13', u'Гүйцэтгэлийн үзүүлэлт', header)
	worksheet1.merge_range('D13:E13', u'Зорилго', header)
	worksheet1.merge_range('F13:G13', u'Тооцох аргачлал', header)
	worksheet1.write('H13', u'Хугацаа', header)
	worksheet1.merge_range('A14:A18', u'2', body)
	worksheet1.merge_range('B14:C18', u'Олборлосон ус, тогтоосон нөөцийн харьцаа', body)
	worksheet1.merge_range('D14:E18', u'Газрын доорх усны нөөцийг зохистойгоор ашиглах', body)
	worksheet1.merge_range('F14:G18', u'P - Олборлосон усны хэмжээг нөөцөд харьцуулсан харьцаа хувиар, % \n Q - Олборлосон усны хэмжээ, м3/хоног \n Qr - Тогтоогдсон нөөц, м3/хоног \n P= Q/Qr x 100%', body)
	worksheet1.merge_range('H14:H18', u'Хугацаа', body)
	worksheet1.merge_range('A19:A23', u'3', body)
	worksheet1.merge_range('B19:C23', u'1м3 ус олборлоход зарцуулсан цахилгаан эрчим хүч', body)
	worksheet1.merge_range('D19:E23', u'Цахилгааны зардлын бодит хэмжээг тодорхойлж, 1м3 ус олборлоход зарцуулж буй цахилгаан эрчим хүчийг бууруулах', body)
	worksheet1.merge_range('F19:G23', u'Ep - 1м3 ус олборлоход зарцуулсан цахилгаан эрчим хүч, кВт.ц, % \n Q - Олборлосон усны хэмжээ, м3 \n Ec - Нийт зарцуулсан эрчим хүч, кВт.ц \n Ep= Ec/Q', body)
	worksheet1.merge_range('H19:H23', u'Хугацаа', body)
	worksheet1.merge_range('A24:A28', u'4', body)
	worksheet1.merge_range('B24:C28', u'Ундны усны чанар', body)
	worksheet1.merge_range('D24:E28', u'Хэрэглэгчдийг стандартад нийцсэн усаар хангахад хяналт тавих', body)
	worksheet1.merge_range('F24:G28', u'Na - Авсан шинжилгээний тоо \n Nb - Стандартад нийцээгүй дүнгийн тоо \n Ko - Стандартын шаардлага хангаагүй тохиолдлын эзлэх хувь, % \n Ko = Nb/Na x100%', body)
	worksheet1.merge_range('H24:H28', u'Хугацаа', body)

	title_text13 = u"3.Цэвэр ус түгээлт"
	worksheet1.merge_range('A31:F31', title_text13, title)
	worksheet1.write('A32', u'№', header)
	worksheet1.merge_range('B32:C32', u'Гүйцэтгэлийн үзүүлэлт', header)
	worksheet1.merge_range('D32:E32', u'Зорилго', header)
	worksheet1.merge_range('F32:G32', u'Тооцох аргачлал', header)
	worksheet1.write('H32', u'Хугацаа', header)
	worksheet1.merge_range('A33:A37', u'5', body)
	worksheet1.merge_range('B33:C37', u'Орлого болоогүй ус', body)
	worksheet1.merge_range('D33:E37', u'Усны алдагдлыг бууруулах', body)
	worksheet1.merge_range('F33:G37', u'Qn - Нийлүүлсэн усны хэмжээ, мян шоо метр \n Qs - Нийт борлуулсан усны хэмжээ, мян шоо метр/өөрийн хэрэглээний ус багтана./ \n X - Нийлүүлсэн борлуулсан усны харьцаа, хувиар \n X= (Qn-Qx)/Qn x 100%', body)
	worksheet1.merge_range('H33:H37', u'Хугацаа', body)
	worksheet1.merge_range('A38:A42', u'6', body)
	worksheet1.merge_range('B38:C42', u'Тоолууржилтын түвшин', body)
	worksheet1.merge_range('D38:E42', u'Усны бодит хэрэглээг хэрэглэгчдийн төрлөөр гаргах, үнэ тарифын системийг боловсронгуй болгох', body)
	worksheet1.merge_range('F38:G42', u'Qm - Тоолууртай хэрэглэгчдийн тоо  \n Qs - Нийт хэрэглэгчдийн тоо \n Qt - Тогтоогдсон нөөц, м3/хоног \n P= Q/Qr x 100%', body)
	worksheet1.merge_range('H38:H42', u'Хугацаа', body)
	worksheet1.merge_range('A43:A47', u'7', body)
	worksheet1.merge_range('B43:C47', u'Цэвэр усны шугамын нэгж уртад ногдох гэмтлийн тоо', body)
	worksheet1.merge_range('D43:E47', u'Шугамын засвөр үйлчилгээг чанартай хийх, цэвэр усаар тасралтгүй хангах', body)
	worksheet1.merge_range('F43:G47', u'Dn - Шугамын нэгж уртад ногдох гэмтлийн тоо \n Nn  - Нийт гэмтлийн тоо \n Ln - Нийт шугамын урт, км \n Dbn= Nn/Ln', body)
	worksheet1.merge_range('H43:H47', u'Хугацаа', body)
	

	title_text14 = u"4.Цэвэрлэх байгууламж"
	worksheet1.merge_range('A51:F51', title_text14, title)
	worksheet1.write('A52', u'№', header)
	worksheet1.merge_range('B52:C52', u'Гүйцэтгэлийн үзүүлэлт', header)
	worksheet1.merge_range('D52:E52', u'Зорилго', header)
	worksheet1.merge_range('F52:G52', u'Тооцох аргачлал', header)
	worksheet1.write('H52', u'Хугацаа', header)
	worksheet1.merge_range('A53:A60', u'8', body)
	worksheet1.merge_range('B53:C60', u'Бохир усны цэвэрлэгээний түвшин', body)
	worksheet1.merge_range('D53:E60', u'Байгаль орчныг бохирдуулахгүй байх', body)
	worksheet1.merge_range('F53:G60', u'BOD5input - Цэвэрлэх байгууламж руу орох усны биологийн хэрэгцээт хүчилтөрөгч 5 хоног, мг\л \n BOD5output - Цэвэрлэх байгууламжаас гарч буй биологийн хэрэгцээт хүчилтөрөгч 5 хоног  \n BOD5= (BOD5input-BOD5output)/BOD5input x 100% \n ' +
	u'Химийн хэрэгцээт хүчилтөрөгч: \n CODinput -  Цэвэрлэх байгууламж руу орж буй бохир усны химийн хэрэгцээт хүчилтөрөгч, мг\л \n  CODoutput - Цэвэрлэх байгууламжаас гарч буй усны химийн хэрэгцээт хүчилтөрөгч  \n СOD= (CODinput-CODoutput)/CODinput x 100% ' +
	u'SSinput -  Цэвэрлэх байгууламж руу орж буй бохир усан дах умбуур бодисын агууламж, мг\л \n  SSoutput - Цэвэрлэх байгууламжаас гарч буй усан дах умбуур бодисын агууламж  \n SS= (SSinput-SSoutput)/SSinput x 100% ', body)
	worksheet1.merge_range('H53:H60', u'Хугацаа', body)

	title_text15 = u"5.Боловсон хүчний үзүүлэлт"
	worksheet1.merge_range('A64:F64', title_text15, title)
	worksheet1.write('A65', u'№', header)
	worksheet1.merge_range('B65:C65', u'Гүйцэтгэлийн үзүүлэлт', header)
	worksheet1.merge_range('D65:E65', u'Зорилго', header)
	worksheet1.merge_range('F65:G65', u'Тооцох аргачлал', header)
	worksheet1.write('H65', u'Хугацаа', header)
	worksheet1.merge_range('A66:A70', u'9', body)
	worksheet1.merge_range('B66:C70', u'Боловсон хүчний бүрдэлт', body)
	worksheet1.merge_range('D66:E70', u'Ажилллагсдын боловсролын түвшинг дээшлүүлэх, байгууллагын хүнийн нөөцийн бодлогыг удирдах', body)
	worksheet1.merge_range('F66:G70', u'K - Боловсон хүчний бүрдэлтийн хувь \n Ne - Боловсролтой ажилтны тоо  \n Nt = Нийт ажилтны тоо \n K= Ne/Nt x 100%', body)
	worksheet1.merge_range('H66:H70', u'Хугацаа', body)
	worksheet1.merge_range('A71:A75', u'10', body)
	worksheet1.merge_range('B71:C75', u'1000 хэрэглэгчдэд ногдох ажиллагсдын тоо', body)
	worksheet1.merge_range('D71:E75', u'Хэрэглэгдэд хүргэх үйлчилгээг сайжруулах', body)
	worksheet1.merge_range('F71:G75', u'Ne - Нийт ажилтны тоо \n С - Нийт хэрэглэгчдийн тоо  \n Сt = 1000 хэрэглэгч тутамд ногдох ажиллагсдын тоо \n Ct = Ne/C x 1000', body)
	worksheet1.merge_range('H71:H75', u'Хугацаа', body)


	title_text21 = u"6.Санхүүгийн үзүүлэлт"
	worksheet2.merge_range('A4:F4', title_text21, title)
	worksheet2.write('A5', u'№', header)
	worksheet2.merge_range('B5:C5', u'Гүйцэтгэлийн үзүүлэлт', header)
	worksheet2.merge_range('D5:E5', u'Зорилго', header)
	worksheet2.merge_range('F5:G5', u'Тооцох аргачлал', header)
	worksheet2.write('H5', u'Хугацаа', header)
	worksheet2.merge_range('A6:A10', u'11', body)
	worksheet2.merge_range('B6:C10', u'Борлуулалтын орлогын шаардагдах хэмжээ - БОш', body)
	worksheet2.merge_range('D6:E10', u'Батлагдсан БОш-н хэрэгжилтийг хянах,\n Коэффициент БОш- 1-ээс бага үзүүлэлттэй байх', body)
	worksheet2.merge_range('F6:G10', u'КБОш - Коэффициент БОш \n БОш-гүйц - Гүйцэтгэлээр гарсан нийт зардал, мян.төг \n БОш-батлагдсан - Тогтоолоор гаргасан БОш, мян.төг \n КБОш = БОш-гүйц/БОш-батлагдсан ', body)
	worksheet2.merge_range('H6:H10', u'Хугацаа', body)
	worksheet2.merge_range('A11:A15', u'12', body)
	worksheet2.merge_range('B11:C15', u'Орлогын нэг төгрөгт ногдох зардал', body)
	worksheet2.merge_range('D11:E15', u'Орлогын нэг төгрөг тутамд зарцуулж буй зардлыг харуулна. Уг үзүүлэлт буурснаар байгууллагын эдийн засгийн үр ашиг дээшилнэ.', body)
	worksheet2.merge_range('F11:G15', u'Зонтн - Орлогын нэг төгрөгт ногдох зардал \n О - Нийт орлого, мян.төг \n З - Нийт зардал, мян.төг \n Зонтн = З/О ', body)
	worksheet2.merge_range('H11:H15', u'Хугацаа', body)
	worksheet2.merge_range('A16:A20', u'13', body)
	worksheet2.merge_range('B16:C20', u'Борлуулсан 1 м3 усанд ногдох үйл ажиллагааны зардал', body)
	worksheet2.merge_range('D16:E20', u'1м3 усанд ногдох үйл ажиллагааны зардлыг хянах, бууруулах \n  - 1м3 цэвэр усны \n  - 1м3 бохир усны ', body)
	worksheet2.merge_range('F16:G20', u'ЗЦУм3 - 1м3 цэвэр усанд ногдох үйл ажиллагааны зардал, төг \n ЦQs - Нийт борлуулсан цэвэр усны хэмжээ, мян.м3 \n ЗЦУ - Цэвэр усны үйл ажиллагааны нийт зардал, мян.төг \n ЗЦУм3 = ЗЦУ/ЦQs \n ЗБУм3 - 1м3 бохир усанд ногдох үйл ажиллагааны зардал, төг \n БQs - Нийт бохир усны хэмжээ, мян.м3 \n ЗБУ - Бохир усны үйл ажиллагааны нийт зардал, мян.төг \n ЗБУм3 = ЗБУ/БQs ', body)
	worksheet2.merge_range('H16:H20', u'Хугацаа', body)
	worksheet2.merge_range('A21:A25', u'14', body)
	worksheet2.merge_range('B21:C25', u'Авлага цуглуулалт', body)
	worksheet2.merge_range('D21:E25', u'Борлуулалтын орлогын бэлэн мөнгөний эргэлтийг нэмэгдүүлж, авлагыг бууруулах', body)
	worksheet2.merge_range('F21:G25', u'Ав - Авлагын харьцаа, хувиар \n М - Бэлэн мөнгөний орлого, мян.төг \n В - Борлуулалтын нийт орлого, мян.төг \n Ав = М/В х 100%  ', body)
	worksheet2.merge_range('H21:H25', u'Хугацаа', body)

	workbook.close()
	xlsx_data = output.getvalue()
	return xlsx_data



def UaTailanHorvuuleh(request, pk=0):
	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=UATailan.xlsx'
	xlsx_data = UaTailanHorvuulehToExcel(tze_id=pk)
	response.write(xlsx_data)
	return response

def UaTailanHorvuulehToExcel(tze_id):
	output = StringIO.StringIO()
	workbook = xlsxwriter.Workbook(output)
	worksheet1 = workbook.add_worksheet(u'Хүснэгт№1')
	worksheet2 = workbook.add_worksheet(u'Хүснэгт№2')
	worksheet3 = workbook.add_worksheet(u'Хүснэгт№3')
	worksheet4 = workbook.add_worksheet(u'Хүснэгт№4')
	worksheet5 = workbook.add_worksheet(u'Хүснэгт№5')
	worksheet6 = workbook.add_worksheet(u'Хүснэгт№6')
	worksheet7 = workbook.add_worksheet(u'Хүснэгт№7')
	worksheet8 = workbook.add_worksheet(u'Хүснэгт№8')
	worksheet9 = workbook.add_worksheet(u'Хүснэгт№9')
	worksheet10 = workbook.add_worksheet(u'Хүснэгт№10')
	worksheet11 = workbook.add_worksheet(u'Хүснэгт№11')
	worksheet12 = workbook.add_worksheet(u'Хүснэгт№12')
	worksheet13 = workbook.add_worksheet(u'Хүснэгт№13')
	worksheet14 = workbook.add_worksheet(u'Хүснэгт№14')

	worksheet1.set_column('C:J', 14)
	worksheet2.set_column('C:J', 14)
	worksheet3.set_column('C:J', 14)
	worksheet4.set_column('C:K', 14)
	worksheet5.set_column('C:J', 14)
	worksheet6.set_column('C:K', 14)
	worksheet7.set_column('C:J', 14)
	worksheet8.set_column('C:J', 14)
	worksheet9.set_column('C:J', 14)
	worksheet10.set_column('C:J', 14)
	worksheet11.set_column('C:J', 14)
	worksheet12.set_column('C:J', 14)
	worksheet13.set_column('C:J', 14)
	worksheet14.set_column('C:J', 14)

	title = workbook.add_format({
    	'bold': True,
    	'font_size': 14,
    	'align': 'center',
    	'valign': 'vcenter'
    	})
	title.set_text_wrap()
	header = workbook.add_format({
    	'bg_color': '#F7F7F7',
    	'color': 'black',
    	'align': 'center',
    	'valign': 'top',
    	'border': 1
    	})
    
	header.set_text_wrap()

	body = workbook.add_format({
		'border' : 1,
		'color': 'black',
    	'align': 'left',
    	'valign': 'middle'
   		})
	body.set_text_wrap()
	body_body = workbook.add_format({
		'border' : 1,
		'color': 'black',
    	'align': 'left',
    	'bold' : True
		})
	ner= Baiguullaga.objects.get(id= tze_id)
	hudag = Hudag.objects.filter(status=True)
 	#   Хүснэгт 11
 	worksheet1.merge_range('B1:J1', ner.org_name, title)
	title_text1 = u"Ус хангамжийн эх үүсвэрийн барилга байгууламжийн судалгаа"
	worksheet1.merge_range('B2:J2', title_text1, title)
	worksheet1.write('B4', u'№', header)
	worksheet1.merge_range('C4:D4', u'Барилга байгууламж', header)
	worksheet1.write('E4', u'Хүчин чадал(м3/хон)', header)
	worksheet1.write('F4', u'Олборлож буй ус(м3/хон)', header)
	worksheet1.write('G4', u'Ашиглалтанд орсон огноо', header)
	worksheet1.write('H4', u'/Тайлбар ажиллаж байгаа эсэх/', header)
	worksheet1.write('I3', u'Хүснэгт№1', header)
	worksheet1.write('I4', u'Эх үүсвэрийн харуул, хамгаалалтын тухай', header)
	if hudag:
		for a in range(len(hudag)):
			worksheet1.write('B%s' %(a+5), a+1, body)
		for iRow, ba in enumerate(hudag):
			worksheet1.write(iRow + 4,3, u'№'+' '+str(ba.id), body)
			worksheet1.write(iRow + 4,4, ba.huchin_chadal, body)
			worksheet1.write(iRow + 4,5, ba.olborloj_bui_us, body)
			worksheet1.write(iRow + 4,6, ba.ashiglaltand_orson_ognoo.strftime('%d/%m/%Y'), body)
			worksheet1.write(iRow + 4,7, ba.tailbar, body)
			worksheet1.write(iRow + 4,8, ba.haruul, body)
		if len(hudag) == 1:
			worksheet1.merge_range(4,2, len(hudag)+ 3,2,  u'Гүний худаг', body)
		if len(hudag) > 1:
			worksheet1.merge_range(4,2, len(hudag)+ 3,2,  u'Гүний худаг', body)
	



	usansan = UsanSan.objects.filter(status=True)
	nasos = NasosStants.objects.filter(status=True)
	lab = Lab.objects.filter(status=True)
#   Хүснэгт 11	
	worksheet2.merge_range('B1:H1', ner.org_name, title)
	title_text2 = u"Ус хангамжийн эх үүсвэрийн барилга байгууламжийн судалгаа"
	worksheet2.merge_range('B2:H2', title_text2, title)
	worksheet2.write('B4', u'№', header)
	worksheet2.merge_range('C4:D4', u'Барилга байгууламж', header)
	worksheet2.write('E4', u'Тоо хэмжээ', header)
	worksheet2.write('F4', u'Хүчин чадал', header)
	worksheet2.write('G4', u'Ашиглалтанд орсон огноо', header)
	worksheet2.write('H4', u'/Тайлбар ажиллаж байгаа эсэх/', header)
	worksheet2.write('H3', u'Хүснэгт№2', header)
	niit2 = 0
	niit_usansan = 0
	niit_nasos = 0
	if usansan and nasos and lab:
		niit2 = len(usansan)+ len(nasos)+ len(lab)
	if usansan:
		niit_usansan = len(usansan) + 4
	if nasos:	
		niit_nasos = len(nasos) + 4 + len(usansan)
	for i in range(niit2):
		worksheet2.write('B%s' %(i+5), i+1, body)
	for iRow2, bab in enumerate(usansan):
		worksheet2.merge_range(iRow2 + 4,2,iRow2 + 4,3, u'Усан сан', body)
		worksheet2.write(iRow2 + 4,4, '1', body)
		worksheet2.write(iRow2 + 4,5, bab.huchin_chadal, body)
		worksheet2.write(iRow2 + 4,6, bab.ashiglaltand_orson_ognoo.strftime('%d/%m/%Y'), body)
		worksheet2.write(iRow2 + 4,7, bab.tailbar, body)	
	for iRow3, baba in enumerate(nasos):
		worksheet2.merge_range(iRow3 + niit_usansan,2,iRow3 + niit_usansan,3, u'Насосны станц', body)
		worksheet2.write(iRow3 + niit_usansan,4, '1', body)
		worksheet2.write(iRow3 + niit_usansan,5, baba.huchin_chadal, body)
		worksheet2.write(iRow3 + niit_usansan,6, baba.ashiglaltand_orson_ognoo.strftime('%d/%m/%Y'), body)
		worksheet2.write(iRow3 + niit_usansan,7, baba.tailbar, body)
	for iRow4, babab in enumerate(lab):
		worksheet2.merge_range(iRow4 + niit_nasos,2,iRow4 + niit_nasos,3, u'Цэвэр усны лаборатори', body)
		worksheet2.write(iRow4 + niit_nasos,4, '1', body)
		worksheet2.write(iRow4 + niit_nasos,5, babab.huchin_chadal, body)
		worksheet2.write(iRow4 + niit_nasos,6, babab.ashiglaltand_orson_ognoo.strftime('%d/%m/%Y'), body)
		worksheet2.write(iRow4 + niit_nasos,7, babab.tailbar, body)
	

	standart1= AnalysisWaterStandart.objects.all().last()
	analysis_tsever = AnalysisWater.objects.filter(status=True).last()
#   Хүснэгт 11
	worksheet3.merge_range('B1:E1', ner.org_name, title)
	title_text3 = u"Цэвэр усны шинжилгээний дүн/жилийн дундаж үзүүлэлт/"
	worksheet3.merge_range('B2:E2', title_text3, title)
	worksheet3.write('B4', u'№', header)

	for i in range(11):
		worksheet3.write('B%s' %(i+5), i+1, body)


	worksheet3.write('C4', u'Үзүүлэлт', header)
	worksheet3.write('D4', u'Стандарт үзүүлэлт', header)
	worksheet3.write('E4', u'Шинжилгээний дүн', header)
	worksheet3.write('E3', u'Хүснэгт№3', header)
	worksheet3.write('C5', u'Ерөнхий хатуулаг', body)
	worksheet3.write('C6', u'Магни', body)
	worksheet3.write('C7', u'Кальци', body)
	worksheet3.write('C8', u'Хлорид', body)
	worksheet3.write('C9', u'Сульфат', body)
	worksheet3.write('C10', u'pH', body)
	worksheet3.write('C11', u'Аммиак', body)
	worksheet3.write('C12', u'Нитрит', body)
	worksheet3.write('C13', u'Амт', body)
	worksheet3.write('C14', u'Үнэр', body)
	worksheet3.write('C15', u'Нийт нянгийн тоо', body)
	worksheet3.write('D5', standart1.hatuulag, body)
	worksheet3.write('D6', standart1.magni, body)
	worksheet3.write('D7', standart1.kalitsi, body)
	worksheet3.write('D8', standart1.hlorid, body)
	worksheet3.write('D9', standart1.sulifat, body)
	worksheet3.write('D10', standart1.ph, body)
	worksheet3.write('D11', standart1.ammiak , body)
	worksheet3.write('D12', standart1.nitrit, body)
	worksheet3.write('D13', standart1.amt, body)
	worksheet3.write('D14', standart1.uner, body)
	worksheet3.write('D15', standart1.nyan, body)
 	if analysis_tsever:
		worksheet3.write('E5', analysis_tsever.hatuulag, body)
		worksheet3.write('E6', analysis_tsever.magni, body)
		worksheet3.write('E7', analysis_tsever.kalitsi, body)
		worksheet3.write('E8', analysis_tsever.hlorid, body)
		worksheet3.write('E9', analysis_tsever.sulifat, body)
		worksheet3.write('E10', analysis_tsever.ph, body)
		worksheet3.write('E11', analysis_tsever.ammiak , body)
		worksheet3.write('E12', analysis_tsever.nitrit, body)
		worksheet3.write('E13', analysis_tsever.amt, body)
		worksheet3.write('E14', analysis_tsever.uner, body)
		worksheet3.write('E15', analysis_tsever.nyan, body)
	else:
		worksheet3.write('E5', '', body)
		worksheet3.write('E6', '', body)
		worksheet3.write('E7', '', body)
		worksheet3.write('E8', '', body)
		worksheet3.write('E9', '', body)
		worksheet3.write('E10','', body)
		worksheet3.write('E11', '' , body)
		worksheet3.write('E12', '', body)
		worksheet3.write('E13', '', body)
		worksheet3.write('E14', '', body)
		worksheet3.write('E15', '', body)	

	tseversuljee = Sh_suljee.objects.filter(tze= tze_id, shugam_torol__in=[u'Эх үүсвэрийн цуглуулах',u'Цэвэр усны дамжуулах шугам',u'Цэвэр ус түгээх шугам'],status=True)
	suljee= Sh_suljeeTable.objects.filter(suljee_id= tseversuljee).last()
	
#   Хүснэгт 11
	worksheet4.merge_range('B1:K1', ner.org_name, title)
	title_text4 = u"Цэвэр усны шугам сүлжээний судалгаа "
	worksheet4.merge_range('B2:K2', title_text4, title)
	worksheet4.merge_range('B4:B5', u'№', header)
	worksheet4.write('K3', u'Хүснэгт№4', header)
	worksheet4.merge_range('C4:C5', u'Шугам сүлжээ', header)
	worksheet4.merge_range('D4:D5', u'Шугамын урт/метрээр илэрхийлнэ./', header)	
	worksheet4.merge_range('E4:G4', u'Шугамын материал/метрээр илэрхийлнэ./', header)
	worksheet4.write('E5', u'Ширэм', header)
	worksheet4.write('F5', u'Хуванцар', header)
	worksheet4.write('G5', u'Цайрдсан ган', header)
	worksheet4.merge_range('H4:H5', u'Шугамын диаметр', header)
	worksheet4.merge_range('I4:I5', u'Шугам дээрх хяналтын худгийн тоо', header)
	worksheet4.merge_range('J4:J5', u'Жилд гарсан гэмтлийн тоо', header)
	worksheet4.merge_range('K4:K5', u'Ашиглалтанд орсон огноо', header)
	if tseversuljee:
		for i in range(len(tseversuljee)):
			worksheet4.write('B%s' %(i+6), i+1, body)
			worksheet4.write(i + 5,4, suljee.shirem, body)
			worksheet4.write(i + 5,5, suljee.huvantsar, body)
			worksheet4.write(i + 5,6, suljee.gan, body)

		for iRow5, bba in enumerate(tseversuljee):
			worksheet4.write(iRow5 + 5,2, bba.shugam_torol, body)
			worksheet4.write(iRow5 + 5,3, bba.shugam_urt, body)
			worksheet4.write(iRow5 + 5,7, bba.diametr, body)
			worksheet4.write(iRow5 + 5,8, bba.hudgiin_too, body)
			worksheet4.write(iRow5 + 5,9, bba.gemtliin_too, body)
			worksheet4.write(iRow5 + 5,10, bba.ashiglaltand_orson_ognoo.strftime('%d/%m/%Y'), body)



	abb= ABB.objects.filter(tze= tze_id, status= True)

#   Хүснэгт 11
	worksheet5.merge_range('B1:F1', ner.org_name, title)
	title_text5 = u"Ашиглалтыг нь хариуцаж буй барилга байгууламжийн судалгаа"
	worksheet5.merge_range('B2:F2', title_text5, title)
	worksheet5.merge_range('B4:B5', u'№', header)
	worksheet5.write('F3', u'Хүснэгт№6', header)
	worksheet5.merge_range('C4:C5', u'Барилга байгууламжийн нэр', header)
	worksheet5.merge_range('D4:D5', u'Нийт тоо хэмжээ', header)
	worksheet5.merge_range('E4:F4', u'Тоолууржилт', header)
	worksheet5.write('E5', u'Тоо хэмжээ', header)
	worksheet5.write('F5', u'%', header)
	worksheet5.write('C6', u'Орон сууцны айл өрх', body)
	worksheet5.write('C7', u'Үйлдвэр', body)
	worksheet5.write('C8', u'Аж ахуйн нэгж', body)
	worksheet5.write('C9', u'Ус дулаан дамжуулах төв', body)
	worksheet5.write('C10', u'Байрын узель', body)
	for i in range(5):
		worksheet5.write('B%s' %(i+6), i+1, body)
		worksheet5.write('D%s' %(i+6), '', body)
		worksheet5.write('E%s' %(i+6), '', body)
		worksheet5.write('F%s' %(i+6), '', body)
	




	bohirsuljee = Sh_suljee.objects.filter(tze= tze_id, shugam_torol__in=[u'Бохир усны гаргалгааны шугам',u'Бохир усны цуглуулах шугам',u'Бохир ус татан зайлуулах шугам'],status=True)
	husnegt2= Sh_suljeeTable.objects.filter(suljee_id= bohirsuljee).last()
#   Хүснэгт 11
	worksheet6.merge_range('B1:E1', ner.org_name, title)
	title_text6 = u"Бохир усны шугам сүлжээний судалгаа "
	worksheet6.merge_range('B2:E2', title_text6, title)
	worksheet6.merge_range('B4:B5', u'№', header)
	worksheet6.write('K3', u'Хүснэгт№6', header)
	worksheet6.merge_range('C4:C5', u'Шугам сүлжээ', header)
	worksheet6.merge_range('D4:D5', u'Шугамын урт/метрээр илэрхийлнэ./', header)
	worksheet6.merge_range('E4:G4', u'Шугамын материал/метрээр илэрхийлнэ./', header)
	worksheet6.write('E5', u'Ширэм', header)
	worksheet6.write('F5', u'Хуванцар', header)
	worksheet6.write('G5', u'Асбето-цемент', header)
	worksheet6.merge_range('H4:H5', u'Шугамын диаметр', header)
	worksheet6.merge_range('I4:I5', u'Шугам дээрх хяналтын худгийн тоо', header)
	worksheet6.merge_range('J4:J5', u'Жилд гарсан гэмтлийн тоо', header)
	worksheet6.merge_range('K4:K5', u'Ашиглалтанд орсон огноо', header)
	if bohirsuljee:
		for i in range(len(bohirsuljee)):
			worksheet6.write('B%s' %(i+6), i+1, body)
			worksheet6.write(i + 5,4, husnegt2.shirem, body)
			worksheet6.write(i + 5,5, husnegt2.huvantsar, body)
			worksheet6.write(i + 5,6, husnegt2.gan, body)
		for iRow61, bbb in enumerate(bohirsuljee):
			worksheet6.write(iRow61 + 5,2, bbb.shugam_torol, body)
			worksheet6.write(iRow61 + 5,3, bbb.shugam_urt, body)
			worksheet6.write(iRow61 + 5,7, bbb.diametr, body)
			worksheet6.write(iRow61 + 5,8, bbb.hudgiin_too, body)
			worksheet6.write(iRow61 + 5,9, bbb.gemtliin_too, body)
			worksheet6.write(iRow61 + 5,10, bbb.ashiglaltand_orson_ognoo.strftime('%d/%m/%Y'), body)




	tseverleh_baig= Ts_baiguulamj.objects.filter(tze= tze_id, status=True)
	tseverleh = Ts_tohooromj.objects.filter(ts_baiguulamj= tseverleh_baig)
#   Хүснэгт 11
	worksheet7.merge_range('B1:E1', ner.org_name, title)
	title_text7 = u"Цэвэрлэх байгууламжийн судалгаа"
	worksheet7.merge_range('B2:E2', title_text7, title)
	worksheet7.write('B4', u'№', header)
	worksheet7.write('I3', u'Хүснэгт№7', header)
	worksheet7.write('C4', u'Цэвэрлэгээний аргууд', header)
	worksheet7.write('D4', u'Барилга байгууламж, тоног төхөөрөмж', header)
	worksheet7.write('E4', u'Тоо хэмжээ', header)
	worksheet7.write('F4', u'Хүчин чадал(м3/хон)', header)
	worksheet7.write('G4', u'Хүлээн авч буй ус(м3/хон)', header)
	worksheet7.write('H4', u'Ашиглалтанд орсон огноо', header)
	worksheet7.write('I4', u'Тайлбар', header)
	if tseverleh:
		for i in range(len(tseverleh)):
			worksheet7.write('B%s' %(i+5), i+1, body)
			for tseverleh_baig in tseverleh_baig:
				if tseverleh_baig.mehanik == True and tseverleh_baig.biologi == True and tseverleh_baig.fizik == True:
					worksheet7.write(i + 4,2, u'Механик, Биологи, Физик-хими, хими', body)
				elif tseverleh_baig.mehanik == True and tseverleh_baig.biologi == False and tseverleh_baig.fizik == False:
					worksheet7.write(i + 4,2, u'Механик', body)
				elif tseverleh_baig.mehanik == True and tseverleh_baig.biologi == True and tseverleh_baig.fizik == False:
					worksheet7.write(i + 4,2, u'Механик, Физик-хими, хими', body)
				elif tseverleh_baig.mehanik == False and tseverleh_baig.biologi == False and tseverleh_baig.fizik == False:
					worksheet7.write(i + 4,2, '', body)
				elif tseverleh_baig.mehanik == False and tseverleh_baig.biologi == True and tseverleh_baig.fizik == False:
					worksheet7.write(i + 4,2, u'Биологи', body)
				elif tseverleh_baig.mehanik == False and tseverleh_baig.biologi == False and tseverleh_baig.fizik == True:
					worksheet7.write(i + 4,2, u'Физик-хими, хими', body)
				elif tseverleh_baig.mehanik == False and tseverleh_baig.biologi == True and tseverleh_baig.fizik == True:
					worksheet7.write(i + 4,2, u'Биологи, Физик-хими, хими', body)
		for iRow101, bbbhj in enumerate(tseverleh):
			worksheet7.write(iRow101 + 4,3, bbbhj.barilga_tonog, body)
			worksheet7.write(iRow101 + 4,4, bbbhj.too, body)
			worksheet7.write(iRow101 + 4,5, bbbhj.huchin_chadall, body)
			worksheet7.write(iRow101 + 4,6, '' , body)
			worksheet7.write(iRow101 + 4,7, bbbhj.ashiglaltand_orson_ognooo.strftime('%d/%m/%Y') , body)
			worksheet7.write(iRow101 + 4,8, bbbhj.tailbarr, body)




 	standart_bohir= AnalysisBohirStandart.objects.all().last()
	analysis_bohir = AnalysisBohir.objects.filter(tze= tze_id,status=True).last()
#   Хүснэгт 11
	worksheet8.merge_range('B1:E1', ner.org_name, title)
	title_text8 = u"Бохир усны шинжилгээний дүн"
	worksheet8.merge_range('B2:E2', title_text8, title)
	worksheet8.merge_range('D3:F3', u'/Сүүлийн шинжилгээний үзүүлэлтийг бичнэ./', body)
	
	worksheet8.merge_range('B4:B5', u'№', header)
	for i in range(3):
		worksheet8.write('B%s' %(i+6), i+1, body)
		worksheet8.write('D%s' %(i+6), '', body)
		worksheet8.write('E%s' %(i+6), '', body)
		worksheet8.write('F%s' %(i+6), '', body)
	worksheet8.merge_range('C4:C5', u'Үзүүлэлт', header)
	worksheet8.merge_range('D4:D5', u'Стандарт үзүүлэлт', header)
	worksheet8.merge_range('E4:F4', u'Огноо', header)
	worksheet8.write('E5', u'Цэвэрлэх байгууламж руу орох', header)
	worksheet8.write('F5', u'Цэвэрлэх байгууламжаас гарах', header)
	worksheet8.write('C6', u'Умбуур бодисын тоо мг/л', body)
	worksheet8.write('C7', u'БХХ мг/л О2', body)
	worksheet8.write('C8', u'ХХХ мг/л О2', body)
	worksheet8.write('D6', standart_bohir.umbuur, body)
	worksheet8.write('D7', standart_bohir.bhh, body)
	worksheet8.write('D8', standart_bohir.hhh, body)
	if analysis_bohir:
		worksheet8.write('C3', analysis_bohir.ognoo.strftime('%d/%m/%Y') , body)
		worksheet8.write('E6', analysis_bohir.umbuuro , body)
		worksheet8.write('E7', analysis_bohir.bhho, body)
		worksheet8.write('E8', analysis_bohir.hhho, body)
		worksheet8.write('F6', analysis_bohir.umbuurgarah, body)
		worksheet8.write('F7', analysis_bohir.bhhgarah, body)
		worksheet8.write('F8', analysis_bohir.hhhgarah, body)




	us12=UsTugeehBair.objects.filter(tze = tze_id,status=True)	
	us1=UsTugeehBair.objects.filter(tze = tze_id,status=True, barilga= u'Гүний эх үүсвэртэй ус түгээх байр')
	us2=UsTugeehBair.objects.filter(tze = tze_id,status=True, barilga= u'Зөөврийн эх үүсвэртэй ус түгээх байр')
	us3=UsTugeehBair.objects.filter(tze = tze_id,status=True, barilga= u'Төвлөрсөн шугамаас тэжээгддэг ус түгээх байр')
	hun_amiin_too=0
	borluulj_bui_us=0
	hun_amiin_too1=0
	borluulj_bui_us1=0
	hun_amiin_too2=0
	borluulj_bui_us2=0
	for us in us12:
		if us.barilga == u'Гүний эх үүсвэртэй ус түгээх байр':
			hun_amiin_too= hun_amiin_too+ us.hun_amiin_too
			borluulj_bui_us= borluulj_bui_us+ us.borluulj_bui_us
		elif us.barilga == u'Зөөврийн эх үүсвэртэй ус түгээх байр':
			hun_amiin_too1= hun_amiin_too1+ us.hun_amiin_too
			borluulj_bui_us1= borluulj_bui_us1+ us.borluulj_bui_us	
		elif us.barilga == u'Төвлөрсөн шугамаас тэжээгддэг ус түгээх байр':
			hun_amiin_too2= hun_amiin_too2+ us.hun_amiin_too
			borluulj_bui_us2= borluulj_bui_us2+ us.borluulj_bui_us
	hun_amiin_too_niit= hun_amiin_too+ hun_amiin_too1 + hun_amiin_too2
	borluulj_bui_us_niit= borluulj_bui_us+ borluulj_bui_us1+ borluulj_bui_us2
#   Хүснэгт 11
	worksheet9.merge_range('B1:E1', ner.org_name, title)
	title_text9 = u"Ус түгээх байрны судалгаа"
	worksheet9.merge_range('B2:E2', title_text9, title)
	worksheet9.write('F3', u'Хүснэгт№9', header)
	worksheet9.merge_range('B4:B5', u'№', header)
	worksheet9.merge_range('C4:C5', u'Барилга байгууламж', header)
	worksheet9.merge_range('D4:D5', u'ТЗЭ-ээр үйлчлүүлж буй хүн амын тоо', header)
	worksheet9.merge_range('E4:E5', u'Худгийн тоо', header)
	worksheet9.merge_range('F4:F5', u'Борлуулж буй ус(м3/хон)', header)
	worksheet9.write('C6', u'Гүний эх үүсвэртэй ус түгээх байр', body)
	worksheet9.write('C7', u'Зөөврийн эх үүсвэртэй ус түгээх байр', body)
	worksheet9.write('C8', u'Төвлөрсөн шугамаас тэжээгддэг ус түгээх байр', body)
	worksheet9.write('C9', u'Нийт', header)
	
	for i in range(4):
		worksheet9.write('B%s' %(i+6), i+1, body)
	worksheet9.write('D6', hun_amiin_too, body)
	worksheet9.write('D7', hun_amiin_too1, body)
	worksheet9.write('D8', hun_amiin_too2, body)
	worksheet9.write('D9', hun_amiin_too_niit , body)
	worksheet9.write('E6', len(us1), body)
	worksheet9.write('E7', len(us2), body)
	worksheet9.write('E8', len(us3), body)
	worksheet9.write('E9', len(us12), body)
	worksheet9.write('F6', borluulj_bui_us, body)
	worksheet9.write('F7', borluulj_bui_us1, body)
	worksheet9.write('F8', borluulj_bui_us2, body)
	worksheet9.write('F9', borluulj_bui_us_niit, body)


	watercar= WaterCar.objects.filter(tze= tze_id, status= True)
#   Хүснэгт 11
	worksheet10.merge_range('B1:H1', ner.org_name, title)
	title_text10 = u"Зөөврийн ус хангамжийн үйлчилгээ үзүүлдэг автомашины судалгаа"
	worksheet10.merge_range('B2:H2', title_text10, title)
	worksheet10.write('H3', u'Хүснэгт№10', header)
	worksheet10.merge_range('B4:B5', u'№', header)
	worksheet10.merge_range('C4:C5', u'Автомашины марк, улсын дугаар', header)
	worksheet10.merge_range('D4:D5', u'Хүчин чадал(тонн)', header)
	worksheet10.merge_range('E4:G4', u'Хэрэглэгчийн тоо', header)
	worksheet10.write('E5', u'ААНБ', header)
	worksheet10.write('F5', u'УТБ', header)
	worksheet10.write('G5', u'Хүн ам', header)
	worksheet10.merge_range('H4:H5', u'Борлуулсан усны хэмжээ(м3/хон)', header)
	if watercar:
		for i in range(len(watercar)):
			worksheet10.write('B%s' %(i+6), i+1, body)
		for iRow7, bbbb in enumerate(watercar):
			worksheet10.write(iRow7 + 5,2, str(bbbb.mark)+' '+str(bbbb.no) ,  body)
			worksheet10.write(iRow7 + 5,3, bbbb.huchin_chadal, body)
			worksheet10.write(iRow7 + 5,4, bbbb.aanb_too, body)
			worksheet10.write(iRow7 + 5,5, bbbb.utb_too, body)
			worksheet10.write(iRow7 + 5,6, bbbb.hun_am_too, body)
			worksheet10.write(iRow7 + 5,7, bbbb.us, body)




	bohircar= BohirCar.objects.filter(tze= tze_id,status= True)
#   Хүснэгт 11
	worksheet11.merge_range('B1:H1', ner.org_name, title)
	title_text11 = u"Бохир ус зөөвөрлөх үйлчилгээ үзүүлдэг автомашины судалгаа"
	worksheet11.merge_range('B2:H2', title_text11, title)
	worksheet11.write('H3', u'Хүснэгт№11', header)
	worksheet11.merge_range('B4:B5', u'№', header)
	worksheet11.merge_range('C4:C5', u'Автомашины марк, улсын дугаар', header)
	worksheet11.merge_range('D4:D5', u'Хүчин чадал(тонн)', header)
	worksheet11.merge_range('E4:F4', u'Хэрэглэгчийн тоо', header)
	worksheet11.write('E5', u'Гэрээт', header)
	worksheet11.write('F5', u'Дуудлагын', header)
	worksheet11.merge_range('G4:G5', u'Зөөвөрлөсөн усны хэмжээ(м3/хон)', header)
	worksheet11.merge_range('H4:H5', u'Бохир ус нийлүүлэх цэгийн байршил', header)
	if bohircar:
		for i in range(len(bohircar)):
			worksheet11.write('B%s' %(i+6), i+1, body)
		for iRow8, bbbba in enumerate(bohircar):
			worksheet11.write(iRow8 + 5,2, str(bbbba.mark)+' '+str(bbbba.no), body)
			worksheet11.write(iRow8 + 5,3, bbbba.huchin_chadal, body)
			worksheet11.write(iRow8 + 5,4, bbbba.gereet_too, body)
			worksheet11.write(iRow8 + 5,5, bbbba.duudlaga_too, body)
			worksheet11.write(iRow8 + 5,6, bbbba.us, body)
			worksheet11.write(iRow8 + 5,7, bbbba.niiluuleh_tseg, body)





	ajiltan= Ajiltan.objects.filter(baiguullaga= tze_id,status= True)
	diplom= School.objects.filter(emp= ajiltan)
	mergejil= Job.objects.filter(emp=ajiltan)
	certificate= EngineeringCertificate.objects.filter(emp=ajiltan)
#   Хүснэгт 11
	worksheet12.merge_range('B1:I1', ner.org_name, title)
	title_text12 = u"Хүний нөөцийн судалгаа"
	worksheet12.merge_range('B2:I2', title_text12, title)
	worksheet12.write('J3', u'Хүснэгт№12', header)
	worksheet12.merge_range('A4:A5', u'№', header)
	worksheet12.merge_range('B4:B5', u'Овог', header)
	worksheet12.merge_range('C4:C5', u'Нэр', header)
	worksheet12.merge_range('D4:D5', u'Нас', header)
	worksheet12.merge_range('E4:E5', u'Хүйс', header)
	worksheet12.merge_range('F4:F5', u'Регистрийн дугаар', header)
	worksheet12.merge_range('G4:G5', u'Албан тушаал', header)
	worksheet12.merge_range('H4:H5', u'Мэргэжил', header)
	worksheet12.merge_range('I4:I5', u'Төгссөн сургууль', header)
	worksheet12.merge_range('J4:J5', u'Диплом, мэргэжлийн үнэмлэхний дугаар', header)
	turshilt =  u''
	turshilt1 = u''
	turshilt2 = u''
	
	if ajiltan:
		for i in range(len(ajiltan)):
			worksheet12.write('A%s' %(i+6), i+1, body)
		for iRow9, bbbbab in enumerate(ajiltan):
			worksheet12.write(iRow9 + 5,1, bbbbab.emp_lname ,  body)
			worksheet12.write(iRow9 + 5,2, bbbbab.emp_name, body)
			worksheet12.write(iRow9 + 5,3, bbbbab.nas, body)
			worksheet12.write(iRow9 + 5,4, bbbbab.gender, body)
			worksheet12.write(iRow9 + 5,5, bbbbab.emp_reg, body)
			positionn= AlbanTushaal.objects.get(id= bbbbab.position_id_id)
			pos= AlbanTushaalList.objects.get(id= positionn.position_name_id)
			worksheet12.write(iRow9 + 5,6, pos.name, body)
			worksheet12.write(iRow9 + 5,7, '', body)
			worksheet12.write(iRow9 + 5,8,'', body)
			worksheet12.write(iRow9 + 5,9,'', body)
			for cert in EngineeringCertificate.objects.filter(emp= bbbbab):
				turshilt2 = turshilt2 +'\n '+ str(cert.certificate_num)
			for school in School.objects.filter(emp= bbbbab):
				turshilt1 = turshilt1 +'\n '+ str(school.diplom_num)
				ih_surguuli= University.objects.filter(id= school.school_name_id)
				for ih in ih_surguuli:
					turshilt = turshilt +'\n ' +ih.university
				
	worksheet12.write(iRow9 + 5,7, turshilt, body)
	worksheet12.write(iRow9 + 5,8, turshilt1, body)
	worksheet12.write(iRow9 + 5,9, turshilt2, body)	



	
	ajiltan1 = ajiltan.filter(zereg=u'Удирдах ажилтан')
	ajiltan2 = ajiltan.filter(zereg=u'Инженер техникийн ажилтан')
	ajiltan3 = ajiltan.filter(zereg=u'Мэргэжлийн ажилтан')
	ajiltan4 = ajiltan.filter(zereg=u'Бусад')
#   Хүснэгт 11
	worksheet13.merge_range('B1:D1', ner.org_name, title)
	title_text13 = u"Боловсролын судалгаа"
	worksheet13.merge_range('B2:D2', title_text13, title)
	worksheet13.write('D3', u'Хүснэгт№13', header)
	worksheet13.merge_range('B4:B5', u'№', header)
	for i in range(5):
		worksheet13.write('B%s' %(i+6), i+1, body)
	worksheet13.merge_range('C4:C5', u'Боловсролын зэрэг', header)
	worksheet13.merge_range('D4:D5', u'Хүний тоо', header)
	worksheet13.write('C6', u'Удирдах ажилтан', body)
	worksheet13.write('C7', u'Инженер техникийн ажилтан', body)
	worksheet13.write('C8', u'Ус түгээх байрны түгээгч', body)
	worksheet13.write('C9', u'Бусад', body)
	worksheet13.write('C10', u'Нийт ажилтнуудын тоо', body)
	worksheet13.write('D6', len(ajiltan1), body)
	worksheet13.write('D7', len(ajiltan2), body)
	worksheet13.write('D8', len(ajiltan3), body)
	worksheet13.write('D9', len(ajiltan4), body)
	worksheet13.write('D10', len(ajiltan), body)



	ajiltanErh= Ajiltan.objects.get(baiguullaga= tze_id, status= True, position_id= AlbanTushaal.objects.get(baiguullaga= tze_id, position_name = AlbanTushaalList.objects.get(name= u'Захирал')))

#	ajiltanErh1= Ajiltan.objects.get(baiguullaga= tze_id, status= True, position_id= AlbanTushaal.objects.get(baiguullaga= tze_id, position_name = AlbanTushaalList.objects.get(name= u'Даргын туслах')))
#	ajiltanErh2= Ajiltan.objects.get(baiguullaga= tze_id, status= True, position_id= AlbanTushaal.objects.get(baiguullaga= tze_id, position_name = AlbanTushaalList.objects.get(name= u'Ерөнхий инженер')))
#	ajiltanErh3= Ajiltan.objects.get(baiguullaga= tze_id, status= True, position_id= AlbanTushaal.objects.get(baiguullaga= tze_id, position_name = AlbanTushaalList.objects.get(name= u'Ерөнхий нягтлан бодогч')))
  	baiguullag= TZE.objects.get(id= tze_id)
#   Хүснэгт 11
	worksheet14.merge_range('B1:E1', ner.org_name, title)
	title_text14 = u"Эрх бүхий ажилчдын мэдээлэл"
	worksheet14.merge_range('B2:E2', title_text14, title)
	worksheet14.write('G3', u'Хүснэгт№14', header)
	
	worksheet14.merge_range('B4:B5', u'№', header)
	for i in range(4):
		worksheet14.write('B%s' %(i+6), i+1, body)
		worksheet14.write('D%s' %(i+6), '', body)
		worksheet14.write('E%s' %(i+6), '', body)
		worksheet14.write('F%s' %(i+6), '', body)
		worksheet14.write('G%s' %(i+6), '', body)
	worksheet14.merge_range('C4:C5', u'Албан тушаал', header)
	worksheet14.merge_range('D4:D5', u'Овог нэр', header)
	worksheet14.merge_range('E4:F4', u'Холбоо барих утас', header)
	worksheet14.write('E5', u'Гар', header)
	worksheet14.write('F5', u'Ажил', header)
	worksheet14.merge_range('G4:G5', u'Имэйл', header)
	worksheet14.write('C6', u'Дарга' , body)
	worksheet14.write('C7', u'Даргын туслах', body)
	worksheet14.write('C8', u'Ерөнхий инженер', body)
	worksheet14.write('C9', u'Ерөнхий нягтлан бодогч', body)
	
	worksheet14.write('D6', ajiltanErh.emp_lname+' '+ajiltanErh.emp_name, body)
	worksheet14.write('E6', ajiltanErh.phone, body)
	worksheet14.write('F6', baiguullag.phone, body)
	worksheet14.write('G6', ajiltanErh.e_mail, body)

	worksheet14.write('D7', '', body)
	worksheet14.write('E7', '', body)
	worksheet14.write('F7', '', body)
	worksheet14.write('G7', '', body)
#	worksheet14.write('D7', ajiltanErh1.emp_lname+' '+ajiltanErh1.emp_name, body)
#	worksheet14.write('E7', ajiltanErh1.phone, body)
#	worksheet14.write('F7', u'Ерөнхий инженер', body)
#	worksheet14.write('G7', ajiltanErh1.e_mail, body)

#	worksheet14.write('D8', ajiltanErh2.emp_lname+' '+ajiltanErh2.emp_name, body)
#	worksheet14.write('E8', ajiltanErh2.phone, body)
#	worksheet14.write('F8', baiguullag.phone, body)
#	worksheet14.write('G8', ajiltanErh2.e_mail, body)

#	worksheet14.write('D8', ajiltanErh3.emp_lname+' '+ajiltanErh3.emp_name, body)
#	worksheet14.write('E8', ajiltanErh3.phone, body)
#	worksheet14.write('F8', baiguullag.phone, body)
#	worksheet14.write('G8', ajiltanErh3.e_mail, body)

	workbook.close()
	xlsx_data = output.getvalue()
	return xlsx_data

	
	
def UaTailanNegtgelHorvuuleh(request):
	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=UATailanNegtgel.xlsx'
	xlsx_data = UaTailanNegtgelHorvuulehToExcel()
	response.write(xlsx_data)
	return response

def UaTailanNegtgelHorvuulehToExcel():
	output = StringIO.StringIO()
	workbook = xlsxwriter.Workbook(output)
	worksheet1 = workbook.add_worksheet(u'Хүснэгт№1')
	worksheet2 = workbook.add_worksheet(u'Хүснэгт№2')
	worksheet3 = workbook.add_worksheet(u'Хүснэгт№3')
	worksheet4 = workbook.add_worksheet(u'Хүснэгт№4')
	worksheet5 = workbook.add_worksheet(u'Хүснэгт№5')
	worksheet6 = workbook.add_worksheet(u'Хүснэгт№6')
	worksheet7 = workbook.add_worksheet(u'Хүснэгт№7')
	worksheet8 = workbook.add_worksheet(u'Хүснэгт№8')
	worksheet9 = workbook.add_worksheet(u'Хүснэгт№9')
	worksheet10 = workbook.add_worksheet(u'Хүснэгт№10')
	worksheet11 = workbook.add_worksheet(u'Хүснэгт№11')
	worksheet12 = workbook.add_worksheet(u'Хүснэгт№12')
	worksheet13 = workbook.add_worksheet(u'Хүснэгт№13')
	worksheet14 = workbook.add_worksheet(u'Хүснэгт№14')

	worksheet1.set_column('C:J', 14)
	worksheet2.set_column('C:J', 14)
	worksheet3.set_column('C:J', 14)
	worksheet4.set_column('C:K', 14)
	worksheet5.set_column('C:J', 14)
	worksheet6.set_column('C:K', 14)
	worksheet7.set_column('C:J', 14)
	worksheet8.set_column('C:J', 14)
	worksheet9.set_column('C:J', 14)
	worksheet10.set_column('C:J', 14)
	worksheet11.set_column('C:J', 14)
	worksheet12.set_column('C:J', 14)
	worksheet13.set_column('C:J', 14)
	worksheet14.set_column('C:J', 14)

	title = workbook.add_format({
    	'bold': True,
    	'font_size': 14,
    	'align': 'center',
    	'valign': 'vcenter'
    	})
	title.set_text_wrap()
	header = workbook.add_format({
    	'bg_color': '#F7F7F7',
    	'color': 'black',
    	'align': 'center',
    	'valign': 'top',
    	'border': 1
    	})
    
	header.set_text_wrap()

	body = workbook.add_format({
		'border' : 1,
		'color': 'black',
    	'align': 'left',
    	'valign': 'middle'
   		})
	body.set_text_wrap()
	body_body = workbook.add_format({
		'border' : 1,
		'color': 'black',
    	'align': 'left',
    	'bold' : True
		})
	baiguullag= TZE.objects.filter(status= True)
	hudag = Hudag.objects.filter(status=True)
 	#   Хүснэгт 11
 	
	title_text1 = u"Ус хангамжийн эх үүсвэрийн барилга байгууламжийн судалгаа"
	worksheet1.merge_range('B2:J2', title_text1, title)
	worksheet1.write('B4', u'№', header)
	worksheet1.merge_range('C4:D4', u'Барилга байгууламж', header)
	worksheet1.write('E4', u'Хүчин чадал(м3/хон)', header)
	worksheet1.write('F4', u'Олборлож буй ус(м3/хон)', header)
	worksheet1.write('G4', u'Ашиглалтанд орсон огноо', header)
	worksheet1.write('H4', u'/Тайлбар ажиллаж байгаа эсэх/', header)
	worksheet1.write('I3', u'Хүснэгт№1', header)
	worksheet1.write('I4', u'Эх үүсвэрийн харуул, хамгаалалтын тухай', header)
	if hudag:
		for a in range(len(hudag)):
			worksheet1.write('B%s' %(a+5), a+1, body)
		for iRow, ba in enumerate(hudag):
			worksheet1.write(iRow + 4,3, u'№'+' '+str(ba.id), body)
			worksheet1.write(iRow + 4,4, ba.huchin_chadal, body)
			worksheet1.write(iRow + 4,5, ba.olborloj_bui_us, body)
			worksheet1.write(iRow + 4,6, ba.ashiglaltand_orson_ognoo.strftime('%d/%m/%Y'), body)
			worksheet1.write(iRow + 4,7, ba.tailbar, body)
			worksheet1.write(iRow + 4,8, ba.haruul, body)
		if len(hudag) == 1:
			worksheet1.merge_range(4,2, len(hudag)+ 3,2,  u'Гүний худаг', body)
		if len(hudag) > 1:
			worksheet1.merge_range(4,2, len(hudag)+ 3,2,  u'Гүний худаг', body)
	



	usansan = UsanSan.objects.filter(status=True)
	nasos = NasosStants.objects.filter(status=True)
	lab = Lab.objects.filter(status=True)
#   Хүснэгт 11	
	
	title_text2 = u"Ус хангамжийн эх үүсвэрийн барилга байгууламжийн судалгаа"
	worksheet2.merge_range('B2:H2', title_text2, title)
	worksheet2.write('B4', u'№', header)
	worksheet2.merge_range('C4:D4', u'Барилга байгууламж', header)
	worksheet2.write('E4', u'Тоо хэмжээ', header)
	worksheet2.write('F4', u'Хүчин чадал', header)
	worksheet2.write('G4', u'Ашиглалтанд орсон огноо', header)
	worksheet2.write('H4', u'/Тайлбар ажиллаж байгаа эсэх/', header)
	worksheet2.write('H3', u'Хүснэгт№2', header)
	niit2 = 0
	niit_usansan = 0
	niit_nasos = 0
	if usansan and nasos and lab:
		niit2 = len(usansan)+ len(nasos)+ len(lab)
	if usansan:
		niit_usansan = len(usansan) + 4
	if nasos:	
		niit_nasos = len(nasos) + 4 + len(usansan)
	for i in range(niit2):
		worksheet2.write('B%s' %(i+5), i+1, body)
	for iRow2, bab in enumerate(usansan):
		worksheet2.merge_range(iRow2 + 4,2,iRow2 + 4,3, u'Усан сан', body)
		worksheet2.write(iRow2 + 4,4, '1', body)
		worksheet2.write(iRow2 + 4,5, bab.huchin_chadal, body)
		worksheet2.write(iRow2 + 4,6, bab.ashiglaltand_orson_ognoo.strftime('%d/%m/%Y'), body)
		worksheet2.write(iRow2 + 4,7, bab.tailbar, body)	
	for iRow3, baba in enumerate(nasos):
		worksheet2.merge_range(iRow3 + niit_usansan,2,iRow3 + niit_usansan,3, u'Насосны станц', body)
		worksheet2.write(iRow3 + niit_usansan,4, '1', body)
		worksheet2.write(iRow3 + niit_usansan,5, baba.huchin_chadal, body)
		worksheet2.write(iRow3 + niit_usansan,6, baba.ashiglaltand_orson_ognoo.strftime('%d/%m/%Y'), body)
		worksheet2.write(iRow3 + niit_usansan,7, baba.tailbar, body)
	for iRow4, babab in enumerate(lab):
		worksheet2.merge_range(iRow4 + niit_nasos,2,iRow4 + niit_nasos,3, u'Цэвэр усны лаборатори', body)
		worksheet2.write(iRow4 + niit_nasos,4, '1', body)
		worksheet2.write(iRow4 + niit_nasos,5, babab.huchin_chadal, body)
		worksheet2.write(iRow4 + niit_nasos,6, babab.ashiglaltand_orson_ognoo.strftime('%d/%m/%Y'), body)
		worksheet2.write(iRow4 + niit_nasos,7, babab.tailbar, body)
	

	standart1= AnalysisWaterStandart.objects.all().last()
	analysis_tsever = AnalysisWater.objects.filter(status=True).last()
#   Хүснэгт 11
	
	title_text3 = u"Цэвэр усны шинжилгээний дүн/жилийн дундаж үзүүлэлт/"
	worksheet3.merge_range('B2:E2', title_text3, title)
	worksheet3.write('B4', u'№', header)

	for i in range(11):
		worksheet3.write('B%s' %(i+5), i+1, body)


	worksheet3.write('C4', u'Үзүүлэлт', header)
	worksheet3.write('D4', u'Стандарт үзүүлэлт', header)
	worksheet3.write('E4', u'Шинжилгээний дүн', header)
	worksheet3.write('E3', u'Хүснэгт№3', header)
	worksheet3.write('C5', u'Ерөнхий хатуулаг', body)
	worksheet3.write('C6', u'Магни', body)
	worksheet3.write('C7', u'Кальци', body)
	worksheet3.write('C8', u'Хлорид', body)
	worksheet3.write('C9', u'Сульфат', body)
	worksheet3.write('C10', u'pH', body)
	worksheet3.write('C11', u'Аммиак', body)
	worksheet3.write('C12', u'Нитрит', body)
	worksheet3.write('C13', u'Амт', body)
	worksheet3.write('C14', u'Үнэр', body)
	worksheet3.write('C15', u'Нийт нянгийн тоо', body)
	worksheet3.write('D5', standart1.hatuulag, body)
	worksheet3.write('D6', standart1.magni, body)
	worksheet3.write('D7', standart1.kalitsi, body)
	worksheet3.write('D8', standart1.hlorid, body)
	worksheet3.write('D9', standart1.sulifat, body)
	worksheet3.write('D10', standart1.ph, body)
	worksheet3.write('D11', standart1.ammiak , body)
	worksheet3.write('D12', standart1.nitrit, body)
	worksheet3.write('D13', standart1.amt, body)
	worksheet3.write('D14', standart1.uner, body)
	worksheet3.write('D15', standart1.nyan, body)
 	if analysis_tsever:
		worksheet3.write('E5', analysis_tsever.hatuulag, body)
		worksheet3.write('E6', analysis_tsever.magni, body)
		worksheet3.write('E7', analysis_tsever.kalitsi, body)
		worksheet3.write('E8', analysis_tsever.hlorid, body)
		worksheet3.write('E9', analysis_tsever.sulifat, body)
		worksheet3.write('E10', analysis_tsever.ph, body)
		worksheet3.write('E11', analysis_tsever.ammiak , body)
		worksheet3.write('E12', analysis_tsever.nitrit, body)
		worksheet3.write('E13', analysis_tsever.amt, body)
		worksheet3.write('E14', analysis_tsever.uner, body)
		worksheet3.write('E15', analysis_tsever.nyan, body)
	else:
		worksheet3.write('E5', '', body)
		worksheet3.write('E6', '', body)
		worksheet3.write('E7', '', body)
		worksheet3.write('E8', '', body)
		worksheet3.write('E9', '', body)
		worksheet3.write('E10','', body)
		worksheet3.write('E11', '' , body)
		worksheet3.write('E12', '', body)
		worksheet3.write('E13', '', body)
		worksheet3.write('E14', '', body)
		worksheet3.write('E15', '', body)	

	tseversuljee = Sh_suljee.objects.filter(shugam_torol__in=[u'Эх үүсвэрийн цуглуулах',u'Цэвэр усны дамжуулах шугам',u'Цэвэр ус түгээх шугам'],status=True)
	suljee= Sh_suljeeTable.objects.filter(suljee_id= tseversuljee).last()
	
#   Хүснэгт 11
	
	title_text4 = u"Цэвэр усны шугам сүлжээний судалгаа "
	worksheet4.merge_range('B2:K2', title_text4, title)
	worksheet4.merge_range('B4:B5', u'№', header)
	worksheet4.write('K3', u'Хүснэгт№4', header)
	worksheet4.merge_range('C4:C5', u'Шугам сүлжээ', header)
	worksheet4.merge_range('D4:D5', u'Шугамын урт/метрээр илэрхийлнэ./', header)	
	worksheet4.merge_range('E4:G4', u'Шугамын материал/метрээр илэрхийлнэ./', header)
	worksheet4.write('E5', u'Ширэм', header)
	worksheet4.write('F5', u'Хуванцар', header)
	worksheet4.write('G5', u'Цайрдсан ган', header)
	worksheet4.merge_range('H4:H5', u'Шугамын диаметр', header)
	worksheet4.merge_range('I4:I5', u'Шугам дээрх хяналтын худгийн тоо', header)
	worksheet4.merge_range('J4:J5', u'Жилд гарсан гэмтлийн тоо', header)
	worksheet4.merge_range('K4:K5', u'Ашиглалтанд орсон огноо', header)
	if tseversuljee:
		for i in range(len(tseversuljee)):
			worksheet4.write('B%s' %(i+6), i+1, body)
			worksheet4.write(i + 5,4, suljee.shirem, body)
			worksheet4.write(i + 5,5, suljee.huvantsar, body)
			worksheet4.write(i + 5,6, suljee.gan, body)

		for iRow5, bba in enumerate(tseversuljee):
			worksheet4.write(iRow5 + 5,2, bba.shugam_torol, body)
			worksheet4.write(iRow5 + 5,3, bba.shugam_urt, body)
			worksheet4.write(iRow5 + 5,7, bba.diametr, body)
			worksheet4.write(iRow5 + 5,8, bba.hudgiin_too, body)
			worksheet4.write(iRow5 + 5,9, bba.gemtliin_too, body)
			worksheet4.write(iRow5 + 5,10, bba.ashiglaltand_orson_ognoo.strftime('%d/%m/%Y'), body)



	abb= ABB.objects.filter(status= True)

#   Хүснэгт 11
	
	title_text5 = u"Ашиглалтыг нь хариуцаж буй барилга байгууламжийн судалгаа"
	worksheet5.merge_range('B2:F2', title_text5, title)
	worksheet5.merge_range('B4:B5', u'№', header)
	worksheet5.write('F3', u'Хүснэгт№6', header)
	worksheet5.merge_range('C4:C5', u'Барилга байгууламжийн нэр', header)
	worksheet5.merge_range('D4:D5', u'Нийт тоо хэмжээ', header)
	worksheet5.merge_range('E4:F4', u'Тоолууржилт', header)
	worksheet5.write('E5', u'Тоо хэмжээ', header)
	worksheet5.write('F5', u'%', header)
	worksheet5.write('C6', u'Орон сууцны айл өрх', body)
	worksheet5.write('C7', u'Үйлдвэр', body)
	worksheet5.write('C8', u'Аж ахуйн нэгж', body)
	worksheet5.write('C9', u'Ус дулаан дамжуулах төв', body)
	worksheet5.write('C10', u'Байрын узель', body)
	for i in range(5):
		worksheet5.write('B%s' %(i+6), i+1, body)
		worksheet5.write('D%s' %(i+6), '', body)
		worksheet5.write('E%s' %(i+6), '', body)
		worksheet5.write('F%s' %(i+6), '', body)
	




	bohirsuljee = Sh_suljee.objects.filter( shugam_torol__in=[u'Бохир усны гаргалгааны шугам',u'Бохир усны цуглуулах шугам',u'Бохир ус татан зайлуулах шугам'],status=True)
	husnegt2= Sh_suljeeTable.objects.filter(suljee_id= bohirsuljee).last()
#   Хүснэгт 11
	
	title_text6 = u"Бохир усны шугам сүлжээний судалгаа "
	worksheet6.merge_range('B2:E2', title_text6, title)
	worksheet6.merge_range('B4:B5', u'№', header)
	worksheet6.write('K3', u'Хүснэгт№6', header)
	worksheet6.merge_range('C4:C5', u'Шугам сүлжээ', header)
	worksheet6.merge_range('D4:D5', u'Шугамын урт/метрээр илэрхийлнэ./', header)
	worksheet6.merge_range('E4:G4', u'Шугамын материал/метрээр илэрхийлнэ./', header)
	worksheet6.write('E5', u'Ширэм', header)
	worksheet6.write('F5', u'Хуванцар', header)
	worksheet6.write('G5', u'Асбето-цемент', header)
	worksheet6.merge_range('H4:H5', u'Шугамын диаметр', header)
	worksheet6.merge_range('I4:I5', u'Шугам дээрх хяналтын худгийн тоо', header)
	worksheet6.merge_range('J4:J5', u'Жилд гарсан гэмтлийн тоо', header)
	worksheet6.merge_range('K4:K5', u'Ашиглалтанд орсон огноо', header)
	if bohirsuljee:
		for i in range(len(bohirsuljee)):
			worksheet6.write('B%s' %(i+6), i+1, body)
			worksheet6.write(i + 5,4, husnegt2.shirem, body)
			worksheet6.write(i + 5,5, husnegt2.huvantsar, body)
			worksheet6.write(i + 5,6, husnegt2.gan, body)
		for iRow61, bbb in enumerate(bohirsuljee):
			worksheet6.write(iRow61 + 5,2, bbb.shugam_torol, body)
			worksheet6.write(iRow61 + 5,3, bbb.shugam_urt, body)
			worksheet6.write(iRow61 + 5,7, bbb.diametr, body)
			worksheet6.write(iRow61 + 5,8, bbb.hudgiin_too, body)
			worksheet6.write(iRow61 + 5,9, bbb.gemtliin_too, body)
			worksheet6.write(iRow61 + 5,10, bbb.ashiglaltand_orson_ognoo.strftime('%d/%m/%Y'), body)




	tseverleh_baig= Ts_baiguulamj.objects.filter(status=True)
	tseverleh = Ts_tohooromj.objects.filter(ts_baiguulamj= tseverleh_baig)
#   Хүснэгт 11
	
	title_text7 = u"Цэвэрлэх байгууламжийн судалгаа"
	worksheet7.merge_range('B2:E2', title_text7, title)
	worksheet7.write('B4', u'№', header)
	worksheet7.write('I3', u'Хүснэгт№7', header)
	worksheet7.write('C4', u'Цэвэрлэгээний аргууд', header)
	worksheet7.write('D4', u'Барилга байгууламж, тоног төхөөрөмж', header)
	worksheet7.write('E4', u'Тоо хэмжээ', header)
	worksheet7.write('F4', u'Хүчин чадал(м3/хон)', header)
	worksheet7.write('G4', u'Хүлээн авч буй ус(м3/хон)', header)
	worksheet7.write('H4', u'Ашиглалтанд орсон огноо', header)
	worksheet7.write('I4', u'Тайлбар', header)
	if tseverleh:
		for i in range(len(tseverleh)):
			worksheet7.write('B%s' %(i+5), i+1, body)
			for tseverleh_baig in tseverleh_baig:
				if tseverleh_baig.mehanik == True and tseverleh_baig.biologi == True and tseverleh_baig.fizik == True:
					worksheet7.write(i + 4,2, u'Механик, Биологи, Физик-хими, хими', body)
				elif tseverleh_baig.mehanik == True and tseverleh_baig.biologi == False and tseverleh_baig.fizik == False:
					worksheet7.write(i + 4,2, u'Механик', body)
				elif tseverleh_baig.mehanik == True and tseverleh_baig.biologi == True and tseverleh_baig.fizik == False:
					worksheet7.write(i + 4,2, u'Механик, Физик-хими, хими', body)
				elif tseverleh_baig.mehanik == False and tseverleh_baig.biologi == False and tseverleh_baig.fizik == False:
					worksheet7.write(i + 4,2, '', body)
				elif tseverleh_baig.mehanik == False and tseverleh_baig.biologi == True and tseverleh_baig.fizik == False:
					worksheet7.write(i + 4,2, u'Биологи', body)
				elif tseverleh_baig.mehanik == False and tseverleh_baig.biologi == False and tseverleh_baig.fizik == True:
					worksheet7.write(i + 4,2, u'Физик-хими, хими', body)
				elif tseverleh_baig.mehanik == False and tseverleh_baig.biologi == True and tseverleh_baig.fizik == True:
					worksheet7.write(i + 4,2, u'Биологи, Физик-хими, хими', body)
		for iRow101, bbbhj in enumerate(tseverleh):
			worksheet7.write(iRow101 + 4,3, bbbhj.barilga_tonog, body)
			worksheet7.write(iRow101 + 4,4, bbbhj.too, body)
			worksheet7.write(iRow101 + 4,5, bbbhj.huchin_chadall, body)
			worksheet7.write(iRow101 + 4,6, '' , body)
			worksheet7.write(iRow101 + 4,7, bbbhj.ashiglaltand_orson_ognooo.strftime('%d/%m/%Y') , body)
			worksheet7.write(iRow101 + 4,8, bbbhj.tailbarr, body)




 	standart_bohir= AnalysisBohirStandart.objects.all().last()
	analysis_bohir = AnalysisBohir.objects.filter(status=True).last()
#   Хүснэгт 11
	
	title_text8 = u"Бохир усны шинжилгээний дүн"
	worksheet8.merge_range('B2:E2', title_text8, title)
	worksheet8.merge_range('D3:F3', u'/Сүүлийн шинжилгээний үзүүлэлтийг бичнэ./', body)
	
	worksheet8.merge_range('B4:B5', u'№', header)
	for i in range(3):
		worksheet8.write('B%s' %(i+6), i+1, body)
		worksheet8.write('D%s' %(i+6), '', body)
		worksheet8.write('E%s' %(i+6), '', body)
		worksheet8.write('F%s' %(i+6), '', body)
	worksheet8.merge_range('C4:C5', u'Үзүүлэлт', header)
	worksheet8.merge_range('D4:D5', u'Стандарт үзүүлэлт', header)
	worksheet8.merge_range('E4:F4', u'Огноо', header)
	worksheet8.write('E5', u'Цэвэрлэх байгууламж руу орох', header)
	worksheet8.write('F5', u'Цэвэрлэх байгууламжаас гарах', header)
	worksheet8.write('C6', u'Умбуур бодисын тоо мг/л', body)
	worksheet8.write('C7', u'БХХ мг/л О2', body)
	worksheet8.write('C8', u'ХХХ мг/л О2', body)
	worksheet8.write('D6', standart_bohir.umbuur, body)
	worksheet8.write('D7', standart_bohir.bhh, body)
	worksheet8.write('D8', standart_bohir.hhh, body)
	if analysis_bohir:
		worksheet8.write('C3', analysis_bohir.ognoo.strftime('%d/%m/%Y') , body)
		worksheet8.write('E6', analysis_bohir.umbuuro , body)
		worksheet8.write('E7', analysis_bohir.bhho, body)
		worksheet8.write('E8', analysis_bohir.hhho, body)
		worksheet8.write('F6', analysis_bohir.umbuurgarah, body)
		worksheet8.write('F7', analysis_bohir.bhhgarah, body)
		worksheet8.write('F8', analysis_bohir.hhhgarah, body)




	us12=UsTugeehBair.objects.filter(status=True)	
	us1=UsTugeehBair.objects.filter(status=True, barilga= u'Гүний эх үүсвэртэй ус түгээх байр')
	us2=UsTugeehBair.objects.filter(status=True, barilga= u'Зөөврийн эх үүсвэртэй ус түгээх байр')
	us3=UsTugeehBair.objects.filter(status=True, barilga= u'Төвлөрсөн шугамаас тэжээгддэг ус түгээх байр')
	hun_amiin_too=0
	borluulj_bui_us=0
	hun_amiin_too1=0
	borluulj_bui_us1=0
	hun_amiin_too2=0
	borluulj_bui_us2=0
	for us in us12:
		if us.barilga == u'Гүний эх үүсвэртэй ус түгээх байр':
			hun_amiin_too= hun_amiin_too+ us.hun_amiin_too
			borluulj_bui_us= borluulj_bui_us+ us.borluulj_bui_us
		elif us.barilga == u'Зөөврийн эх үүсвэртэй ус түгээх байр':
			hun_amiin_too1= hun_amiin_too1+ us.hun_amiin_too
			borluulj_bui_us1= borluulj_bui_us1+ us.borluulj_bui_us	
		elif us.barilga == u'Төвлөрсөн шугамаас тэжээгддэг ус түгээх байр':
			hun_amiin_too2= hun_amiin_too2+ us.hun_amiin_too
			borluulj_bui_us2= borluulj_bui_us2+ us.borluulj_bui_us
	hun_amiin_too_niit= hun_amiin_too+ hun_amiin_too1 + hun_amiin_too2
	borluulj_bui_us_niit= borluulj_bui_us+ borluulj_bui_us1+ borluulj_bui_us2
#   Хүснэгт 11
	
	title_text9 = u"Ус түгээх байрны судалгаа"
	worksheet9.merge_range('B2:E2', title_text9, title)
	worksheet9.write('F3', u'Хүснэгт№9', header)
	worksheet9.merge_range('B4:B5', u'№', header)
	worksheet9.merge_range('C4:C5', u'Барилга байгууламж', header)
	worksheet9.merge_range('D4:D5', u'ТЗЭ-ээр үйлчлүүлж буй хүн амын тоо', header)
	worksheet9.merge_range('E4:E5', u'Худгийн тоо', header)
	worksheet9.merge_range('F4:F5', u'Борлуулж буй ус(м3/хон)', header)
	worksheet9.write('C6', u'Гүний эх үүсвэртэй ус түгээх байр', body)
	worksheet9.write('C7', u'Зөөврийн эх үүсвэртэй ус түгээх байр', body)
	worksheet9.write('C8', u'Төвлөрсөн шугамаас тэжээгддэг ус түгээх байр', body)
	worksheet9.write('C9', u'Нийт', header)
	
	for i in range(4):
		worksheet9.write('B%s' %(i+6), i+1, body)
	worksheet9.write('D6', hun_amiin_too, body)
	worksheet9.write('D7', hun_amiin_too1, body)
	worksheet9.write('D8', hun_amiin_too2, body)
	worksheet9.write('D9', hun_amiin_too_niit , body)
	worksheet9.write('E6', len(us1), body)
	worksheet9.write('E7', len(us2), body)
	worksheet9.write('E8', len(us3), body)
	worksheet9.write('E9', len(us12), body)
	worksheet9.write('F6', borluulj_bui_us, body)
	worksheet9.write('F7', borluulj_bui_us1, body)
	worksheet9.write('F8', borluulj_bui_us2, body)
	worksheet9.write('F9', borluulj_bui_us_niit, body)


	watercar= WaterCar.objects.filter(status= True)
#   Хүснэгт 11
	
	title_text10 = u"Зөөврийн ус хангамжийн үйлчилгээ үзүүлдэг автомашины судалгаа"
	worksheet10.merge_range('B2:H2', title_text10, title)
	worksheet10.write('H3', u'Хүснэгт№10', header)
	worksheet10.merge_range('B4:B5', u'№', header)
	worksheet10.merge_range('C4:C5', u'Автомашины марк, улсын дугаар', header)
	worksheet10.merge_range('D4:D5', u'Хүчин чадал(тонн)', header)
	worksheet10.merge_range('E4:G4', u'Хэрэглэгчийн тоо', header)
	worksheet10.write('E5', u'ААНБ', header)
	worksheet10.write('F5', u'УТБ', header)
	worksheet10.write('G5', u'Хүн ам', header)
	worksheet10.merge_range('H4:H5', u'Борлуулсан усны хэмжээ(м3/хон)', header)
	if watercar:
		for i in range(len(watercar)):
			worksheet10.write('B%s' %(i+6), i+1, body)
		for iRow7, bbbb in enumerate(watercar):
			worksheet10.write(iRow7 + 5,2, str(bbbb.mark)+' '+str(bbbb.no) ,  body)
			worksheet10.write(iRow7 + 5,3, bbbb.huchin_chadal, body)
			worksheet10.write(iRow7 + 5,4, bbbb.aanb_too, body)
			worksheet10.write(iRow7 + 5,5, bbbb.utb_too, body)
			worksheet10.write(iRow7 + 5,6, bbbb.hun_am_too, body)
			worksheet10.write(iRow7 + 5,7, bbbb.us, body)




	bohircar= BohirCar.objects.filter(status= True)
#   Хүснэгт 11
	
	title_text11 = u"Бохир ус зөөвөрлөх үйлчилгээ үзүүлдэг автомашины судалгаа"
	worksheet11.merge_range('B2:H2', title_text11, title)
	worksheet11.write('H3', u'Хүснэгт№11', header)
	worksheet11.merge_range('B4:B5', u'№', header)
	worksheet11.merge_range('C4:C5', u'Автомашины марк, улсын дугаар', header)
	worksheet11.merge_range('D4:D5', u'Хүчин чадал(тонн)', header)
	worksheet11.merge_range('E4:F4', u'Хэрэглэгчийн тоо', header)
	worksheet11.write('E5', u'Гэрээт', header)
	worksheet11.write('F5', u'Дуудлагын', header)
	worksheet11.merge_range('G4:G5', u'Зөөвөрлөсөн усны хэмжээ(м3/хон)', header)
	worksheet11.merge_range('H4:H5', u'Бохир ус нийлүүлэх цэгийн байршил', header)
	if bohircar:
		for i in range(len(bohircar)):
			worksheet11.write('B%s' %(i+6), i+1, body)
		for iRow8, bbbba in enumerate(bohircar):
			worksheet11.write(iRow8 + 5,2, str(bbbba.mark)+' '+str(bbbba.no), body)
			worksheet11.write(iRow8 + 5,3, bbbba.huchin_chadal, body)
			worksheet11.write(iRow8 + 5,4, bbbba.gereet_too, body)
			worksheet11.write(iRow8 + 5,5, bbbba.duudlaga_too, body)
			worksheet11.write(iRow8 + 5,6, bbbba.us, body)
			worksheet11.write(iRow8 + 5,7, bbbba.niiluuleh_tseg, body)





	ajiltan= Ajiltan.objects.filter(status= True)
	diplom= School.objects.filter(emp= ajiltan)
	mergejil= Job.objects.filter(emp=ajiltan)
	certificate= EngineeringCertificate.objects.filter(emp=ajiltan)
#   Хүснэгт 11
	
	title_text12 = u"Хүний нөөцийн судалгаа"
	worksheet12.merge_range('B2:I2', title_text12, title)
	worksheet12.write('J3', u'Хүснэгт№12', header)
	worksheet12.merge_range('A4:A5', u'№', header)
	worksheet12.merge_range('B4:B5', u'Овог', header)
	worksheet12.merge_range('C4:C5', u'Нэр', header)
	worksheet12.merge_range('D4:D5', u'Нас', header)
	worksheet12.merge_range('E4:E5', u'Хүйс', header)
	worksheet12.merge_range('F4:F5', u'Регистрийн дугаар', header)
	worksheet12.merge_range('G4:G5', u'Албан тушаал', header)
	worksheet12.merge_range('H4:H5', u'Мэргэжил', header)
	worksheet12.merge_range('I4:I5', u'Төгссөн сургууль', header)
	worksheet12.merge_range('J4:J5', u'Диплом, мэргэжлийн үнэмлэхний дугаар', header)
	turshilt =  u''
	turshilt1 = u''
	turshilt2 = u''
	ajiltan_too= 0
	for baiguullag1 in baiguullag:
		ajiltan= Ajiltan.objects.filter(baiguullaga= baiguullag1.id ,status= True)
		diplom= School.objects.filter(emp= ajiltan)
		mergejil= Job.objects.filter(emp=ajiltan)
		certificate= EngineeringCertificate.objects.filter(emp=ajiltan)
		worksheet12.merge_range('B6:B10', baiguullag1.org_name, header)
		ajiltan_too= ajiltan_too + len(ajiltan)
		
	if ajiltan:
		for i in range(len(ajiltan)):
			worksheet12.write('A%s' %(i+6), i+1, body)
		for iRow9, bbbbab in enumerate(ajiltan):
			worksheet12.write(iRow9 + 5,1, bbbbab.emp_lname ,  body)
			worksheet12.write(iRow9 + 5,2, bbbbab.emp_name, body)
			worksheet12.write(iRow9 + 5,3, bbbbab.nas, body)
			worksheet12.write(iRow9 + 5,4, bbbbab.gender, body)
			worksheet12.write(iRow9 + 5,5, bbbbab.emp_reg, body)
			positionn= AlbanTushaal.objects.get(id= bbbbab.position_id_id)
			pos= AlbanTushaalList.objects.get(id= positionn.position_name_id)
			worksheet12.write(iRow9 + 5,6, pos.name, body)
			worksheet12.write(iRow9 + 5,7, '', body)
			worksheet12.write(iRow9 + 5,8,'', body)
			worksheet12.write(iRow9 + 5,9,'', body)
			for cert in EngineeringCertificate.objects.filter(emp= bbbbab):
				turshilt2 = turshilt2 +'\n '+ str(cert.certificate_num)
			for school in School.objects.filter(emp= bbbbab):
				turshilt1 = turshilt1 +'\n '+ str(school.diplom_num)
				ih_surguuli= University.objects.filter(id= school.school_name_id)
				for ih in ih_surguuli:
					turshilt = turshilt +'\n ' +ih.university
				
	worksheet12.write(iRow9 + 5,7, turshilt, body)
	worksheet12.write(iRow9 + 5,8, turshilt1, body)
	worksheet12.write(iRow9 + 5,9, turshilt2, body)	



	
#   Хүснэгт 11
	
	title_text13 = u"Боловсролын судалгаа"
	worksheet13.merge_range('B2:D2', title_text13, title)
	worksheet13.write('D3', u'Хүснэгт№13', header)
	worksheet13.merge_range('A4:A5', u'№', header)
	worksheet13.merge_range('B4:B5', u'Тусгай зөвшөөрөл эзэмшигч', header)
	for i in range(5):
		worksheet13.write('A%s' %(i+6), i+1, body)
	worksheet13.merge_range('C4:C5', u'Боловсролын зэрэг', header)
	worksheet13.merge_range('D4:D5', u'Хүний тоо', header)
	hast=0
	has=0
	ha= 0
	for baiguullag2 in baiguullag:
		worksheet13.merge_range('B6:B10', baiguullag2.org_name, header)
		ajiltan1 = ajiltan.filter(zereg=u'Удирдах ажилтан')
		ajiltan2 = ajiltan.filter(zereg=u'Инженер техникийн ажилтан')
		ajiltan3 = ajiltan.filter(zereg=u'Мэргэжлийн ажилтан')
		ajiltan4 = ajiltan.filter(zereg=u'Бусад')
		ha= ha+ 1
		hast = ha-1
		has = hast*5
		worksheet13.write(4,2 + has, u'Удирдах ажилтан', body)
		worksheet13.write(4,3 + has, u'Инженер техникийн ажилтан', body)
		worksheet13.write(4,4 + has, u'Ус түгээх байрны түгээгч', body)
		worksheet13.write(4,5 + has, u'Бусад', body)
		worksheet13.write(4,6 + has, u'Нийт ажилтнуудын тоо', body)

		worksheet13.write('D6', len(ajiltan1), body)
		worksheet13.write('D7', len(ajiltan2), body)
		worksheet13.write('D8', len(ajiltan3), body)
		worksheet13.write('D9', len(ajiltan4), body)
		worksheet13.write('D10', len(ajiltan), body)
	
	
		
		

	
#   Хүснэгт 11
	
	title_text14 = u"Эрх бүхий ажилчдын мэдээлэл"
	worksheet14.merge_range('B2:E2', title_text14, title)
	worksheet14.write('G3', u'Хүснэгт№14', header)
	
	worksheet14.merge_range('A4:A5', u'№', header)
	worksheet14.merge_range('B4:B5', u'ТУсгай зөвшөөрөл эзэмшигч', header)
	for i in range(4):
		worksheet14.write('A%s' %(i+6), i+1, body)
		worksheet14.write('D%s' %(i+6), '', body)
		worksheet14.write('E%s' %(i+6), '', body)
		worksheet14.write('F%s' %(i+6), '', body)
		worksheet14.write('G%s' %(i+6), '', body)
	worksheet14.merge_range('C4:C5', u'Албан тушаал', header)
	worksheet14.merge_range('D4:D5', u'Овог нэр', header)
	worksheet14.merge_range('E4:F4', u'Холбоо барих утас', header)
	worksheet14.write('E5', u'Гар', header)
	worksheet14.write('F5', u'Ажил', header)
	worksheet14.merge_range('G4:G5', u'Имэйл', header)
	worksheet14.write('C6', u'Дарга' , body)
	worksheet14.write('C7', u'Даргын туслах', body)
	worksheet14.write('C8', u'Ерөнхий инженер', body)
	worksheet14.write('C9', u'Ерөнхий нягтлан бодогч', body)
	nemeg= 0
	for baiguullag in baiguullag:
		urjver= nemeg* 4
		worksheet14.merge_range(5+ urjver,1,8+urjver,1, baiguullag.org_name, header)
		nemeg = nemeg +1 
		ajiltanErh= Ajiltan.objects.get(baiguullaga_id= baiguullag.id,status= True, position_id= AlbanTushaal.objects.filter(baiguullaga= baiguullag.id,position_name = AlbanTushaalList.objects.get(name= u'Захирал')))
	#	ajiltanErh1= Ajiltan.objects.get(baiguullaga= tze_id, status= True, position_id= AlbanTushaal.objects.get(baiguullaga= tze_id, position_name = AlbanTushaalList.objects.get(name= u'Даргын туслах')))
	#	ajiltanErh2= Ajiltan.objects.get(baiguullaga= tze_id, status= True, position_id= AlbanTushaal.objects.get(baiguullaga= tze_id, position_name = AlbanTushaalList.objects.get(name= u'Ерөнхий инженер')))
	#	ajiltanErh3= Ajiltan.objects.get(baiguullaga= tze_id, status= True, position_id= AlbanTushaal.objects.get(baiguullaga= tze_id, position_name = AlbanTushaalList.objects.get(name= u'Ерөнхий нягтлан бодогч')))
  
		worksheet14.write('D6', ajiltanErh.emp_lname+' '+ajiltanErh.emp_name, body)
		worksheet14.write('E6', ajiltanErh.phone, body)
		worksheet14.write('F6', baiguullag.phone, body)
		worksheet14.write('G6', ajiltanErh.e_mail, body)

		worksheet14.write('D7', '', body)
		worksheet14.write('E7', '', body)
		worksheet14.write('F7', '', body)
		worksheet14.write('G7', '', body)
	#	worksheet14.write('D7', ajiltanErh1.emp_lname+' '+ajiltanErh1.emp_name, body)
	#	worksheet14.write('E7', ajiltanErh1.phone, body)
	#	worksheet14.write('F7', u'Ерөнхий инженер', body)
	#	worksheet14.write('G7', ajiltanErh1.e_mail, body)

	#	worksheet14.write('D8', ajiltanErh2.emp_lname+' '+ajiltanErh2.emp_name, body)
	#	worksheet14.write('E8', ajiltanErh2.phone, body)
	#	worksheet14.write('F8', baiguullag.phone, body)
	#	worksheet14.write('G8', ajiltanErh2.e_mail, body)

	#	worksheet14.write('D8', ajiltanErh3.emp_lname+' '+ajiltanErh3.emp_name, body)
	#	worksheet14.write('E8', ajiltanErh3.phone, body)
	#	worksheet14.write('F8', baiguullag.phone, body)
	#	worksheet14.write('G8', ajiltanErh3.e_mail, body)

	workbook.close()
	xlsx_data = output.getvalue()
	return xlsx_data

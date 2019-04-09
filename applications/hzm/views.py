# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
from django.http import *
from django.views.generic import TemplateView, ListView, FormView
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from .forms import *
from applications.app.views import LoginRequired, get_object_or_none
from applications.app.models import *
from django.http import HttpResponseRedirect, HttpResponse, Http404
import jsonpickle
from django.shortcuts import get_object_or_404
from .filters import *
from django.views.decorators.csrf import csrf_exempt
from applications.engineering.filters import TZ_tze_Huselt_filter
from applications.tza.views import TZA_TohooromjjView, TZA_Gunii_Hudag_list, TZA_Usan_San_list
from applications.tza.views import TZA_Nasos_list, TZA_Lab_list, TZA_Sh_Suljee_list, TZA_Ts_Baiguulamj_list
from applications.tza.views import TZA_Us_Tugeeh_list, TZA_Us_Damjuulah_list, TZA_Water_Car_list
from applications.tza.views import TZA_Bohir_Car_list, TZA_Tonog_Tohooromj_list, tzaAjiltanView, TZA_Ajiltan_delgerengui, TZA_ABB_list, TZA_Us_hangamjiin_schema_zurag_list
from applications.tza.views import TZA_Baiguullaga_delgerengui, TZA_TZ_gerchilgee_listView, TZA_TZ_gerchilgee_delgerenguiView, Tza_huselt_delgerengui, TZA_TZ_Sent_materialView, TZA_TZ_Material_check, Tza_Huselt_list, TZ_huselt_check_finish_tza
from applications.tza.filters import Ajiltan_filter, TZE_search

from django.contrib.auth.models import Group

from applications.engineering.views import Base_Ajax_FormView
from applications.uta.filters import TZE_uta_darga_filter, TZE_uta_mergejilten_filter
from notifications.signals import notify
# Create your views here.

class Home(LoginRequired, TemplateView):
	perm_code_names = ['hzm_mergejilten_permission']
	template_name = 'hzm/hzm_home.html'


''' HZM mergejilten views START '''

class HZM_Huselt_list(Tza_Huselt_list): # tusgai zovshoorliin huseltiin shalgah list
	perm_code_names = ['hzm_mergejilten_permission']
	template_name = 'hzm/tz_huselt_shalgah/hzm_huselt_shalgah.html'
	def dispatch(self, request, *args, **kwargs):
		
		return super(HZM_Huselt_list, self).dispatch(request, *args, **kwargs)
	def get_queryset(self):
		queryset = TZ_Huselt.objects.exclude(yavts=u'Материал бүрдүүлэлт').exclude(yavts=u'Буцаагдсан')
		queryset = self.filter(queryset)
		return queryset
	def filter(self, queryset):
		return queryset
	def get_context_data(self, **kwargs):
		context = super(HZM_Huselt_list, self).get_context_data(**kwargs)
		#context['nots'] = Notification.objects.unread()
		return context


class HZM_tz_huselt_delgerengui(Tza_huselt_delgerengui):
	perm_code_names = ['hzm_mergejilten_permission']
	template_name = 'hzm/tz_huselt_shalgah/hzm_huselt_delgerengui.html'
class HZM_TZ_Sent_materialView(TZA_TZ_Sent_materialView):
	perm_code_names = ['hzm_mergejilten_permission']
	def get_material_check_url(self):
		return reverse_lazy('hzm_material_check', kwargs = {'burdel_history_id': self.burdel_history.id, 'material_number': self._material_number})
class HZM_TZ_Material_check(TZA_TZ_Material_check):
	perm_code_names = ['hzm_mergejilten_permission']
	def get_view_url(self, burdel_history_id, material_number):
		return reverse_lazy('hzm_material_check', kwargs={'burdel_history_id': burdel_history_id, 'material_number':material_number})
	def get_success_url(self):
		self.success_url = reverse_lazy('hzm_tz_huselt_delgerengui', kwargs={'huselt_id': self.burdel_history.tz_huselt.id})
		return super(TZA_TZ_Material_check, self).get_success_url()
class TZ_huselt_check_finish_hzm(TZ_huselt_check_finish_tza):
	perm_code_names = ['hzm_mergejilten_permission']
	def get(self, request, *args, **kwargs):
		self.view_url = reverse_lazy('huselt_check_finish_hzm', kwargs={'huselt_id': kwargs['huselt_id']})
		return super(TZ_huselt_check_finish_tza, self).get(request, *args, **kwargs)
	def post(self, request, *args, **kwargs):
		self.view_url = reverse_lazy('huselt_check_finish_hzm', kwargs={'huselt_id': self._huselt_id})
		return super(TZ_huselt_check_finish_tza, self).post(request, *args, **kwargs)

	def form_valid(self, form):
		print 'baksdgjalkdsjglakjdf;lasdkjfa;slkjfa;sl\n\n'
		burdel_history = burdel_history = Burdel_history.objects.filter(tz_huselt = self._tz_huselt).order_by('-ilgeesen_datetime').first()

		#print 'hzm huselt check finsih form valid\n\n'
		if burdel_history.is_hzm_materialiud_zovshoorson():
			burdel_history.hzm_check_finished = True # hzm shalgaj duussan. Huselt butsaagdah esehiig materialiudiin status yamar baihaas shaltgaalna
			burdel_history.save()


			if burdel_history.uta_check_finished == True and burdel_history.tza_check_finished == True:
				
				if burdel_history.is_all_zovshoorson():
					self._tz_huselt.change_yavts_to_bichig_barimt_OK()

					burdel_history.now_checking = False # dahij shalgah bolomjgui bolno
					burdel_history.save()

					messages.success(self.request, 'Амжилттай хадгаллаа. Бичиг баримтуудыг хүлээн авсан.')
				else:
					#print 'hzm tz huselt butsaah'
					self._tz_huselt.change_yavts_to_butsaagdsan()

					burdel_history.now_checking = False
					burdel_history.save()

					self._tz_huselt.burdel.material_butsaah_function()
					messages.success(self.request, 'Амжилттай хадгаллаа. Бичиг баримтууд буцаагдсан.')
			else:
				group_tza_darga = Group.objects.get(name = u'ТЗА дарга')
				notify.send(self._tz_huselt.tze, recipient=group_tza_darga, verb=self._tz_huselt.tze.org_name + ' ' + self._tz_huselt.tze.org_type + ' ' + u'тусгай зөвшөөрлийн хүсэлт илгээсэн байна.', url_data = reverse_lazy('tza darga huselt huvaarilah'))
				group_uta_darga = Group.objects.get(name = u'ҮТА дарга')
				notify.send(self._tz_huselt.tze, recipient=group_uta_darga, verb=self._tz_huselt.tze.org_name + ' ' + self._tz_huselt.tze.org_type + ' ' + u'тусгай зөвшөөрлийн хүсэлт илгээсэн байна.', url_data = reverse_lazy('uta darga huselt huvaarilah'))

				messages.success(self.request, 'Амжилттай хадгаллаа. Тусгай зөвшөөрлийн хүсэлтийг шалгаж дууслаа.')
		else:
			self._tz_huselt.change_yavts_to_butsaagdsan()

			burdel_history.now_checking = False
			burdel_history.save()

			self._tz_huselt.burdel.material_butsaah_function()
			messages.success(self.request, 'Амжилттай хадгаллаа. Тусгай зөвшөөрлийн хүсэлт буцаагдсан.')
		return super(TZ_huselt_check_finish_tza, self).form_valid(form)


''' HZM mergejilten views END '''



"""    HZM baiguullaga views START  """

class HZM_BaiguullagaaView(LoginRequired, TemplateView):
	perm_code_names = ['hzm_mergejilten_permission']
	template_name = "hzm/baiguullaga/baiguullaga.html"

	def get_user_objects(self):	# hereglegchid hamaaraltai objectuudiig get
		objects = TZE.objects.filter(status = True)
		return objects
	def get_filter_class(self):
		filter_class = HZM_tze_filter
		return filter_class
	def get_filter_form(self):
		filter_class = self.get_filter_class()
		return filter_class(self.request.GET)
	def get_filtered_objects(self, queryset):
		city = self.request.GET.get('city')
		district = self.request.GET.get('district')
		khoroo = self.request.GET.get('khoroo')
		tza_mergejilten = self.request.GET.get('tza_mergejilten')
		uta_mergejilten = self.request.GET.get('uta_mergejilten')
		tz_list = self.request.GET.getlist('tz')
		if city:
			queryset = queryset.filter(city = city)
		if district:
			queryset = queryset.filter(district = district)
		if khoroo:
			queryset = queryset.filter(khoroo = khoroo)
		if uta_mergejilten:
			rel_baigs_filtered = Rel_baig_zz_ajilchid.objects.filter(uta_mergejilten = uta_mergejilten)
			tzes_for_ajiltan = []
			for i in rel_baigs_filtered:
				tzes_for_ajiltan.append(i.tze.id)
			queryset = queryset.filter(id__in = tzes_for_ajiltan)
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
		return queryset

	def get_context_data(self, **kwargs):
		context = super(HZM_BaiguullagaaView, self).get_context_data(**kwargs)
		objects = self.get_user_objects()
		filter_form = self.get_filter_form()
		search_form = TZE_search(self.request.GET)
		context['filter_form'] = filter_form
		context['search_form'] = search_form
		if self.request.GET.get('search'):
			search = self.request.GET.get('search')
			context['baig'] = objects.filter(org_name__icontains = search) | objects.filter(reg_num = search) | objects.filter(ubd = search)
		else:
			context['baig'] = self.get_filtered_objects(queryset = objects)

		return context

class HZM_Baiguullaga_delgerengui(TZA_Baiguullaga_delgerengui):
	perm_code_names = ['hzm_mergejilten_permission']


"""    HZM baiguullaga views END  """



"""    HZM hunii noots views START  """
class HZM_AjiltanView(tzaAjiltanView):
	perm_code_names = ['hzm_mergejilten_permission']
	template_name = "hzm/hunii_noots/ajiltan.html"


class HZM_Ajiltan_delgerengui(TZA_Ajiltan_delgerengui):
	perm_code_names = ['hzm_mergejilten_permission']

	
"""    HZM hunii noots views END  """


"""    HZM tonog tohooromj views  START  """
class HZM_TohooromjjView(TZA_TohooromjjView):
	perm_code_names = ['hzm_mergejilten_permission']
	template_name = "hzm/tonog_tohooromj/tohooromj.html"

"""    HZM tonog tohooromj views  END  """


"""    HZM TZ gerchilgee views START  """

class HZM_TZ_gerchilgee_listView(TZA_TZ_gerchilgee_listView):
	perm_code_names = ['hzm_mergejilten_permission']
	template_name = 'hzm/tusgai_zovshoorol/hzm_tz_gerchilgee_list.html'
	queryset = Certificate.objects.filter(status = True)
	

class HZM_TZ_gerchilgee_delgerenguiView(TZA_TZ_gerchilgee_delgerenguiView):
	perm_code_names = ['hzm_mergejilten_permission']


"""    HZM TZ gerchilgee views END  """
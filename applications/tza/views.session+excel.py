# -*- coding: utf-8 -*-


from django.views.generic import FormView, View, TemplateView, UpdateView, ListView
from django.views.generic.edit import BaseFormView
from multiforms import MultiFormsView
from applications.app.views import LoginRequired
from applications.app.models import *
from applications.app.forms import *
from applications.tza.forms import *
from applications.engineering.filters import *
from applications.tza.filters import *
from applications.engineering.views import e_mail_sending
from applications.engineering.views import tailan_names
import datetime
import jsonpickle
import json
from django.core.exceptions import ObjectDoesNotExist
from multiforms import MultiFormsView
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
from applications.director.views import AjaxTemplateMixin
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.template import loader, RequestContext
from django.db.models import Min
from .filters import TZE_filter, TZE_search

class Tza_darga_huselt_huvaarilalt_list(LoginRequired, ListView):
	permission = 101
	super_permission = 102
	model = TZ_Huselt
	queryset = TZ_Huselt.objects.exclude(ilgeesen_datetime = None)
	context_object_name="tz_huselts"
	template_name = "tza/tza_darga_huselt_huvaarilah.html"

class TZ_huselt_huvaarilah(LoginRequired, FormView):
	permission = 101
	super_permission = 102
	form_class = TZ_huselt_tza_huvaarilahForm
	template_name = "div_htmls/tz_huselt_huvaarilah_div.html"
	success_url = reverse_lazy('tza darga huselt huvaarilah')

	def dispatch(self, request, *args, **kwargs):
		a = self.request.session['user']
		self._user = jsonpickle.decode(a)
		self._baiguullaga = self._user.user_id.baiguullaga
		self._huselt_id = self.kwargs['huselt_id']
		self._huselt = get_object_or_404(TZ_Huselt, id=self._huselt_id)
		return super(TZ_huselt_huvaarilah, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(TZ_huselt_huvaarilah, self).get_context_data(**kwargs)
		context['huselt_id'] = self._huselt_id
		context['tz_huselt'] = self._huselt
		return context
	def form_valid(self, form):
		self._huselt.tza_mergejilten = form.cleaned_data['tza_mergejilten']
		self._huselt.save()
		messages.success(self.request, 'Амжилттай хадгаллаа.')
		return super(TZ_huselt_huvaarilah, self).form_valid(form)
	def form_invalid(self, form):
		messages.error(self.request, 'Мэдээлэл дутуу бөглөгдсөн тул үйлдэл амжилтгүй боллоо.')
		return HttpResponseRedirect(self.get_success_url())

class TZ_huselt_hural_tovloh(TZ_huselt_huvaarilah):
	permission = 101
	super_permission = 102
	form_class = TZ_huselt_hural_tovlohForm
	template_name = "div_htmls/tz_huselt_hural_tovloh_div.html"

	def form_valid(self, form):
		self._huselt.hurliin_date = form.cleaned_data['hural_date']
		self._huselt.save()
		messages.success(self.request, 'Амжилттай хадгаллаа.')
		return HttpResponseRedirect(self.get_success_url())

class Ajliin_heseg_date_tovloh(TZ_huselt_huvaarilah):
	permission = 101
	super_permission = 102
	form_class = Ajliin_heseg_date_tovlohForm
	template_name = "div_htmls/ajliin_heseg_date_tovloh_div.html"

	def form_valid(self, form):
		self._huselt.ajliin_heseg_date = form.cleaned_data['date']
		self._huselt.save()
		messages.success(self.request, 'Амжилттай хадгаллаа.')
		return HttpResponseRedirect(self.get_success_url())

class TZ_huselt_huvaarilah_first_time(TZ_huselt_huvaarilah):
	permission = 101
	super_permission = 102
	form_class = TZ_huselt_first_timeForm
	template_name = "div_htmls/tz_huselt_first_time_div.html"

	def form_valid(self, form):
		if form.cleaned_data['choice'] == 'huleen_avsan':
			self._huselt.change_yavts_to_huseltiig_huleen_avsan()
			self._huselt.tza_mergejilten=form.cleaned_data['tza_mergejilten']
			self._huselt.huleen_avsan = True
		else:
			self._huselt.change_yavts_to_tsutslagdsan()
		self._huselt.save()
		messages.success(self.request, 'Амжилттай хадгаллаа.')
		return HttpResponseRedirect(self.get_success_url())

''' ТZA view '''
class Tza_Huselt_list(LoginRequired, TemplateView): # tusgai zovshoorliin huseltiin shalgah list
	permission = 103
	super_permission = 104
	template_name = 'tza/tza_huselt_shalgah.html'
	def dispatch(self, request, *args, **kwargs):
		a = self.request.session['user']
		self._user = jsonpickle.decode(a)
		self._baiguullaga = self._user.user_id.baiguullaga
		self._f = TZ_tze_Huselt_filter(self.request.GET, queryset = TZ_Huselt.objects.filter(tza_mergejilten = self._user.user_id))
		return super(Tza_Huselt_list, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(Tza_Huselt_list, self).get_context_data(**kwargs)
		context['tza_huselt_filter'] = self._f
		return context

class Tza_huselt_delgerengui(LoginRequired, TemplateView):
	permission = 103
	super_permission = 104
	template_name = 'div_htmls/tza_huselt_delgerengui.html'

	def dispatch(self, request, *args, **kwargs):
		a = self.request.session['user']
		self._user = jsonpickle.decode(a)
		self._baiguullaga = self._user.user_id.baiguullaga
		self._huselt_id = self.kwargs['huselt_id']
		return super(Tza_huselt_delgerengui, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(Tza_huselt_delgerengui, self).get_context_data(**kwargs)
		context['h'] = TZ_Huselt.objects.get(id = self._huselt_id)
		context['warnings'] = TZ_anhaaruulga.objects.filter(tz_huselt = context['h'])
		context['burdel_histories'] = Burdel_history.objects.filter(tz_huselt = context['h']).order_by('-ilgeesen_datetime')
		context['tz_huselt_medegdels'] = TZ_medegdel.objects.filter(tz_huselt = context['h'])
		return context

class TZ_shuud_olgolt_listView(LoginRequired, TemplateView):
	permission = 1
	super_permission = 2

	template_name = 'tza/tz_shuud_olgolt.html'

	def get_context_data(self, **kwargs):
		context = super(TZ_shuud_olgolt_listView, self).get_context_data(**kwargs)
		context['org'] = TZE.objects.filter(status=True)
		cert_org_dic = {}
		for o in context['org']:
			cert_org_dic[o.id] = Certificate.objects.filter(baiguullaga = o, status = True)
		context['cert_org_dic'] = cert_org_dic
		return context
class Material_check(LoginRequired, FormView):
	permission = 103
	super_permission = 104
	template_name = 'div_htmls/material_check.html'
	form_class = Material_check_form
	success_url = '/tza/huseltuud/'

	def dispatch(self, request, *args, **kwargs):
		a = self.request.session['user']
		self._user = jsonpickle.decode(a)
		self._baiguullaga = self._user.user_id.baiguullaga
		self._burdel_history_id = self.kwargs['burdel_history_id']
		self._material_number = self.kwargs['material_number']
		return super(Material_check, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(Material_check, self).get_context_data(**kwargs)
		context['burdel_history_id'] = self._burdel_history_id
		context['material_number'] = self._material_number
		context['material'] = get_object_or_404(TZ_material, material_number = self._material_number)
		return context

	def form_valid(self, form):
		burdel_history = get_object_or_404(Burdel_history, id = self._burdel_history_id)
		material = get_object_or_404(TZ_material, material_number = self._material_number)
		m = burdel_history.materialiud_list.get(material = material)
		
		
		if form.cleaned_data['status'] == 'zovshoorson':
			m.change_status_to_zovshoorson(timezone.now(), self._user)
		elif form.cleaned_data['status'] == 'hangaltgui':
			m.tatgalzsan_tailbar = form.cleaned_data['tailbar']
			m.change_status_to_hangaltgui(timezone.now(), self._user)

		messages.success(self.request, 'Амжилттай хадгаллаа.')
		return super(Material_check, self).form_valid(form)

	def form_invalid(self, form):
		messages.error(self.request, 'Мэдээллийг дутуу бөглөсөн тул үйлдэл амжилтгүй боллоо.')
		return HttpResponseRedirect(self.get_success_url())

class TZ_huselt_check_finish_tza(LoginRequired, FormView):
	permission = 103
	super_permission = 104
	template_name = 'div_htmls/tz_huselt_check.html'
	form_class = ShalgajDuussanForm
	success_url = '/tza/huseltuud/'

	def dispatch(self, request, *args, **kwargs):
		a = self.request.session['user']
		self._user = jsonpickle.decode(a)
		self._baiguullaga = self._user.user_id.baiguullaga
		self._huselt_id = self.kwargs['huselt_id']
		self._tz_huselt = get_object_or_404(TZ_Huselt, id=self._huselt_id)
		return super(TZ_huselt_check_finish_tza, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(TZ_huselt_check_finish_tza, self).get_context_data(**kwargs)
		context['huselt_id'] = self._huselt_id
		context['tz_huselt'] = self._tz_huselt
		return context

	def form_valid(self, form):
		self._tz_huselt.tza_checked_OK = True # tza shalgaj duussan. Huselt butsaagdah esehiig materialiudiin status yamar baihaas shaltgaalna
		self._tz_huselt.save()
		if self._tz_huselt.uta_checked_OK == True and self._tz_huselt.hzm_checked_OK == True:
			burdel_history = Burdel_history.objects.filter(tz_huselt = self._tz_huselt).order_by('-ilgeesen_datetime')[0]
			if burdel_history.is_all_zovshoorson():
				self._tz_huselt.change_yavts_to_bichig_barimt_OK()
				messages.success(self.request, 'Амжилттай хадгаллаа. Бичиг баримтуудыг хүлээн авсан.')
			else:
				self._tz_huselt.change_yavts_to_material_burduulelt()
				self._tz_huselt.burdel.change_materialiud_list()
				messages.success(self.request, 'Амжилттай хадгаллаа. Бичиг баримтууд буцаагдсан.')
		else:
			messages.success(self.request, 'Амжилттай хадгаллаа. Тусгай зөвшөөрлийн хүсэлтийг шалгаж дууслаа.')
		return super(TZ_huselt_check_finish_tza, self).form_valid(form)

	def form_invalid(self, form):
		messages.error(self.request, 'Мэдээллийг дутуу бөглөсөн тул үйлдэл амжилтгүй боллоо.')
		return HttpResponseRedirect(self.get_success_url())

class Hurliin_shiidver_saving(LoginRequired, FormView):
	permission = 103
	super_permission = 104
	template_name = 'div_htmls/hurliin_shiidver_saving.html'
	form_class = Hurliin_shiidver_Form
	success_url = '/tza/huseltuud/'

	def get_form_kwargs(self):
		kwargs = super(Hurliin_shiidver_saving, self).get_form_kwargs()
		tz_choices = TZ.objects.all()
		kwargs['tz_choices'] = tz_choices
		return kwargs

	def dispatch(self, request, *args, **kwargs):
		a = self.request.session['user']
		self._user = jsonpickle.decode(a)
		self._baiguullaga = self._user.user_id.baiguullaga
		self._huselt_id = self.kwargs['huselt_id']
		return super(Hurliin_shiidver_saving, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(Hurliin_shiidver_saving, self).get_context_data(**kwargs)
		context['huselt_id'] = self._huselt_id
		context['tz_huselt'] = get_object_or_404(TZ_Huselt, id = self._huselt_id)
		return context

	def form_invalid(self, form):
		messages.error(self.request, 'Мэдээллийг дутуу бөглөсөн тул үйлдэл амжилтгүй боллоо.')
		return HttpResponseRedirect(self.get_success_url())

	def form_valid(self, form):

		messages.success(self.request, 'Хурлын шийдвэрийг амжилттай хадгаллаа.')
		return super(Hurliin_shiidver_saving, self).form_valid(form)

class TZ_gerchilgee_status_change(LoginRequired, UpdateView):
	template_name = 'div_htmls/TZ_gerchilgee_olgoh.html'
	form_class = Certificate_status_change_Form
	success_url = '/tza/huseltuud/'


	def dispatch(self, request, *args, **kwargs):
		a = self.request.session['user']
		self._user = jsonpickle.decode(a)
		self._baiguullaga = self._user.user_id.baiguullaga
		self._huselt_id = self.kwargs['huselt_id']
		return super(TZ_gerchilgee_olgoh, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(TZ_gerchilgee_olgoh, self).get_context_data(**kwargs)
		context['huselt_id'] = self._huselt_id
		context['tz_huselt'] = get_object_or_404(TZ_Huselt, id = self._huselt_id)
		return context

	def form_valid(self, form):

		messages.success(self.request, 'Амжилттай хадгаллаа. Тусгай зөвшөөрлийн гэрчилгээ хүчинтэй болсон.')
		return super(TZ_gerchilgee_olgoh, self).form_valid(form)

	def form_invalid(self, form):
		messages.error(self.request, 'Мэдээллийг дутуу бөглөсөн тул үйлдэл амжилтгүй боллоо.')
		return HttpResponseRedirect(self.get_success_url())

class tzaTohooromjjView(LoginRequired, TemplateView):
	permission = 111
	super_permission = 112
	template_name = "tza/tohooromj.html"
	
	def get_context_data(self, **kwargs):
		context = super(tzaTohooromjjView, self).get_context_data(**kwargs)
		context['bb'] = BB.objects.filter(status=True)

		context['car']=Car.objects.filter(status=True)
		context['tonog']=Equipment.objects.filter(status=True)
		my_dic = {}
		for i in context['bb']:
 			if Hudag.objects.filter(id= i.id):
 				my_dic[i.id] = u'Худаг' 
	 		elif Nasos.objects.filter(id= i.id):
	 			my_dic[i.id]= u'Насос станц'
	 		elif Lab.objects.filter(id= i.id):
	 			my_dic[i.id]= u'Лаборатори'
	 		elif Sh_suljee.objects.filter(id= i.id):
	 			my_dic[i.id]= u'Шугам сүлжээ'
	 		elif UsanSan.objects.filter(id= i.id):
	 			my_dic[i.id]= u'Усансан'
	 		elif UsTugeehBair.objects.filter(id= i.id):
	 			my_dic[i.id]= u'Ус түгээх байр'
	 		elif UsDamjuulahBair.objects.filter(id= i.id):
	 			my_dic[i.id]= u'Ус, дулаан дамжуулах төв'
	 		elif Ts_baiguulamj.objects.filter(id= i.id):
	 			my_dic[i.id]= u'Цэвэрлэх байгууламж'

		context['my_dic'] = my_dic
		return context

class tzaAjiltanView(LoginRequired, TemplateView):
	permission = 109
	super_permission = 110
	template_name = "tza/ajiltan.html"
	def get_context_data(self, **kwargs):
		context = super(tzaAjiltanView, self).get_context_data(**kwargs)
		context['baig'] = TZE.objects.filter(status= True)	
		context['ajiltan'] = Ajiltan.objects.filter(baiguullaga= context['baig'])
		return context



class tzaBaiguullagaaView(LoginRequired, FormView):
	permission = 107
	super_permission = 108
	form_class = Baiguullaga_huvaarilalt_tza_Form
	template_name = "tza/baiguullaga.html"
	success_url = '/tza/baiguullaga/'
	def dispatch(self, request, *args, **kwargs):
		a = self.request.session['user']
		self._user = jsonpickle.decode(a)
		self._baiguullaga = self._user.user_id.baiguullaga
		return super(tzaBaiguullagaaView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(tzaBaiguullagaaView, self).get_context_data(**kwargs)
		all_tzes = TZE.objects.filter(status= True)		
		filter_form = TZE_filter(self.request.GET)
		search_form = TZE_search(self.request.GET)
		context['filter_form'] = filter_form
		context['search_form'] = search_form
		if self.request.GET.get('search_type'):
			search = self.request.GET.get('search')
			if self.request.GET.get('search_type') == '1':
				context['baig'] = all_tzes.filter(org_name = search)
			elif self.request.GET.get('search_type') == '2':
				context['baig'] = all_tzes.filter(reg_num = search)
			elif self.request.GET.get('search_type') == '3':
				context['baig'] = all_tzes.filter(ubd = search)
		else:
			filtered_tzes = all_tzes
			city = self.request.GET.get('city')
			district = self.request.GET.get('district')
			khoroo = self.request.GET.get('khoroo')
			tza_mergejilten = self.request.GET.get('tza_mergejilten')
			if city:
				filtered_tzes = filtered_tzes.filter(city = city)
			if district:
				filtered_tzes = filtered_tzes.filter(district = district)
			if khoroo:
				filtered_tzes = filtered_tzes.filter(khoroo = khoroo)
			if tza_mergejilten:
				tzes_for_ajiltan = Rel_baig_zz_ajilchid.objects.filter(tza_mergejilten = tza_mergejilten)
				filtered_tzes = filtered_tzes.filter(id__in = tzes_for_ajiltan)
			context['baig'] = filtered_tzes

		return context
	def form_valid(self, form):
		baig_ids = self.request.POST.getlist('chosen_baigs')
		all_baigs = TZE.objects.filter(status = True)
		#print "baig_ids: ", baig_ids
		for i in baig_ids:
			baig = all_baigs.get(id = i)
			r, created = Rel_baig_zz_ajilchid.objects.get_or_create(tze = baig)
			r.tza_mergejilten = form.cleaned_data['tza_mergejilten']
			r.created_by = self._user
			r.status = True
			r.save_and_history_writing()
		messages.success(self.request, 'Амжилттай хадгаллаа.')
		return super(tzaBaiguullagaaView, self).form_valid(form)

class TZA_Baiguullaga_delgerengui(LoginRequired, TemplateView):
	permission = 107
	super_permission = 108
	template_name = 'div_htmls/baiguullaga_delgerengui.html'
	def dispatch(self, request, *args, **kwargs):
		baig_id = kwargs['baiguullaga_id']
		self._object = get_object_or_404(TZE, id = baig_id)
		return super(TZA_Baiguullaga_delgerengui, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(TZA_Baiguullaga_delgerengui, self).get_context_data(**kwargs)
		context['baig'] = self._object
		context['cert'] = Certificate.objects.filter(baiguullaga = self._object, status = True)
		return context

class tzauatailanView(LoginRequired,TemplateView):
	permission = 115
	super_permission = 116
	template_name = "tza/uatailan.html"

	def dispatch(self, request, *args, **kwargs):
		a = self.request.session['user']
		self._user = jsonpickle.decode(a)
		self._baiguullaga = self._user.user_id.baiguullaga
		self._f = UAT_yavts_filter(self.request.GET, queryset = UAT_yavts.objects.all())
		return super(tzauatailanView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(tzauatailanView, self).get_context_data(**kwargs)
		context['uatailan_filter'] = self._f
		return context

class tzauatailanTZEView(LoginRequired,TemplateView):
	permission = 115
	super_permission = 116
	template_name = "tza/uatailan.html"

	def dispatch(self, request, *args, **kwargs):
		baig_id = kwargs['pk']
		self._object = get_object_or_404(TZE, id = baig_id)
		a = self.request.session['user']
		self._user = jsonpickle.decode(a)
		self._baiguullaga = self._user.user_id.baiguullaga
		self._f = UAT_yavts_filter(self.request.GET, queryset = UAT_yavts.objects.all())
		if request.method == "GET":
 			mm=  self._object
 			mmm= Hudag.objects.filter(tze= mm, status= True)
 			request.session['mmm'] = jsonpickle.encode(list(mmm))
		return super(tzauatailanTZEView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(tzauatailanTZEView, self).get_context_data(**kwargs)
		context['uatailan_filter'] = self._f
		context['baiguullaga']= self._object
		context['uatailan'] = UAT_yavts.objects.filter(tze=self._object, status= True)
		my_dict = {}
		if Hudag.objects.filter(tze = self._object,status=True):
			my_dict[1] = u'Боломжтой' 
		if UsanSan.objects.filter(tze = self._object,status=True) or Nasos.objects.filter(tze = self._object,status=True) or Lab.objects.filter(tze = self._object,status=True):
			my_dict[2] = u'Боломжтой'
		if AnalysisWater.objects.filter(tze = self._object,status=True):
			my_dict[3] = u'Боломжтой' 
		if Sh_suljee.objects.filter(tze = self._object,status=True):
			my_dict[4] = u'Боломжтой' 
		if ABB.objects.filter(tze = self._object,status=True):
			my_dict[5] = u'Боломжтой' 
		if Sh_suljee.objects.filter(tze = self._object,status=True):
			my_dict[6] = u'Боломжтой' 
		if Ts_baiguulamj.objects.filter(tze = self._object,status=True):
			my_dict[7] = u'Боломжтой' 
		if AnalysisBohir.objects.filter(tze = self._object,status=True):
			my_dict[8] = u'Боломжтой' 
		if UsTugeehBair.objects.filter(tze = self._object,status=True):
			my_dict[9] = u'Боломжтой' 
		if WaterCar.objects.filter(tze = self._object,status=True):
			my_dict[10] = u'Боломжтой' 
		if BohirCar.objects.filter(tze = self._object,status=True):
			my_dict[11] = u'Боломжтой' 
		if Ajiltan.objects.filter(baiguullaga = self._object,status=True):
			my_dict[12] = u'Боломжтой'
			my_dict[13] = u'Боломжтой'
			my_dict[14] = u'Боломжтой'
		context['my_dict'] = my_dict
		try:
			olgogdson = Certificate_tolov.objects.get(tolov = 'Олгогдсон')
		except ObjectDoesNotExist:
			olgogdson = Certificate_tolov.objects.create(tolov = 'Олгогдсон')
		tz_certificates = Certificate.objects.filter(baiguullaga = self._object,tolov = olgogdson)
		zaaltuud_choices = []
		if tz_certificates:	# tusgai zovshoorol ezemshij baival
			for i in tz_certificates:
				for j in i.tz_id.all():
					zaaltuud_choices.append(j.tz)
			tailans = tailan_names(zaaltuud_choices)
			context['tailans'] = tailans
		return context

class tzagshutailanView(LoginRequired,TemplateView):
	permission = 117
	super_permission = 118
	template_name = "tza/gshu_tailan.html"

	def dispatch(self, request, *args, **kwargs):
		a = self.request.session['user']
		self._user = jsonpickle.decode(a)
		self._baiguullaga = self._user.user_id.baiguullaga
		return super(tzagshutailanView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(tzagshutailanView, self).get_context_data(**kwargs)
		return context

class tzaNegtgelView(LoginRequired,TemplateView):
	permission = 119
	super_permission = 120
	template_name = "tza/negtgel.html"

	def dispatch(self, request, *args, **kwargs):
		a = self.request.session['user']
		self._user = jsonpickle.decode(a)
		self._baiguullaga = self._user.user_id.baiguullaga
		self._f = UAT_yavts_ognoo_filter(self.request.GET, queryset = UAT_yavts.objects.all())
		return super(tzaNegtgelView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(tzaNegtgelView, self).get_context_data(**kwargs)
		context['uatailan_filter'] = self._f
		my_dict = {}
		tzenuud= TZE.objects.all()
		if Hudag.objects.filter(tze = tzenuud, status=True):
			my_dict[1] = u'Боломжтой' 
		if UsanSan.objects.filter(tze = tzenuud, status=True) or Nasos.objects.filter(tze = tzenuud, status=True) or Lab.objects.filter(tze = tzenuud, status=True):
			my_dict[2] = u'Боломжтой'
		if AnalysisWater.objects.filter(tze = tzenuud, status=True):
			my_dict[3] = u'Боломжтой' 
		if Sh_suljee.objects.filter(tze = tzenuud, status=True):
			my_dict[4] = u'Боломжтой' 
		if ABB.objects.filter(tze = tzenuud, status=True):
			my_dict[5] = u'Боломжтой' 
		if Sh_suljee.objects.filter(tze = tzenuud, status=True):
			my_dict[6] = u'Боломжтой' 
		if Ts_baiguulamj.objects.filter(tze = tzenuud, status=True):
			my_dict[7] = u'Боломжтой' 
		if AnalysisBohir.objects.filter(tze = tzenuud, status=True):
			my_dict[8] = u'Боломжтой' 
		if UsTugeehBair.objects.filter(tze = tzenuud, status=True):
			my_dict[9] = u'Боломжтой' 
		if WaterCar.objects.filter(tze = tzenuud, status=True):
			my_dict[10] = u'Боломжтой' 
		if BohirCar.objects.filter(tze = tzenuud, status=True):
			my_dict[11] = u'Боломжтой' 
		if Ajiltan.objects.filter(baiguullaga = tzenuud, status=True):
			my_dict[12] = u'Боломжтой'
			my_dict[13] = u'Боломжтой'
			my_dict[14] = u'Боломжтой'
		context['my_dict'] = my_dict
		try:
			olgogdson = Certificate_tolov.objects.get(tolov = 'Олгогдсон')
		except ObjectDoesNotExist:
			olgogdson = Certificate_tolov.objects.create(tolov = 'Олгогдсон')
		tz_certificates = Certificate.objects.filter(baiguullaga = tzenuud,tolov = olgogdson)
		zaaltuud_choices = []
		if tz_certificates:	# tusgai zovshoorol ezemshij baival
			for i in tz_certificates:
				for j in i.tz_id.all():
					zaaltuud_choices.append(j.tz)
			tailans = tailan_names(zaaltuud_choices)
			context['tailans'] = tailans
		return context

class Tza_Huselt_list(LoginRequired, TemplateView): # tusgai zovshoorliin huseltiin shalgah list
	permission = 103
	super_permission = 104
	template_name = 'tza/tza_huselt_shalgah.html'
	def dispatch(self, request, *args, **kwargs):
		a = self.request.session['user']
		self._user = jsonpickle.decode(a)
		self._baiguullaga = self._user.user_id.baiguullaga
		self._f = TZ_tze_Huselt_filter(self.request.GET, queryset = TZ_Huselt.objects.filter(tza_mergejilten = self._user.user_id))
		return super(Tza_Huselt_list, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(Tza_Huselt_list, self).get_context_data(**kwargs)
		context['tza_huselt_filter'] = self._f
		return context


class TzaHome(LoginRequired, TemplateView):
	permission = 1
	super_permission = 2
	template_name = 'tzahome.html'

class Handah_erh_huselt_list(LoginRequired, TemplateView):
	permission = 1
	super_permission = 2
	template_name='tza/handah_erh_huselt_list.html'
	def get_context_data(self, **kwargs):
		context = super(Handah_erh_huselt_list, self).get_context_data(**kwargs)
		l = []
		for u in User.objects.all():
			l.append(u.user_id.baiguullaga.id)
		context['tze'] = TZE.objects.exclude(id__in = set(l))
		
		paginator1 = Paginator(TZE.objects.exclude(id__in = set(l)), 5)
		page1 = self.request.GET.get('page')
		try:
			context['tzee'] = paginator1.page(page1)
		except PageNotAnInteger:
			context['tzee'] = paginator1.page(1)
		except EmptyPage:
			context['tzee'] = paginator1.page(paginator1.num_pages)

		context['ajiltan'] = Ajiltan.objects.filter(baiguullaga = context['tze'])
		context['organization'] = TZE.objects.filter(id__in = set(l))
		paginator2 = Paginator(TZE.objects.filter(id__in = set(l)), 5)
		page2 = self.request.GET.get('page')
		try:
			context['org'] = paginator2.page(page2)
		except PageNotAnInteger:
			context['org'] = paginator2.page(1)
		except EmptyPage:
			context['org'] = paginator2.page(paginator2.num_pages)

		cert_org_dic = {}
		for o in context['org']:
			cert_org_dic[o.id] = Certificate.objects.filter(baiguullaga = o, status = True)
		context['cert_org_dic'] = cert_org_dic
		return context
	

class Add_baiguullaga(LoginRequired, FormView):
	form_class = TZEForm
	template_name='div_htmls/add_baiguullaga_div.html'
	success_url = reverse_lazy('tz shuud olgoh list')
	def form_valid(self, form):
		a=form.save()
		request_email(self.request, id=a['baiguullaga'].id)
		return super(Add_baiguullaga, self).form_valid(form)

def request_email(request, id = 0):
	try:
		user = Ajiltan.objects.get(baiguullaga = TZE.objects.get(id=id))
		password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
		e_mail_subject = "Бүртгэл амжилттай хийгдлээ"
		body = "Бүртгэл амжилтай хийгдлээ. Нууц үг: " + password
		e_mail_sending('wsrcmon@gmail.com', user.e_mail, e_mail_subject, body, 'QjErHKfS76KmRQBB')
		User.objects.create(user_id = user, username = user.e_mail, password = password, status = True)
	except:
		pass
	return HttpResponseRedirect('/tza/')

def remove_email(request, id = 0):
	try:
		user = Ajiltan.objects.get(baiguullaga = TZE.objects.get(id=id))
		e_mail_subject = "Таны хүсэлт цуцлагдлаа"
		body = ""
		e_mail_sending('wsrcmon@gmail.com', user.e_mail, e_mail_subject, body, 'QjErHKfS76KmRQBB')
		TZE.objects.get(id=id).delete()
	except:
		pass
	return HttpResponseRedirect('/tza/')

"""
class Baig_huvaarilalt_update(LoginRequired, UpdateView):
	template_name = 'baig_huvaarilalt_update.html'
	form_class = Baiguullaga_huvaarilaltForm
	success_url = reverse_lazy('home_tza')

	def dispatch(self, request, *args, **kwargs):
		a = self.request.session['user']
		self._user = jsonpickle.decode(a)
		self._baiguullaga = self._user.user_id.baiguullaga
		self._b_id = self.kwargs['baiguullaga_id']
		return super(Baig_huvaarilalt_update, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(Baig_huvaarilalt_update, self).get_context_data(**kwargs)
		context['baiguullaga_id'] = self._b_id
		return context


	def get_object(self, queryset = None):
		tze = TZE.objects.get(id = self._b_id)
		try:
			m = Rel_baig_zz_ajilchid.objects.get(tze = tze)
		except ObjectDoesNotExist:
			m = Rel_baig_zz_ajilchid(tze = tze, uta_mergejilten = None, tza_mergejilten = None, created_by = self._user, status = True)
			m.save_and_history_writing()
		return m

	def form_valid(self, form):
		self.object = form.save(commit = False)
		self.object.status = True
		self.object.created_by = self._user
		self.object.save_and_history_writing()
		response_data = {}
		response_data['result'] = 'Create post successful!'
		response_data['tze'] = self.object.tze.org_name
		response_data['uta_mergejilten'] = self.object.uta_mergejilten.emp_name
		response_data['tza_mergejilten'] = self.object.tza_mergejilten.emp_name
		if self.request.is_ajax():
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		else:
			messages.success(self.request, 'Амжилттай хадгаллаа.')
			return super(Baig_huvaarilalt_update, self).form_valid(form)
			
	def form_invalid(self, form):
		messages.error(self.request, 'Мэдээллийг дутуу бөглөсөн тул үйлдэл амжилтгүй боллоо.')
		return HttpResponseRedirect(self.get_success_url())
		"""

class Baig_huvaarilalt_bundle(LoginRequired, FormView):
	template_name = 'baig_huvaarilalt_bundle.html'
	form_class = Baig_huvaarilalt_bundleForm
	success_url = reverse_lazy('home_tza')

class Show_gerchilgee(LoginRequired, TemplateView):
	permission = 1
	super_permission = 2
	template_name = 'div_htmls/show_gerchilgee.html'

	def dispatch(self, request, *args, **kwargs):
		a = self.request.session['user']
		self._user = jsonpickle.decode(a)
		self._baiguullaga = self._user.user_id.baiguullaga
		self._b_id = self.kwargs['baiguullaga_id']
		return super(Show_gerchilgee, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(Show_gerchilgee, self).get_context_data(**kwargs)
		context['certs'] = Certificate.objects.filter(baiguullaga = self._b_id, status = True)
		tze = TZE.objects.get(id = self._b_id)
		context['tze'] = tze
		return context

class TZ_shuud_olgoh(LoginRequired, FormView):
	permission = 1
	super_permission = 2
	template_name = 'div_htmls/TZ_shuud_olgoh_div.html'
	success_url = reverse_lazy('tz shuud olgoh list')
	form_class = Certificate_giving_Form
	
	def get_form_kwargs(self):
		kwargs = super(TZ_shuud_olgoh, self).get_form_kwargs()
		tz_choices = TZ.objects.all()
		kwargs['tz_choices'] = tz_choices
		return kwargs

	def dispatch(self, request, *args, **kwargs):
		a = self.request.session['user']
		self._user = jsonpickle.decode(a)
		self._baiguullaga = self._user.user_id.baiguullaga
		self._b_id = self.kwargs['baiguullaga_id']
		self._tze = get_object_or_404(TZE, id = self._b_id)
		return super(TZ_shuud_olgoh, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(TZ_shuud_olgoh, self).get_context_data(**kwargs)
		context['baiguullaga_id'] = self._b_id
		return context

	def form_valid(self, form):
		new_tz_certificate = form.save(commit = False)
		new_tz_certificate.baiguullaga = self._tze
		new_tz_certificate.change_tolov_to_olgogdson()
		new_tz_certificate.begin_time = timezone.now()
		new_tz_certificate.created_by = self._user
		new_tz_certificate.status = True
		new_tz_certificate.save()

		tz_ids = form.cleaned_data.get("tz_id")
		new_tz_certificate.tz_id.clear()
		for i in tz_ids:
			new_tz_certificate.tz_id.add(i)

		new_tz_certificate.history_writing()
		messages.success(self.request, 'Амжилттай хадгаллаа.')
		return super(TZ_shuud_olgoh, self).form_valid(form)

	def form_invalid(self, form):
		messages.error(self.request, 'Мэдээллийг дутуу бөглөсөн тул үйлдэл амжилтгүй боллоо.')
		return HttpResponseRedirect(self.get_success_url())


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
	 		elif Nasos.objects.filter(id= bbbb.id):
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
#	ner= request.session[0]
#	hudag = Hudag.objects.filter(status=True)
	hudag = list(jsonpickle.decode(request.session['mmm']))
	for row, rowdata in enumerate(hudag):
		for col, val in enumerate(rowdata):
			if isinstance(val, datetime):
				worksheet1.write(row,col,val.strftime('%d/%m/%Y'), body)
			worksheet1.write(row,col,val, body)
	workbook.close()
	xlsx_data = output.getvalue()
	

	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=UATailan.xlsx'
	response.write(xlsx_data)
	return response
 	#   Хүснэгт 11
# 	worksheet1.merge_range('B1:J1', ner.org_name, title)
'''	title_text1 = u"Ус хангамжийн эх үүсвэрийн барилга байгууламжийн судалгаа"
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
			worksheet1.merge_range(4,2, len(hudag)+ 3,2,  u'Гүний худаг', body)'''


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
#	ner= request.session[0]
#	hudag = Hudag.objects.filter(status=True)
	hudag = list(request.session[0])
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
	workbook.close()
	xlsx_data = output.getvalue()
	return xlsx_data


'''

	usansan = UsanSan.objects.filter(status=True)
	nasos = Nasos.objects.filter(status=True)
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
#	worksheet14.write('G8', ajiltanErh3.e_mail, body)'''
	
	
	
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
	nasos = Nasos.objects.filter(status=True)
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

	
	

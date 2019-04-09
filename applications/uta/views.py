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
from applications.tza.views import TZA_TohooromjjView, TZA_Gunii_Hudag_list, TZA_Usan_San_list, Base_List_FilterView
from applications.tza.views import TZA_Nasos_list, TZA_Lab_list, TZA_Sh_Suljee_list, TZA_Ts_Baiguulamj_list
from applications.tza.views import TZA_Us_Tugeeh_list, TZA_Us_Damjuulah_list, TZA_Water_Car_list, TZA_ABB_list, TZA_Us_hangamjiin_schema_zurag_list
from applications.tza.views import TZA_Bohir_Car_list, TZA_Tonog_Tohooromj_list, tzaAjiltanView, TZA_Ajiltan_delgerengui, TZA_TZ_Material_check, TZA_TZ_Sent_materialView
from applications.tza.views import TZA_Baiguullaga_delgerengui, TZA_TZ_gerchilgee_listView, TZA_TZ_gerchilgee_delgerenguiView, Tza_huselt_delgerengui, TZ_huselt_check_finish_tza, tzagshutailanView
from applications.tza.filters import Ajiltan_filter, TZE_search, TZ_huselt_tza_filter

from applications.engineering.views import Base_Ajax_FormView
from applications.director.models import *
from django_messages.models import Message
from django.core.paginator import Paginator, Page, EmptyPage, PageNotAnInteger
from notifications.signals import notify
# Create your views here.

class Home(LoginRequired, TemplateView):
	perm_code_names = ['uta_mergejilten_permission']
	template_name = 'uta/uta_home.html'

''' UTA darga views START'''

class UTA_darga_huselt_huvaarilalt_list(LoginRequired, ListView, Base_List_FilterView):
	perm_code_names = ['uta_darga_permission']
	context_object_name="tz_huselts"
	template_name = "uta/tz_huselt_huvaarilah/uta_darga_huselt_huvaarilah.html"
	filter_class = TZ_huselt_huvaarilah_uta_filter
	def get_context_data(self, **kwargs):
		context = super(UTA_darga_huselt_huvaarilalt_list, self).get_context_data(**kwargs)
		context['filter_form'] = self.get_filter()
		return context
	def get_queryset(self):
		queryset = TZ_Huselt.objects.exclude(yavts=u'Материал бүрдүүлэлт').exclude(yavts=u'Буцаагдсан') #| TZ_Huselt.objects.filter(hzm_checked_OK = True, yavts = material_huleen_avsan)
		exclude_id_list=[]
		for i in queryset:
			burdel_history = Burdel_history.objects.filter(tz_huselt = i).order_by('-ilgeesen_datetime').first()
			#print i
			if burdel_history:
				if burdel_history.hzm_check_finished == False:
					#print 'haha'
					exclude_id_list.append(i.id)

		for i in exclude_id_list:
			queryset = queryset.exclude(id = i)
		queryset = self.filter(queryset)
		return queryset

	def filter(self, queryset):
		return queryset

class TZ_huselt_uta_huvaarilah(Base_Ajax_FormView):
	perm_code_names = ['uta_darga_permission']
	form_class = TZ_huselt_uta_huvaarilahForm
	template_name = "uta/tz_huselt_huvaarilah/form_div_htmls/tz_huselt_uta_huvaarilah_div.html"
	success_url = reverse_lazy('uta darga huselt huvaarilah')

	def dispatch(self, request, *args, **kwargs):
		self._huselt_id = self.kwargs['huselt_id']
		self._huselt = get_object_or_404(TZ_Huselt, id=self._huselt_id)
		return super(TZ_huselt_uta_huvaarilah, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(TZ_huselt_uta_huvaarilah, self).get_context_data(**kwargs)
		context['huselt_id'] = self._huselt_id
		context['tz_huselt'] = self._huselt
		return context
	def form_valid(self, form):
		uta_mergejilten_user = get_object_or_404(User, user_id = form.cleaned_data['uta_mergejilten'])

		self._huselt.uta_mergejilten = form.cleaned_data['uta_mergejilten']
		self._huselt.save()

		notify.send(self._huselt.tze, recipient=uta_mergejilten_user, verb=self._huselt.tze.org_name + ' ' + self._huselt.tze.org_type + u' илгээсэн ТЗ хүсэлтийг таньд хуваарилалаа.', url_data = reverse_lazy('uta huselt check'))

		messages.success(self.request, 'Амжилттай хадгаллаа.')
		return super(TZ_huselt_uta_huvaarilah, self).form_valid(form)


''' UTA darga views END '''

''' UTA mergejilten views START '''

class UTA_Huselt_list(LoginRequired, ListView, Base_List_FilterView): # tusgai zovshoorliin huseltiin shalgah list
	perm_code_names = ['uta_mergejilten_permission']
	template_name = 'uta/tz_huselt_shalgah/uta_huselt_shalgah.html'
	context_object_name="tz_huseltuud"
	filter_class = TZ_huselt_tza_filter
	def get_context_data(self, **kwargs):
		context = super(UTA_Huselt_list, self).get_context_data(**kwargs)
		context['filter_form'] = self.get_filter()
		return context
	def get_queryset(self):
		queryset = TZ_Huselt.objects.filter(uta_mergejilten = self.user.user_id).exclude(yavts=u'Материал бүрдүүлэлт').exclude(yavts=u'Буцаагдсан')
		queryset = self.filter(queryset)
		return queryset
	def filter(self, queryset):
		return queryset
class UTA_tz_huselt_delgerengui(Tza_huselt_delgerengui):
	perm_code_names = ['uta_mergejilten_permission']
	template_name = 'uta/tz_huselt_shalgah/uta_huselt_delgerengui.html'
class UTA_TZ_Sent_materialView(TZA_TZ_Sent_materialView):
	perm_code_names = ['uta_mergejilten_permission']
	def get_material_check_url(self):
		return reverse_lazy('uta_material_check', kwargs = {'burdel_history_id': self.burdel_history.id, 'material_number': self._material_number})
class UTA_TZ_Material_check(TZA_TZ_Material_check):
	perm_code_names = ['uta_mergejilten_permission']
	def get_view_url(self, burdel_history_id, material_number):
		return reverse_lazy('uta_material_check', kwargs={'burdel_history_id': burdel_history_id, 'material_number':material_number})
	def get_success_url(self):
		self.success_url = reverse_lazy('uta_tz_huselt_delgerengui', kwargs={'huselt_id': self.burdel_history.tz_huselt.id})
		return super(TZA_TZ_Material_check, self).get_success_url()
class TZ_huselt_check_finish_uta(TZ_huselt_check_finish_tza):
	perm_code_names = ['uta_mergejilten_permission']
	def get(self, request, *args, **kwargs):
		self.view_url = reverse_lazy('huselt_check_finish_uta', kwargs={'huselt_id': kwargs['huselt_id']})
		return super(TZ_huselt_check_finish_tza, self).get(request, *args, **kwargs)
	def post(self, request, *args, **kwargs):
		self.view_url = reverse_lazy('huselt_check_finish_uta', kwargs={'huselt_id': self._huselt_id})
		return super(TZ_huselt_check_finish_tza, self).post(request, *args, **kwargs)
	def form_valid(self, form):
		burdel_history = Burdel_history.objects.filter(tz_huselt = self._tz_huselt).order_by('-ilgeesen_datetime').first()
		burdel_history.uta_check_finished = True # tza shalgaj duussan. Huselt butsaagdah esehiig materialiudiin status yamar baihaas shaltgaalna
		burdel_history.save()
		if burdel_history.hzm_check_finished == True and burdel_history.tza_check_finished == True:
			if burdel_history.is_all_zovshoorson():
				self._tz_huselt.change_yavts_to_bichig_barimt_OK()

				burdel_history.now_checking = False # dahij shalgah bolomjgui bolno
				burdel_history.save()

				messages.success(self.request, 'Амжилттай хадгаллаа. Бичиг баримтуудыг хүлээн авсан.')
			else:
				self._tz_huselt.change_yavts_to_butsaagdsan()

				burdel_history.now_checking = False # dahij shalgah bolomjgui bolno
				burdel_history.save()

				self._tz_huselt.burdel.material_butsaah_function()
				messages.success(self.request, 'Амжилттай хадгаллаа. Бичиг баримтууд буцаагдсан.')
		else:
			messages.success(self.request, 'Амжилттай хадгаллаа. Тусгай зөвшөөрлийн хүсэлтийг шалгаж дууслаа.')
		return super(TZ_huselt_check_finish_tza, self).form_valid(form)


''' UTA mergejilten views END '''



"""    UTA baiguullaga views START  """

class UTA_BaiguullagaaView(LoginRequired, FormView):
	perm_code_names = ['uta_mergejilten_permission']
	form_class = Baiguullaga_huvaarilalt_uta_Form
	template_name = "uta/baiguullaga/baiguullaga.html"
	success_url = '/uta/baiguullaga/'

	def get_user_objects(self):	# hereglegchid hamaaraltai objectuudiig get
		objects = TZE.objects.filter(status = True)
		if not self.user.has_uta_darga_permission():
			rel_baigs = Rel_baig_zz_ajilchid.objects.filter(uta_mergejilten = self.user.user_id)
			tzes_for_ajiltan = []
			for i in rel_baigs:
				tzes_for_ajiltan.append(i.tze.id)
			objects = objects.filter(id__in = tzes_for_ajiltan)
		return objects
	def get_filter_class(self):
		if self.user.has_uta_darga_permission():
			filter_class = TZE_uta_darga_filter
		else:
			filter_class = TZE_uta_mergejilten_filter
		return filter_class
	def get_filter_form(self):
		filter_class = self.get_filter_class()
		return filter_class(self.request.GET)
	def get_filtered_objects(self, queryset):
		if self.user.has_uta_darga_permission():
			city = self.request.GET.get('city')
			district = self.request.GET.get('district')
			khoroo = self.request.GET.get('khoroo')
			uta_mergejilten = self.request.GET.get('uta_mergejilten')
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
		else:
			city = self.request.GET.get('city')
			district = self.request.GET.get('district')
			khoroo = self.request.GET.get('khoroo')
			if city:
				queryset = queryset.filter(city = city)
			if district:
				queryset = queryset.filter(district = district)
			if khoroo:
				queryset = queryset.filter(khoroo = khoroo)
		return queryset

	def get_context_data(self, **kwargs):
		context = super(UTA_BaiguullagaaView, self).get_context_data(**kwargs)
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
	def form_valid(self, form):
		baig_ids = self.request.POST.getlist('chosen_baigs')
		all_baigs = TZE.objects.filter(status = True)
		for i in baig_ids:
			baig = all_baigs.get(id = i)
			r, created = Rel_baig_zz_ajilchid.objects.get_or_create(tze = baig)
			r.uta_mergejilten = form.cleaned_data['uta_mergejilten']
			r.created_by = self.user
			r.status = True
			r.save()
			#r.save_and_history_writing()
		messages.success(self.request, 'Амжилттай хадгаллаа.')

		return super(UTA_BaiguullagaaView, self).form_valid(form)

class UTA_Baiguullaga_delgerengui(TZA_Baiguullaga_delgerengui):
	perm_code_names = ['uta_mergejilten_permission']

"""    UTA baiguullaga views END  """



"""    UTA hunii noots views START  """
class UTA_AjiltanView(tzaAjiltanView):
	perm_code_names = ['uta_mergejilten_permission']
	template_name = "uta/hunii_noots/ajiltan.html"


class UTA_Ajiltan_delgerengui(TZA_Ajiltan_delgerengui):
	perm_code_names = ['uta_mergejilten_permission']
	template_name = 'tza/hunii_noots/delgerengui_div_htmls/ajiltan_delgerengui.html'
	
"""    UTA hunii noots views END  """


"""    UTA tonog tohooromj views  START  """
class UTA_TohooromjjView(TZA_TohooromjjView):
	perm_code_names = ['uta_mergejilten_permission']
	template_name = "uta/tonog_tohooromj/tohooromj.html"

"""    UTA tonog tohooromj views  END  """


"""    UTA TZ gerchilgee views START  """

class UTA_TZ_gerchilgee_listView(TZA_TZ_gerchilgee_listView):
	perm_code_names = ['uta_mergejilten_permission']
	template_name = 'uta/tusgai_zovshoorol/uta_tz_gerchilgee_list.html'


class UTA_TZ_gerchilgee_delgerenguiView(TZA_TZ_gerchilgee_delgerenguiView):
	perm_code_names = ['uta_mergejilten_permission']
	


"""    UTA TZ gerchilgee views END  """






class UTA_gshutailanView(tzagshutailanView):
	perm_code_names = ['uta_mergejilten_permission']
	template_name = "uta/gshu_tailan/gshu_tailan.html"




class Paginator1(Paginator):

	def _get_page(self, *args ,**kwargs):
		return Page1(*args, **kwargs)

class Page1(Page):

	def has_two_previous(self):
		return self.number > 2

	def has_two_next(self):
		return self.number < self.paginator.num_pages-1

	def two_next_page_number(self):
		return self.paginator.validate_number(self.number + 2)

	def two_previous_page_number(self):
		return self.paginator.validate_number(self.number - 2)



class Report(LoginRequired, TemplateView):
	perm_code_names = ['uta_mergejilten_permission']
	template_name = 'report.html'

	def get_context_data(self, *args, **kwargs):
		context = super(Report, self).get_context_data(**kwargs)
		context['filter'] = BaiguullagaFilterForm
		if self.request.GET.get('name'):
			a = self.request.GET.get('name')
			context['orgs'] = TZE.objects.filter(org_name__icontains = a)
			context['not_pagination'] = False
		else:
			paginator = Paginator1(TZE.objects.all(), 10)
			page = self.request.GET.get('page')
			context['not_pagination'] = True
			try:
				context['orgs'] = paginator.page(page)
			except PageNotAnInteger:
				context['orgs'] = paginator.page(1)
			except EmptyPage:
				context['orgs'] = paginator.page(paginator.num_pages)
		return context


class ReportOrg(LoginRequired, TemplateView):
	perm_code_names = ['uta_mergejilten_permission']
	template_name = 'report_org.html'

	def get_context_data(self, *args, **kwargs):
		context = super(ReportOrg, self).get_context_data(*args, **kwargs)
		print(self.kwargs['org'])
		context['tailan'] = Sudalgaa.objects.filter(tze__id = self.kwargs['org'], yvts = u'Хүлээн авсан')
		context['org'] = TZE.objects.get(id = self.kwargs['org'])
		return context

class CheckSezView(LoginRequired, Base_List_FilterView, TemplateView):
	perm_code_names = ['uta_mergejilten_permission']
	template_name = 'check_sez.html'

	def get_context_data(self, *args, **kwargs):
		context = super(CheckSezView, self).get_context_data(*args, **kwargs)
		context['tailan'] = SariinTailan.objects.filter(tze__in = self.get_mergejilten_tzes(), yvts__in = [u'Илгээсэн', u'Буцаасан', u'Хүлээн авсан'], month__gt = 0).order_by('yvts','-month')
		return context

class CheckListView(LoginRequired, TemplateView):
	perm_code_names = ['uta_mergejilten_permission']
	template_name = 'checklist.html'

	def get_context_data(self, **kwargs):
		context = super(CheckListView, self).get_context_data(**kwargs)
		context['baiguullaga'] = TZE.objects.get(id = self.kwargs['org'])
		context['tailan'] = SariinTailan.objects.get(tze__id = self.kwargs['org'], id = self.kwargs['id'])
		context['hereglegch'] = context['tailan'].hereglegch
		context['golch'] = context['tailan'].golch_return()
		context['golch_hangagch'] = context['tailan'].golch_hangagch_return()
		context['tariffgolch'] = context['tailan'].tariff_hereglegch_golch()
		context['tariffus'] = context['tailan'].tariff_hereglegch_us()
		context['ol'] = context['tailan'].olborlolt
		return context

@csrf_exempt
def tolov(request):
	if request.method == "POST":
		a = request.POST.getlist('tailan')
		b = request.POST.get('t')
		if b == '1':
			for i in a:
				b = SariinTailan.objects.get(id = i)
				b.yvts = u'Буцаасан'
				b.tailan_status = True
				b.save()
		else:
			for i in a:
				b = SariinTailan.objects.get(id = i)
				b.yvts = u'Хүлээн авсан'
				tailan_status = False
				b.save()
		return HttpResponseRedirect('/uta/sez/')













#  Үнэ тарифын алба санхүүгийн судалгаа шалгах

class SudalgaaList(LoginRequired, ListView):
	perm_code_names = ['uta_mergejilten_permission']
	queryset = Sudalgaa.objects.filter(yvts__in = [u'Илгээсэн', u'Буцаасан', u'Хүлээн авсан'])

	'''def get_context_data(self, *args, **kwargs):
		context = super(Report, self).get_context_data(**kwargs)
		context['filter'] = BaiguullagaFilterForm
		if self.request.GET.get('name'):
			a = self.request.GET.get('name')
			context['orgs'] = TZE.objects.filter(org_name__icontains = a)
			context['not_pagination'] = False
		else:
			paginator = Paginator1(TZE.objects.all(), 10)
			page = self.request.GET.get('page')
			context['not_pagination'] = True
			try:
				context['orgs'] = paginator.page(page)
			except PageNotAnInteger:
				context['orgs'] = paginator.page(1)
			except EmptyPage:
				context['orgs'] = paginator.page(paginator.num_pages)
		return context'''


class SudalgaaSelf(LoginRequired, TemplateView):
	template_name = 'director/sudalgaa.html'

	def get_context_data(self, *args, **kwargs):
		context = super(SudalgaaSelf, self).get_context_data(*args, **kwargs)
		try:
			context['sudalgaa'] = Sudalgaa.objects.get(id = self.kwargs.pop('id', None))
		except: pass
		return context

	@staticmethod
	def sudalgaa_tolov_huleen_avah(request, id = 0):
		a = Sudalgaa.objects.get(id = id)
		a.yvts = u'Хүлээн авсан'
		a.save()
		return HttpResponseRedirect(reverse('sudalgaa_self', args=[id]))

	@staticmethod
	def sudalgaa_tolov_butsaah(request, id = 0):
		a = Sudalgaa.objects.get(id = id)
		a.yvts = u'Буцаасан'
		a.save()
		return HttpResponseRedirect(reverse('sudalgaa_self', args=[id]))
	

def sudalgaa_husnegt(request, org_id = 0, id = 0, table_id = 0):
	context = {}
	context['org'] = TZE.objects.get(id = org_id)
	context['sudalgaa'] = Sudalgaa.objects.get(id = id)

	if table_id == '1':
		return render_to_response('husnegt/1.html', context)
	elif table_id == '2':
		return render_to_response('sudalgaa/2.html', context)
	elif table_id == '3':
		return render_to_response('husnegt/3.html', context)
	elif table_id == '4':
		return render_to_response('sudalgaa/4.html', context)
	elif table_id == '5':
		return render_to_response('sudalgaa/5.html', context)
	elif table_id == '6':
		return render_to_response('sudalgaa/6.html', context)
	elif table_id == '7':
		return render_to_response('sudalgaa/7.html', context)
	elif table_id == '8':
		return render_to_response('sudalgaa/8.html', context)
	elif table_id == '9':
		return render_to_response('sudalgaa/9.html', context)
	elif table_id == '10':
		return render_to_response('sudalgaa/10.html', context)
	elif table_id == '11':
		return render_to_response('sudalgaa/11.html', context)
	elif table_id == '12':
		count0 = count1 = 0
		for i in range(15):
			context['sum%s' %i] = context['sudalgaa'].example(i)
			count0 += context['sum%s' %i]
			context['nem%s' %i] = context['sudalgaa'].example(i) * 12
			count1 += context['nem%s' %i]
		context['count0'] = count0
		context['count1'] = count1
		return render_to_response('sudalgaa/12.html', context)
	elif table_id == '13':
		return render_to_response('sudalgaa/13.html', context)
	elif table_id == '14':
		return render_to_response('sudalgaa/14.html', context)
	elif table_id == '15':
		return render_to_response('sudalgaa/15.html', context)
	elif table_id == '16':
		return render_to_response('sudalgaa/16.html', context)

class MessageView(LoginRequired, FormView):
	template_name = 'director/sudalgaa_message.html'
	form_class = MessageForm
	success_url = reverse_lazy('sudalgaa_list')

	def form_valid(self, form):
		a = self.kwargs.pop('id', None)
		b = User.objects.filter(user_id__baiguullaga__id = a)
		for i in b:
			Message.objects.create(
				subject = form.cleaned_data['subject'],
				body = form.cleaned_data['body'],
				sender = self.user,
				recipient = i
				)
		return super(MessageView, self).form_valid(form)

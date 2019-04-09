# -*- coding: utf-8 -*-
import datetime
import jsonpickle
import json
import xlrd
import xlsxwriter
import StringIO
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, MultipleObjectsReturned
from django.core.mail import EmailMessage, send_mail
from django.views.generic import FormView, View, TemplateView, UpdateView, CreateView, ListView
from applications.app.views import LoginRequired
from applications.app.forms import *
from .forms import *
from applications.app.models import *
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseForbidden, JsonResponse
import random
import string
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader, RequestContext
from django.db.models import Min, Count, Sum as s
from django import forms as f
from django.forms.utils import ErrorList
from django.forms.models import inlineformset_factory
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.forms.formsets import formset_factory
from django.forms import modelformset_factory
from .filters import TZ_tze_Huselt_filter, UAT_yavts_ognoo_filter
from applications.director.models import SariinTailan
from django.contrib.auth.models import Group
from notifications.signals import notify
import threading

''' Engineering view '''


def tze_notifications_set_read(request):
	if request.is_ajax():
		if request.user.is_authenticated():
			request.user.notifications.unread().mark_all_as_read()
			return HttpResponse('set all as read successfully')
		else:
			return HttpResponse('user is not is_authenticated')
	


############################################################# UILSEE CODE START ###############################################


def e_mail_sending(toaddr, subject, body):
	try:
		#email = EmailMessage(subject, body, to = [toaddr])
		#email.send()
		send_mail(subject, body, 'wsrcmon@gmail.com', [toaddr])

		print "successfully sent\n"
	except:
		print "failed\n"

class E_mail_sending_thread(threading.Thread):
	def __init__(self, toaddr, subject, body):
		threading.Thread.__init__(self)
		self.toaddr = toaddr
		self.subject = subject
		self.body = body
	def run(self):
		e_mail_sending(self.toaddr, self.subject, self.body)

class Base_Ajax_FormView(LoginRequired, FormView):
	view_url = '/'
	
	
	def get_context_data(self, **kwargs):
		context = super(Base_Ajax_FormView, self).get_context_data(**kwargs)
		context['view_url'] = self.view_url
		return context


class Base_DeleteView(FormView):
	form_class = EmptyForm
	template_name = 'tonog_tohooromj/form_div_htmls/tze_general_delete.html'
	delete_message = 'Мэдээллийг устгалаа.'
	modal_header = 'Мэдээлэл устгах'
	confirm_question = 'Мэдээллийг устгах уу?'
	pk_url_kwarg='pk'
	view_url = '/'

	def dispatch(self, request, *args, **kwargs):
		object_id = kwargs[self.pk_url_kwarg]
		self.object = get_object_or_404(self.model, id = object_id)
		return super(Base_DeleteView, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(Base_DeleteView, self).get_context_data(**kwargs)
		context['view_url'] = self.get_view_url()
		context['modal_header'] = self.get_modal_header()
		context['delete_confirm_question'] = self.get_confirm_question()
		return context
	def form_valid(self, form):
		self.object.status = False
		self.object.created_by = self.user
		self.object.save()
		messages.success(self.request, self.get_delete_message())
		return HttpResponseRedirect(self.get_success_url())
	def get_delete_message(self):
		return self.delete_message
	def get_modal_header(self):
		return self.modal_header
	def get_confirm_question(self):
		return self.confirm_question
	def get_view_url(self):
		return self.view_url
class BaseFormView_with_formset(FormView):
	formset_class = None
	formset_initial = {}
	formset_prefix = None
	formset_queryset = None
	def get(self,request, *args, **kwargs):
		form = self.get_form()
		formset = self.get_formset()
		return self.render_to_response(self.get_context_data(form=form, formset = formset))
	def post(self, request, *args, **kwargs):
		form = self.get_form()
		formset = self.get_formset()
		if form.is_valid() and formset.is_valid():
			return self.form_valid(form, formset)
		else:
			return self.form_invalid(form, formset)
	def form_valid(self, form, formset):
		return HttpResponseRedirect(self.get_success_url())
	def form_invalid(self, form, formset):
		return self.render_to_response(self.get_context_data(form=form, formset = formset))
	def get_formset(self, formset_class = None):
		if formset_class is None:
			formset_class = self.get_formset_class()
		return formset_class(**self.get_formset_kwargs())
	def get_formset_class(self):
		return self.formset_class
	def get_formset_kwargs(self):
		kwargs = {
		'initial': self.get_formset_initial(),
		'prefix': self.get_formset_prefix(),
		'queryset': self.get_formset_queryset(),
		}
		if self.request.method in ('POST', 'PUT'):
			kwargs.update({
			    'data': self.request.POST,
			    'files': self.request.FILES,
			})
		return kwargs
	def get_formset_initial(self):
		return self.formset_initial.copy()
	def get_formset_prefix(self):
		return self.formset_prefix
	def get_formset_queryset(self):
		return self.formset_queryset



''' handah erh menu '''
class Handah_erhView(LoginRequired, TemplateView): # zahiral engineer nyagtlan hoyriin handah erhiig oorchloh
	perm_code_names=['tze_handah_erh_menu_view']
	template_name = 'handah_erh/handah_erh_list.html'

	def get_context_data(self, **kwargs):
		context = super(Handah_erhView, self).get_context_data(**kwargs)

		user_change_histories = User_change_history.objects.filter(baiguullaga = self.baiguullaga).order_by('-begin_time')
		context['user_change_histories'] = user_change_histories
		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		context['director'] = tze.tze_users_bind.user_zahiral
		context['eng_user'] = tze.tze_users_bind.user_engineer
		context['acc_user'] = tze.tze_users_bind.user_account
		return context


class Engineer_user_change(Base_Ajax_FormView):
	perm_code_names = ['tze_handah_erh_change_view']
	template_name = 'handah_erh/form_div_htmls/user_change_form.html'
	form_class = EmptyForm
	success_url = reverse_lazy('tze_handah_erh_menu')

	header_text = "Инженерийн хандах эрх солих"
	table_header_text = "Инженерийг сонгоно уу"
	no_object_text = 'Байгууллагад бүртгэлтэй инженер байхгүй байна. Инженер бүртгэх бол "Хүний нөөц" цэс рүү орж ажилчдаа бүртгэнэ үү.'
	alban_tushaal_contains = 'инженер'
	view_url = reverse_lazy('tze_engineer_user_change')

	def get_user(self):
		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		if tze.tze_users_bind.user_engineer:
			return tze.tze_users_bind.user_engineer
		else:
			return False
	def remove_user(self):
		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		tze.tze_users_bind.user_engineer.status = False
		tze.tze_users_bind.user_engineer.created_by = self.user
		tze.tze_users_bind.user_engineer.save()
		engineer_old_user = tze.tze_users_bind.user_engineer
		engineer_old = tze.tze_users_bind.user_engineer.user_id
		tze.tze_users_bind.user_engineer = None
		tze.tze_users_bind.save()
		try:
			m = User_change_history.objects.get(user_id = engineer_old, change_name = u"Хандах эрх олгогдсон")
		except ObjectDoesNotExist:
			print "ERROR user change history doesn't exist ERROR\n"
			m = User_change_history(baiguullaga = engineer_old.baiguullaga, user_id = engineer_old, change_name = u"Хандах эрх олгогдсон", created_by = self.user)
		except MultipleObjectsReturned:
			m = User_change_history.objects.filter(user_id = engineer_old, change_name = u"Хандах эрх олгогдсон")[0]
		m.change_name = u"Хандах эрх цуцлагдсан"
		m.save()

		e_mail_subject = "Системд хандах эрх цуцлагдлаа."
		body = "Сайн байна уу.\n\n Таны системд хандах инженерийн эрх цуцлагдлаа."

		thread = E_mail_sending_thread(engineer_old.e_mail, e_mail_subject, body)
		thread.start()
		print "thread started"
		#send_mail(e_mail_subject, body, 'wsrcmon@gmail.com', [engineer_old.e_mail])


		group_engineer = Group.objects.get(name = 'ТЗЭ инженер')
		tze.tze_users_bind.user_zahiral.groups.add(group_engineer)

		engineer_old_user.groups.clear()
		engineer_old_user.is_active = False
	def assign_user(self, obj):
		password = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
		try:
			object_user = User.objects.get(user_id = obj)
			object_user.username = obj.e_mail
			#object_user.password = password
			object_user.created_by = self.user
			object_user.is_active = True
		except ObjectDoesNotExist:
			object_user = User(user_id = obj, username = obj.e_mail, created_by = self.user, is_active = True)
		object_user.set_password(password)
		object_user.save()
		
		m = User_change_history(baiguullaga = object_user.user_id.baiguullaga, user_id = object_user.user_id, change_name = u"Хандах эрх олгогдсон", created_by = self.user)
		m.save()

		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		tze.tze_users_bind.user_engineer = object_user
		tze.tze_users_bind.save()


		e_mail_subject = "Системд хандах эрх олгогдлоо."
		body = "Сайн байна уу.\n\n Таньд системд хандах инженерийн эрх олгогдлоо.\nНууц үг: " + password

		thread = E_mail_sending_thread(obj.e_mail, e_mail_subject, body)
		thread.start()
		#send_mail(e_mail_subject, body, 'wsrcmon@gmail.com', [obj.e_mail])
		print "thread started"


		group_zahiral = Group.objects.get(name = 'ТЗЭ захирал')
		group_engineer = Group.objects.get(name = 'ТЗЭ инженер')

		tze.tze_users_bind.user_zahiral.groups.remove(group_engineer)
		tze.tze_users_bind.user_engineer.groups.clear()
		tze.tze_users_bind.user_engineer.groups.add(group_engineer)
	def change_user(self, obj):
		self.remove_user()
		self.assign_user(obj)
	def form_valid(self, form):
		ajiltan_id = self.request.POST.get('user_choice', False)
		if ajiltan_id:
			object_ajiltan = get_object_or_404(Ajiltan, id = ajiltan_id)
			if self.get_user():
				user = self.get_user()
				if not object_ajiltan == user.user_id:
					if object_ajiltan.e_mail:
						self.change_user(object_ajiltan)
					else:
						print "choice has no e_mail"
				else:
					print "choice is same as old one"
			else:
				if object_ajiltan.e_mail:
					self.assign_user(object_ajiltan)
				else:
					print "choice has no e_mail"
		else:
			print "not chosen ajiltan"
		return super(Engineer_user_change, self).form_valid(form)
	def get_context_data(self, **kwargs):
		context = super(Engineer_user_change, self).get_context_data(**kwargs)
		context['header_text'] = self.header_text
		context['table_header_text'] = self.table_header_text
		context['no_object_text'] = self.no_object_text

		tasag = Tasag.objects.filter(baiguullaga = self.baiguullaga, status = True)
		albanTushaaluud = AlbanTushaal.objects.filter(dep_id = tasag, position_name__icontains = self.alban_tushaal_contains, status = True)
		object_list = Ajiltan.objects.filter(baiguullaga = self.baiguullaga, alban_tushaal = albanTushaaluud, status = True)

		context['object_list'] = object_list

		context['view_url'] = self.view_url
		
		return context

class Account_user_change(Engineer_user_change):

	header_text = "Нягтлангийн хандах эрх солих"
	table_header_text = "Нягтланг сонгоно уу"
	no_object_text = 'Байгууллагад бүртгэлтэй нягтлан байхгүй байна. Нягтлан бүртгэх бол "Хүний нөөц" цэс рүү орж ажилчдаа бүртгэнэ үү.'
	alban_tushaal_contains = 'нягтлан'

	def get_user(self):
		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		if tze.tze_users_bind.user_account:
			return tze.tze_users_bind.user_account
		else:
			return False
	def remove_user(self):
		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		tze.tze_users_bind.user_account.status = False
		tze.tze_users_bind.user_account.created_by = self.user
		tze.tze_users_bind.user_account.save()
		account_old_user = tze.tze_users_bind.user_account
		account_old = tze.tze_users_bind.user_account.user_id
		tze.tze_users_bind.user_account = None
		tze.tze_users_bind.save()
		try:
			m = User_change_history.objects.get(user_id = account_old, change_name = u"Хандах эрх олгогдсон")
		except ObjectDoesNotExist:
			print "ERROR user change history doesn't exist ERROR\n"
			m = User_change_history(baiguullaga = account_old.baiguullaga, user_id = account_old, change_name = u"Хандах эрх олгогдсон", created_by = self.user)
		except:
			m = User_change_history.objects.filter(user_id = account_old, change_name = u"Хандах эрх олгогдсон")[0]
		m.change_name = u"Хандах эрх цуцлагдсан"
		m.save()

		e_mail_subject = "Системд хандах эрх цуцлагдлаа."
		body = "Сайн байна уу.\n\n Таны системд хандах нягтлагийн эрх цуцлагдлаа."

		thread = E_mail_sending_thread(account_old.e_mail, e_mail_subject, body)
		thread.start()
		print "thread started"

		group_account = Group.objects.get(name = 'ТЗЭ нягтлан')
		tze.tze_users_bind.user_zahiral.groups.add(group_account)

		account_old_user.groups.clear()
		account_old_user.is_active = False
	def assign_user(self, obj):
		password = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8)) ############# generate hiigeed e-mail-eer yavuuldag baih yostoi
		try:
			object_user = User.objects.get(user_id = obj)
			object_user.username = obj.e_mail
			object_user.created_by = self.user
			object_user.status = True
		except ObjectDoesNotExist:
			object_user = User(user_id = obj, username = obj.e_mail, created_by = self.user, status = True)
		object_user.set_password(password)
		object_user.save()

		m = User_change_history(baiguullaga = object_user.user_id.baiguullaga, user_id = object_user.user_id, change_name = u"Хандах эрх олгогдсон", created_by = self.user)
		m.save()

		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		tze.tze_users_bind.user_account = object_user
		tze.tze_users_bind.save()


		e_mail_subject = "Системд хандах эрх олгогдлоо."
		body = "Сайн байна уу.\n\n Таньд системд хандах нягтлангийн эрх олгогдлоо.\nНууц үг: " + password

		thread = E_mail_sending_thread(obj.e_mail, e_mail_subject, body)
		thread.start()
		print "thread started"


		group_zahiral = Group.objects.get(name = 'ТЗЭ захирал')
		group_account = Group.objects.get(name = 'ТЗЭ нягтлан')

		tze.tze_users_bind.user_zahiral.groups.remove(group_account)
		tze.tze_users_bind.user_account.groups.clear()
		tze.tze_users_bind.user_account.groups.add(group_account)


class Engineer_user_remove(Engineer_user_change):
	perm_code_names = ['tze_handah_erh_change_view']
	template_name = 'handah_erh/form_div_htmls/user_delete_form.html'
	form_class = EmptyForm
	success_url = reverse_lazy('tze_handah_erh_menu')

	header_text = "Инженерийн хандах эрхийг цуцлах"
	anhaaruulga_msg = "Та инженерийг хандах эрхгүй болгох бол цуцлах дээр дарна уу."
	view_url = reverse_lazy('tze_engineer_user_remove')

	def get_context_data(self, **kwargs):
		context = super(Engineer_user_change, self).get_context_data(**kwargs)
		context['anhaaruulga_msg'] = self.anhaaruulga_msg
		context['header_text'] = self.header_text
		context['view_url'] = self.view_url
		return context

	def form_valid(self, form):
		self.remove_user()
		return super(Engineer_user_change, self).form_valid(form)

class Account_user_remove(Account_user_change):
	perm_code_names = ['tze_handah_erh_change_view']
	template_name = 'handah_erh/form_div_htmls/user_delete_form.html'
	form_class = EmptyForm
	success_url = reverse_lazy('tze_handah_erh_menu')

	header_text = "Нягтлангийн хандах эрхийг цуцлах"
	anhaaruulga_msg = "Та нягтланг хандах эрхгүй болгох бол цуцлах дээр дарна уу."
	view_url = reverse_lazy('tze_engineer_user_remove')

	def get_context_data(self, **kwargs):
		context = super(Engineer_user_change, self).get_context_data(**kwargs)
		context['anhaaruulga_msg'] = self.anhaaruulga_msg
		context['header_text'] = self.header_text
		context['view_url'] = self.view_url
		return context

	def form_valid(self, form):
		self.remove_user()
		return super(Engineer_user_change, self).form_valid(form)



''' baiguullaga menu '''
class BaiguullagaaView(LoginRequired, TemplateView):
	perm_code_names = ['tze_baiguullaga_menu_view']
	template_name = 'baiguullaga/baiguullaga.html'

	def get_context_data(self, **kwargs):
		#notify.send(self.user, recipient=self.user, verb='you reached level 10', url_data = reverse_lazy('tze_uamedee_menu'))
		date = []
		context = super(BaiguullagaaView, self).get_context_data(**kwargs)
		for i in range(3):
			date.append(int(timezone.now().year)-(i+1))
		context['date'] = date

		object1 = ZDTodorhoilolt.objects.filter(tze = self.baiguullaga, status = True)
		object2 = HangagchBaiguullaga.objects.filter(tze = self.baiguullaga, status = True)
		object3 = TaxTodorhoilolt.objects.filter(tze = self.baiguullaga, status = True)
		object4 = AuditDugnelt.objects.filter(tze = self.baiguullaga, status = True)
		object5 = NormStandart.objects.filter(tze = self.baiguullaga, status = True)
		object6 = Baig_huuli_durem.objects.filter(tze = self.baiguullaga, status = True)
		object7 = UsZuvshuurul.objects.filter(tze = self.baiguullaga, status = True)
		object8 = SanhuuTailan.objects.filter(tze = self.baiguullaga, status = True)
		object10 = OronTooniiSchema.objects.filter(tze = self.baiguullaga, status = True)
		object11 = AjliinBair.objects.filter(tze = self.baiguullaga, status = True)
		object12 = UildverTechnology.objects.filter(tze= self.baiguullaga, status = True)
		

		context['zasag_count'] = object1.count()
		context['hangagch_count'] = object2.count()
		context['tax_tod_count'] = object3.count()
		context['audit_count'] = object4.count()
		context['norm_standart_count'] = object5.count()
		context['huuli_durem_count'] = object6.count()
		context['us_zovshoorol_count'] = object7.count()
		context['sanhuu_tailan_count'] = object8.count()
		context['oron_toonii_schema_count'] = object10.count()
		context['ajliin_bair_dugnelt_count'] = object11.count()
		context['uildver_tech_schema_count'] = object12.count()
		

		context['baiguullaga'] = get_object_or_404(TZE, id=self.baiguullaga.id)


		context['url0'] = reverse_lazy('tze_baig_medeelel_list')
		context['url1'] = reverse_lazy('tze_zasag_tod_list')
		context['url2'] = reverse_lazy('tze_hangagch_baig_list')
		context['url3'] = reverse_lazy('tze_tatvar_tod_list')
		context['url4'] = reverse_lazy('tze_audit_dugnelt_list')
		context['url5'] = reverse_lazy('tze_norm_standart_list')
		context['url6'] = reverse_lazy('tze_huuli_durem_list')
		context['url7'] = reverse_lazy('tze_us_ashigluulah_zovshoorol_list')
		context['url8'] = reverse_lazy('tze_sanhuu_tailan_list')
		context['url9'] = reverse_lazy('tze_oron_toonii_schema_list')
		context['url10'] = reverse_lazy('tze_sez_sudalgaa_list')
		context['url_ajliin_bair_dugnelt_list'] = reverse_lazy('tze_ajliin_bair_dugnelt_list')
		context['url_uildver_tech_schema_list'] = reverse_lazy('tze_uildver_tech_schema_list')

		return context

class OrgUpdateView(LoginRequired, UpdateView):
	model = TZE
	template_name = 'baiguullaga/org.html'
	form_class = TZE_updateForm
	success_url = reverse_lazy('baiguullaga_menu')
	perm_code_names = ['change_baiguullaga']

	def get_object(self, queryset=None):
		tze = get_object_or_404(TZE, id=self.baiguullaga.id)
		return tze

	def form_valid(self, form):
		org = form.save(commit = False)
		if org.reg_num and org.ubd and org.org_name and org.org_type and org.org_date \
		and org.phone  and org.e_mail and org.fax and org.city and org.khoroo and org.district:

			for i in TZ_Huselt.objects.filter(tze = org):
				print "Dfasdffd"
				mat_1 = i.burdel.get_material_1()
				mat_1.change_status_to_burdsen(timezone.now())
		org.save()
		return super(OrgUpdateView, self).form_valid(form)
class TZE_baig_medeelel_list(LoginRequired, TemplateView):
	perm_code_names = ['tze_baiguullaga_menu_view']
	template_name = 'baiguullaga/list_htmls/tze_baiguullaga_delgerengui.html'


class TZE_zasag_tod_list(LoginRequired, ListView):
	perm_code_names = ['tze_baiguullaga_menu_view']
	template_name = 'baiguullaga/list_htmls/tze_zasag_tod_list.html'
	def get_queryset(self):
		queryset = ZDTodorhoilolt.objects.filter(tze = self.baiguullaga, status = True)
		return queryset
class TZE_hangagch_baig_list(LoginRequired, ListView):
	perm_code_names = ['tze_baiguullaga_menu_view']
	template_name = 'baiguullaga/list_htmls/tze_hangagch_baigs_list.html'
	def get_queryset(self):
		queryset = HangagchBaiguullaga.objects.filter(tze = self.baiguullaga, status = True)
		return queryset
class TZE_tatvar_tod_list(LoginRequired, ListView):
	perm_code_names = ['tze_baiguullaga_menu_view']
	template_name = 'baiguullaga/list_htmls/tze_tax_tod_list.html'
	def get_queryset(self):
		queryset = TaxTodorhoilolt.objects.filter(tze = self.baiguullaga, status = True)
		return queryset
class TZE_audit_dugnelt_list(LoginRequired, ListView):
	perm_code_names = ['tze_baiguullaga_menu_view']
	template_name = 'baiguullaga/list_htmls/tze_audit_dugnelt_list.html'
	def get_queryset(self):
		queryset = AuditDugnelt.objects.filter(tze = self.baiguullaga, status = True)
		return queryset
class TZE_norm_standart_list(LoginRequired, ListView):
	perm_code_names = ['tze_baiguullaga_menu_view']
	template_name = 'baiguullaga/list_htmls/tze_norm_standart_list.html'
	def get_queryset(self):
		queryset = NormStandart.objects.filter(tze = self.baiguullaga, status = True)
		return queryset
class TZE_huuli_durem_list(LoginRequired, ListView):
	perm_code_names = ['tze_baiguullaga_menu_view']
	template_name = 'baiguullaga/list_htmls/tze_huuli_juram_list.html'
	def get_queryset(self):
		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		queryset = Baig_huuli_durem.objects.filter(tze = tze, status = True)
		return queryset
class TZE_ajliin_bair_dugnelt_list(LoginRequired, ListView):
	perm_code_names = ['tze_baiguullaga_menu_view']
	template_name = 'baiguullaga/list_htmls/tze_ajliin_bair_dugnelt_list.html'
	def get_queryset(self):
		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		queryset = AjliinBair.objects.filter(tze = tze, status = True)
		return queryset
class TZE_uildver_tech_schema_list(LoginRequired, ListView):
	perm_code_names = ['tze_baiguullaga_menu_view']
	template_name = 'baiguullaga/list_htmls/tze_uildver_tech_schema_list.html'
	def get_queryset(self):
		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		queryset = UildverTechnology.objects.filter(tze = tze, status = True)
		return queryset
class TZE_us_ashigluulah_zovshoorol_list(LoginRequired, ListView):
	perm_code_names = ['tze_baiguullaga_menu_view']
	template_name = 'baiguullaga/list_htmls/tze_us_zovshoorol_list.html'
	def get_queryset(self):
		queryset = UsZuvshuurul.objects.filter(tze = self.baiguullaga, status = True)
		return queryset
class TZE_sanhuu_tailan_list(LoginRequired, ListView):
	perm_code_names = ['tze_baiguullaga_menu_view']
	template_name = 'baiguullaga/list_htmls/tze_sanhuu_tailan_list.html'
	def get_queryset(self):
		queryset = SanhuuTailan.objects.filter(tze = self.baiguullaga, status = True)
		return queryset
class TZE_oron_toonii_schema(LoginRequired, ListView):
	perm_code_names = ['tze_baiguullaga_menu_view']
	template_name = 'baiguullaga/list_htmls/tze_oron_toonii_schema_list.html'
	def get_queryset(self):
		queryset = OronTooniiSchema.objects.filter(tze = self.baiguullaga, status = True)
		return queryset
class TZE_SEZ_sudalgaa(LoginRequired, ListView):
	perm_code_names = ['tze_baiguullaga_menu_view']
	template_name = 'baiguullaga/list_htmls/sanhuu_sudalgaa.html'
	def get_queryset(self):
		queryset = SariinTailan.objects.filter(tze = self.baiguullaga, month = 0, status = True)
		return queryset

class Zasag_tod_FormView(Base_Ajax_FormView):
	perm_code_names = ['add_zdtodorhoilolt']
	template_name = 'baiguullaga/form_div_htmls/zasag_tod_form.html'
	success_url = reverse_lazy('baiguullaga_menu')
	form_class = ZDTForm
	view_url = reverse_lazy('zasag_tod_insert')
	def form_valid(self, form):
		obj = form.save(commit=False)
		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		obj.tze = tze
		obj.created_by = self.user
		obj.status = True
		obj.save()
		#messages.success(self.request, 'Амжилттай хадгаллаа.')
		return super(Zasag_tod_FormView, self).form_valid(form)
class Hangagch_baig_FormView(Base_Ajax_FormView):
	perm_code_names = ['add_hangagchbaiguullaga']
	template_name = 'baiguullaga/form_div_htmls/hangagch_baig_form.html'
	success_url = reverse_lazy('baiguullaga_menu')
	form_class = HBGereeForm
	view_url = reverse_lazy('han_baig_insert')
	def form_valid(self, form):
		obj = form.save(commit=False)
		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		obj.tze = tze
		obj.created_by = self.user
		obj.status = True
		obj.save()
		#messages.success(self.request, 'Амжилттай хадгаллаа.')
		return super(Hangagch_baig_FormView, self).form_valid(form)
class Tax_tod_FormView(Base_Ajax_FormView):
	perm_code_names = ['add_taxtodorhoilolt']
	template_name = 'baiguullaga/form_div_htmls/tax_tod_form.html'
	success_url = reverse_lazy('baiguullaga_menu')
	form_class = TaxTodorhoiloltForm
	view_url = reverse_lazy('tax_tod_insert')
	def form_valid(self, form):
		obj = form.save(commit=False)
		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		obj.tze = tze
		obj.created_by = self.user
		obj.status = True
		obj.save()
		#messages.success(self.request, 'Амжилттай хадгаллаа.')
		return super(Tax_tod_FormView, self).form_valid(form)
class Audit_dugnelt_FormView(Base_Ajax_FormView):
	perm_code_names = ['add_auditdugnelt']
	template_name = 'baiguullaga/form_div_htmls/audit_dugnelt_form.html'
	success_url = reverse_lazy('baiguullaga_menu')
	form_class = AuditDugneltForm
	view_url = reverse_lazy('audit_dugnelt_insert')
	def form_valid(self, form):
		obj = form.save(commit=False)
		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		obj.tze = tze
		obj.created_by = self.user
		obj.status = True
		obj.save()
		#messages.success(self.request, 'Амжилттай хадгаллаа.')
		return super(Audit_dugnelt_FormView, self).form_valid(form)
class Norm_standart_FormView(Base_Ajax_FormView):
	perm_code_names = ['add_normstandart']
	template_name = 'baiguullaga/form_div_htmls/norm_standart_form.html'
	success_url = reverse_lazy('tze_norm_standart_list')
	form_class = EmptyForm
	view_url = reverse_lazy('norm_standart_insert')
	def form_valid(self, form):
		chosen_standart_ids = self.request.POST.getlist('chosen_standarts')
		standarts_all = Standart.objects.all()
		baig_norms = NormStandart.objects.filter(tze = self.baiguullaga, status = True)
		for i in baig_norms:
			i.status=False
			i.begin_time = timezone.now()
			i.created_by = self.user
			i.save()
		for i in chosen_standart_ids:
			standart = standarts_all.get(id = i)
			tze = get_object_or_404(TZE, id = self.baiguullaga.id)
			n = NormStandart.objects.filter(tze = tze, standart = standart)
			if n:
				obj = n[0]
			else:
				obj = NormStandart(tze = tze, standart = standart)
			obj.status = True
			obj.created_by = self.user
			obj.begin_time = timezone.now()
			obj.save()
		return super(Norm_standart_FormView, self).form_valid(form)
	def get_context_data(self, **kwargs):
		context = super(Norm_standart_FormView, self).get_context_data(**kwargs)
		context['view_url'] = self.view_url
		context['standarts'] = Standart.objects.all()
		baig_standarts = NormStandart.objects.filter(tze = self.baiguullaga, status = True)
		initial_dic={}
		for i in baig_standarts:
			initial_dic[i.standart.id] = True
		context['initial_dic'] = initial_dic
		return context
class Huuli_durem_FormView(Base_Ajax_FormView):
	perm_code_names = ['add_baig_huuli_durem']
	template_name = 'baiguullaga/form_div_htmls/huuli_durem_juram_norm.html'
	success_url = reverse_lazy('tze_huuli_durem_list')
	form_class = EmptyForm
	view_url = reverse_lazy('tze_huuli_durem_insert')
	def form_valid(self, form):
		chosen_huuliud_ids = self.request.POST.getlist('chosen_huuliud')
		huuli_all = Huuli_durem_norm.objects.all()
		baig_huuliud = Baig_huuli_durem.objects.filter(tze = self.baiguullaga, status = True)
		for i in baig_huuliud:
			i.status=False
			i.begin_time = timezone.now()
			i.created_by = self.user
			i.save()
		for i in chosen_huuliud_ids:
			durem = huuli_all.get(id = i)
			tze = get_object_or_404(TZE, id = self.baiguullaga.id)
			n = Baig_huuli_durem.objects.filter(tze = tze, durem = durem)
			if n:
				obj = n[0]
			else:
				obj = Baig_huuli_durem(tze = tze, durem = durem)
			obj.status = True
			obj.created_by = self.user
			obj.begin_time = timezone.now()
			obj.save()
		return super(Huuli_durem_FormView, self).form_valid(form)
	def get_context_data(self, **kwargs):
		context = super(Huuli_durem_FormView, self).get_context_data(**kwargs)
		context['view_url'] = self.view_url
		context['huuliud'] = Huuli_durem_norm.objects.all()
		baig_huuliud = Baig_huuli_durem.objects.filter(tze = self.baiguullaga, status = True)
		initial_dic={}
		for i in baig_huuliud:
			initial_dic[i.durem.id] = True
		context['initial_dic'] = initial_dic
		return context
class Us_zovshoorol_FormView(Base_Ajax_FormView):
	perm_code_names=['add_uszuvshuurul']
	template_name = 'baiguullaga/form_div_htmls/us_zovshoorol_form.html'
	success_url = reverse_lazy('tze_us_ashigluulah_zovshoorol_list')
	form_class = UsZuvshuurulForm
	view_url = reverse_lazy('us_zovshoorol_insert')
	def form_valid(self, form):
		obj = form.save(commit=False)
		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		obj.tze = tze
		obj.created_by = self.user
		obj.status = True
		obj.save()	
		#messages.success(self.request, 'Амжилттай хадгаллаа.')
		return super(Us_zovshoorol_FormView, self).form_valid(form)
class Sanhuu_tailan_FormView(Base_Ajax_FormView):
	perm_code_names = ['add_sanhuutailan']
	template_name = 'baiguullaga/form_div_htmls/sanhuu_tailan_form.html'
	success_url = reverse_lazy('tze_sanhuu_tailan_list')
	form_class = SanhuuTailanForm
	view_url = reverse_lazy('sanhuu_tailan_insert')
	def form_valid(self, form):
		obj = form.save(commit=False)
		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		obj.tze = tze
		obj.created_by = self.user
		obj.status = True
		obj.save()
		#messages.success(self.request, 'Амжилттай хадгаллаа.')
		return super(Sanhuu_tailan_FormView, self).form_valid(form)
class Oron_too_schema_FormView(Base_Ajax_FormView):
	perm_code_names = ['add_orontooniischema']
	template_name = 'baiguullaga/form_div_htmls/oron_too_schema_form.html'
	success_url = reverse_lazy('tze_oron_toonii_schema_list')
	form_class = SchemaForm
	view_url = reverse_lazy('oron_too_schema_insert')
	def form_valid(self, form):
		obj = form.save(commit=False)
		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		obj.tze = tze
		obj.created_by = self.user
		obj.status = True
		obj.save()
		#messages.success(self.request, 'Амжилттай хадгаллаа.')
		return super(Oron_too_schema_FormView, self).form_valid(form)
class Uildver_tech_schema_FormView(Base_Ajax_FormView):
	perm_code_names = ['tze_tz_huselt_ilgeeh_view']
	template_name = 'baiguullaga/form_div_htmls/uildver_tech_schema_form.html'
	success_url = reverse_lazy('baiguullaga_menu')
	form_class = UildverTechnologyForm
	view_url = reverse_lazy('uildver_tech_schema_insert_tz')
	def form_valid(self, form):
		obj = form.save(commit=False)
		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		obj.tze = tze
		obj.created_by = self.user
		obj.status = True
		obj.save()
		#messages.success(self.request, 'Амжилттай хадгаллаа.')
		return super(Uildver_tech_schema_FormView, self).form_valid(form)
class Ajliin_bair_dugnelt_FormView(Base_Ajax_FormView):
	perm_code_names = ['tze_tz_huselt_ilgeeh_view']
	template_name = 'baiguullaga/form_div_htmls/ajliin_bair_dugnelt_form.html'
	success_url = reverse_lazy('baiguullaga_menu')
	form_class = AjliinBairForm
	view_url = reverse_lazy('ajliin_bair_dugnelt_insert_tz') # form post hiiih url, viewiin url
	def form_valid(self, form):
		obj = form.save(commit=False)
		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		obj.tze = tze
		obj.created_by = self.user
		obj.status = True
		obj.save()
		#messages.success(self.request, 'Амжилттай хадгаллаа.')
		return super(Ajliin_bair_dugnelt_FormView, self).form_valid(form)

class Zasag_tod_DeleteView(LoginRequired, Base_DeleteView):
	perm_code_names = ['add_zdtodorhoilolt']
	success_url = reverse_lazy('baiguullaga_menu')
	pk_url_kwarg = 'id'
	model = ZDTodorhoilolt
	modal_header = 'Засаг даргын тодорхойлолтийг устгах'
	confirm_question = 'Засаг даргын тодорхойлолтийг устгах уу?'
	delete_message = 'Засаг даргын тодорхойлолтийг устгалаа.'
	def get_view_url(self):
		return reverse_lazy('zasag_tod_delete', kwargs={'id': self.object.id})
class Hangagch_baig_DeleteView(LoginRequired, Base_DeleteView):
	perm_code_names = ['add_hangagchbaiguullaga']
	success_url = reverse_lazy('baiguullaga_menu')
	pk_url_kwarg = 'id'
	model = HangagchBaiguullaga
	modal_header = 'Хангагч байгууллагын тодорхойлолт, гэрээг устгах'
	confirm_question = 'Хангагч байгууллагын тодорхойлолт, гэрээг устгах уу?'
	delete_message = 'Хангагч байгууллагын тодорхойлолт, гэрээг устгалаа.'
	def get_view_url(self):
		return reverse_lazy('han_baig_delete', kwargs={'id': self.object.id})
class Tax_tod_DeleteView(LoginRequired, Base_DeleteView):
	perm_code_names = ['add_taxtodorhoilolt']
	success_url = reverse_lazy('baiguullaga_menu')
	pk_url_kwarg = 'id'
	model = TaxTodorhoilolt
	modal_header = 'Татварын тодорхойлолтыг устгах'
	confirm_question = 'Татварын тодорхойлолтыг устгах уу?'
	delete_message = 'Татварын тодорхойлолтыг устгалаа.'
	def get_view_url(self):
		return reverse_lazy('tax_tod_delete', kwargs={'id': self.object.id})
class Audit_dugnelt_DeleteView(LoginRequired, Base_DeleteView):
	perm_code_names = ['add_auditdugnelt']
	success_url = reverse_lazy('baiguullaga_menu')
	pk_url_kwarg = 'id'
	model = AuditDugnelt
	modal_header = 'Аудитын дүгнэлтийг устгах'
	confirm_question = 'Аудитын дүгнэлтийг устгах уу?'
	delete_message = 'Аудитын дүгнэлтийг устгалаа.'
	def get_view_url(self):
		return reverse_lazy('audit_dugnelt_delete', kwargs={'id': self.object.id})
class Norm_standart_DeleteView(LoginRequired, Base_DeleteView):
	perm_code_names = ['add_normstandart']
	success_url = reverse_lazy('baiguullaga_menu')
	pk_url_kwarg = 'id'
	model = NormStandart
	modal_header = 'Норм стандартын мэдээллийг устгах'
	confirm_question = 'Норм стандартын мэдээллийг устгах уу?'
	delete_message = 'Норм стандартын мэдээллийг устгалаа.'
	def get_view_url(self):
		return reverse_lazy('norm_standart_delete', kwargs={'id': self.object.id})
class TZE_huuli_durem_delete(LoginRequired, Base_DeleteView):
	perm_code_names = ['add_baig_huuli_durem']
	success_url = reverse_lazy('baiguullaga_menu')
	pk_url_kwarg = 'id'
	model = Baig_huuli_durem
	modal_header = 'Хууль журмыг хасах'
	confirm_question = 'Хууль журмыг байгууллагын мөрддөг хууль журмыг жагсаалтаас хасах уу?'
	delete_message = 'Хууль журмын мэдээллийг хаслаа.'
	def get_view_url(self):
		return reverse_lazy('tze_huuli_durem_delete', kwargs={'id': self.object.id})
class Us_zovshoorol_DeleteView(LoginRequired, Base_DeleteView):
	perm_code_names=['add_uszuvshuurul']
	success_url = reverse_lazy('baiguullaga_menu')
	pk_url_kwarg = 'id'
	model = UsZuvshuurul
	modal_header = 'Ус ашиглуулах дүгнэлт, зөвшөөрөл, гэрээг устгах'
	confirm_question = 'Ус ашиглуулах дүгнэлт, зөвшөөрөл, гэрээг устгах уу?'
	delete_message = 'Ус ашиглуулах дүгнэлт, зөвшөөрөл, гэрээг устгалаа.'
	def get_view_url(self):
		return reverse_lazy('us_zovshoorol_delete', kwargs={'id': self.object.id})
class Sanhuu_tailan_DeleteView(LoginRequired, Base_DeleteView):
	perm_code_names = ['add_sanhuutailan']
	success_url = reverse_lazy('baiguullaga_menu')
	pk_url_kwarg = 'id'
	model = SanhuuTailan
	modal_header = 'Санхүүгийн балансыг устгах'
	confirm_question = 'Санхүүгийн балансыг устгах уу?'
	delete_message = 'Санхүүгийн балансыг устгалаа.'
	def get_view_url(self):
		return reverse_lazy('sanhuu_tailan_delete', kwargs={'id': self.object.id})
class Oron_too_schema_DeleteView(LoginRequired, Base_DeleteView):
	perm_code_names = ['add_orontooniischema']
	success_url = reverse_lazy('baiguullaga_menu')
	pk_url_kwarg = 'id'
	model = OronTooniiSchema
	modal_header = 'Орон тооны бүтцийн схем зургийг устгах'
	confirm_question = 'Орон тооны бүтцийн схем зургийг устгах уу?'
	delete_message = 'Орон тооны бүтцийн схем зургийг устгалаа.'
	def get_view_url(self):
		return reverse_lazy('oron_too_schema_delete', kwargs={'id': self.object.id})
class Ajliin_bair_dugnelt_DeleteView(LoginRequired, Base_DeleteView):
	perm_code_names = ['add_ajliinbair']
	success_url = reverse_lazy('baiguullaga_menu')
	pk_url_kwarg = 'id'
	model = AjliinBair
	modal_header = 'Ажлын байрны дүгнэлтийг устгах'
	confirm_question = 'Ажлын байрны дүгнэлтийг устгах уу?'
	delete_message = 'Ажлын байрны дүгнэлтийг устгалаа.'
	def get_view_url(self):
		return reverse_lazy('ajliin_bair_dugnelt_delete', kwargs={'id': self.object.id})
class Uildver_tech_schema_deleteView(LoginRequired, Base_DeleteView):
	perm_code_names = ['add_uildvertechnology']
	success_url = reverse_lazy('baiguullaga_menu')
	pk_url_kwarg = 'id'
	model = UildverTechnology
	modal_header = 'Үйлдвэрийн технологийн схемийг устгах'
	confirm_question = 'Үйлдвэрийн технологийн схемийг устгах уу?'
	delete_message = 'Үйлдвэрийн технологийн схемийг устгалаа.'
	def get_view_url(self):
		return reverse_lazy('uildver_tech_schema_delete', kwargs={'id': self.object.id})










''' hunii noots menu '''
class EmployeeView(LoginRequired, TemplateView):
	perm_code_names = ['tze_hunii_noots_menu_view']
	menu_num = 4
	template_name = 'employee/ajiltan.html'

	def get_context_data(self, **kwargs):
		context = super(EmployeeView, self).get_context_data(**kwargs)
		ajiltan = Ajiltan.objects.filter(baiguullaga = self.baiguullaga, status=True)
		paginator = Paginator(Ajiltan.objects.filter(baiguullaga = self.baiguullaga, status = True).order_by('-id'), 10)
		page = self.request.GET.get('page')
		
		try:
			context['ajiltan'] = paginator.page(page)
		except PageNotAnInteger:
			context['ajiltan'] = paginator.page(1)
		except EmptyPage:
			context['ajiltan'] = paginator.page(paginator.num_pages)
		context['object_list'] = ajiltan
		context['ajiltan1'] = ajiltan.filter(zereg=u'Удирдах ажилтан')
		context['ajiltan2'] = ajiltan.filter(zereg=u'Инженер техникийн ажилтан')
		context['ajiltan3'] = ajiltan.filter(zereg=u'Мэргэжлийн ажилтан')
		context['ajiltan4'] = ajiltan.filter(zereg=u'Бусад')

		
		url0 = reverse_lazy('tze_ajiltan_alba_tasag_list')
		url1 = reverse_lazy('tze_ajiltan_all_list')
		url2 = reverse_lazy('tze_ajiltan_udirdah_list')
		url3 = reverse_lazy('tze_ajiltan_engineer_list')
		url4 = reverse_lazy('tze_ajiltan_mergejil_list')
		url5 = reverse_lazy('tze_ajiltan_busad_list')

		context['url0'] = url0
		context['url1'] = url1
		context['url2'] = url2
		context['url3'] = url3
		context['url4'] = url4
		context['url5'] = url5

		return context

class TZE_Ajiltan_all_list(LoginRequired, ListView):
	perm_code_names = ['tze_hunii_noots_menu_view']
	template_name = 'employee/list_htmls/tze_ajiltan_list.html'
	list_header=u"Нийт ажилчдын жагсаалт"
	def get_queryset(self):
		self.queryset = Ajiltan.objects.filter(baiguullaga = self.baiguullaga, status = True)
		return super(TZE_Ajiltan_all_list, self).get_queryset()
	def get_context_data(self, **kwargs):
		context = super(TZE_Ajiltan_all_list,self).get_context_data(**kwargs)
		context['list_header'] = self.list_header
		return context
class TZE_Ajiltan_udirdah_list(LoginRequired, ListView):
	perm_code_names = ['tze_hunii_noots_menu_view']
	template_name = 'employee/list_htmls/tze_ajiltan_list.html'
	list_header=u"Удирдах ажилчдын жагсаалт"
	def get_queryset(self):
		self.queryset = Ajiltan.objects.filter(baiguullaga = self.baiguullaga, status = True, zereg=u'Удирдах ажилтан')
		return super(TZE_Ajiltan_udirdah_list, self).get_queryset()
	def get_context_data(self, **kwargs):
		context = super(TZE_Ajiltan_udirdah_list,self).get_context_data(**kwargs)
		context['list_header'] = self.list_header
		return context
class TZE_Ajiltan_engineer_list(LoginRequired, ListView):
	perm_code_names = ['tze_hunii_noots_menu_view']
	template_name = 'employee/list_htmls/tze_ajiltan_list.html'
	list_header="Инженер техникийн ажилчдын жагсаалт"
	def get_queryset(self):
		self.queryset = Ajiltan.objects.filter(baiguullaga = self.baiguullaga, status = True, zereg=u'Инженер техникийн ажилтан')
		return super(TZE_Ajiltan_engineer_list, self).get_queryset()
	def get_context_data(self, **kwargs):
		context = super(TZE_Ajiltan_engineer_list,self).get_context_data(**kwargs)
		context['list_header'] = self.list_header
		return context
class TZE_Ajiltan_mergejliin_list(LoginRequired, ListView):
	perm_code_names = ['tze_hunii_noots_menu_view']
	template_name = 'employee/list_htmls/tze_ajiltan_list.html'
	list_header="Мэргэжлийн ажилчдын жагсаалт"
	def get_queryset(self):
		self.queryset = Ajiltan.objects.filter(baiguullaga = self.baiguullaga, status = True, zereg=u'Мэргэжлийн ажилтан')
		return super(TZE_Ajiltan_mergejliin_list, self).get_queryset()
	def get_context_data(self, **kwargs):
		context = super(TZE_Ajiltan_mergejliin_list,self).get_context_data(**kwargs)
		context['list_header'] = self.list_header
		return context
class TZE_Ajiltan_busad_list(LoginRequired, ListView):
	perm_code_names = ['tze_hunii_noots_menu_view']
	template_name = 'employee/list_htmls/tze_ajiltan_list.html'
	list_header="Бусад ажилчдын жагсаалт"
	def get_queryset(self):
		self.queryset = Ajiltan.objects.filter(baiguullaga = self.baiguullaga, status = True, zereg=u'Бусад')
		return super(TZE_Ajiltan_busad_list, self).get_queryset()
	def get_context_data(self, **kwargs):
		context = super(TZE_Ajiltan_busad_list,self).get_context_data(**kwargs)
		context['list_header'] = self.list_header
		return context
class TZE_alba_tasag_list(LoginRequired, TemplateView):
	perm_code_names = ['tze_hunii_noots_menu_view']
	template_name = 'employee/list_htmls/tze_ajiltan_alba_tasag_list.html'

	def get_context_data(self, **kwargs):
		context = super(TZE_alba_tasag_list, self).get_context_data(**kwargs)
		context['object_list'] = Tasag.objects.filter(baiguullaga = self.baiguullaga, status = True)
		return context

class TZE_alban_tushaal_list(LoginRequired, ListView):
	perm_code_names = ['tze_hunii_noots_menu_view']
	template_name = 'employee/list_htmls/tze_ajiltan_alban_tushaal_list.html'
	def get(self, request, *args, **kwargs):
		tasag_id = kwargs['id']
		self.tasag = get_object_or_404(Tasag, id = tasag_id)
		return super(TZE_alban_tushaal_list, self).get(request, *args, **kwargs)
	def get_queryset(self):
		self.queryset = self.tasag.get_alban_tushaal_queryset()
		return super(TZE_alban_tushaal_list, self).get_queryset()
	def get_context_data(self, **kwargs):
		context = super(TZE_alban_tushaal_list, self).get_context_data(**kwargs)
		context['tasag_object'] = self.tasag
		return context
class TZE_alba_tasgiin_ajilchid_list(LoginRequired, ListView):
	perm_code_names = ['tze_hunii_noots_menu_view']
	template_name = 'employee/list_htmls/tze_alba_tasgiin_ajilchid_list.html'
	def get(self, request, *args, **kwargs):
		tasag_id = kwargs['id']
		self.tasag = get_object_or_404(Tasag, id = tasag_id)
		return super(TZE_alba_tasgiin_ajilchid_list, self).get(request, *args, **kwargs)
	def get_queryset(self):
		self.queryset = self.tasag.get_ajiltan_queryset()
		return super(TZE_alba_tasgiin_ajilchid_list, self).get_queryset()
	def get_context_data(self, **kwargs):
		context = super(TZE_alba_tasgiin_ajilchid_list, self).get_context_data(**kwargs)
		context['tasag_object'] = self.tasag
		return context

class TZE_alba_tasag_insert(Base_Ajax_FormView):
	perm_code_names = ['add_tasag']
	template_name = 'employee/form_div_htmls/tze_alba_tasag_insert.html'
	form_class = Alba_tasag_form
	success_url = reverse_lazy('tze_ajiltan_alba_tasag_list')
	view_url = reverse_lazy('tze_alba_tasag_insert')
	def form_valid(self, form):
		tasag_new = form.save(commit=False)
		tasag_new.baiguullaga = self.baiguullaga
		tasag_new.status = True
		tasag_new.begin_time = timezone.now()
		tasag_new.save()
		#messages.success(self.request, 'Алба тасгийг амжилттай нэмлээ')
		return super(TZE_alba_tasag_insert, self).form_valid(form)
class TZE_alban_tushaal_edit(LoginRequired, BaseFormView_with_formset):
	perm_code_names = ['add_albantushaal']
	template_name = 'employee/form_div_htmls/tze_alban_tushaal_edit.html'
	success_url = reverse_lazy('tze_ajiltan_alba_tasag_list')
	form_class = EmptyForm
	formset_class = AlbanTushaal_formset
	def dispatch(self, request, *args, **kwargs):
		tasag_id = kwargs['id']
		self.tasag = get_object_or_404(Tasag, id = tasag_id)
		return super(TZE_alban_tushaal_edit, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(TZE_alban_tushaal_edit, self).get_context_data(**kwargs)
		context['view_url'] = reverse_lazy('tze_alban_tushaal_edit', kwargs={'id': self.tasag.id})
		return context
	def get_formset_queryset(self):
		return AlbanTushaal.objects.filter(dep_id = self.tasag, status = True)
	def form_valid(self, form, formset):
		#form.save()
		new_alban_tushaals = formset.save(commit = False)
		for i in new_alban_tushaals: # shineer nemegdsen, bolon oorchlogdson alban tushaaluudiig hadgalj baina
			i.dep_id = self.tasag
			i.status = True
			i.begin_time = timezone.now()
			i.save()
		for f in formset.deleted_forms: # ustgasan alban_tushaaluudiig ustgaj baina
			at = f.cleaned_data['id']
			if at:
				at.status = False
				at.save()
		return super(TZE_alban_tushaal_edit, self).form_valid(form, formset)
	def form_invalid(self, form, formset):
		return HttpResponseRedirect(self.get_success_url())


class Ajiltan_createView(LoginRequired, BaseFormView_with_formset):
	perm_code_names = ['add_ajiltan']
	form_class = TZEAForm
	formset_class = School_formset
	template_name = "employee/ajiltan_create.html"
	success_url = reverse_lazy('ajiltan')
	formset_class1 = EngineeringCertificate_formset

	formset_prefix = 'prefix'
	formset_queryset = School.objects.none()

	formset_initial1 = {}
	formset_prefix1 = 'prefix1'
	formset_queryset1 = EngineeringCertificate.objects.none()


	def get(self,request, *args, **kwargs):
		form = self.get_form()
		formset = self.get_formset()
		formset1 = self.get_formset1()
		return self.render_to_response(self.get_context_data(form=form, formset = formset, formset1 = formset1))
	def post(self, request, *args, **kwargs):
		form = self.get_form()
		formset = self.get_formset()
		formset1 = self.get_formset1()
		if form.is_valid() and formset.is_valid() and formset1.is_valid():
			return self.form_valid(form, formset, formset1)
		else:
			return self.form_invalid(form, formset, formset1)
	
	def get_formset1(self, formset_class1 = None):
		if formset_class1 is None:
			formset_class1 = self.get_formset_class1()
		return formset_class1(**self.get_formset_kwargs1())
	
	def get_formset_class1(self):
		return self.formset_class1
	
	def get_formset_kwargs1(self):
		kwargs = {
		'initial': self.get_formset_initial1(),
		'prefix': self.get_formset_prefix1(),
		'queryset': self.get_formset_queryset1(),
		}
		if self.request.method in ('POST', 'PUT'):
			kwargs.update({
			    'data': self.request.POST,
			    'files': self.request.FILES,
			})
		return kwargs
	
	def get_formset_initial1(self):
		return self.formset_initial1.copy()
	def get_formset_prefix1(self):
		return self.formset_prefix1
	def get_formset_queryset1(self):
		return self.formset_queryset1

	def form_valid(self, form, formset, formset1):
		new_emp = form.save(commit=False)
		new_emp.baiguullaga = self.baiguullaga
		new_emp.status = True
		new_emp.begin_time = timezone.now()
		new_emp.save()
		new_schools = formset.save(commit = False)
		for i in new_schools: # shineer nemegdsen, bolon oorchlogdson alban tushaaluudiig hadgalj baina
			i.emp = new_emp
			i.status = True
			i.begin_time = timezone.now()
			i.save()
		for f in formset.deleted_forms:
			at = f.cleaned_data['id']
			if at:
				at.status = False
				at.save()
		new_eng_certs = formset1.save(commit = False)
		for i in new_eng_certs:
			i.emp = new_emp
			i.status = True
			i.begin_time = timezone.now()
			i.save()
		for f in formset1.deleted_forms:
			at = f.cleaned_data['id']
			if at:
				at.status = False
				at.save()

		return HttpResponseRedirect(self.get_success_url())
	def form_invalid(self, form, formset, formset1):
		return self.render_to_response(self.get_context_data(form=form, formset = formset, formset1 = formset1))

	def get_initial(self):
		self.initial = {'baiguullaga': self.baiguullaga}
		return super(Ajiltan_createView, self).get_initial()
class AjiltanUpdateView(Ajiltan_createView):
	form_class = TZEAUpdateForm
	def dispatch(self, request, *args, **kwargs):
		object_id = kwargs['id']
		self.object = get_object_or_404(Ajiltan, id = object_id)
		return super(AjiltanUpdateView, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(AjiltanUpdateView, self).get_form_kwargs()
		kwargs.update({'instance': self.object})
		return kwargs
	def get_formset_queryset(self):
		qs = School.objects.filter(emp = self.object, status = True)
		return qs
	def get_formset_queryset1(self):
		qs = EngineeringCertificate.objects.filter(emp = self.object, status = True)
		return qs
class TZE_Ajiltan_delgerengui(LoginRequired, TemplateView):
	perm_code_names = ['tze_hunii_noots_menu_view']
	template_name = 'tza/hunii_noots/delgerengui_div_htmls/ajiltan_delgerengui.html'
	def dispatch(self, request, *args, **kwargs):
		obj_id = kwargs['id']
		if 'year' in kwargs and 'month' in kwargs and 'day' in kwargs:
			year = int(kwargs['year'])
			month = int(kwargs['month'])
			day = int(kwargs['day'])
			if 'hour' in kwargs:
				hour = int(kwargs['hour'])
			else:
				hour = 23
			if 'minute' in kwargs:
				minute = int(kwargs['minute'])
			else:
				minute = 59
			self.date_time = datetime.datetime(*[year, month, day, hour, minute])
		else:
			self.date_time = False
		self.obj = get_object_or_404(Ajiltan, id = obj_id)
		return super(TZE_Ajiltan_delgerengui, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(TZE_Ajiltan_delgerengui, self).get_context_data(**kwargs)
		if self.date_time:
			context['is_history'] = True
			context['ajiltan'] = self.obj.get_history_object(self.date_time)
			context['date'] = self.date_time
			context['schools'] = self.obj.get_sub_objects(School, 'emp', self.date_time)
			context['engineer_certificates'] = self.obj.get_sub_objects(EngineeringCertificate, 'emp', self.date_time)
		else:
			context['is_history'] = False
			context['ajiltan'] = self.obj
			context['schools'] = self.obj.school_set.filter(status=True)
			context['engineer_certificates'] = self.obj.engineeringcertificate_set.filter(status=True)
		return context
class TZE_AjiltanDeleteView(Base_Ajax_FormView):
	perm_code_names = ['add_ajiltan']
	form_class = EmptyForm
	success_url = reverse_lazy('ajiltan')
	template_name = 'employee/form_div_htmls/tze_ajiltan_delete.html'
	def dispatch(self, request, *args, **kwargs):
		object_id = kwargs['id']
		self.object = get_object_or_404(Ajiltan, id = object_id)
		return super(TZE_AjiltanDeleteView, self).dispatch(request, *args, **kwargs)
	def form_valid(self, form):
		self.object.status = False
		self.object.begin_time = timezone.now()
		self.object.save()
		return super(TZE_AjiltanDeleteView, self).form_valid(form)
class TZE_alba_tasag_update(Base_Ajax_FormView):
	perm_code_names = ['add_tasag']
	template_name = 'employee/form_div_htmls/tze_alba_tasag_insert.html'
	form_class = Alba_tasag_form
	success_url = reverse_lazy('tze_ajiltan_alba_tasag_list')
	def dispatch(self, request, *args, **kwargs):
		object_id = kwargs['id']
		self.object = get_object_or_404(Tasag, id = object_id)
		self.view_url = reverse_lazy('tze_alba_tasag_update', kwargs={'id': object_id})
		return super(TZE_alba_tasag_update, self).dispatch(request, *args, **kwargs)
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.begin_time = timezone.now()
		self.object.save()
		return super(TZE_alba_tasag_update, self).form_valid(form)
	def get_form_kwargs(self):
		kwargs = super(TZE_alba_tasag_update, self).get_form_kwargs()
		kwargs.update({'instance': self.object})
		return kwargs
class TZE_alba_tasag_delete(Base_Ajax_FormView):
	perm_code_names = ['add_tasag']
	template_name = 'employee/form_div_htmls/tze_alba_tasag_delete.html'
	form_class = EmptyForm
	success_url = reverse_lazy('tze_ajiltan_alba_tasag_list')
	def dispatch(self, request, *args, **kwargs):
		object_id = kwargs['id']
		self.object = get_object_or_404(Tasag, id = object_id)
		self.view_url = reverse_lazy('tze_alba_tasag_delete', kwargs={'id': object_id})
		return super(TZE_alba_tasag_delete, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(TZE_alba_tasag_delete, self).get_context_data(**kwargs)
		context['ajiltan_count'] = self.object.get_ajiltan_queryset().count()
		return context
	def form_valid(self, form):
		if self.object.get_ajiltan_queryset().count() == 0:
			self.object.status = False
			self.object.created_by = self.user
			self.object.begin_time = timezone.now()
			self.object.save()
		return super(TZE_alba_tasag_delete, self).form_valid(form)
@csrf_exempt
def nameFilter(request):
	a = []
	if request.method == 'POST':
		b = request.POST.get('emp_name')
		c = request.POST.get('tze')
		e = request.POST.get('reg')
		for emp in Ajiltan.objects.filter(emp_name__contains = b, baiguullaga = TZE.objects.get(id = c), emp_reg__contains = e, status = True):
			d = str(emp.begin_time)
			a.append({'name' : emp.emp_name, 'id' : emp.id, 'lname' : emp.emp_lname, 'reg' : emp.emp_reg , 'phone' : emp.phone, 'nas':emp.nas, 'gender' : emp.gender, 'begin_time': d[0:16] })
	return HttpResponse(json.dumps(a), content_type="application/json")












''' Tonog tohooromj menu '''
class TohooromjjView(LoginRequired, TemplateView):
	perm_code_names =['tze_tonog_tohooromj_menu_view']
	template_name = "tonog_tohooromj/tohooromj.html"

	def get_context_data(self, **kwargs):
		context = super(TohooromjjView, self).get_context_data(**kwargs)
		object1 = BB.objects.filter(tze = self.baiguullaga, status=True)
		object2 = Hudag.objects.filter(tze = self.baiguullaga, status=True)
		object3 = UsanSan.objects.filter(tze = self.baiguullaga, status=True)
		object4 = NasosStants.objects.filter(tze = self.baiguullaga, status=True)
		object5 = Lab.objects.filter(tze = self.baiguullaga, status=True)
		object6 = Sh_suljee.objects.filter(tze = self.baiguullaga, status=True)
		object7 = Ts_baiguulamj.objects.filter(tze = self.baiguullaga, status=True)
		object8 = Car.objects.filter(tze = self.baiguullaga, status=True)
		object9 = WaterCar.objects.filter(tze = self.baiguullaga, status=True)
		object10 = BohirCar.objects.filter(tze = self.baiguullaga, status=True)
		object11 = UsDamjuulahBair.objects.filter(tze = self.baiguullaga, status=True)
		object12 = UsTugeehBair.objects.filter(tze = self.baiguullaga, status=True)
		object13 = Equipment.objects.filter(tze = self.baiguullaga, status=True)
		object14 = ABB.objects.filter(tze = self.baiguullaga, status = True)
		object15 = HudagNegtsgesenBairshliinZurag.objects.filter(tze = self.baiguullaga, status = True)

		context['object_list'] = object2
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

		url_niit_bb_list = reverse_lazy('tze_bb_list')
		url_hudag_list = reverse_lazy('tze_gunii_hudag_list')
		url_usansan_list = reverse_lazy('tze_usan_san_list')
		url_nasos_list = reverse_lazy('tze_nasos_list')
		url_lab_list = reverse_lazy('tze_lab_list')
		url_sh_suljee_list = reverse_lazy('tze_sh_suljee_list')
		url_ts_baig_list = reverse_lazy('tze_ts_baig_list')
		url_niit_car_list = reverse_lazy('tze_car_list')
		url_water_car_list = reverse_lazy('tze_water_car_list')
		url_bohir_car_list = reverse_lazy('tze_bohir_car_list')
		url_us_damjuulah_list = reverse_lazy('tze_us_damjuulah_list')
		url_us_tugeeh_list = reverse_lazy('tze_us_tugeeh_list')
		url_equipment_list = reverse_lazy('tze_tonog_tohooromj_list')
		url_abb_list = reverse_lazy('tze_hariutsaj_barilguud_list')
		url_us_hangamj_schema_list = reverse_lazy('tze_us_hangamj_schema_list')
			

		context['url_niit_bb_list'] = url_niit_bb_list
		context['url_hudag_list'] = url_hudag_list
		context['url_usansan_list'] = url_usansan_list
		context['url_nasos_list'] = url_nasos_list
		context['url_lab_list'] = url_lab_list
		context['url_sh_suljee_list'] = url_sh_suljee_list
		context['url_ts_baig_list'] = url_ts_baig_list
		context['url_niit_car_list'] = url_niit_car_list
		context['url_water_car_list'] = url_water_car_list
		context['url_bohir_car_list'] = url_bohir_car_list
		context['url_us_damjuulah_list'] = url_us_damjuulah_list
		context['url_us_tugeeh_list'] = url_us_tugeeh_list
		context['url_equipment_list'] = url_equipment_list
		context['url_abb_list'] = url_abb_list
		context['url_us_hangamj_schema_list'] = url_us_hangamj_schema_list
		return context

class Tohooromj_Gunii_Hudag_list(LoginRequired, ListView):
	perm_code_names = ['tze_tonog_tohooromj_menu_view']
	template_name = 'tonog_tohooromj/list_htmls/tze_gunii_hudag_list.html'
	def get_queryset(self):
		queryset = Hudag.objects.filter(tze = self.baiguullaga, status = True)
		return queryset
class Tohooromj_Usan_San_list(LoginRequired, ListView):
	perm_code_names = ['tze_tonog_tohooromj_menu_view']
	template_name = 'tonog_tohooromj/list_htmls/tze_usan_san_list.html'
	def get_queryset(self):
		queryset = UsanSan.objects.filter(tze = self.baiguullaga, status = True)
		return queryset
class Tohooromj_Nasos_list(LoginRequired, ListView):
	perm_code_names = ['tze_tonog_tohooromj_menu_view']
	template_name = 'tonog_tohooromj/list_htmls/tze_nasos_list.html'
	def get_queryset(self):
		queryset = NasosStants.objects.filter(tze = self.baiguullaga, status = True)
		return queryset
class Tohooromj_Lab_list(LoginRequired, ListView):
	perm_code_names = ['tze_tonog_tohooromj_menu_view']
	template_name = 'tonog_tohooromj/list_htmls/tze_lab_list.html'
	def get_queryset(self):
		queryset = Lab.objects.filter(tze = self.baiguullaga, status = True)
		return queryset
class Tohooromj_Sh_Suljee_list(LoginRequired, ListView):
	perm_code_names = ['tze_tonog_tohooromj_menu_view']
	template_name = 'tonog_tohooromj/list_htmls/tze_sh_suljee_list.html'
	def get_queryset(self):
		queryset = Sh_suljee.objects.filter(tze = self.baiguullaga, status = True)
		return queryset
class Tohooromj_Ts_Baiguulamj_list(LoginRequired, ListView):
	perm_code_names = ['tze_tonog_tohooromj_menu_view']
	template_name = 'tonog_tohooromj/list_htmls/tze_ts_baiguulamj_list.html'
	def get_queryset(self):
		queryset = Ts_baiguulamj.objects.filter(tze = self.baiguullaga, status = True)
		return queryset
class Tohooromj_Us_Tugeeh_list(LoginRequired, ListView):
	perm_code_names = ['tze_tonog_tohooromj_menu_view']
	template_name = 'tonog_tohooromj/list_htmls/tze_us_tugeeh_list.html'
	def get_queryset(self):
		queryset = UsTugeehBair.objects.filter(tze = self.baiguullaga, status = True)
		return queryset
class Tohooromj_Us_Damjuulah_list(LoginRequired, ListView):
	perm_code_names = ['tze_tonog_tohooromj_menu_view']
	template_name = 'tonog_tohooromj/list_htmls/tze_us_damjuulah_list.html'
	def get_queryset(self):
		queryset = UsDamjuulahBair.objects.filter(tze = self.baiguullaga, status = True)
		return queryset

class TZE_hariutsaj_barilguud_list(LoginRequired, ListView):
	perm_code_names = ['tze_tonog_tohooromj_menu_view']
	template_name = 'tonog_tohooromj/list_htmls/tze_abb_list.html'
	def get_queryset(self):
		queryset = ABB.objects.filter(tze = self.baiguullaga, status = True)
		return queryset
class Us_hangamjiin_schema_zurag_list(LoginRequired, ListView):
	perm_code_names = ['tze_tonog_tohooromj_menu_view']
	template_name = 'tonog_tohooromj/list_htmls/tze_us_hangamj_schema_list.html'
	def get_queryset(self):
		queryset = HudagNegtsgesenBairshliinZurag.objects.filter(tze = self.baiguullaga, status = True)
		return queryset

class Tohooromj_Water_Car_list(LoginRequired, ListView):
	perm_code_names = ['tze_tonog_tohooromj_menu_view']
	template_name = 'tonog_tohooromj/list_htmls/tze_water_car_list.html'
	def get_queryset(self):
		queryset = WaterCar.objects.filter(tze = self.baiguullaga, status = True)
		return queryset
class Tohooromj_Bohir_Car_list(LoginRequired, ListView):
	perm_code_names = ['tze_tonog_tohooromj_menu_view']
	template_name = 'tonog_tohooromj/list_htmls/tze_bohir_car_list.html'
	def get_queryset(self):
		queryset = BohirCar.objects.filter(tze = self.baiguullaga, status = True)
		return queryset
class Tohooromj_Tonog_Tohooromj_list(LoginRequired, ListView):
	perm_code_names = ['tze_tonog_tohooromj_menu_view']
	template_name = 'tonog_tohooromj/list_htmls/tze_tonog_tohooromj_list.html'
	def get_queryset(self):
		queryset = Equipment.objects.filter(tze = self.baiguullaga, status = True)
		return queryset

class Tohooromj_Lab_shinjilgee_list(LoginRequired, TemplateView):
	perm_code_names = ['tze_tonog_tohooromj_menu_view']
	template_name = 'tonog_tohooromj/list_htmls/tze_lab_shinjilgee_list.html'
	def dispatch(self, request, *args, **kwargs):
		object_id = kwargs['id']
		self.obj = get_object_or_404(Lab, id=object_id)
		return super(Tohooromj_Lab_shinjilgee_list, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(Tohooromj_Lab_shinjilgee_list, self).get_context_data(**kwargs)
		context['shinjilgee_list'] = self.obj.get_shinjilgee_list_names()
		context['obj'] = self.obj
		return context

class Tohooromj_delgerengui_base(LoginRequired, TemplateView):
	perm_code_names = ['tze_tonog_tohooromj_menu_view']
	template_name = 'tonog_tohooromj/tonog_tohooromj_delgerengui/hudag_delgerengui.html'
	object_class = None
	def dispatch(self, request, *args, **kwargs):
		obj_id = kwargs['id']
		if 'year' in kwargs and 'month' in kwargs and 'day' in kwargs:
			year = int(kwargs['year'])
			month = int(kwargs['month'])
			day = int(kwargs['day'])
			if 'hour' in kwargs:
				hour = int(kwargs['hour'])
			else:
				hour = 23
			if 'minute' in kwargs:
				minute = int(kwargs['minute'])
			else:
				minute = 59
			self.date_time = datetime.datetime(*[year, month, day, hour, minute])
		else:
			self.date_time = False
		self.obj = get_object_or_404(self.object_class, id = obj_id)
		return super(Tohooromj_delgerengui_base, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(Tohooromj_delgerengui_base, self).get_context_data(**kwargs)
		if self.date_time:
			context['is_history'] = True
			context['obj'] = self.obj.get_history_object(self.date_time)
			context['date'] = self.date_time
		else:
			context['is_history'] = False
			context['obj'] = self.obj
		return context
class Tohooromj_Gunii_Hudag_delgerengui(Tohooromj_delgerengui_base):
	template_name = 'tonog_tohooromj/tonog_tohooromj_delgerengui/hudag_delgerengui.html'
	object_class = Hudag
	
class Tohooromj_Usan_San_delgerengui(Tohooromj_delgerengui_base):
	template_name = 'tonog_tohooromj/tonog_tohooromj_delgerengui/usansan_delgerengui.html'
	object_class = UsanSan

class Tohooromj_NasosStants_delgerengui(Tohooromj_delgerengui_base):
	template_name = 'tonog_tohooromj/tonog_tohooromj_delgerengui/nasosStants_delgerengui.html'
	object_class = NasosStants
	def get_context_data(self, **kwargs):
		context = super(Tohooromj_NasosStants_delgerengui, self).get_context_data(**kwargs)
		if context['is_history']:
			context['sub_objects'] = self.obj.get_sub_objects(Nasoss, 'nasos_stants', self.date_time)
		else:
			context['sub_objects'] = Nasoss.objects.filter(nasos_stants = self.obj, status=True)
		return context
class Tohooromj_Lab_delgerengui(Tohooromj_delgerengui_base):
	template_name = 'tonog_tohooromj/tonog_tohooromj_delgerengui/lab_delgerengui.html'
	object_class = Lab
	def get_context_data(self, **kwargs):
		context=super(Tohooromj_Lab_delgerengui, self).get_context_data(**kwargs)
		if context['is_history']:
			context['lab_bagaj'] = self.obj.get_sub_objects(LabBagaj, 'lab_id', self.date_time)
			context['lab_orgotgol'] = self.obj.get_sub_objects(Lab_orgotgol, 'lab_id', self.date_time)
		else:
			context['lab_bagaj'] = LabBagaj.objects.filter(lab_id=self.obj, status = True)
			context['lab_orgotgol'] = Lab_orgotgol.objects.filter(lab_id=self.obj, status = True)
		return context
class Tohooromj_Sh_Suljee_delgerengui(Tohooromj_delgerengui_base):
	template_name = 'tonog_tohooromj/tonog_tohooromj_delgerengui/suljee_delgerengui.html'
	object_class = Sh_suljee
	def get_context_data(self, **kwargs):
		context = super(Tohooromj_Sh_Suljee_delgerengui, self).get_context_data(**kwargs)
		if context['is_history']:
			context['sub_objects'] = self.obj.get_sub_objects(Hooloi, 'sh_suljee', self.date_time)
		else:
			context['sub_objects'] = Hooloi.objects.filter(sh_suljee = self.obj, status=True)
		return context
class Tohooromj_Ts_Baiguulamj_delgerengui(Tohooromj_delgerengui_base):
	template_name = 'tonog_tohooromj/tonog_tohooromj_delgerengui/tseverleh_delgerengui.html'
	object_class = Ts_baiguulamj
	def get_context_data(self, **kwargs):
		context = super(Tohooromj_Ts_Baiguulamj_delgerengui, self).get_context_data(**kwargs)
		if context['is_history']:
			context['sub_objects'] = self.obj.get_sub_objects(Ts_tohooromj, 'ts_baiguulamj', self.date_time)
		else:
			context['sub_objects'] = Ts_tohooromj.objects.filter(ts_baiguulamj = self.obj, status=True)
		return context
class Tohooromj_Us_Tugeeh_delgerengui(Tohooromj_delgerengui_base):
	template_name = 'tonog_tohooromj/tonog_tohooromj_delgerengui/ustugeeh_delgerengui.html'
	object_class = UsTugeehBair
class Tohooromj_Us_Damjuulah_delgerengui(Tohooromj_delgerengui_base):
	template_name = 'tonog_tohooromj/tonog_tohooromj_delgerengui/usdamjuulah_delgerengui.html'
	object_class = UsDamjuulahBair
	def get_context_data(self, **kwargs):
		context=super(Tohooromj_Us_Damjuulah_delgerengui, self).get_context_data(**kwargs)
		if context['is_history']:
			qs = self.obj.get_sub_objects(UsDamjuulahBairTonog, 'us_id', self.date_time)
			context['sub_objects'] = qs
		else:
			context['sub_objects'] = UsDamjuulahBairTonog.objects.filter(us_id = self.obj, status=True)
		return context
class Tohooromj_Water_Car_delgerengui(Tohooromj_delgerengui_base):
	template_name = 'tonog_tohooromj/tonog_tohooromj_delgerengui/watercar_delgerengui.html'
	object_class = WaterCar
class Tohooromj_Bohir_Car_delgerengui(Tohooromj_delgerengui_base):
	template_name = 'tonog_tohooromj/tonog_tohooromj_delgerengui/bohircar_delgerengui.html'
	object_class = BohirCar
class Tohooromj_Tonog_Tohooromj_delgerengui(Tohooromj_delgerengui_base):
	template_name = 'tonog_tohooromj/tonog_tohooromj_delgerengui/tonog_delgerengui.html'
	object_class = Equipment
class Tohooromj_ABB_delgerengui(Tohooromj_delgerengui_base):
	template_name = 'tonog_tohooromj/tonog_tohooromj_delgerengui/abb_delgerengui.html'
	object_class = ABB



class HudagZuragFormView(Base_Ajax_FormView):
	perm_code_names = ['add_hudagnegtsgesenbairshliinzurag']
	form_class = HudagNegtsgesenBairshliinZuragForm
	template_name = 'tonog_tohooromj/form_div_htmls/hudag_zurag_form_div.html'
	success_url = reverse_lazy('tze_us_hangamj_schema_list')
	def form_valid(self, form):
		obj = form.save(commit=False)
		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		obj.tze = tze 
		obj.created_by= self.user
		obj.status= True
		obj.save()
		return super(HudagZuragFormView, self).form_valid(form)
	def form_invalid(self, form):
		#return JsonResponse(form.errors)
		return JsonResponse({'stat': 'error', 'error_messages': form.errors.as_json(),})

class HudagFormView(Base_Ajax_FormView):
	perm_code_names = ['add_hudag']
	success_url = reverse_lazy('tze_gunii_hudag_list')
	form_class = Gunii_Hudag_insertForm
	template_name = 'tonog_tohooromj/form_div_htmls/hudag_form_div.html'
	view_url = reverse_lazy('hudag_insert')

	def form_valid(self, form):
		obj = form.save(commit = False)
		obj.created_by= self.user
		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		obj.tze = tze
		obj.status= True
		obj.save()
		obj_bb = get_object_or_404(BB, id = obj.id)
		obj_bb.save()
		return super(HudagFormView, self).form_valid(form)
class UsanSanFormView(Base_Ajax_FormView):
	perm_code_names = ['add_usansan']
	form_class = UsanSanForm
	template_name = 'tonog_tohooromj/form_div_htmls/usansan_form_div.html'
	success_url = reverse_lazy('tze_usan_san_list')
	def form_valid(self, form):
		obj = form.save(commit = False)
		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		obj.tze = tze
		obj.status = True
		obj.created_by = self.user
		obj.save()
		obj_bb = get_object_or_404(BB, id = obj.id)
		obj_bb.save()
		return super(UsanSanFormView, self).form_valid(form)
class UsTugeehBairFormView(Base_Ajax_FormView):
	perm_code_names = ['add_ustugeehbair']
	form_class = UsTugeehBairForm
	template_name = 'tonog_tohooromj/form_div_htmls/us_tugeeh_form_div.html'
	success_url = reverse_lazy('tze_us_tugeeh_list')
	def form_valid(self, form):
		obj = form.save(commit=False)
		tze = get_object_or_404(TZE, id=self.baiguullaga.id)
		obj.tze = tze
		obj.status = True
		obj.created_by = self.user
		obj.save()
		obj_bb = get_object_or_404(BB, id = obj.id)
		obj_bb.save()
		return super(UsTugeehBairFormView, self).form_valid(form)
class WaterCarFormView(Base_Ajax_FormView):
	perm_code_names = ['add_watercar']
	form_class = WaterCarForm
	template_name = 'tonog_tohooromj/form_div_htmls/car_form_div.html'
	success_url = reverse_lazy('tze_water_car_list')
	def form_valid(self, form):
		obj = form.save(commit = False)
		tze = get_object_or_404(TZE, id=self.baiguullaga.id)
		obj.tze = tze
		obj.created_by = self.user
		obj.status= True
		obj.save()
		return super(WaterCarFormView, self).form_valid(form)
class BohirCarFormView(Base_Ajax_FormView):
	perm_code_names = ['add_bohircar']
	form_class = BohirCarForm
	template_name = 'tonog_tohooromj/form_div_htmls/bohircar_form_div.html'
	success_url = reverse_lazy('tze_bohir_car_list')
	def form_valid(self, form):
		obj = form.save(commit = False)
		tze = get_object_or_404(TZE, id=self.baiguullaga.id)
		obj.tze = tze
		obj.created_by = self.user
		obj.status= True
		obj.save()
		return super(BohirCarFormView, self).form_valid(form)
class EquipmentFormView(Base_Ajax_FormView):
	perm_code_names = ['add_equipment']
	form_class = EquipmentForm
	template_name = 'tonog_tohooromj/form_div_htmls/tonog_form_div.html'
	success_url = reverse_lazy('tze_tonog_tohooromj_list')
	def form_valid(self, form):
		obj = form.save(commit = False)
		tze = get_object_or_404(TZE, id=self.baiguullaga.id)
		obj.tze = tze
		obj.status = True
		obj.created_by = self.user
		obj.save()
		return super(EquipmentFormView, self).form_valid(form)
class Hariutssan_barilguud_FormView(Base_Ajax_FormView):
	perm_code_names = ['add_abb']
	template_name = 'tonog_tohooromj/form_div_htmls/hariutssan_barilguud_form.html'
	success_url = reverse_lazy('tze_hariutsaj_barilguud_list')
	form_class = ABBForm
	view_url = reverse_lazy('hariutssan_barilguud_insert')
	def form_valid(self, form):
		obj = form.save(commit=False)
		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		obj.tze = tze
		obj.created_by = self.user
		obj.status = True
		obj.save()
		#messages.success(self.request, 'Амжилттай хадгаллаа.')
		return super(Hariutssan_barilguud_FormView, self).form_valid(form)
	def get_context_data(self, **kwargs):
		context = super(Hariutssan_barilguud_FormView, self).get_context_data(**kwargs)
		context['view_url'] = self.view_url
		return context

class NasosStantsFormView(LoginRequired, BaseFormView_with_formset):
	perm_code_names = ['add_nasosstants']
	form_class = NasosForm
	formset_class = Nasoss_formset
	formset_queryset = Nasoss.objects.none()
	template_name = 'tonog_tohooromj/form_div_htmls/nasos_stants_form_div.html'
	success_url = reverse_lazy('tze_nasos_list')
	
	def form_valid(self, form, formset):
		print 'nasos stants form \n\n\n\n\n'
		obj = form.save(commit = False)
		tze = get_object_or_404(TZE, id=self.baiguullaga.id)
		obj.tze = tze
		obj.status = True
		obj.created_by = self.user
		obj.save()
		obj_bb = get_object_or_404(BB, id = obj.id)
		obj_bb.save()
		new_objs = formset.save(commit = False)
		for i in new_objs:
			i.nasos_stants = obj
			i.status = True
			i.begin_time = timezone.now()
			i.save()
			print 'ne object'
		for f in formset.deleted_forms:
			at = f.cleaned_data['id']
			if at:
				at.status = False
				at.save()
		return super(NasosStantsFormView, self).form_valid(form, formset)
class ShugamSuljeeFormView(LoginRequired, BaseFormView_with_formset):
	perm_code_names = ['add_sh_suljee']
	form_class = Sh_suljeeForm
	template_name = 'tonog_tohooromj/form_div_htmls/shugam_form_div.html'
	formset_class = Hooloi_formset
	formset_queryset = Hooloi.objects.none()
	success_url = reverse_lazy('tze_sh_suljee_list')

	def form_valid(self, form, formset):
		print "shugam form \n\n\n"
		obj = form.save(commit = False)
		tze = get_object_or_404(TZE, id=self.baiguullaga.id)
		obj.tze = tze
		obj.created_by = self.user
		obj.status = True
		obj.save()
		obj_bb = get_object_or_404(BB, id = obj.id)
		obj_bb.save()
		new_objs = formset.save(commit = False)
		for i in new_objs:
			i.sh_suljee = obj
			i.status = True
			i.begin_time = timezone.now()
			i.save()
		for f in formset.deleted_forms:
			at = f.cleaned_data['id']
			if at:
				at.status = False
				at.save()
		return super(ShugamSuljeeFormView, self).form_valid(form, formset)
class TseverlehBaiguulamjFormView(LoginRequired, BaseFormView_with_formset):
	perm_code_names = ['add_ts_baiguulamj']
	form_class = Ts_baiguulamjForm
	template_name = 'tonog_tohooromj/form_div_htmls/ts_baiguulamj_form_div.html'
	formset_class = Ts_tohooromj_formset
	formset_queryset = Ts_tohooromj.objects.none()
	success_url = reverse_lazy('tze_ts_baig_list')

	def form_valid(self, form, formset):
		obj = form.save(commit = False)
		tze = get_object_or_404(TZE, id=self.baiguullaga.id)
		obj.tze = tze
		obj.created_by = self.user
		obj.status = True
		obj.save()
		obj_bb = get_object_or_404(BB, id = obj.id)
		obj_bb.save()
		new_objs = formset.save(commit = False)
		for i in new_objs:
			i.ts_baiguulamj = obj
			i.status = True
			i.begin_time = timezone.now()
			i.save()
		for f in formset.deleted_forms: # ustgasan alban_tushaaluudiig ustgaj baina
			at = f.cleaned_data['id']
			if at:
				at.status = False
				at.save()
		return super(TseverlehBaiguulamjFormView, self).form_valid(form, formset)
class UsDamjuulahBairFormView(LoginRequired, BaseFormView_with_formset):
	perm_code_names = ['add_usdamjuulahbair']
	form_class = UsDamjuulahBairForm
	template_name = 'tonog_tohooromj/form_div_htmls/us_damjuulah_form_div.html'
	formset_class = UsDamjuulahBairTonog_formset
	formset_queryset = UsDamjuulahBairTonog.objects.none()
	success_url = reverse_lazy('tze_us_damjuulah_list')
	def form_valid(self, form, formset):
		obj = form.save(commit = False)
		tze = get_object_or_404(TZE, id=self.baiguullaga.id)
		obj.tze = tze
		obj.created_by = self.user
		obj.status= True
		obj.save()
		obj_bb = get_object_or_404(BB, id = obj.id)
		obj_bb.save()

		new_objs = formset.save(commit = False)
		for i in new_objs:
			i.tze = tze
			i.us_id = obj
			i.status = True
			i.created_by = self.user
			i.save()
		for f in formset.deleted_forms:
			at = f.cleaned_data['id']
			if at:
				at.status = False
				at.save()
		return super(UsDamjuulahBairFormView, self).form_valid(form, formset)
class LabFormView(LoginRequired, BaseFormView_with_formset):
	perm_code_names = ['add_lab']
	form_class = LabForm
	template_name = 'tonog_tohooromj/form_div_htmls/lab_form_div.html'
	success_url = reverse_lazy('tze_lab_list')

	formset_class = LabBagaj_formset
	formset_class1 = Lab_orgotgol_formset


	formset_prefix = 'prefix'
	formset_queryset = LabBagaj.objects.none()

	formset_initial1 = {}
	formset_prefix1 = 'prefix1'
	formset_queryset1 = Lab_orgotgol.objects.none()



	def get(self,request, *args, **kwargs):
		form = self.get_form()
		formset = self.get_formset()
		formset1 = self.get_formset1()
		return self.render_to_response(self.get_context_data(form=form, formset = formset, formset1 = formset1))
	def post(self, request, *args, **kwargs):
		form = self.get_form()
		formset = self.get_formset()
		formset1 = self.get_formset1()
		if form.is_valid() and formset.is_valid() and formset1.is_valid():
			return self.form_valid(form, formset, formset1)
		else:
			return self.form_invalid(form, formset, formset1)
	
	def get_formset1(self, formset_class1 = None):
		if formset_class1 is None:
			formset_class1 = self.get_formset_class1()
		return formset_class1(**self.get_formset_kwargs1())

	
	def get_formset_class1(self):
		return self.formset_class1

	
	def get_formset_kwargs1(self):
		kwargs = {
		'initial': self.get_formset_initial1(),
		'prefix': self.get_formset_prefix1(),
		'queryset': self.get_formset_queryset1(),
		}
		if self.request.method in ('POST', 'PUT'):
			kwargs.update({
			    'data': self.request.POST,
			    'files': self.request.FILES,
			})
		return kwargs

	
	def get_formset_initial1(self):
		return self.formset_initial1.copy()
	def get_formset_prefix1(self):
		return self.formset_prefix1
	def get_formset_queryset1(self):
		return self.formset_queryset1


	def form_valid(self, form, formset, formset1):
		obj = form.save(commit = False)
		tze = get_object_or_404(TZE, id=self.baiguullaga.id)
		obj.tze = tze
		obj.created_by = self.user
		obj.status= True
		obj.save()
		obj_bb = get_object_or_404(BB, id = obj.id)
		obj_bb.save()
		lab_bagajs = formset.save(commit = False)
		for i in lab_bagajs:
			i.lab_id = obj
			i.status = True
			i.begin_time = timezone.now()
			i.save()
		for f in formset.deleted_forms:
			at = f.cleaned_data['id']
			if at:
				at.status = False
				at.save()
		lab_orgotgols = formset1.save(commit = False)
		for i in lab_orgotgols:
			i.lab_id = obj
			i.status = True
			i.begin_time = timezone.now()
			i.save()
		for f in formset1.deleted_forms:
			at = f.cleaned_data['id']
			if at:
				at.status = False
				at.save()

		return HttpResponseRedirect(self.get_success_url())
	def form_invalid(self, form, formset, formset1):
		return self.render_to_response(self.get_context_data(form=form, formset = formset, formset1 = formset1))


class UsanSan_UgaalgaFormView(LoginRequired, BaseFormView_with_formset):
	perm_code_names = ['add_usansanugaalga']
	form_class = EmptyForm
	template_name = 'tonog_tohooromj/form_div_htmls/tze_usansan_ugaalga_form.html'
	formset_class = UsanSanUgaalga_formset
	success_url = reverse_lazy('tohooromj_menu')
	def dispatch(self, request, *args, **kwargs):
		object_id = kwargs['id']
		self.object = get_object_or_404(UsanSan, id = object_id)
		return super(UsanSan_UgaalgaFormView, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(UsanSan_UgaalgaFormView, self).get_context_data(**kwargs)
		context['view_url'] = reverse_lazy('tze_usan_san_wash_edit', kwargs={'id': self.object.id})
		return context
	def get_formset_queryset(self):
		return UsanSanUgaalga.objects.filter(usansan_id = self.object, status = True)
	def form_valid(self, form, formset):
		#form.save()
		new_objs = formset.save(commit = False)
		for i in new_objs: # shineer nemegdsen, bolon oorchlogdson alban tushaaluudiig hadgalj baina
			i.usansan_id = self.object
			i.status = True
			i.created_by = self.user
			i.save()
		for f in formset.deleted_forms: # ustgasan alban_tushaaluudiig ustgaj baina
			at = f.cleaned_data['id']
			if at:
				at.status = False
				at.created_by = self.user
				at.save()
		return super(UsanSan_UgaalgaFormView, self).form_valid(form, formset)
	def form_invalid(self, form, formset):
		return HttpResponseRedirect(self.get_success_url())
class UsanSan_UgaalgaListView(LoginRequired, ListView):
	perm_code_names = ['tze_tonog_tohooromj_menu_view']
	template_name = 'tonog_tohooromj/tonog_tohooromj_delgerengui/tze_usansan_wash_delgerengui_list.html'
	def dispatch(self, request, *args, **kwargs):
		object_id = kwargs['id']
		self.object = get_object_or_404(UsanSan, id = object_id)
		return super(UsanSan_UgaalgaListView, self).dispatch(request, *args, **kwargs)
	def get_queryset(self):
		queryset = UsanSanUgaalga.objects.filter(usansan_id = self.object, status = True)
		return queryset
	def get_context_data(self, **kwargs):
		context = super(UsanSan_UgaalgaListView, self).get_context_data(**kwargs)
		context['obj'] = self.object
		return context
class UsTugeehB_Sav_ugaalgaFormView(LoginRequired, BaseFormView_with_formset):
	perm_code_names = ['add_ustugeehbairsavugaalga']
	form_class = EmptyForm
	template_name = 'tonog_tohooromj/form_div_htmls/tze_ustugeeh_ugaalga_form.html'
	formset_class = UsTugeehBairSavUgaalga_formset
	success_url = reverse_lazy('tohooromj_menu')
	def dispatch(self, request, *args, **kwargs):
		object_id = kwargs['id']
		self.object = get_object_or_404(UsTugeehBair, id = object_id)
		return super(UsTugeehB_Sav_ugaalgaFormView, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(UsTugeehB_Sav_ugaalgaFormView, self).get_context_data(**kwargs)
		context['view_url'] = reverse_lazy('tze_us_tugeeh_wash_edit', kwargs={'id': self.object.id})
		return context
	def get_formset_queryset(self):
		return UsTugeehBairSavUgaalga.objects.filter(ussav_id = self.object, status = True)
	def form_valid(self, form, formset):
		#form.save()
		new_objs = formset.save(commit = False)
		for i in new_objs:
			i.ussav_id = self.object
			i.status = True
			i.created_by = self.user
			i.save()
		for f in formset.deleted_forms: 
			at = f.cleaned_data['id']
			if at:
				at.status = False
				at.created_by = self.user
				at.save()
		return super(UsTugeehB_Sav_ugaalgaFormView, self).form_valid(form, formset)
	def form_invalid(self, form, formset):
		return HttpResponseRedirect(self.get_success_url())


class Base_BB_UpdateView(UpdateView):
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.created_by = self.user
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())
class HudagUpdateView(LoginRequired, Base_BB_UpdateView):
	perm_code_names = ['add_hudag']
	template_name = 'tonog_tohooromj/form_div_htmls/hudag_form_div.html'
	model = Hudag
	form_class = Gunii_Hudag_insertForm
	success_url = reverse_lazy('tze_gunii_hudag_list')
class UsansanUpdateView(LoginRequired, Base_BB_UpdateView):
	perm_code_names = ['add_usansan']
	template_name = 'tonog_tohooromj/form_div_htmls/usansan_form_div.html'
	model = UsanSan
	form_class = UsanSanUpdateForm
	success_url = reverse_lazy('tze_usan_san_list')
	def get_form_kwargs(self):
		kwargs = super(UsansanUpdateView, self).get_form_kwargs()
		kwargs['usansan_id'] = self.object.id
		return kwargs
class WatercarUpdateView(LoginRequired, Base_BB_UpdateView):
	perm_code_names = ['add_watercar']
	template_name = 'tonog_tohooromj/form_div_htmls/car_form_div.html'
	model = WaterCar
	form_class = WaterCarUpdateForm
	success_url = reverse_lazy('tze_water_car_list')
	def get_form_kwargs(self):
		kwargs = super(WatercarUpdateView, self).get_form_kwargs()
		kwargs['watercar_id'] = self.object.id
		return kwargs
class BohircarUpdateView(LoginRequired, Base_BB_UpdateView):
	perm_code_names = ['add_bohircar']
	template_name = 'tonog_tohooromj/form_div_htmls/bohircar_form_div.html'
	model = BohirCar
	form_class = BohirCarUpdateForm
	success_url = reverse_lazy('tze_bohir_car_list')
	def get_form_kwargs(self):
		kwargs = super(BohircarUpdateView, self).get_form_kwargs()
		kwargs['bohircar_id'] = self.object.id
		return kwargs
class UstugeehUpdateView(LoginRequired, Base_BB_UpdateView):
	perm_code_names = ['add_ustugeehbair']
	template_name = 'tonog_tohooromj/form_div_htmls/us_tugeeh_form_div.html'
	model = UsTugeehBair
	form_class = UsTugeehBairUpdateForm
	success_url = reverse_lazy('tze_us_tugeeh_list')
	def get_form_kwargs(self):
		kwargs = super(UstugeehUpdateView, self).get_form_kwargs()
		kwargs['ustugeeh_id'] = self.object.id
		return kwargs
class EquipmentUpdateView(LoginRequired, Base_BB_UpdateView):
	perm_code_names = ['add_equipment']
	template_name = 'tonog_tohooromj/form_div_htmls/tonog_form_div.html'
	model = Equipment
	form_class = EquipmentForm
	success_url = reverse_lazy('tze_tonog_tohooromj_list')

class NasosUpdateView(NasosStantsFormView):
	form_class = NasosUpdateForm
	def dispatch(self, request, *args, **kwargs):
		object_id = kwargs['pk']
		self.object = get_object_or_404(NasosStants, id = object_id)
		return super(NasosUpdateView, self).dispatch(request, *args, **kwargs)
	def get_form_kwargs(self):
		kwargs = super(NasosUpdateView, self).get_form_kwargs()
		kwargs.update({'instance': self.object})
		return kwargs
	def get_formset_queryset(self):
		qs = Nasoss.objects.filter(nasos_stants = self.object, status = True)
		return qs
class SuljeeUpdateView(ShugamSuljeeFormView):
	form_class = Sh_suljeeForm
	def dispatch(self, request, *args, **kwargs):
		object_id = kwargs['pk']
		self.object = get_object_or_404(Sh_suljee, id = object_id)
		return super(SuljeeUpdateView, self).dispatch(request, *args, **kwargs)
	def get_form_kwargs(self):
		kwargs = super(SuljeeUpdateView, self).get_form_kwargs()
		kwargs.update({'instance': self.object})
		return kwargs
	def get_formset_queryset(self):
		qs = Hooloi.objects.filter(sh_suljee = self.object, status = True)
		return qs
class Ts_baiguulamjUpdateView(TseverlehBaiguulamjFormView):
	form_class = Ts_baiguulamjForm
	def dispatch(self, request, *args, **kwargs):
		object_id = kwargs['pk']
		self.object = get_object_or_404(Ts_baiguulamj, id = object_id)
		return super(Ts_baiguulamjUpdateView, self).dispatch(request, *args, **kwargs)
	def get_form_kwargs(self):
		kwargs = super(Ts_baiguulamjUpdateView, self).get_form_kwargs()
		kwargs.update({'instance': self.object})
		return kwargs
	def get_formset_queryset(self):
		qs = Ts_tohooromj.objects.filter(ts_baiguulamj = self.object, status = True)
		return qs
class UsdamjuulahUpdateView(UsDamjuulahBairFormView):
	form_class = UsDamjuulahBairForm
	def dispatch(self, request, *args, **kwargs):
		object_id = kwargs['pk']
		self.object = get_object_or_404(UsDamjuulahBair, id = object_id)
		return super(UsdamjuulahUpdateView, self).dispatch(request, *args, **kwargs)
	def get_form_kwargs(self):
		kwargs = super(UsdamjuulahUpdateView, self).get_form_kwargs()
		kwargs.update({'instance': self.object})
		return kwargs
	def get_formset_queryset(self):
		qs = UsDamjuulahBairTonog.objects.filter(us_id = self.object, status = True)
		return qs
class LabUpdateView(LabFormView):
	def dispatch(self, request, *args, **kwargs):
		object_id = kwargs['pk']
		self.object = get_object_or_404(Lab, id = object_id)
		return super(LabUpdateView, self).dispatch(request, *args, **kwargs)
	def get_form_kwargs(self):
		kwargs = super(LabUpdateView, self).get_form_kwargs()
		kwargs.update({'instance': self.object})
		return kwargs
	def get_formset_queryset(self):
		qs = LabBagaj.objects.filter(lab_id = self.object, status = True)
		return qs
	def get_formset_queryset1(self):
		qs = Lab_orgotgol.objects.filter(lab_id = self.object, status = True)
		return qs

class BB_deleteView(LoginRequired, Base_DeleteView):
	perm_code_names = ['add_bb']
	success_url = reverse_lazy('tohooromj_menu')
	pk_url_kwarg = 'id'
	model = BB
	modal_header = 'Барилга байгууламжийн мэдээллийг устгах'
	confirm_question = 'Барилга байгууламжийн мэдээллийг устгах уу?'
	delete_message = 'Барилга байгууламжийн мэдээллийг устгалаа.'
	def get_view_url(self):
		return reverse_lazy('tze_bb_delete', kwargs={'id': self.object.id})
class Car_deleteView(LoginRequired, Base_DeleteView):
	perm_code_names = ['add_car']
	success_url = reverse_lazy('tohooromj_menu')
	pk_url_kwarg = 'id'
	model = Car
	modal_header = 'Тээврийн хэрэгслийн мэдээллийг устгах'
	confirm_question = 'Тээврийн хэрэгслийн мэдээллийг устгах уу?'
	delete_message = 'Тээврийн хэрэгслийн мэдээллийг устгалаа.'
	def get_view_url(self):
		return reverse_lazy('tze_car_delete', kwargs={'id': self.object.id})
class Equipment_deleteView(LoginRequired, Base_DeleteView):
	perm_code_names = ['add_equipment']
	success_url = reverse_lazy('tohooromj_menu')
	pk_url_kwarg = 'id'
	model = Equipment
	modal_header = 'Тоног төхөөрөмжийн мэдээллийг устгах'
	confirm_question = 'Тоног төхөөрөмжийн мэдээллийг устгах уу?'
	delete_message = 'Тоног төхөөрөмжийн мэдээллийг устгалаа.'
	def get_view_url(self):
		return reverse_lazy('tze_equipment_delete', kwargs={'id': self.object.id})
class Hariutssan_barilguud_DeleteView(LoginRequired, Base_DeleteView):
	perm_code_names = ['add_abb']
	success_url = reverse_lazy('baiguullaga_menu')
	pk_url_kwarg = 'id'
	model = ABB
	modal_header = 'Ашиглалтыг нь хариуцаж буй барилга, байгууламжийг устгах'
	confirm_question = 'Ашиглалтыг нь хариуцаж буй барилга, байгууламжийг устгах уу?'
	delete_message = 'Ашиглалтыг нь хариуцаж буй барилга, байгууламжийг устгалаа.'
	def get_view_url(self):
		return reverse_lazy('hariutssan_barilguud_delete', kwargs={'id': self.object.id})
class Us_hangamj_deleteView(LoginRequired, Base_DeleteView):
	perm_code_names = ['add_hudagnegtsgesenbairshliinzurag']
	success_url = reverse_lazy('tohooromj_menu')
	pk_url_kwarg = 'id'
	model = HudagNegtsgesenBairshliinZurag
	modal_header = 'Схем зургийг устгах'
	confirm_question = 'Ус хангамжийн схем зургийг устгах уу?'
	delete_message = 'Мэдээллийг устгалаа.'
	def get_view_url(self):
		return reverse_lazy('tze_us_hangamj_schema_delete', kwargs={'id': self.object.id})



class WaterAnalysisUpdateView(LoginRequired, UpdateView):
	perm_code_names = ['add_analysiswater']
	template_name = 'uamedee/water_analysis_update.html'
	model = AnalysisWater
	form_class = AnalysisWaterForm
	success_url = '/engineering/uamedee/'
class BohirAnalysisUpdateView(LoginRequired, UpdateView):
	perm_code_names = ['add_analysisbohir']
	template_name = 'uamedee/bohir_analysis_update.html'
	model = AnalysisBohir
	form_class = AnalysisBohirForm
	success_url = '/engineering/uamedee/'




''' tusgai zovshoorol menu '''
class Tusgai_zovshoorolView(LoginRequired, TemplateView):
	perm_code_names = ['tze_tusgai_zovshoorol_menu_view']
	template_name = 'tz_huselt/tusgai_zovshoorol_menu.html'

	def get_context_data(self, **kwargs):
		context = super(Tusgai_zovshoorolView, self).get_context_data(**kwargs)
		tz_huseltuud = TZ_Huselt.objects.filter(tze = self.baiguullaga)
		context['tz_huseltuud'] = tz_huseltuud
		context['tz_certificates'] = Certificate.objects.filter(tze = context['baiguullaga'], status = True)
		return context
class TZE_huselt_delgerengui(LoginRequired, TemplateView):
	perm_code_names = ['tze_tusgai_zovshoorol_menu_view']
	template_name = 'tz_huselt/list_htmls/tze_tz_huselt_delgerengui.html'
	def dispatch(self, request, *args, **kwargs):
		self._huselt_id = self.kwargs['huselt_id']
		return super(TZE_huselt_delgerengui, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(TZE_huselt_delgerengui, self).get_context_data(**kwargs)
		context['h'] = TZ_Huselt.objects.get(id = self._huselt_id)
		context['warnings'] = TZ_anhaaruulga.objects.filter(tz_huselt = context['h'])
		context['burdel_histories'] = Burdel_history.objects.filter(tz_huselt = context['h']).order_by('-ilgeesen_datetime')
		context['tz_huselt_medegdels'] = TZ_medegdel.objects.filter(tz_huselt = context['h'])
		return context
class TZE_TZ_gerchilgee_delgerengui(LoginRequired, TemplateView):
	perm_code_names = ['tze_tusgai_zovshoorol_menu_view']
	template_name = 'tza/tusgai_zovshoorol/delgerengui_div_htmls/tz_gerchilgee_delgerengui.html'
	def dispatch(self, request, *args, **kwargs):
		object_id = kwargs['tz_gerchilgee_id']
		self._object = get_object_or_404(Certificate, id = object_id)
		return super(TZE_TZ_gerchilgee_delgerengui, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(TZE_TZ_gerchilgee_delgerengui, self).get_context_data(**kwargs)
		context['certificate'] = self._object
		context['sungalt'] = Certificate_sungalt.objects.filter(certificate=self._object)
		return context
class TZ_tze_huselt_ilgeeh(LoginRequired, FormView):
	perm_code_names = ['tze_tz_huselt_ilgeeh_view']
	template_name = 'tz_huselt/form_div_htmls/tze_tz_huselt_ilgeeh_div.html'
	form_class = Huselt_ilgeeh_Form
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')
	def dispatch(self, request, *args, **kwargs):
		self._huselt_id = self.kwargs['huselt_id']
		self.tz_huselt = get_object_or_404(TZ_Huselt, id = self._huselt_id)
		return super(TZ_tze_huselt_ilgeeh, self).dispatch(request, *args, **kwargs)
	def form_valid(self, form):
		if form.cleaned_data['check']:
			

			# burdeliiin medeelel burdel_history-d oroh yostoi
			burdel_history = self.tz_huselt.huselt_ilgeeh()

			medegdel = TZ_medegdel.objects.create(tz_huselt = self.tz_huselt, datetime = timezone.now(), message = 'Хүсэлтийг зохицуулах зөвлөл рүү илгээсэн.', created_by = self.user)

			group_hzm = Group.objects.get(name = 'Хууль зүйн мэргэжилтэн')
			notify.send(self.baiguullaga, recipient=group_hzm, verb=self.baiguullaga.org_name + ' ' + self.baiguullaga.org_type + u' тусгай зөвшөөрлийн хүсэлт илгээлээ', url_data = reverse_lazy('hzm huselt check'))

			messages.success(self.request, 'Хүсэлтийг зохицуулах зөвлөл рүү илгээлээ.')
			return super(TZ_tze_huselt_ilgeeh, self).form_valid(form)
		else:
			return reverse_lazy('tusgai zovshoorol huselt menu')
	def get_context_data(self, **kwargs):
		context = super(TZ_tze_huselt_ilgeeh, self).get_context_data(**kwargs)
		context['huselt_id'] = self._huselt_id
		return context
class TZ_tze_huselt_tsutslah(LoginRequired, FormView):
	perm_code_names = ['tze_tz_huselt_ilgeeh_view']
	template_name = 'tz_huselt/form_div_htmls/tze_tz_huselt_tsutslah_div.html'
	form_class = EmptyForm
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')
	def dispatch(self, request, *args, **kwargs):
		self._huselt_id = self.kwargs['huselt_id']
		return super(TZ_tze_huselt_tsutslah, self).dispatch(request, *args, **kwargs)
	def form_valid(self, form):
		tz_huselt = TZ_Huselt.objects.get(id = self._huselt_id)
		tz_huselt.change_yavts_to_tsutslagdsan()

		medegdel = TZ_medegdel.objects.create(tz_huselt = tz_huselt, datetime = timezone.now(), message = 'Хүсэлтийг компани цуцалсан.', created_by = self.user)

		messages.success(self.request, 'Хүсэлтийг цуцаллаа.')
		return super(TZ_tze_huselt_tsutslah, self).form_valid(form)
	def form_invalid(self, form):
		messages.error(self.request, 'Үйлдэл амжилтгүй боллоо.')
		return HttpResponseRedirect(self.get_success_url())
	def get_context_data(self, **kwargs):
		context = {}
		context['huselt_id'] = self._huselt_id
		return context

class TZ_huselt_new(Base_Ajax_FormView):
	perm_code_names = ['tze_tz_huselt_uusgeh_view']
	form_class = New_TZ_Huselt_Form
	template_name = 'tz_huselt/form_div_htmls/tze_tz_huselt_new_div.html'
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')
	view_url = reverse_lazy('tze_tz_huselt_new')

	def form_valid(self, form):
		burdel = form.save(commit=False)
		tze = get_object_or_404(TZE, id=self.baiguullaga.id)
		tz_huselt = TZ_Huselt(tze = tze)
		tz_huselt.created_by = self.user
		tz_huselt.change_yavts_to_material_burduulelt()

		burdel.tze = tze
		burdel.tz_huselt = tz_huselt
		burdel.save()
		huselt_angilal = form.cleaned_data['huselt_angilal']

		if huselt_angilal == u'1':
			tzs = form.cleaned_data['tz_choices_hodoo_oron_nutag']
			for t in tzs:
				burdel.tz.add(t)
		elif huselt_angilal == u'2':
			a1 = TZ.objects.get(tz='12.2.4')
			a2 = TZ.objects.get(tz='12.2.5')
			a3 = TZ.objects.get(tz='12.2.6')
			a4 = TZ.objects.get(tz='12.2.7')
			a5 = TZ.objects.get(tz='12.2.8')
			burdel.tz.add(a1, a2, a3, a4, a5)
			if form.cleaned_data['tz_choices_oron_suuts']:
				tzs = form.cleaned_data['tz_choices_oron_suuts']
				for t in tzs:
					burdel.tz.add(t)
		elif huselt_angilal == u'3':
			a1 = TZ.objects.get(tz='12.2.1')
			a2 = TZ.objects.get(tz='12.2.2')
			burdel.tz.add(a1, a2)
		elif huselt_angilal == u'4':
			print 'bohir us zoovorloh\n\n\n'
			a = TZ.objects.get(tz='12.2.14')
			burdel.tz.add(a)

		burdel.change_materialiud_list()
		medegdel = TZ_medegdel.objects.create(tz_huselt = tz_huselt, datetime = timezone.now(), message = 'Хүсэлт үүсэв.', created_by = self.user)
		messages.success(self.request, 'Хүсэлтийг үүсгэлээ. Шаардлагатай материалиудыг бүрдүүлэн зохицуулах зөвлөл рүү илгээнэ үү.')
		return super(TZ_huselt_new, self).form_valid(form)
	#def get_form_kwargs(self):
	#	kwargs = super(TZ_huselt_new, self).get_form_kwargs()
	#	tze = get_object_or_404(TZE, id=self.baiguullaga.id)
	#	kwargs['tze'] = tze
	#	return kwargs
class TZ_huselt_zaalt_edit(LoginRequired, UpdateView):
	perm_code_names = ['tze_tz_huselt_uusgeh_view']
	form_class = New_TZ_Huselt_Form
	template_name='tz_huselt/form_div_htmls/tze_tz_huselt_zaalt_edit_div.html'
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')
	model = Burdel
	pk_url_kwarg = 'burdel_id'
	context_object_name = 'burdel'
	def form_valid(self, form):
		
		if self.object.tz_huselt.is_yavts_material_burduulelt():
			if form.has_changed():

				#self.object.tz.clear()
				#self.object.tz.add(*form.cleaned_data['tz'])
				self.object = form.save()
				form.save_m2m()
				self.object.materialiud_list.all().delete()
				self.object.change_materialiud_list()

				medegdel = TZ_medegdel.objects.create(tz_huselt = self.object.tz_huselt, datetime = timezone.now(), message = 'Хүсэлтийн заалтуудад өөрчлөлт оруулсан.', created_by = self.user)
				medegdel.save()
				messages.success(self.request, 'Мэдээллийг амжилттай хадгаллаа.')
			else:
				messages.success(self.request, 'Заалтад өөрчлөлт орсонгүй.')
		else:
			messages.error(self.request, 'Үйлдэл амжилтгүй боллоо.')
		return HttpResponseRedirect(self.get_success_url())
	def get_form_kwargs(self):
		kwargs = super(TZ_huselt_zaalt_edit, self).get_form_kwargs()
		self.tze = get_object_or_404(TZE, id=self.baiguullaga.id)
		kwargs['tze'] = self.tze
		kwargs['huselt_tzs'] = self.object.tz.all()
		return kwargs

class Sent_materialView(LoginRequired, TemplateView):
	perm_code_names = ['tze_tusgai_zovshoorol_menu_view']
	def dispatch(self, request, *args, **kwargs):
		burdel_hist_id = self.kwargs['burdel_history_id']
		self.burdel_history = get_object_or_404(Burdel_history, id = burdel_hist_id)
		self._material_number = int(self.kwargs['material_number'])
		self.template_name = 'bichig_barimtuud/sent/sent_{:02d}.html'.format(self._material_number)
		return super(Sent_materialView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(Sent_materialView, self).get_context_data(**kwargs)
		context['burdel_history'] = self.burdel_history
		context['tsever_usnii_damjuulah'] = self.burdel_history.shugam_suljees.filter(shugam_torol = u'Цэвэр усны дамжуулах шугам')
		context['tsever_usnii_tugeeh'] = self.burdel_history.shugam_suljees.filter(shugam_torol = u'Цэвэр ус түгээх шугам')
		context['bohir_us_gargalgaa_shugam'] = self.burdel_history.shugam_suljees.filter(shugam_torol = u'Бохир усны гаргалгааны шугам')
		context['bohir_us_tsugluulah_shugam'] = self.burdel_history.shugam_suljees.filter(shugam_torol = u'Бохир усны цуглуулах шугам')
		context['bohir_us_tatan_zailuulah_shugam'] = self.burdel_history.shugam_suljees.filter(shugam_torol = u'Бохир ус татан зайлуулах шугам')
		material = get_object_or_404(TZ_material, material_number = self._material_number)
		context['tz_material_status_bind'] = self.burdel_history.materialiud_list.get(material=material)
		context['material_angilal'] = context['tz_material_status_bind'].material.material_angilal
		context['material_check_url'] = self.get_material_check_url()
		return context
	def get_material_check_url(self):
		return 0
class Show_materialView(LoginRequired, TemplateView):
	perm_code_names = ['tze_tusgai_zovshoorol_menu_view']
	def dispatch(self, request, *args, **kwargs):
		self._material_number = int(self.kwargs['material_number'])
		self._burdel_id = int(self.kwargs['burdel_id'])
		self._burdel = get_object_or_404(Burdel, id = self._burdel_id)
		self.template_name = 'bichig_barimtuud/show/show_{:02d}.html'.format(self._material_number)
		return super(Show_materialView, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(Show_materialView, self).get_context_data(**kwargs)
		context['ajiltan'] = Ajiltan.objects.filter(baiguullaga=context['baiguullaga'], status=True)
		context['h'] = self._burdel.tz_huselt
		context['ehudag'] = Hudag.objects.filter(tze = context['baiguullaga'],status=True)
		context['enasos'] = NasosStants.objects.filter(tze = context['baiguullaga'],status=True)
		context['elab'] = Lab.objects.filter(tze = context['baiguullaga'],status=True, torol=u'Цэвэр усны лаборатори')
		context['eusansan'] = UsanSan.objects.filter(tze = context['baiguullaga'],status=True)
		context['ewatercar'] = WaterCar.objects.filter(tze = context['baiguullaga'], status = True)
		context['ebohircar'] = BohirCar.objects.filter(tze = context['baiguullaga'], status = True)

		context['shugam_suljee'] = Sh_suljee.objects.filter(tze=context['baiguullaga'], status=True)
		context['tonog']=Equipment.objects.filter(tze = context['baiguullaga'],status=True)
		context['tseverleh_baig'] = Ts_baiguulamj.objects.filter(tze = context['baiguullaga'], status=True, torol='Бохир усны')
		context['tsevershuuleh_baig'] = Ts_baiguulamj.objects.filter(tze = context['baiguullaga'], status=True, torol='Цэвэр усны')
		context['usdamjuulah'] = UsDamjuulahBair.objects.filter(tze = context['baiguullaga'], status = True)

		context['baig'] = TZE.objects.filter(id=context['baiguullaga'].id)		
		context['zdt'] = ZDTodorhoilolt.objects.filter(tze = context['baiguullaga'], status = True)
		context['han'] = HangagchBaiguullaga.objects.filter(tze = context['baiguullaga'], status = True)
		context['tax'] = TaxTodorhoilolt.objects.filter(tze = context['baiguullaga'], status = True)
		context['audit'] = AuditDugnelt.objects.filter(tze = context['baiguullaga'], status = True)
		context['norm'] = NormStandart.objects.filter(tze = context['baiguullaga'], status = True)
		context['akt'] = Baig_huuli_durem.objects.filter(tze = context['baiguullaga'], status = True)
		context['us'] = UsZuvshuurul.objects.filter(tze = context['baiguullaga'], status = True)
		context['oron'] = OronTooniiSchema.objects.filter(tze = context['baiguullaga'], status = True)
		context['sanhuu'] = SanhuuTailan.objects.filter(tze = context['baiguullaga'], status = True)
		context['abb'] = ABB.objects.filter(tze = context['baiguullaga'], status = True)
		context['uildver'] = UildverTechnology.objects.filter(tze = context['baiguullaga'], status = True)
		context['hyanalt'] = MergejliinHyanalt.objects.filter(tze = context['baiguullaga'], status = True)
		context['ajliinbair'] = AjliinBair.objects.filter(tze = context['baiguullaga'], status = True)
		context['ustugeeh'] = UsTugeehBair.objects.filter(tze = context['baiguullaga'], status = True)
		context['us_shinjilgee'] = self._burdel.us_shinjilgee
		context['bohir_shinjilgee'] = self._burdel.bohir_shinjilgee
		#context['aimag'] = Aimag.objects.all()
		#context['sum'] = Sum.objects.all()
		#context['bag'] = Bag.objects.all()
		return context

class TZ_materialBase_chooseView(LoginRequired, FormView):
	perm_code_names = ['tze_tz_huselt_ilgeeh_view']
	template_name = 'tz_formuud/zasag_tod_choose.html'
	form_class = EmptyForm
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')

	def form_valid(self, form):
		self.success_url = reverse_lazy('tze_tz_huselt_delgerengui', kwargs={'huselt_id': self.kwargs['huselt_id']})
		return super(TZ_materialBase_chooseView, self).form_valid(form)
class TZ_material2_chooseView(TZ_materialBase_chooseView):
	template_name = 'tz_formuud/zasag_tod_choose.html'
	form_class = EmptyForm
	

	def get_context_data(self, **kwargs):
		context = super(TZ_material2_chooseView, self).get_context_data(**kwargs)
		context['huselt_id'] = self.kwargs['huselt_id']
		context['zasag_dargiin_tods_all'] = ZDTodorhoilolt.objects.filter(tze = self.baiguullaga, status=True)
		return context

	def form_valid(self, form):
		ids = self.request.POST.getlist('ids')
		huselt_id = self.kwargs['huselt_id']
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		baig_zdts = ZDTodorhoilolt.objects.filter(tze = self.baiguullaga, status = True)
		burdel.zasag_dargiin_todorhoilolts.clear()
		if ids:
			for i in ids:
				a = baig_zdts.get(id = i)
				burdel.zasag_dargiin_todorhoilolts.add(a)
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 2))
			mat_status_bind_instance.change_status_to_burdsen(timezone.now(), self.user)
		else:
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 2))
			mat_status_bind_instance.change_status_to_med_dutuu(timezone.now(), self.user)
		return super(TZ_material2_chooseView, self).form_valid(form)
class TZ_material3_chooseView(TZ_materialBase_chooseView):
	template_name = 'tz_formuud/hangagch_baig_choose.html'
	form_class = EmptyForm
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')


	def get_context_data(self, **kwargs):
		context = super(TZ_material3_chooseView, self).get_context_data(**kwargs)
		context['huselt_id'] = self.kwargs['huselt_id']
		context['hangagch_baiguullaga_all'] = HangagchBaiguullaga.objects.filter(tze = self.baiguullaga, status=True)
		return context

	def form_valid(self, form):
		ids = self.request.POST.getlist('ids')
		huselt_id = self.kwargs['huselt_id']
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		objs_baig_all = HangagchBaiguullaga.objects.filter(tze = self.baiguullaga, status = True)
		burdel.hangagch_baigs.clear()
		if ids:
			for i in ids:
				a = objs_baig_all.get(id = i)
				burdel.hangagch_baigs.add(a)
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 3))
			mat_status_bind_instance.change_status_to_burdsen(timezone.now(), self.user)
		else:
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 3))
			mat_status_bind_instance.change_status_to_med_dutuu(timezone.now(), self.user)
		return super(TZ_material3_chooseView, self).form_valid(form)
class TZ_material4_chooseView(TZ_materialBase_chooseView):
	template_name = 'tz_formuud/tax_tod_choose.html'
	form_class = EmptyForm
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')


	def get_context_data(self, **kwargs):
		context = super(TZ_material4_chooseView, self).get_context_data(**kwargs)
		context['huselt_id'] = self.kwargs['huselt_id']
		context['TaxTodorhoilolt_all'] = TaxTodorhoilolt.objects.filter(tze = self.baiguullaga, status=True)
		return context

	def form_valid(self, form):
		ids = self.request.POST.getlist('ids')
		huselt_id = self.kwargs['huselt_id']
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		objs_baig_all = TaxTodorhoilolt.objects.filter(tze = self.baiguullaga, status = True)
		burdel.tax_tods.clear()
		if ids:
			for i in ids:
				a = objs_baig_all.get(id = i)
				burdel.tax_tods.add(a)
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 4))
			mat_status_bind_instance.change_status_to_burdsen(timezone.now(), self.user)
		else:
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 4))
			mat_status_bind_instance.change_status_to_med_dutuu(timezone.now(), self.user)
		return super(TZ_material4_chooseView, self).form_valid(form)
class TZ_material5_chooseView(TZ_materialBase_chooseView):
	template_name = 'tz_formuud/sanhuu_tailan_choose.html'
	form_class = EmptyForm
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')


	def get_context_data(self, **kwargs):
		context = super(TZ_material5_chooseView, self).get_context_data(**kwargs)
		context['huselt_id'] = self.kwargs['huselt_id']
		context['SanhuuTailan_all'] = SanhuuTailan.objects.filter(tze = self.baiguullaga, status=True)
		return context

	def form_valid(self, form):
		ids = self.request.POST.getlist('ids')
		huselt_id = self.kwargs['huselt_id']
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		objs_baig_all = SanhuuTailan.objects.filter(tze = self.baiguullaga, status = True)
		burdel.sanhuu_tailans.clear()
		if ids:
			for i in ids:
				a = objs_baig_all.get(id = i)
				burdel.sanhuu_tailans.add(a)
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 5))
			mat_status_bind_instance.change_status_to_burdsen(timezone.now(), self.user)
		else:
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 5))
			mat_status_bind_instance.change_status_to_med_dutuu(timezone.now(), self.user)
		return super(TZ_material5_chooseView, self).form_valid(form)
class TZ_material6_chooseView(TZ_materialBase_chooseView):
	template_name = 'tz_formuud/audit_dugnelt_choose.html'
	form_class = EmptyForm
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')


	def get_context_data(self, **kwargs):
		context = super(TZ_material6_chooseView, self).get_context_data(**kwargs)
		context['huselt_id'] = self.kwargs['huselt_id']
		context['AuditDugnelt_all'] = AuditDugnelt.objects.filter(tze = self.baiguullaga, status=True)
		return context

	def form_valid(self, form):
		ids = self.request.POST.getlist('ids')
		huselt_id = self.kwargs['huselt_id']
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		objs_baig_all = AuditDugnelt.objects.filter(tze = self.baiguullaga, status = True)
		burdel.audit_dugnelts.clear()
		if ids:
			for i in ids:
				a = objs_baig_all.get(id = i)
				burdel.audit_dugnelts.add(a)
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 6))
			mat_status_bind_instance.change_status_to_burdsen(timezone.now(), self.user)
		else:
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 6))
			mat_status_bind_instance.change_status_to_med_dutuu(timezone.now(), self.user)
		return super(TZ_material6_chooseView, self).form_valid(form)
class TZ_material7_chooseView(TZ_materialBase_chooseView):
	template_name = 'tz_formuud/oron_too_schema_choose.html'
	form_class = EmptyForm
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')


	def get_context_data(self, **kwargs):
		context = super(TZ_material7_chooseView, self).get_context_data(**kwargs)
		context['huselt_id'] = self.kwargs['huselt_id']
		context['OronTooniiSchema_all'] = OronTooniiSchema.objects.filter(tze = self.baiguullaga, status=True)
		return context

	def form_valid(self, form):
		ids = self.request.POST.getlist('ids')
		huselt_id = self.kwargs['huselt_id']
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		objs_baig_all = OronTooniiSchema.objects.filter(tze = self.baiguullaga, status = True)
		burdel.oron_toonii_schemas.clear()
		if ids:
			for i in ids:
				a = objs_baig_all.get(id = i)
				burdel.oron_toonii_schemas.add(a)
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 7))
			mat_status_bind_instance.change_status_to_burdsen(timezone.now(), self.user)
		else:
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 7))
			mat_status_bind_instance.change_status_to_med_dutuu(timezone.now(), self.user)
		return super(TZ_material7_chooseView, self).form_valid(form)
class TZ_material8_chooseView(TZ_materialBase_chooseView):
	template_name = 'tz_formuud/norm_standart_choose.html'
	form_class = EmptyForm
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')


	def get_context_data(self, **kwargs):
		context = super(TZ_material8_chooseView, self).get_context_data(**kwargs)
		context['huselt_id'] = self.kwargs['huselt_id']
		context['NormStandart_all'] = NormStandart.objects.filter(tze = self.baiguullaga, status=True)
		return context

	def form_valid(self, form):
		ids = self.request.POST.getlist('ids')
		huselt_id = self.kwargs['huselt_id']
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		objs_baig_all = NormStandart.objects.filter(tze = self.baiguullaga, status = True)
		burdel.norm_standarts.clear()
		if ids:
			for i in ids:
				a = objs_baig_all.get(id = i)
				burdel.norm_standarts.add(a)
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 8))
			mat_status_bind_instance.change_status_to_burdsen(timezone.now(), self.user)
		else:
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 8))
			mat_status_bind_instance.change_status_to_med_dutuu(timezone.now(), self.user)
		return super(TZ_material8_chooseView, self).form_valid(form)
class TZ_material9_chooseView(TZ_materialBase_chooseView):
	template_name = 'tz_formuud/ulsiin_akt_choose.html'
	form_class = EmptyForm
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')


	def get_context_data(self, **kwargs):
		context = super(TZ_material9_chooseView, self).get_context_data(**kwargs)
		context['huselt_id'] = self.kwargs['huselt_id']
		context['Ulsiin_akt_all'] = UlsiinAkt.objects.filter(tze = self.baiguullaga, status=True)
		return context

	def form_valid(self, form):
		ids = self.request.POST.getlist('ids')
		huselt_id = self.kwargs['huselt_id']
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		objs_baig_all = UlsiinAkt.objects.filter(tze = self.baiguullaga, status = True)
		burdel.ulsiin_komis_akts.clear()
		if ids:
			for i in ids:
				a = objs_baig_all.get(id = i)
				burdel.ulsiin_komis_akts.add(a)
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 9))
			mat_status_bind_instance.change_status_to_burdsen(timezone.now(), self.user)
		else:
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 9))
			mat_status_bind_instance.change_status_to_med_dutuu(timezone.now(), self.user)
		return super(TZ_material9_chooseView, self).form_valid(form)
class TZ_material10_chooseView(TZ_materialBase_chooseView):
	template_name = 'tz_formuud/us_ashiglah_zovshoorol_choose.html'
	form_class = EmptyForm
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')


	def get_context_data(self, **kwargs):
		context = super(TZ_material10_chooseView, self).get_context_data(**kwargs)
		context['huselt_id'] = self.kwargs['huselt_id']
		context['UsZuvshuurul_all'] = UsZuvshuurul.objects.filter(tze = self.baiguullaga, status=True)
		return context

	def form_valid(self, form):
		ids = self.request.POST.getlist('ids')
		huselt_id = self.kwargs['huselt_id']
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		objs_baig_all = UsZuvshuurul.objects.filter(tze = self.baiguullaga, status = True)
		burdel.us_ashiglah_zovshoorols.clear()
		if ids:
			for i in ids:
				a = objs_baig_all.get(id = i)
				burdel.us_ashiglah_zovshoorols.add(a)
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 10))
			mat_status_bind_instance.change_status_to_burdsen(timezone.now(), self.user)
		else:
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 10))
			mat_status_bind_instance.change_status_to_med_dutuu(timezone.now(), self.user)
		return super(TZ_material10_chooseView, self).form_valid(form)
class TZ_material11_chooseView(TZ_materialBase_chooseView):
	template_name = 'tz_formuud/uildver_tech_schema_choose.html'
	form_class = EmptyForm
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')


	def get_context_data(self, **kwargs):
		context = super(TZ_material11_chooseView, self).get_context_data(**kwargs)
		context['huselt_id'] = self.kwargs['huselt_id']
		context['uildver_tech_all'] = UildverTechnology.objects.filter(tze = self.baiguullaga, status=True)
		return context

	def form_valid(self, form):
		ids = self.request.POST.getlist('ids')
		huselt_id = self.kwargs['huselt_id']
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		objs_baig_all = UildverTechnology.objects.filter(tze = self.baiguullaga, status = True)
		burdel.uildver_tech_schemas.clear()
		if ids:
			for i in ids:
				a = objs_baig_all.get(id = i)
				burdel.uildver_tech_schemas.add(a)
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 11))
			mat_status_bind_instance.change_status_to_burdsen(timezone.now(), self.user)
		else:
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 11))
			mat_status_bind_instance.change_status_to_med_dutuu(timezone.now(), self.user)
		return super(TZ_material11_chooseView, self).form_valid(form)
class TZ_material12_chooseView(TZ_materialBase_chooseView):
	template_name = 'tz_formuud/mheg_dugnelt_choose.html'
	form_class = EmptyForm
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')


	def get_context_data(self, **kwargs):
		context = super(TZ_material12_chooseView, self).get_context_data(**kwargs)
		context['huselt_id'] = self.kwargs['huselt_id']
		context['mheg_dugnelt_all'] = MergejliinHyanalt.objects.filter(tze = self.baiguullaga, status=True)
		return context

	def form_valid(self, form):
		ids = self.request.POST.getlist('ids')
		huselt_id = self.kwargs['huselt_id']
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		objs_baig_all = MergejliinHyanalt.objects.filter(tze = self.baiguullaga, status = True)
		burdel.mheg_dugnelts.clear()
		if ids:
			for i in ids:
				a = objs_baig_all.get(id = i)
				burdel.mheg_dugnelts.add(a)
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 12))
			mat_status_bind_instance.change_status_to_burdsen(timezone.now(), self.user)
		else:
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 12))
			mat_status_bind_instance.change_status_to_med_dutuu(timezone.now(), self.user)
		return super(TZ_material12_chooseView, self).form_valid(form)
class TZ_material13_chooseView(TZ_materialBase_chooseView):
	template_name = 'tz_formuud/ajliin_bair_dugnelt_choose.html'
	form_class = EmptyForm
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')


	def get_context_data(self, **kwargs):
		context = super(TZ_material13_chooseView, self).get_context_data(**kwargs)
		context['huselt_id'] = self.kwargs['huselt_id']
		context['ajliin_bair_dugnelt_all'] = AjliinBair.objects.filter(tze = self.baiguullaga, status=True)
		return context

	def form_valid(self, form):
		ids = self.request.POST.getlist('ids')
		huselt_id = self.kwargs['huselt_id']
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		objs_baig_all = AjliinBair.objects.filter(tze = self.baiguullaga, status = True)
		burdel.ajliin_bair_dugnelts.clear()
		if ids:
			for i in ids:
				a = objs_baig_all.get(id = i)
				burdel.ajliin_bair_dugnelts.add(a)
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 13))
			mat_status_bind_instance.change_status_to_burdsen(timezone.now(), self.user)
		else:
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 13))
			mat_status_bind_instance.change_status_to_med_dutuu(timezone.now(), self.user)
		return super(TZ_material13_chooseView, self).form_valid(form)
class TZ_material14_chooseView(TZ_materialBase_chooseView):
	template_name = 'tz_formuud/hunii_noots_choose.html'
	form_class = EmptyForm
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')


	def get_context_data(self, **kwargs):
		context = super(TZ_material14_chooseView, self).get_context_data(**kwargs)
		context['huselt_id'] = self.kwargs['huselt_id']
		context['Ajiltan_all'] = Ajiltan.objects.filter(baiguullaga = self.baiguullaga, status=True)
		return context

	def form_valid(self, form):
		ids = self.request.POST.getlist('ids')
		huselt_id = self.kwargs['huselt_id']
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		objs_baig_all = Ajiltan.objects.filter(baiguullaga = self.baiguullaga, status = True)
		burdel.ajiltans.clear()
		if ids:
			for i in ids:
				a = objs_baig_all.get(id = i)
				burdel.ajiltans.add(a)
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 14))
			mat_status_bind_instance.change_status_to_burdsen(timezone.now(), self.user)
		else:
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 14))
			mat_status_bind_instance.change_status_to_med_dutuu(timezone.now(), self.user)
		return super(TZ_material14_chooseView, self).form_valid(form)
class TZ_material15_chooseView(TZ_materialBase_chooseView):
	template_name = 'tz_formuud/mashin_tonog_tohooromj_choose.html'
	form_class = EmptyForm
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')


	def get_context_data(self, **kwargs):
		context = super(TZ_material15_chooseView, self).get_context_data(**kwargs)
		context['huselt_id'] = self.kwargs['huselt_id']
		context['Equipment_all'] = Equipment.objects.filter(tze = self.baiguullaga, status=True)
		return context

	def form_valid(self, form):
		ids = self.request.POST.getlist('ids')
		huselt_id = self.kwargs['huselt_id']
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		objs_baig_all = Equipment.objects.filter(tze = self.baiguullaga, status = True)
		burdel.mashin_tonog_tohooromjs.clear()
		if ids:
			for i in ids:
				a = objs_baig_all.get(id = i)
				burdel.mashin_tonog_tohooromjs.add(a)
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 15))
			mat_status_bind_instance.change_status_to_burdsen(timezone.now(), self.user)
		else:
			mat_status_bind_instance = burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = 15))
			mat_status_bind_instance.change_status_to_med_dutuu(timezone.now(), self.user)
		return super(TZ_material15_chooseView, self).form_valid(form)
class TZ_material16_chooseView(TZ_materialBase_chooseView):
	template_name = 'tz_formuud/material_burdsen_check_choose.html'
	form_class = Material_Burdsen_Check_Form
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')


	def get_context_data(self, **kwargs):
		context = super(TZ_material16_chooseView, self).get_context_data(**kwargs)
		context['huselt_id'] = self.kwargs['huselt_id']
		context['material_number'] = self.kwargs['material_number']
		return context

	def form_valid(self, form):
		huselt_id = self.kwargs['huselt_id']
		material_number = self.kwargs['material_number']
		huselt = TZ_Huselt.objects.get(id = huselt_id)

		if form.cleaned_data['check']:
			mat_status_bind_instance = huselt.burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = material_number))
			mat_status_bind_instance.change_status_to_burdsen(timezone.now(), self.user)
		else:
			mat_status_bind_instance = huselt.burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = material_number))
			mat_status_bind_instance.change_status_to_med_dutuu(timezone.now(), self.user)
		return super(TZ_material16_chooseView, self).form_valid(form)



class TZ_Uildver_tech_schema_FormView(Uildver_tech_schema_FormView):
	success_url = reverse_lazy('baiguullaga_menu')
	view_url = reverse_lazy('uildver_tech_schema_insert_tz')
class TZ_MHEG_dugnelt_FormView(LoginRequired, FormView):
	perm_code_names = ['tze_tz_huselt_ilgeeh_view']
	template_name = 'tz_huselt/form_div_htmls/mheg_dugnelt_form.html'
	success_url = reverse_lazy('baiguullaga_menu')
	form_class = MergejliinHyanaltForm
	view_url = reverse_lazy('MHEG_dugnelt_insert_tz')
	def form_valid(self, form):
		tze = get_object_or_404(TZE, id=self.baiguullaga.id)
		dakt = MergejliinHyanalt(tze=tze)
		dakt.dugnelt = form.cleaned_data['dugnelt']
		dakt.begin_time=timezone.now()
		dakt.created_by=self.user
		dakt.status = True
		dakt.save()
		#messages.success(self.request, 'Амжилттай хадгаллаа.')
		return super(TZ_MHEG_dugnelt_FormView, self).form_valid(form)
	def get_context_data(self, **kwargs):
		context = super(TZ_MHEG_dugnelt_FormView, self).get_context_data(**kwargs)
		context['view_url'] = self.view_url
		return context
class TZ_Ajliin_bair_dugnelt_FormView(Ajliin_bair_dugnelt_FormView):
	success_url = reverse_lazy('baiguullaga_menu')
	view_url = reverse_lazy('ajliin_bair_dugnelt_insert_tz') # form post hiiih url, viewiin url
class TZ_Zasag_tod_FormView(Zasag_tod_FormView):
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')
	view_url = reverse_lazy('zasag_tod_insert_tz')
class TZ_Hangagch_baig_FormView(Hangagch_baig_FormView):
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')
	view_url = reverse_lazy('han_baig_insert_tz')
class TZ_Tax_tod_FormView(Tax_tod_FormView):
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')
	view_url = reverse_lazy('tax_tod_insert_tz')
class TZ_Audit_dugnelt_FormView(Audit_dugnelt_FormView):
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')
	view_url = reverse_lazy('audit_dugnelt_insert_tz')
class TZ_Norm_standart_FormView(Norm_standart_FormView):
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')
	view_url = reverse_lazy('norm_standart_insert_tz')
class TZ_Us_zovshoorol_FormView(Us_zovshoorol_FormView):
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')
	view_url = reverse_lazy('us_zovshoorol_insert_tz')
class TZ_Sanhuu_tailan_FormView(Sanhuu_tailan_FormView):
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')
	view_url = reverse_lazy('sanhuu_tailan_insert_tz')
class TZ_Hariutssan_barilguud_FormView(Hariutssan_barilguud_FormView):
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')
	view_url = reverse_lazy('hariutssan_barilguud_insert_tz')
class TZ_Oron_too_schema_FormView(Oron_too_schema_FormView):
	success_url = reverse_lazy('tusgai zovshoorol huselt menu')
	view_url = reverse_lazy('oron_too_schema_insert_tz')

class TZ_hudag_formView(HudagFormView):
	template_name = 'tz_huselt/form_div_htmls/tz_huselt_hudag_form_div.html'
	view_url = reverse_lazy('tz_hudag_insert')
	def form_valid(self, form):
		self.success_url = reverse_lazy('tze_tz_huselt_delgerengui', kwargs={'huselt_id': self.kwargs['huselt_id']})
		return super(TZ_hudag_formView, self).form_valid(form)
class TZ_usansan_formView(UsanSanFormView):
	template_name = 'tz_huselt/form_div_htmls/tz_huselt_usansan_form_div.html'
	view_url = reverse_lazy('tz_hudag_insert')
	def form_valid(self, form):
		self.success_url = reverse_lazy('tze_tz_huselt_delgerengui', kwargs={'huselt_id': self.kwargs['huselt_id']})
		return super(TZ_usansan_formView, self).form_valid(form)
class TZ_nasosStants_formView(NasosStantsFormView):
	template_name = 'tz_huselt/form_div_htmls/tz_huselt_nasos_stants_form_div.html'
	def dispatch(self, request, *args, **kwargs):
		self.view_url = reverse_lazy('tz_nasosStants_insert', kwargs={'huselt_id': kwargs['huselt_id']})
		return super(TZ_nasosStants_formView, self).dispatch(request, *args, **kwargs)
	def form_valid(self, form, formset):
		self.success_url = reverse_lazy('tze_tz_huselt_delgerengui', kwargs={'huselt_id': self.kwargs['huselt_id']})
		return super(TZ_nasosStants_formView, self).form_valid(form, formset)
class TZ_lab_formView(LabFormView):
	template_name = 'tz_huselt/form_div_htmls/tz_huselt_lab_form_div.html'
	view_url = reverse_lazy('tz_hudag_insert')
	def form_valid(self, form, formset, formset1):
		self.success_url = reverse_lazy('tze_tz_huselt_delgerengui', kwargs={'huselt_id': self.kwargs['huselt_id']})
		return super(TZ_lab_formView, self).form_valid(form, formset, formset1)
class TZ_abb_formView(Hariutssan_barilguud_FormView):
	template_name = 'tz_huselt/form_div_htmls/tz_huselt_hariutssan_barilguud_form.html'
	def dispatch(self, request, *args, **kwargs):
		self.view_url = reverse_lazy('tz_abb_insert', kwargs={'huselt_id': kwargs['huselt_id']})
		return super(TZ_abb_formView, self).dispatch(request, *args, **kwargs)
	def form_valid(self, form):
		self.success_url = reverse_lazy('tze_tz_huselt_delgerengui', kwargs={'huselt_id': self.kwargs['huselt_id']})
		return super(TZ_abb_formView, self).form_valid(form)
class TZ_us_damjuulah_formView(UsDamjuulahBairFormView):
	template_name = 'tz_huselt/form_div_htmls/tz_huselt_us_damjuulah_form_div.html'
	view_url = reverse_lazy('tz_hudag_insert')
	def form_valid(self, form, formset):
		self.success_url = reverse_lazy('tze_tz_huselt_delgerengui', kwargs={'huselt_id': self.kwargs['huselt_id']})
		return super(TZ_us_damjuulah_formView, self).form_valid(form, formset)
class TZ_sh_suljee_formView(ShugamSuljeeFormView):
	template_name = 'tz_huselt/form_div_htmls/tz_huselt_shugam_form_div.html'
	view_url = reverse_lazy('tz_hudag_insert')
	def form_valid(self, form, formset):
		self.success_url = reverse_lazy('tze_tz_huselt_delgerengui', kwargs={'huselt_id': self.kwargs['huselt_id']})
		return super(TZ_sh_suljee_formView, self).form_valid(form, formset)
class TZ_ts_baig_formView(TseverlehBaiguulamjFormView):
	template_name = 'tz_huselt/form_div_htmls/tz_huselt_ts_baiguulamj_form_div.html'
	view_url = reverse_lazy('tz_hudag_insert')
	def form_valid(self, form, formset):
		self.success_url = reverse_lazy('tze_tz_huselt_delgerengui', kwargs={'huselt_id': self.kwargs['huselt_id']})
		return super(TZ_ts_baig_formView, self).form_valid(form, formset)
class TZ_us_tugeeh_formView(UsTugeehBairFormView):
	template_name = 'tz_huselt/form_div_htmls/tz_huselt_us_tugeeh_form_div.html'
	view_url = reverse_lazy('tz_hudag_insert')
	def form_valid(self, form):
		self.success_url = reverse_lazy('tze_tz_huselt_delgerengui', kwargs={'huselt_id': self.kwargs['huselt_id']})
		return super(TZ_us_tugeeh_formView, self).form_valid(form)
class TZ_water_car_formView(WaterCarFormView):
	template_name = 'tz_huselt/form_div_htmls/tz_huselt_car_form_div.html'
	def dispatch(self, request, *args, **kwargs):
		self.view_url = reverse_lazy('tz_abb_insert', kwargs={'huselt_id': kwargs['huselt_id']})
		return super(TZ_water_car_formView, self).dispatch(request, *args, **kwargs)
	def form_valid(self, form):
		self.success_url = reverse_lazy('tze_tz_huselt_delgerengui', kwargs={'huselt_id': self.kwargs['huselt_id']})
		return super(TZ_water_car_formView, self).form_valid(form)
class TZ_bohir_car_formView(BohirCarFormView):
	template_name = 'tz_huselt/form_div_htmls/tz_huselt_bohircar_form_div.html'
	view_url = reverse_lazy('tz_hudag_insert')
	def form_valid(self, form):
		self.success_url = reverse_lazy('tze_tz_huselt_delgerengui', kwargs={'huselt_id': self.kwargs['huselt_id']})
		return super(TZ_bohir_car_formView, self).form_valid(form)


class TZ_standard_formView(Norm_standart_FormView):
	template_name = 'tz_huselt/form_div_htmls/tz_huselt_bohircar_form_div.html'
	def dispatch(self, request, *args, **kwargs):
		self.view_url = reverse_lazy('tz_norm_standart_insert', kwargs={'huselt_id': kwargs['huselt_id']})
		return super(TZ_standard_formView, self).dispatch(request, *args, **kwargs)
	def form_valid(self, form):
		self.success_url = reverse_lazy('tze_tz_huselt_delgerengui', kwargs={'huselt_id': self.kwargs['huselt_id']})
		return super(TZ_standard_formView, self).form_valid(form)
class TZ_huuli_durem_formView(Huuli_durem_FormView):
	template_name = 'tz_huselt/form_div_htmls/tz_huselt_huuli_durem_juram_norm.html'
	def dispatch(self, request, *args, **kwargs):
		self.view_url = reverse_lazy('tz_huuli_durem_insert', kwargs={'huselt_id': kwargs['huselt_id']})
		return super(TZ_huuli_durem_formView, self).dispatch(request, *args, **kwargs)
	def form_valid(self, form):
		self.success_url = reverse_lazy('tze_tz_huselt_delgerengui', kwargs={'huselt_id': self.kwargs['huselt_id']})
		return super(TZ_huuli_durem_formView, self).form_valid(form)
class TZ_oron_too_schema_formView(Oron_too_schema_FormView):
	template_name = 'tz_huselt/form_div_htmls/tz_huselt_oron_too_schema_form.html'
	def dispatch(self, request, *args, **kwargs):
		self.view_url = reverse_lazy('tz_oron_too_insert', kwargs={'huselt_id': kwargs['huselt_id']})
		return super(TZ_oron_too_schema_formView, self).dispatch(request, *args, **kwargs)
	def form_valid(self, form):
		self.success_url = reverse_lazy('tze_tz_huselt_delgerengui', kwargs={'huselt_id': self.kwargs['huselt_id']})
		return super(TZ_oron_too_schema_formView, self).form_valid(form)
class TZ_equipment_formView(EquipmentFormView):
	template_name = 'tz_huselt/form_div_htmls/tz_huselt_tonog_form_div.html'
	def dispatch(self, request, *args, **kwargs):
		self.view_url = reverse_lazy('tz_equipment_insert', kwargs={'huselt_id': kwargs['huselt_id']})
		return super(TZ_equipment_formView, self).dispatch(request, *args, **kwargs)
	def form_valid(self, form):
		self.success_url = reverse_lazy('tze_tz_huselt_delgerengui', kwargs={'huselt_id': self.kwargs['huselt_id']})
		return super(TZ_equipment_formView, self).form_valid(form)
class TZ_material_water_shijilgee(Base_Ajax_FormView):
	perm_code_names = ['tze_tz_huselt_ilgeeh_view']
	form_class = TZ_huselt_water_analysisForm
	template_name = 'tz_huselt/form_div_htmls/tz_huselt_water_analysis_form.html'
	mat_number = 23
	field_name = 'us_shinjilgee'
	def dispatch(self, request, *args, **kwargs):
		self.burdel_id = int(self.kwargs['burdel_id'])
		self.burdel = get_object_or_404(Burdel, id=self.burdel_id)
		return super(TZ_material_water_shijilgee, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(TZ_material_water_shijilgee, self).get_context_data(**kwargs)
		context['view_url'] = reverse_lazy('tz_huselt_us_shijilgee_insert', kwargs ={'burdel_id': self.burdel.id})
		return context
	def form_valid(self, form):
		self.success_url = reverse_lazy('tze_tz_huselt_delgerengui', kwargs={'huselt_id': self.burdel.tz_huselt.id})

		obj = form.save(commit=False)
		obj.tze = get_object_or_404(TZE, id=self.baiguullaga.id)
		obj.status = True
		obj.save()

		setattr(self.burdel, self.field_name, obj)
		self.burdel.save()

		mat_status_bind_instance = self.burdel.materialiud_list.get(material = TZ_material.objects.get(material_number = self.mat_number))
		mat_status_bind_instance.change_status_to_burdsen(timezone.now(), self.user)
		return super(TZ_material_water_shijilgee, self).form_valid(form)
class TZ_water_shinjilgee_update(LoginRequired, UpdateView):
	perm_code_names = ['tze_tz_huselt_ilgeeh_view']
	template_name = 'tz_huselt/form_div_htmls/tz_huselt_water_analysis_form.html'
	model = TZ_huselt_water_analysis
	form_class = TZ_huselt_water_analysisForm
	def dispatch(self, request, *args, **kwargs):
		self.burdel_id = int(self.kwargs['burdel_id'])
		self.burdel = get_object_or_404(Burdel, id=self.burdel_id)
		self.success_url = reverse_lazy('tze_tz_huselt_delgerengui', kwargs={'huselt_id': self.burdel.tz_huselt.id})
		return super(TZ_water_shinjilgee_update, self).dispatch(request, *args, **kwargs)
	def get_object(self, queryset=None):
		return self.burdel.us_shinjilgee

class TZ_material_bohir_shinjilgee(TZ_material_water_shijilgee):
	form_class = TZ_huselt_bohir_analysisForm
	template_name = 'tz_huselt/form_div_htmls/tz_huselt_bohir_analysis_form.html'
	mat_number = 24
	field_name = 'bohir_shinjilgee'
	def get_context_data(self, **kwargs):
		context = super(TZ_material_bohir_shinjilgee, self).get_context_data(**kwargs)
		context['view_url'] = reverse_lazy('tz_huselt_bohir_shijilgee_insert', kwargs ={'burdel_id': self.burdel.id})
		return context
class TZ_bohir_shinjilgee_update(LoginRequired, UpdateView):
	perm_code_names = ['tze_tz_huselt_ilgeeh_view']
	template_name = 'tz_huselt/form_div_htmls/tz_huselt_bohir_analysis_form.html'
	model = TZ_huselt_bohir_analysis
	form_class = TZ_huselt_bohir_analysisForm
	def dispatch(self, request, *args, **kwargs):
		self.burdel_id = int(self.kwargs['burdel_id'])
		self.burdel = get_object_or_404(Burdel, id=self.burdel_id)
		self.success_url = reverse_lazy('tze_tz_huselt_delgerengui', kwargs={'huselt_id': self.burdel.tz_huselt.id})
		return super(TZ_bohir_shinjilgee_update, self).dispatch(request, *args, **kwargs)
	def get_object(self, queryset=None):
		return self.burdel.bohir_shinjilgee
class TZ_bohir_shinjilgee_delgerengui(LoginRequired, TemplateView):
	perm_code_names = ['tze_tz_huselt_ilgeeh_view']
	template_name = 'tz_huselt/delgerengui_htmls/tz_huselt_bohir_analysis_delgerengui.html'
	def get_context_data(self, **kwargs):
		context=super(TZ_bohir_shinjilgee_delgerengui, self).get_context_data(**kwargs)
		obj_id = kwargs['id']
		obj = get_object_or_404(TZ_huselt_bohir_analysis, id=obj_id)
		context['obj'] = obj
		return context



''' uil ajillagaanii tailan '''




''' sanhuugiin medee '''






''' sanhuugiin tailan '''





''' GSHUT '''
class GSHU_tailan(LoginRequired, TemplateView):
	perm_code_names = ['tze_gshu_tailan_menu_view']
	template_name = 'gshu_tailan/gshu_tailan.html'
	def get_context_data(self, **kwargs):
		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		context = super(GSHU_tailan,self).get_context_data(**kwargs)
		context['gshu_tailans'] = GShU.objects.filter(tze = tze)
		return context


class GSHU_insertBase(LoginRequired, FormView):
	perm_code_names = ['tze_gshu_tailan_menu_view']
	template_name = 'gshu_tailan/form_div_htmls/gshu_form.html'
	header = "Гүйцэтгэлийн шалгуур үзүүлэлтийн тайлан"
	success_url = reverse_lazy('gshu_tailan')
	def dispatch(self, request, *args, **kwargs):
		gshu_id = kwargs['gshu_id']
		self.gshu = get_object_or_404(GShU, id=gshu_id)
		self.view_url = reverse_lazy('gshu_insert', kwargs={'gshu_id': gshu_id})
		return super(GSHU_insertBase, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(GSHU_insertBase, self).get_context_data(**kwargs)
		context['header'] = self.header
		return context
	def get_form_class(self):
		self.tze = get_object_or_404(TZE, id=self.baiguullaga.id)
		fields = self.tze.get_gshu_fields()
		form_class = get_gshu_form_class(fields)
		return form_class
	def get_form_kwargs(self):
		kwargs = super(GSHU_insertBase, self).get_form_kwargs()
		if hasattr(self, 'gshu'):
			kwargs.update({'instance': self.gshu})
		return kwargs
	def form_valid(self, form):
		if self.gshu.can_edit:
			obj= form.save(commit=False)
			obj.status = True
			obj.created_by = self.user
			obj.change_tolov_to_ilgeesen()
		return super(GSHU_insertBase, self).form_valid(form)




class GSHU_tailan_materials_view(LoginRequired, TemplateView):
	perm_code_names = ['tze_gshu_tailan_menu_view']
	template_name = 'gshu_tailan/gshu_tailan_material.html'
	def get_context_data(self, **kwargs):
		gshu_id = kwargs['gshu_id']
		gshu = get_object_or_404(GShU, id=gshu_id)
		context = super(GSHU_tailan_materials_view, self).get_context_data(**kwargs)
		context['gshu'] = gshu
		if gshu.uzuulelt_1:
			if gshu.Pasdws != None and gshu.Nmean != None:
				context['result1'] = gshu.Pasdws * 100/gshu.Nmean
			else:
				context['result1'] = 'Мэдээлэл байхгүй'
		if gshu.uzuulelt_2:
			if gshu.Q1 != None and gshu.Qr != None:
				context['result2'] = gshu.Q1*100/gshu.Qr
			else:
				context['result2'] = 'Мэдээлэл байхгүй'
		if gshu.uzuulelt_3:
			if gshu.Q2 != None and gshu.Ec != None:
				context['result3'] = gshu.Ec/gshu.Q2
			else:
				context['result3'] = 'Мэдээлэл байхгүй'
		if gshu.uzuulelt_4:
			if gshu.Nb != None and gshu.Na != None:
				context['result4'] = gshu.Nb * 100/gshu.Na
			else:
				context['result4'] = 'Мэдээлэл байхгүй'
		if gshu.uzuulelt_5:
			if gshu.Qn != None and gshu.Qs1 != None:
				context['result5'] = (gshu.Qn-gshu.Qs1)*100/gshu.Qn
			else:
				context['result5'] = 'Мэдээлэл байхгүй'
		if gshu.uzuulelt_6:
			if gshu.Qm != None and gshu.Qs2 != None:
				context['result6'] = gshu.Qm * 100/gshu.Qs2
			else:
				context['result6'] = 'Мэдээлэл байхгүй'
		if gshu.uzuulelt_7:
			if gshu.Nn != None and gshu.Ln != None:
				context['result7'] = gshu.Nn/gshu.Ln
			else:
				context['result7'] = 'Мэдээлэл байхгүй'
		if gshu.uzuulelt_8:
			if gshu.BOD5input != None and gshu.BOD5output != None:
				context['result8a'] = (gshu.BOD5input-gshu.BOD5output)*100/gshu.BOD5input
			else:
				context['result8a'] = 'Мэдээлэл байхгүй'
			if gshu.COD5input != None and gshu.COD5output != None:
				context['result8b'] = (gshu.COD5input-gshu.COD5output)*100/gshu.COD5input
			else:
				context['result8b'] = 'Мэдээлэл байхгүй'
			if gshu.SSinput != None and gshu.SSoutput != None:
				context['result8c'] = (gshu.SSinput-gshu.SSoutput)*100/gshu.SSinput
			else:
				context['result8c'] = 'Мэдээлэл байхгүй'
		if gshu.uzuulelt_9:
			if gshu.Ne1 != None and gshu.N1 != None:
				context['result9'] = gshu.Ne1 * 100/gshu.N1
			else:
				context['result9'] = 'Мэдээлэл байхгүй'
		if gshu.uzuulelt_10:
			if gshu.Ne1 != None and  gshu.C != None:
				context['result10'] = gshu.Ne1*1000/gshu.C
			else:
				context['result10'] = 'Мэдээлэл байхгүй'
		if gshu.uzuulelt_11:
			if gshu.BOsh != None and gshu.BOshb != None:
				context['result11'] = gshu.BOsh/gshu.BOshb
			else:
				context['result11'] = 'Мэдээлэл байхгүй'
		if gshu.uzuulelt_12:
			if gshu.O != None and gshu.Z != None:
				context['result12'] = gshu.Z/gshu.O
			else:
				context['result12'] = 'Мэдээлэл байхгүй'
		if gshu.uzuulelt_13:
			if gshu.TsQs != None and gshu.ZTsU != None:
				context['result13a'] = gshu.ZTsU/gshu.TsQs
			else:
				context['result13a'] = 'Мэдээлэл байхгүй'
			if gshu.BQs != None and gshu.ZBU != None:
				context['result13b'] = gshu.ZBU/gshu.BQs
			else:
				context['result13b'] = 'Мэдээлэл байхгүй'
		if gshu.uzuulelt_14:
			if gshu.M != None and gshu.B != None:
				context['result14'] = gshu.M*100/gshu.B
			else:
				context['result14'] = 'Мэдээлэл байхгүй'
		return context

class GSHU_uilchilgeenii_hurteemj_delgerengui(LoginRequired, TemplateView):
	perm_code_names = ['tze_gshu_tailan_menu_view']
	template_name = 'gshu_tailan/delgerengui_htmls/uilchilgee_hurteemj_delgerengui.html'
	def get_context_data(self, **kwargs):
		context = super(GSHU_uilchilgeenii_hurteemj_delgerengui, self).get_context_data(**kwargs)
		gshu_id = kwargs['gshu_id']
		gshu = get_object_or_404(GShU, id = gshu_id)
		context['obj'] = gshu.u_hurteemj
		if gshu.u_hurteemj.Pasdws and gshu.u_hurteemj.Nmean:
			context['result'] = gshu.u_hurteemj.Pasdws*100/gshu.u_hurteemj.Nmean
		else:
			context['result'] = "Өгөгдөл дутуу учир тооцоолох боломжгүй"
		return context
class GSHU_tsever_us_olborlolt_delgerengui(LoginRequired, TemplateView):
	perm_code_names = ['tze_gshu_tailan_menu_view']
	template_name = 'gshu_tailan/delgerengui_htmls/tsever_us_olborlolt_delgerengui.html'
	def get_context_data(self, **kwargs):
		context = super(GSHU_tsever_us_olborlolt_delgerengui, self).get_context_data(**kwargs)
		gshu_id = kwargs['gshu_id']
		gshu = get_object_or_404(GShU, id = gshu_id)
		context['obj'] = gshu.tsever_us_olborlolt
		return context
class GSHU_tsever_us_delgerengui(LoginRequired, TemplateView):
	perm_code_names = ['tze_gshu_tailan_menu_view']
	template_name = 'gshu_tailan/delgerengui_htmls/tsever_us_tugeelt_delgerengui.html'
	def get_context_data(self, **kwargs):
		context = super(GSHU_tsever_us_delgerengui, self).get_context_data(**kwargs)
		gshu_id = kwargs['gshu_id']
		gshu = get_object_or_404(GShU, id = gshu_id)
		context['obj'] = gshu.tsever_us_tugeelt
		return context
class GSHU_tseverleh_baiguulamj_delgerengui(LoginRequired, TemplateView):
	perm_code_names = ['tze_gshu_tailan_menu_view']
	template_name = 'gshu_tailan/delgerengui_htmls/ts_baiguulamj_delgerengui.html'
	def get_context_data(self, **kwargs):
		context = super(GSHU_tseverleh_baiguulamj_delgerengui, self).get_context_data(**kwargs)
		gshu_id = kwargs['gshu_id']
		gshu = get_object_or_404(GShU, id = gshu_id)
		context['obj'] = gshu.ts_baiguulamj
		return context
class GSHU_bolovson_huchin_delgerengui(LoginRequired, TemplateView):
	perm_code_names = ['tze_gshu_tailan_menu_view']
	template_name = 'gshu_tailan/delgerengui_htmls/bolovson_huchin_delgerengui.html'
	def get_context_data(self, **kwargs):
		context = super(GSHU_bolovson_huchin_delgerengui, self).get_context_data(**kwargs)
		gshu_id = kwargs['gshu_id']
		gshu = get_object_or_404(GShU, id = gshu_id)
		context['obj'] = gshu.b_huch_uzuulelt
		if gshu.b_huch_uzuulelt.Ne1 and gshu.b_huch_uzuulelt.N1:
			context['result_burdelt'] = gshu.b_huch_uzuulelt.Ne1*100/gshu.b_huch_uzuulelt.N1
		else:
			context['result_burdelt'] = "Өгөгдөл дутуу учир тооцоолох боломжгүй"
		if gshu.b_huch_uzuulelt.N1 and gshu.b_huch_uzuulelt.C:
			context['result_hereglegch'] = gshu.b_huch_uzuulelt.N1*1000/gshu.b_huch_uzuulelt.C
		else:
			context['result_hereglegch'] = "Өгөгдөл дутуу учир тооцоолох боломжгүй"
		return context
class GSHU_sanhuu_delgerengui(LoginRequired, TemplateView):
	perm_code_names = ['tze_gshu_tailan_menu_view']
	template_name = 'gshu_tailan/delgerengui_htmls/sanhuu_uzuulelt_delgerengui.html'
	def get_context_data(self, **kwargs):
		context = super(GSHU_sanhuu_delgerengui, self).get_context_data(**kwargs)
		gshu_id = kwargs['gshu_id']
		gshu = get_object_or_404(GShU, id = gshu_id)
		context['obj'] = gshu.s_uzuulelt
		return context










	

class uamedeeView(LoginRequired,TemplateView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = "uamedee.html"

	def get_context_data(self, **kwargs):
		context = super(uamedeeView, self).get_context_data(**kwargs)
		self._f = UAT_yavts_ognoo_filter(self.request.GET, queryset = UAT_yavts.objects.filter(tze= self.baiguullaga))
		tze = get_object_or_404(TZE, id = self.baiguullaga.id)
		context['uatailan_ognoo_filter'] = self._f
		
		context['water'] = UA_water_analysis.objects.filter(tze = context['baiguullaga'], status= True)
		context['bohir'] = AnalysisBohir.objects.filter(tze = context['baiguullaga'], status=True)
		
		tailans = tze.get_tailan_names()
		context['tailans'] = tailans
		return context

class UATailan_listView(uamedeeView):
	template_name = "uamedee/list_htmls/tze_uatailan_list.html"
class Water_analysis_listView(LoginRequired, ListView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = 'uamedee/list_htmls/tze_water_analysis_list.html'
	def get_queryset(self):
		tze = get_object_or_404(TZE, id=self.baiguullaga.id)
		self.queryset = UA_water_analysis.objects.filter(tze = tze, status = True)
		return super(Water_analysis_listView, self).get_queryset()

class Bohir_analysis_listView(LoginRequired, ListView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = 'uamedee/list_htmls/tze_bohir_analysis_list.html'
	def get_queryset(self):
		tze = get_object_or_404(TZE, id=self.baiguullaga.id)
		self.queryset = AnalysisBohir.objects.filter(tze = tze, status = True)
		return super(Bohir_analysis_listView, self).get_queryset()

class UA_water_analysis_insert(Base_Ajax_FormView):
	perm_code_names = ['add_analysiswater']
	form_class = UA_water_analysisForm
	success_url = reverse_lazy('tze_uamedee_menu')
	view_url = reverse_lazy('tze_water_analysis_insert')
	template_name = 'uamedee/form_div_htmls/savlasan_water_analysis.html'
	def form_valid(self, form):
		obj = form.save(commit = False)
		tze = get_object_or_404(TZE, id=self.baiguullaga.id)
		obj.tze = tze
		obj.status = True
		obj.created_by = self.user
		obj.save()
		return super(UA_water_analysis_insert, self).form_valid(form)

class Bohir_analysis_formView(Base_Ajax_FormView):
	perm_code_names = ['add_analysisbohir']
	form_class = AnalysisBohirForm
	success_url = reverse_lazy('tze_uamedee_menu')
	view_url = reverse_lazy('tze_bohir_analysis_insert')
	template_name = 'uamedee/form_div_htmls/bohir_analysis_form.html'
	def form_valid(self, form):
		obj = form.save(commit = False)
		tze = get_object_or_404(TZE, id=self.baiguullaga.id)
		obj.tze = tze
		obj.status = True
		obj.created_by = self.user
		obj.save()
		return super(Bohir_analysis_formView, self).form_valid(form)

class UA_water_analysis_delgerengui(LoginRequired, TemplateView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = "uamedee/shinjilgee_delgerengui/savlasan_water_analysis_delgerengui.html"
	object_class = AnalysisWater
	def dispatch(self, request, *args, **kwargs):
		obj_id = kwargs['pk']
		self.obj = get_object_or_404(self.object_class, id = obj_id)
		return super(UA_water_analysis_delgerengui, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):
		context = super(UA_water_analysis_delgerengui, self).get_context_data(**kwargs)
		context['obj'] = self.obj
		return context

class BohirWater_analysis_delgerengui(UA_water_analysis_delgerengui):
	template_name = "uamedee/shinjilgee_delgerengui/bohir_water_analysis_delgerengui.html"
	object_class = AnalysisBohir

	




def waterAnalysisDelete(request, id):
	try:
		note = get_object_or_404(AnalysisWater, pk=id)
		note.end_time = timezone.now()
		note.created_by = jsonpickle.decode(request.session['user'])
		note.status = False
		note.save()
		notee = AjiltanWaterHistory.objects.filter(analysiswater=note).last()

		notee.end_time = timezone.now()
		notee.created_by = jsonpickle.decode(request.session['user'])
		notee.status = False
		notee.save()
	except:
		raise Http404
	return HttpResponseRedirect("/engineering/uamedee/")

def bohirAnalysisDelete(request, id):
	try:
		note = get_object_or_404(AnalysisBohir, pk=id)
		note.end_time = timezone.now()
		note.created_by = jsonpickle.decode(request.session['user'])
		note.status = False
		note.save()
	#	notee = get_object_or_404(NormStandartHistory, normstandart=note)
	#	notee.end_time = timezone.now()
	#	notee.created_by = jsonpickle.decode(request.session['user'])
	#	notee.status = False
	#	notee.save()
	except:
		raise Http404
	return HttpResponseRedirect("/engineering/uamedee/")




class UAT_hudag_sudalgaa(LoginRequired, ListView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = "uatailan/gunii_hudag_sudalgaa.html"
	def get_queryset(self):
		queryset = Hudag.objects.filter(tze = self.baiguullaga,status=True)
		return queryset
class UAT_tsevershuuleh(LoginRequired, ListView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = "uatailan/tsevershuuleh_sudalgaa.html"
	def get_queryset(self):
		queryset = Ts_baiguulamj.objects.filter(tze = self.baiguullaga, torol=u'Цэвэр усны', status=True)
		return queryset
class UAT_usansan(LoginRequired, ListView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = "uatailan/usansan_sudalgaa.html"
	def get_queryset(self):
		queryset = UsanSan.objects.filter(tze = self.baiguullaga, status=True)
		return queryset
class UAT_tsever_us_nasosStants(LoginRequired, ListView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = "uatailan/tsever_us_nasos_stants_sudalgaa.html"
	def get_queryset(self):
		queryset = NasosStants.objects.filter(tze = self.baiguullaga, nasos_torol = u'Цэвэр усны насос станц', status=True)
		return queryset
class UAT_tsever_us_lab(LoginRequired, ListView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = "uatailan/tsever_us_lab_sudalgaa.html"
	def get_queryset(self):
		queryset = Lab.objects.filter(tze = self.baiguullaga, status=True)
		return queryset
class UAT_tsever_us_sh_suljee(LoginRequired, ListView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = "uatailan/tsever_us_sh_suljee.html"
	def get_queryset(self):
		queryset = Sh_suljee.objects.filter(tze = self.baiguullaga, shugam_helber = u'Цэвэр усны шугам сүлжээ', status = True)
		return queryset
class UAT_bohir_us_sh_suljee(LoginRequired, ListView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = "uatailan/bohir_us_sh_suljee_sudalgaa.html"
	def get_queryset(self):
		queryset = Sh_suljee.objects.filter(tze = self.baiguullaga, shugam_helber = u'Бохир усны шугам сүлжээ', status = True)
		return queryset
class UAT_abb(LoginRequired, ListView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = "uatailan/abb_sudalgaa.html"
	def get_queryset(self):
		queryset = ABB.objects.filter(tze = self.baiguullaga, status = True)
		return queryset
class UAT_us_dulaan_damjuulah(LoginRequired, ListView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = "uatailan/us_dulaan_damjuulah_tov_sudalgaa.html"
	def get_queryset(self):
		queryset = UsDamjuulahBair.objects.filter(tze = self.baiguullaga, status = True)
		return queryset
class UAT_us_tugeeh(LoginRequired, ListView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = "uatailan/us_tugeeh_bair_sudalgaa.html"
	def get_queryset(self):
		queryset = UsTugeehBair.objects.filter(tze = self.baiguullaga,status=True)
		return queryset
class UAT_tseverleh(LoginRequired, ListView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = "uatailan/tseverleh_sudalgaa.html"
	def get_queryset(self):
		queryset = Ts_baiguulamj.objects.filter(tze = self.baiguullaga, status=True)
		return queryset
class UAT_bohir_us_nasosStants(LoginRequired, ListView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = "uatailan/bohir_us_nasos_stants_sudalgaa.html"
	def get_queryset(self):
		queryset = NasosStants.objects.filter(tze = self.baiguullaga, nasos_torol = u'Бохир усны насос станц', status=True)
		return queryset
class UAT_water_car(LoginRequired, ListView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = "uatailan/water_car_sudalgaa.html"
	def get_queryset(self):
		queryset = WaterCar.objects.filter(tze = self.baiguullaga,status=True)
		return queryset
class UAT_bohir_car(LoginRequired, ListView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = "uatailan/bohir_car_sudalgaa.html"
	def get_queryset(self):
		queryset = BohirCar.objects.filter(tze = self.baiguullaga,status=True)
		return queryset
class UAT_hunii_noots(LoginRequired, TemplateView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = "uatailan/hunii_noots_sudalgaa.html"
	def get_context_data(self, *args, **kwargs):
		context = super(UAT_hunii_noots, self).get_context_data(*args, **kwargs)
		context['object_list'] = Ajiltan.objects.filter(baiguullaga = self.baiguullaga,status=True)
		context['school'] = School.objects.filter(emp = context['object_list'])
		context['engineeringcertificate'] = EngineeringCertificate.objects.filter(emp = context['object_list'])
		school_ajiltan_dic={}
		engCert_ajiltan_dic={}
		for a in context['object_list']:
			school_ajiltan_dic[a.id] = context['school'].filter(emp = a)
			engCert_ajiltan_dic[a.id] = context['engineeringcertificate'].filter(emp = a)
		context['school_ajiltan_dic'] = school_ajiltan_dic
		context['engCert_ajiltan_dic'] = engCert_ajiltan_dic
		return context






class Husnegt1View(LoginRequired, TemplateView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = 'uamedee/husnegt1.html'
	success_url = reverse_lazy('uamedee')
	def get_context_data(self, **kwargs):
		context = super(Husnegt1View, self).get_context_data(**kwargs)
		context['ajiltan'] = Ajiltan.objects.filter(baiguullaga = context['baiguullaga'],status=True)
		
		school_ajiltan_dic={}
		job_ajiltan_dic={}
		engCert_ajiltan_dic={}
		for a in context['ajiltan']:
			school_ajiltan_dic[a.id] = context['school'].filter(emp = a)
			job_ajiltan_dic[a.id] = context['job'].filter(emp = a)
			engCert_ajiltan_dic[a.id] = context['engineeringcertificate'].filter(emp = a)
		context['school_ajiltan_dic'] = school_ajiltan_dic
		context['job_ajiltan_dic'] = job_ajiltan_dic
		context['engCert_ajiltan_dic'] = engCert_ajiltan_dic
		
		return context

class Husnegt2View(LoginRequired, TemplateView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = 'uamedee/husnegt2.html'
	success_url = reverse_lazy('uamedee')
	def get_context_data(self, **kwargs):
		context = super(Husnegt2View, self).get_context_data(**kwargs)
		context['ajiltan'] = Ajiltan.objects.filter(baiguullaga = context['baiguullaga'],status=True)
		
		return context

class Husnegt3View(LoginRequired, TemplateView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = 'uamedee/husnegt3.html'
	success_url = reverse_lazy('uamedee')
	def get_context_data(self, **kwargs):
		context = super(Husnegt3View, self).get_context_data(**kwargs)
		context['norm'] = NormStandart.objects.filter(tze = context['baiguullaga'],status=True)
		return context

class Husnegt4View(LoginRequired, TemplateView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = 'uamedee/husnegt4.html'
	success_url = reverse_lazy('uamedee')
	def get_context_data(self, **kwargs):
		context = super(Husnegt4View, self).get_context_data(**kwargs)
		context['tonog']=Equipment.objects.filter(tze = context['baiguullaga'],status=True)
		return context
class Husnegt5View(LoginRequired, TemplateView):
	perm_code_names = ['tze_ua_tailan_menu_view']
	template_name = 'uamedee/husnegt5.html'
	success_url = reverse_lazy('uamedee')
	def get_context_data(self, **kwargs):
		context = super(Husnegt5View, self).get_context_data(**kwargs)
		return context

def ilgeeh(request):
#	for i in Certificate.objects.filter(tolov= 'huchintei').values('baiguullaga').distinct():
#	if not UAT_yavts.objects.filter(tze = TZE.objects.get(id = i.values()[0])):
#		u = UAT_yavts.objects.create(tze = TZE.objects.get(id = i.values()[0]), status = True)
#	else:
#		u = UAT_yavts.objects.get(tze = TZE.objects.get(id = i.values()[0]))
#	a = UAT_yavts(tze= TZE.objects.filter())
#	a.tailan_yavts = u'Илгээсэн'
#	a.status= True
#	a.save()
#	for i in tz_certificates:
#		for j in i.tz_id.all():
#			zaaltuud_choices.append(j.tz)
#			tailans = tailan_names(zaaltuud_choices)
#			context['tailans'] = tailans
#	for z in tailans:
#		a.uat.add(z.id)
	return HttpResponseRedirect('/engineering/uamedee/')

def Horvuuleh(request, pk=0):
	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=UATailan.xlsx'
	queryset = Sh_suljee.objects.all()


	output = StringIO.StringIO()

	workbook = xlsxwriter.Workbook(output)
	worksheet = workbook.add_worksheet('test') 
	Sh_suljee.export_to_excel(worksheet = worksheet, row_start=5, col_start=1, queryset = queryset, date_time=timezone.now())

	worksheet1 = workbook.add_worksheet('gunii_hudag')
	Hudag.export_to_excel(worksheet = worksheet1, row_start=5, col_start=1, queryset=Hudag.objects.all())

	worksheet2 = workbook.add_worksheet('abb')
	a = ABB.objects.all()
	ABB.export_to_excel(worksheet = worksheet2, row_start=5, col_start=1, queryset=a, date_time=timezone.now())

	worksheet3 = workbook.add_worksheet('equipment')
	Equipment.export_to_excel(worksheet = worksheet3, row_start=5, col_start=1, queryset=Equipment.objects.all())
	

	worksheet4 = workbook.add_worksheet('watercar')
	WaterCar.export_to_excel(worksheet = worksheet4, row_start=5, col_start=1, queryset=WaterCar.objects.all())
	

	worksheet5 = workbook.add_worksheet('bohircar')
	BohirCar.export_to_excel(worksheet = worksheet5, row_start=5, col_start=1, queryset=BohirCar.objects.all())

	worksheet6 = workbook.add_worksheet('usansan')
	UsanSan.export_to_excel(worksheet = worksheet6, row_start=5, col_start=1, queryset=UsanSan.objects.all())

	worksheet7 = workbook.add_worksheet('us tugeeh bair')
	UsTugeehBair.export_to_excel(worksheet = worksheet7, row_start=5, col_start=1, queryset=UsTugeehBair.objects.all())

	worksheet8 = workbook.add_worksheet('nasos stants')
	NasosStants.export_to_excel(worksheet=worksheet8, row_start=5, col_start=1, queryset=NasosStants.objects.all(), date_time=timezone.now())

	worksheet9 = workbook.add_worksheet('ts baiguulamj')
	Ts_baiguulamj.export_to_excel(worksheet=worksheet9, row_start=5, col_start=1, queryset=Ts_baiguulamj.objects.all(), date_time=timezone.now())

	worksheet10 = workbook.add_worksheet('us damjuulah')
	UsDamjuulahBair.export_to_excel(worksheet=worksheet10, row_start=5, col_start=1, queryset=UsDamjuulahBair.objects.all(), date_time=timezone.now())

	worksheet11 = workbook.add_worksheet('lab')
	Lab.export_to_excel(worksheet=worksheet11, row_start=5, col_start=1, queryset=Lab.objects.all(), date_time=timezone.now())

	worksheet12 = workbook.add_worksheet('hunii noots')
	tzes = TZE.objects.all()
	ajiltans = Ajiltan.objects.filter(baiguullaga=tzes).order_by('baiguullaga__org_name')
	Ajiltan.export_to_excel(worksheet=worksheet12, row_start=5, col_start=1, queryset=ajiltans, date_time=timezone.now())

	workbook.close()

	xlsx_data = output.getvalue()
	response.write(xlsx_data)
	return response

def HorvuulehToExcel(tze_id):
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

	hudag = Hudag.objects.filter(status=True, tze= tze_id)
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
	



	usansan = UsanSan.objects.filter(status=True, tze= tze_id)
	nasos = NasosStants.objects.filter(status=True, tze= tze_id)
	lab = Lab.objects.filter(status=True, tze= tze_id)
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
	analysis_tsever = AnalysisWater.objects.filter(status=True, tze= tze_id).last()
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

	tseversuljee = Sh_suljee.objects.filter(tze= tze_id, shugam_torol__in=[u'Эх үүсвэрийн цуглуулах',u'Цэвэр усны дамжуулах шугам',u'Цэвэр ус түгээх шугам'],status=True)
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



	abb= ABB.objects.filter(tze= tze_id, status= True)

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
	




	bohirsuljee = Sh_suljee.objects.filter(tze= tze_id, shugam_torol__in=[u'Бохир усны гаргалгааны шугам',u'Бохир усны цуглуулах шугам',u'Бохир ус татан зайлуулах шугам'],status=True)
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




	tseverleh_baig= Ts_baiguulamj.objects.filter(tze= tze_id, status=True)
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
	analysis_bohir = AnalysisBohir.objects.filter(tze= tze_id,status=True).last()
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
			positionn= AlbanTushaal.objects.get(id= bbbbab.alban_tushaal_id)
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



	ajiltanErh= Ajiltan.objects.get(baiguullaga= tze_id, status= True, alban_tushaal= AlbanTushaal.objects.get(baiguullaga= tze_id, position_name = AlbanTushaalList.objects.get(name= u'Захирал')))

#	ajiltanErh1= Ajiltan.objects.get(baiguullaga= tze_id, status= True, alban_tushaal= AlbanTushaal.objects.get(baiguullaga= tze_id, position_name = AlbanTushaalList.objects.get(name= u'Даргын туслах')))
#	ajiltanErh2= Ajiltan.objects.get(baiguullaga= tze_id, status= True, alban_tushaal= AlbanTushaal.objects.get(baiguullaga= tze_id, position_name = AlbanTushaalList.objects.get(name= u'Ерөнхий инженер')))
#	ajiltanErh3= Ajiltan.objects.get(baiguullaga= tze_id, status= True, alban_tushaal= AlbanTushaal.objects.get(baiguullaga= tze_id, position_name = AlbanTushaalList.objects.get(name= u'Ерөнхий нягтлан бодогч')))
  	baiguullag= TZE.objects.get(id= tze_id)
#   Хүснэгт 11
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

	




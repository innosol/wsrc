# -*- coding: utf-8 -*-
import datetime
import jsonpickle
import json
from django.core.exceptions import ObjectDoesNotExist
from multiforms import MultiFormsView
from django.views.generic import FormView, View, TemplateView, UpdateView
from applications.app.views import Permission, LoginRequired
from applications.app.forms import *
from .forms import *
from applications.app.models import *
import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
import random
import string
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from django.utils import timezone
from applications.director.views import AjaxTemplateMixin
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def lab_insert_func(self, form):
	user = self.request.session['user']
	a = form.save(commit = False)
	a.tze = TZE.objects.get(org_name=self.request.POST.get('tze'))
	a.status = True
	a.created_by = jsonpickle.decode(user)
	a.save()
	lab_history_writing(a)

def nasos_insert_func(self, form):
	user = self.request.session['user']
	bb = form.save(commit = False)
	bb.tze = TZE.objects.get(org_name = self.request.POST.get('tze'))
	bb.status = True
	bb.created_by = jsonpickle.decode(user)
	bb.save()
	nasos_history_writing(bb)
	nasos_picture = self.request.FILES.getlist('nasos_picture')
	for i in range(len(nasos_picture)):
		ab=NasosZurag(nasos_id=bb, nasos_picture= nasos_picture[i])
		ab.save()
		ad= NasosZuragHistory(nasoszurag=ab,nasos_id=bb,nasos_picture= str(nasos_picture[i]))
		ad.save()

def usansan_insert_func(self, form):
	user = self.request.session['user']
	ff = UsanSan(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
	ff.ashiglaltand_orson_ognoo = form.cleaned_data['ashiglaltand_orson_ognoo']
	ff.tailbar = form.cleaned_data['tailbar']
	ff.usansan_helber = form.cleaned_data['usansan_helber']
	ff.ner = form.cleaned_data['ner']
	ff.usansan_aimag = form.cleaned_data['usansan_aimag']
	ff.usansan_sum = form.cleaned_data['usansan_sum']
	ff.usansan_bag = form.cleaned_data['usansan_bag']
	ff.usansan_address = form.cleaned_data['usansan_address']
	ff.bagtaamj = form.cleaned_data['bagtaamj']
	ff.huurai_hlor = form.cleaned_data['huurai_hlor']
	ff.shingen_hlor = form.cleaned_data['shingen_hlor']
	ff.davsnii_uusmal = form.cleaned_data['davsnii_uusmal']
	ff.usansan_haruul = form.cleaned_data['usansan_haruul']
	ff.bairshiliin_schema = form.cleaned_data['bairshiliin_schema']
	ff.bairshiliin_photo = form.cleaned_data['bairshiliin_photo']
	ff.status = True
	ff.created_by=jsonpickle.decode(user)
	ff.save()
	usan_san_history_writing(ff)
	
	ognoo = self.request.POST.getlist('ognoo')
	akt = self.request.FILES.getlist('akt')
	if len(ognoo) == len(akt):
		for i in range(len(ognoo)):
			ab=UsanSanUgaalga(usansan_id=ff, ognoo= ognoo[i], akt= akt[i],created_by=jsonpickle.decode(user))
			ab.save()
			ad= UsanSanUgaalgaHistory(usansanugaalga=ab,usansan_id=ff, ognoo= ognoo[i], akt= str(akt[i]),created_by=jsonpickle.decode(user))
			ad.save()

def sh_suljee_insert_func(self, form):
	user = self.request.session['user']
	dd = Sh_suljee(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
	dd.shugam_helber = form.cleaned_data['shugam_helber']
	dd.shugam_torol = form.cleaned_data['shugam_torol']
	dd.shugam_urt= form.cleaned_data['shugam_urt']
	dd.ashiglaltand_orson_ognoo = form.cleaned_data['ashiglaltand_orson_ognoo']
	dd.diametr= form.cleaned_data['diametr']
	dd.hudgiin_too= form.cleaned_data['hudgiin_too']
	dd.gemtliin_too= form.cleaned_data['gemtliin_too']
	dd.schema = form.cleaned_data['schema']
	dd.created_by=jsonpickle.decode(user)
	dd.status = True
	dd.save()
	sh_suljee_history_writing(dd)
	table_diametr = self.request.POST.getlist('table_diametr')
	gan = self.request.POST.getlist('gan')
	huvantsar = self.request.POST.getlist('huvantsar')
	shirem = self.request.POST.getlist('shirem')
	busad = self.request.POST.getlist('busad')
	ashiglalt_ognoo = self.request.POST.getlist('ashiglalt_ognoo')
	if len(table_diametr) == len(gan) and len(gan) == len(huvantsar) and len(huvantsar) == len(shirem) and len(shirem) == len(busad) and len(busad) == len(ashiglalt_ognoo):
		for i in range(len(gan)):
			ab=Sh_suljeeTable(suljee_id=dd, table_diametr= table_diametr[i],gan= gan[i],huvantsar= huvantsar[i],shirem= shirem[i],busad= busad[i],ashiglalt_ognoo= ashiglalt_ognoo[i],created_by=jsonpickle.decode(user))
			ab.save()
			ad= Sh_suljeeTableHistory(table=ab,suljee_id=dd, table_diametr= table_diametr[i],gan= gan[i],huvantsar= huvantsar[i],shirem= shirem[i],busad= busad[i],ashiglalt_ognoo= ashiglalt_ognoo[i],created_by=jsonpickle.decode(user))
			ad.save()

def hudag_insert_func(self, form):
	user = self.request.session['user']
	a = Hudag(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
	a.huchin_chadal = form.cleaned_data['huchin_chadal']
	a.ashiglaltand_orson_ognoo = form.cleaned_data['ashiglaltand_orson_ognoo']
	a.tailbar = form.cleaned_data['tailbar']
	a.olborloj_bui_us=form.cleaned_data['olborloj_bui_us']
	a.haruul = form.cleaned_data['haruul']
	a.tsoonog= form.cleaned_data['tsoonog']
	a.created_by=jsonpickle.decode(user)
	a.status= True
	a.save()
	hudag_history_writing(a)
	
	outside_picture = self.request.FILES.getlist('outside_picture')
	for i in range(len(outside_picture)):
		ab=HudagOutsidePicture(hudag_id=a, outside_picture= outside_picture[i])
		ab.save()
		ad= HudagOutsidePictureHistory(hudagoutsidepicture=ab,hudag_id=a,outside_picture= str(outside_picture[i]))
		ad.save()

def us_tugeeh_insert_func(self, form):
	user = self.request.session['user']
	tzee = TZE.objects.get(org_name = self.request.POST.get('tze'))
	hh = form.save(commit=False)
	hh.tze = tzee
	hh.status = True
	hh.created_by=jsonpickle.decode(user)
	hh.save()
	us_tugeeh_history_writing(hh)	# history-d hiine bas hadgalna
	ugaalga_ognoo = self.request.POST.getlist('ugaalga_ognoo')
	for i in range(len(ugaalga_ognoo)):
		ab=UsTugeehBairSavUgaalga(ussav_id=hh, ugaalga_ognoo= ugaalga_ognoo[i],created_by=jsonpickle.decode(user))
		ab.save()
		ad= UsTugeehBairSavUgaalgaHistory(ustugeehbairsavugaalga=ab, ussav_id=hh, ugaalga_ognoo= ugaalga_ognoo[i], created_by=jsonpickle.decode(user))
		ad.save()

def zdt(self, form):
	user = self.request.session['user']
	dd = ZDTodorhoilolt(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
	dd.todorhoilolt_picture = form.cleaned_data['todorhoilolt_picture']
	dd.begin_time=timezone.now()
	dd.created_by=jsonpickle.decode(user)
	dd.status=True
	dd.save()
	dda = ZDTodorhoiloltHistory(zdtodorhoilolt= dd)
	dda.todorhoilolt_picture = form.cleaned_data['todorhoilolt_picture']
	dda.begin_time=dd.begin_time
	dda.created_by=jsonpickle.decode(user)
	dda.status = True
	dda.save()

def hangagch(self,form):
	user = self.request.session['user']
	de = HangagchBaiguullaga(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
	de.h_b_todorhoilolt  = form.cleaned_data['h_b_todorhoilolt']
	de.baiguulsan_geree  = form.cleaned_data['baiguulsan_geree']
	de.begin_time=timezone.now()
	de.created_by=jsonpickle.decode(user)
	de.status=True
	de.save()
	dde = HangagchBaiguullagaHistory(hangagchbaiguullaga= de)
	dde.h_b_todorhoilolt = form.cleaned_data['h_b_todorhoilolt']
	dde.baiguulsan_geree  = form.cleaned_data['baiguulsan_geree']
	dde.begin_time=de.begin_time
	dde.created_by=jsonpickle.decode(user)
	dde.status=True
	dde.save()

def tax(self, form):
	user = self.request.session['user']
	da= TaxTodorhoilolt(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
	da.todorhoilolt = form.cleaned_data['todorhoilolt']
	da.begin_time=timezone.now()
	da.created_by=jsonpickle.decode(user)
	da.status=True
	da.save()
	daad = TaxTodorhoiloltHistory(taxtodorhoilolt= da)
	daad.todorhoilolt = form.cleaned_data['todorhoilolt']
	daad.begin_time=da.begin_time
	daad.created_by=jsonpickle.decode(user)
	daad.status=True
	daad.save()

def audit(self, form):
	user = self.request.session['user']
	df = AuditDugnelt(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
	df.dugnelt = form.cleaned_data['dugnelt']
	df.begin_time=timezone.now()
	df.created_by=jsonpickle.decode(user)
	df.status=True
	df.save()
	dfa = AuditDugneltHistory(auditdugnelt= df)
	dfa.dugnelt = form.cleaned_data['dugnelt']
	dfa.begin_time=df.begin_time
	dfa.created_by=jsonpickle.decode(user)
	dfa.status=True
	dfa.save()

def norm(self, form):
	user = self.request.session['user']
	ds = NormStandart(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
	ds.code = form.cleaned_data['code']
	ds.ner = form.cleaned_data['ner']
	ds.too = form.cleaned_data['too']
	ds.begin_time=timezone.now()
	ds.status=True
	ds.created_by=jsonpickle.decode(user)
	ds.save()
	dsa = NormStandartHistory(normstandart= ds)
	dsa.code = form.cleaned_data['code']
	dsa.ner = form.cleaned_data['ner']
	dsa.too = form.cleaned_data['too']
	dsa.begin_time=ds.begin_time
	dsa.created_by=jsonpickle.decode(user)
	dsa.status=True
	dsa.save()

def ulsiinakt(self, form):
	user = self.request.session['user']
	dakt = UlsiinAkt(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
	dakt.akt = form.cleaned_data['akt']
	dakt.begin_time=timezone.now()
	dakt.created_by=jsonpickle.decode(user)
	dakt.status = True
	dakt.save()
	dka = UlsiinAktHistory(ulsiinakt= dakt)
	dka.akt = form.cleaned_data['akt']
	dka.begin_time=dakt.begin_time
	dka.created_by=jsonpickle.decode(user)
	dka.status=True
	dka.save()

def uszuvshuurul(self, form):
	user = self.request.session['user']
	dus = UsZuvshuurul(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
	dus.zuvshuurul = form.cleaned_data['zuvshuurul']
	dus.dugnelt = form.cleaned_data['dugnelt']
	dus.geree = form.cleaned_data['geree']
	dus.begin_time=timezone.now()
	dus.status=True
	dus.created_by=jsonpickle.decode(user)
	dus.save()
	dusa = UsZuvshuurulHistory(uszuvshuurul= dus)
	dusa.zuvshuurul = form.cleaned_data['zuvshuurul']
	dusa.dugnelt = form.cleaned_data['dugnelt']
	dusa.geree = form.cleaned_data['geree']
	dusa.begin_time=dus.begin_time
	dusa.status=True
	dusa.created_by=jsonpickle.decode(user)
	dusa.save()	

def orontoo(self, form):
	user = self.request.session['user']
	doron = OronTooniiSchema(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
	doron.tailbar = form.cleaned_data['tailbar']
	doron.schema = form.cleaned_data['schema']
	doron.begin_time=timezone.now()
	doron.status=True
	doron.created_by=jsonpickle.decode(user)
	doron.save()
	dorona = OronTooniiSchemaHistory(orontoo= doron)
	dorona.tailbar = form.cleaned_data['tailbar']
	dorona.schema = form.cleaned_data['schema']
	dorona.begin_time=doron.begin_time
	dorona.status=True
	dorona.created_by=jsonpickle.decode(user)
	dorona.save()

def sanhuu(self, form):
	user = self.request.session['user']
	dsan = SanhuuTailan(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
	dsan.tailan = form.cleaned_data['tailan']
	dsan.begin_time=timezone.now()
	dsan.status=True
	dsan.created_by=jsonpickle.decode(user)
	dsan.save()
	dsana = SanhuuTailanHistory(sanhuutailan= dsan)
	dsana.tailan = form.cleaned_data['tailan']
	dsana.begin_time=dsan.begin_time
	dsana.status=True
	dsana.created_by=jsonpickle.decode(user)
	dsana.save()

def abb(self, form):
	user = self.request.session['user']
	dabb = ABB(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
	dabb.barilga_ner = form.cleaned_data['barilga_ner']
	dabb.niit = form.cleaned_data['niit']
	dabb.tooluurjilt_too = form.cleaned_data['tooluurjilt_too']
	dabb.bairshil_picture = form.cleaned_data['bairshil_picture']
	dabb.photo = form.cleaned_data['photo']
	dabb.city = form.cleaned_data['city']
	dabb.district = form.cleaned_data['district']
	dabb.khoroo = form.cleaned_data['khoroo']
	dabb.address = form.cleaned_data['address']
	dabb.begin_time=timezone.now()
	dabb.status=True
	dabb.created_by=jsonpickle.decode(user)
	dabb.save()
	dabba = ABBHistory(abb= dabb)
	dabba.barilga_ner = form.cleaned_data['barilga_ner']
	dabba.niit = form.cleaned_data['niit']
	dabba.tooluurjilt_too = form.cleaned_data['tooluurjilt_too']
	dabba.bairshil_picture = form.cleaned_data['bairshil_picture']
	dabba.photo = form.cleaned_data['photo']
	dabba.city = form.cleaned_data['city']
	dabba.district = form.cleaned_data['district']
	dabba.khoroo = form.cleaned_data['khoroo']
	dabba.address = form.cleaned_data['address']
	dabba.begin_time=dabb.begin_time
	dabba.status=True
	dabba.created_by=jsonpickle.decode(user)
	dabba.save()	

def uildvertechnology(self, form):
	user = self.request.session['user']
	dakt = UildverTechnology(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
	dakt.schema = form.cleaned_data['schema']
	dakt.begin_time=timezone.now()
	dakt.created_by=jsonpickle.decode(user)
	dakt.status = True
	dakt.save()
	dka = UildverTechnologyHistory(uildvertechnology= dakt)
	dka.schema = form.cleaned_data['schema']
	dka.begin_time=dakt.begin_time
	dka.created_by=jsonpickle.decode(user)
	dka.status=True
	dka.save()

def mergejliinhyanalt(self, form):
	user = self.request.session['user']
	dakt = MergejliinHyanalt(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
	dakt.dugnelt = form.cleaned_data['dugnelt']
	dakt.begin_time=timezone.now()
	dakt.created_by=jsonpickle.decode(user)
	dakt.status = True
	dakt.save()
	dka = MergejliinHyanaltHistory(mergejliinhyanalt= dakt)
	dka.dugnelt = form.cleaned_data['dugnelt']
	dka.begin_time=dakt.begin_time
	dka.created_by=jsonpickle.decode(user)
	dka.status=True
	dka.save()

def ajliinbair(self, form):
	user = self.request.session['user']
	dakt = AjliinBair(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
	dakt.dugnelt = form.cleaned_data['dugnelt']
	dakt.begin_time=timezone.now()
	dakt.created_by=jsonpickle.decode(user)
	dakt.status = True
	dakt.save()
	dka = AjliinBairHistory(ajliinbair= dakt)
	dka.dugnelt = form.cleaned_data['dugnelt']
	dka.begin_time=dakt.begin_time
	dka.created_by=jsonpickle.decode(user)
	dka.status=True
	dka.save()
''' Engineering view '''
############################################################# UILSEE CODE START ###############################################


def e_mail_sending(fromaddr, toaddr, subject, body, passwd):
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = subject
	msg.attach(MIMEText(body, 'plain'))

	# The actual mail send
	try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.starttls()
		server.ehlo()
		server.login(fromaddr,passwd)
		text = msg.as_string()
		server.sendmail(fromaddr, toaddr, text)
		server.quit()
		print "successfully sent\n"
	except:
		print "failed\n"

class Handah_erhView(LoginRequired, MultiFormsView): # zahiral engineer nyagtlan hoyriin handah erhiig oorchloh
	
	template_name = 'handah_erh_list.html'
	success_url = '/engineering/handah_erh_list/'
	__user = None
	form_classes = {
	'user_engineer_choiceForm': User_engineer_choiceForm,
	'user_account_choiceForm': User_account_choiceForm,
	'user_engineer_delForm': User_engineer_delForm,
	'user_account_delForm': User_account_delForm,
	}

	def dispatch(self, request, *args, **kwargs):
		a = self.request.session['user']
		self.__user = jsonpickle.decode(a)
		return super(Handah_erhView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(Handah_erhView, self).get_context_data(**kwargs)
		
		try:
			eng_albanTushaalList = AlbanTushaalList.objects.get(name = 'Инженер')
		except ObjectDoesNotExist:
			eng_albanTushaalList = AlbanTushaalList(name = 'Инженер')
			eng_albanTushaalList.save()
		try:
			acc_albanTushaalList = AlbanTushaalList.objects.get(name = 'Нягтлан')
		except ObjectDoesNotExist:
			acc_albanTushaalList = AlbanTushaalList(name = 'Нягтлан')
			acc_albanTushaalList.save()

		eng_albanTushaaluud = AlbanTushaal.objects.filter(baiguullaga = context['baiguullaga'], position_name = eng_albanTushaalList)
		#print "\n\n engineer alban tushaaluud \n\n", eng_albanTushaaluud, "\n\n\n"
		acc_albanTushaaluud = AlbanTushaal.objects.filter(baiguullaga = context['baiguullaga'], position_name = acc_albanTushaalList)
		engineers = []
		accounts = []
		for i in eng_albanTushaaluud:
			engineers.extend( Ajiltan.objects.filter(baiguullaga = context['baiguullaga'], position_id = i))
			#print '\n\n engieers \n\n', engineers, '\n\n\n'
		for i in acc_albanTushaaluud:
			accounts.extend(Ajiltan.objects.filter(baiguullaga = context['baiguullaga'], position_id = i))

		all_active_users = User.objects.filter(status = True)

		eng_users = []
		eng_count = 0
		acc_users = []
		acc_count = 0
		#print "\n\n\n", all_active_users, "\n\n\n"
		for i in all_active_users:
			if i.user_id.baiguullaga == context['baiguullaga']:
				if i.user_id.position_id.position_name.name == u'Инженер':
					eng_count+=1
					eng_users.append(i.user_id)
				elif i.user_id.position_id.position_name.name == u'Нягтлан':
					acc_count+=1
					acc_users.append(i.user_id)

		if eng_count == 1:
			context['eng_user'] = eng_users[0]
		elif eng_count > 1:	# hervee negees olon user oldson bol buh user status-iig False bolgono
			for i in range(eng_count):
				eng_users[i].user.status = False
				eng_users[i].user.save()

		if acc_count == 1:
			context['acc_user'] = acc_users[0]
		elif acc_count > 1:	# hervee negees olon user oldson bol buh user status-iig False bolgono
			for i in range(acc_count):
				acc_users[i].user.status = False
				acc_users[i].user.save()
		#context['eng_user'] = User.objects.get(user_id = )
		context['engineers'] = engineers
		context['accounts'] = accounts

		user_change_histories = User_change_history.objects.filter(baiguullaga = context['baiguullaga'])
		context['user_change_histories'] = user_change_histories
		return context

	def user_engineer_choiceForm_form_valid(self, form):
		ajiltan_id = self.request.POST.get('user_engineer_choice', False)
		engineer_old_id = self.request.POST.get('user_engineer_old')
		#print "\n\nengineer user change form successs:", ajiltan_id, "\n\n"
		if ajiltan_id:
			engineer = Ajiltan.objects.get(id=ajiltan_id)
			if engineer_old_id:
				engineer_old = Ajiltan.objects.get(id=engineer_old_id)
				if engineer != engineer_old:
					engineer_old.user.status = False
					engineer_old.user.save()
					try:
						m = User_change_history.objects.get(user_id = engineer_old, change_name = u"Хандах эрх олгогдсон")
					except ObjectDoesNotExist:
						print "ERROR user change history doesn't exist ERROR\n"
						m = User_change_history(baiguullaga = engineer_old.baiguullaga, user_id = engineer_old, change_name = u"Хандах эрх олгогдсон", created_by = self.__user)
						m.save()
					m.change_name = u"Хандах эрх цуцлагдсан"
					m.save()

					password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15)) ############# generate hiigeed e-mail-eer yavuuldag baih yostoi

					e_mail_subject = "Бүртгэл амжилттай хийгдлээ"
					body = "Бүртгэл амжилтай хийгдлээ. Нууц үг: " + password
					e_mail_sending('wsrcmon@gmail.com', engineer.e_mail, e_mail_subject, body, 'QjErHKfS76KmRQBB')
					
					try:
						eng_user = User.objects.get(user_id = engineer)
						eng_user.username = engineer.e_mail
						eng_user.password = password
						eng_user.created_by = self.__user
						eng_user.status = True
					except ObjectDoesNotExist:
						eng_user = User(user_id = engineer, username = engineer.e_mail, password = password, created_by = self.__user, status = True)
					eng_user.save()
					m = User_change_history(baiguullaga = eng_user.user_id.baiguullaga, user_id = eng_user.user_id, change_name = "Хандах эрх олгогдсон", created_by = self.__user)
					m.save()
			else:
				password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15)) ############# generate hiigeed e-mail-eer yavuuldag baih yostoi

				e_mail_subject = "Бүртгэл амжилттай хийгдлээ"
				body = "Бүртгэл амжилтай хийгдлээ. Нууц үг: " + password
				e_mail_sending('wsrcmon@gmail.com', engineer.e_mail, e_mail_subject, body, 'QjErHKfS76KmRQBB')

				try:
					eng_user = User.objects.get(user_id = engineer)
					eng_user.username = engineer.e_mail
					eng_user.password = password
					eng_user.created_by = self.__user
					eng_user.status = True
				except ObjectDoesNotExist:
					eng_user = User(user_id = engineer, username = engineer.e_mail, password = password, created_by = self.__user, status = True)
				eng_user.save()
				m = User_change_history(baiguullaga = eng_user.user_id.baiguullaga, user_id = eng_user.user_id, change_name = u"Хандах эрх олгогдсон", created_by = self.__user)
				m.save()
		############## permission_group nemj ogoh dutuu
		############## user history - d hadgaldag baih yostoi. Modelee sain todruulah heregtei
		############## Omnoh useriin status - iig false bolgoh yostoi

		return super(Handah_erhView, self).forms_valid(form, form)

	def user_account_choiceForm_form_valid(self, form):
		ajiltan_id = self.request.POST.get('user_account_choice', False)
		account_old_id = self.request.POST.get('user_account_old')
		#print "\n\nengineer user change form successs:", ajiltan_id, "\n\n"
		if ajiltan_id:
			account = Ajiltan.objects.get(id=ajiltan_id)
			if account_old_id:
				account_old = Ajiltan.objects.get(id=account_old_id)
				if account != account_old:
					account_old.user.status = False
					account_old.user.save()
					try:
						m = User_change_history.objects.get(user_id = account_old, change_name = u"Хандах эрх олгогдсон")
					except ObjectDoesNotExist:
						print "ERROR user change history doesn't exist ERROR\n"
						m = User_change_history(baiguullaga = account_old.baiguullaga, user_id = account_old, change_name = u"Хандах эрх олгогдсон", created_by = self.__user)
						m.save()
					m.change_name = u"Хандах эрх цуцлагдсан"
					m.save()
					password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15)) ############# generate hiigeed e-mail-eer yavuuldag baih yostoi

					e_mail_subject = "Бүртгэл амжилттай хийгдлээ"
					body = "Бүртгэл амжилтай хийгдлээ. Нууц үг: " + password
					e_mail_sending('wsrcmon@gmail.com', account.e_mail, e_mail_subject, body, 'QjErHKfS76KmRQBB')

					try:
						acc_user = User.objects.get(user_id = account)
						acc_user.username = account.e_mail
						acc_user.password = password
						acc_user.created_by = self.__user
						acc_user.status = True
					except ObjectDoesNotExist:
						acc_user = User(user_id = account, username = account.e_mail, password = password, created_by = self.__user, status = True)
						m = User_change_history(baiguullaga = acc_user.user_id.baiguullaga, user_id = acc_user.user_id, change_name = u"Хандах эрх олгогдсон", created_by = self.__user)
						m.save()
					acc_user.save()
			else:
				password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15)) ############# generate hiigeed e-mail-eer yavuuldag baih yostoi

				e_mail_subject = "Бүртгэл амжилттай хийгдлээ"
				body = "Бүртгэл амжилтай хийгдлээ. Нууц үг: " + password
				e_mail_sending('wsrcmon@gmail.com', account.e_mail, e_mail_subject, body, 'QjErHKfS76KmRQBB')

				try:
					acc_user = User.objects.get(user_id = account)
					acc_user.username = account.e_mail
					acc_user.password = password
					acc_user.created_by = self.__user
					acc_user.status = True
				except ObjectDoesNotExist:
					acc_user = User(user_id = account, username = account.e_mail, password = password, created_by = self.__user, status = True)
				acc_user.save()
				m = User_change_history(baiguullaga = acc_user.user_id.baiguullaga, user_id = acc_user.user_id, change_name = u"Хандах эрх олгогдсон", created_by = self.__user)
				m.save()
		return super(Handah_erhView, self).forms_valid(form, form)

	def user_engineer_delForm_form_valid(self, form):
		engineer_old_id = self.request.POST.get('user_engineer_old')
		if engineer_old_id:
			engineer_old = Ajiltan.objects.get(id=engineer_old_id)
			engineer_old.user.status = False
			engineer_old.user.save()
			try:
				m = User_change_history.objects.get(user_id = engineer_old, change_name = u"Хандах эрх олгогдсон")
			except ObjectDoesNotExist:
				print "ERROR user change history doesn't exist ERROR\n"
				m = User_change_history(baiguullaga = engineer_old.baiguullaga, user_id = engineer_old, change_name = u"Хандах эрх олгогдсон", created_by = self.__user)
				m.save()
			m.change_name = u"Хандах эрх цуцлагдсан"
			m.save()
		return super(Handah_erhView, self).forms_valid(form, form)

	def user_account_delForm_form_valid(self, form):
		account_old_id = self.request.POST.get('user_account_old')
		if account_old_id:
			account_old = Ajiltan.objects.get(id=account_old_id)
			account_old.user.status = False
			account_old.user.save()
			try:
				m = User_change_history.objects.get(user_id = account_old, change_name = u"Хандах эрх олгогдсон")
			except ObjectDoesNotExist:
				print "ERROR user change history doesn't exist ERROR\n"
				m = User_change_history(baiguullaga = account_old.baiguullaga, user_id = account_old, change_name = u"Хандах эрх олгогдсон", created_by = self.__user)
				m.save()
			m.change_name = u"Хандах эрх цуцлагдсан"
			m.save()
		return super(Handah_erhView, self).forms_valid(form, form)



def material_names(zaaltuud_choices):	# tusgai zovshoorliin zaaltuudaas hamaaran materialiudiin nersiig todruulah function
	m_names = [
				TZ_material.objects.get(material_number = 1),	# 
				TZ_material.objects.get(material_number = 2),	# 
				TZ_material.objects.get(material_number = 3),	# 
				TZ_material.objects.get(material_number = 4),	# 
				TZ_material.objects.get(material_number = 5),	# 
				TZ_material.objects.get(material_number = 6),	# 
				TZ_material.objects.get(material_number = 7),	# 
				TZ_material.objects.get(material_number = 8),	# 
				TZ_material.objects.get(material_number = 14),	# 
				TZ_material.objects.get(material_number = 15),	# 
				TZ_material.objects.get(material_number = 30),	# 
				
	]	# end buh huselted zaaval baih materialuudiin nersiig hiij ogno
	#if '12.2.3' in zaaltuud_choices or '12.2.4' in zaaltuud_choices or '12.2.5' in zaaltuud_choices or '12.2.6' in zaaltuud_choices or '12.2.7' in zaaltuud_choices or '12.2.8' in zaaltuud_choices or '12.2.9' in zaaltuud_choices or '12.2.10' in zaaltuud_choices or '12.2.11' in zaaltuud_choices or '12.2.12' in zaaltuud_choices or '12.2.13' in zaaltuud_choices:
	#	TZ_material.objects.get(material_number =24), # Хангагч байгууллагын тодорхойлолт
	#	TZ_material.objects.get(material_number =25), # Хангагч байгууллагатай байгуулсан гэрээ

	#if '12.2.1' in zaaltuud_choices or '12.2.2' in zaaltuud_choices:
	#	m_names.append(TZ_material.objects.get(material_number =10)) # Шугам сүлжээ барилга байгууламжийн зураг, технологийн схем

	if '12.2.1' in zaaltuud_choices:
		m_names.append(TZ_material.objects.get(material_number =10)) # Үйлдвэрийн технологи, түүний схем зураг, тайлбар
		m_names.append(TZ_material.objects.get(material_number =11)) # Усны чанарын шинжилгээний дүн, дүгнэлт
		m_names.append(TZ_material.objects.get(material_number =12)) # Лабораторийн шинжилгээнд МХГ-ын дүгнэлт
		m_names.append(TZ_material.objects.get(material_number =13)) # Байгаль орчны асуудал эрхэлсэн төрийн захиргааны төв байгууллагын ус ашиглалтын дүгнэлт, ус ашиглах зөвшөөрөл, гэрээ
		m_names.append(TZ_material.objects.get(material_number =16))
		

	if '12.2.2' in zaaltuud_choices:
		if not '12.2.1' in zaaltuud_choices:
			m_names.append(TZ_material.objects.get(material_number =11)) # Үйлдвэрийн технологи, түүний схем зураг, тайлбар
			m_names.append(TZ_material.objects.get(material_number =12)) # Усны чанарын шинжилгээний дүн, дүгнэлт
			m_names.append(TZ_material.objects.get(material_number =13)) # Лабораторийн шинжилгээнд МХГ-ын дүгнэлт
			#m_names.append(TZ_material.objects.get(material_number =22)) # Байгаль орчны асуудал эрхэлсэн төрийн захиргааны төв байгууллагын ус ашиглалтын дүгнэлт, ус ашиглах зөвшөөрөл, гэрээ
		m_names.append(TZ_material.objects.get(material_number =17)) # 

	if '12.2.3' in zaaltuud_choices:
		m_names.append(TZ_material.objects.get(material_number =18)) # 

	if '12.2.4' in zaaltuud_choices:
		m_names.append(TZ_material.objects.get(material_number =19)) # 

	if '12.2.5' in zaaltuud_choices:
		m_names.append(TZ_material.objects.get(material_number =20)) # 
		m_names.append(TZ_material.objects.get(material_number =9)) #

	if '12.2.6' in zaaltuud_choices:
		m_names.append(TZ_material.objects.get(material_number =21)) # 

	if '12.2.7' in zaaltuud_choices:
		m_names.append(TZ_material.objects.get(material_number =22)) # 

	if '12.2.8' in zaaltuud_choices:
		m_names.append(TZ_material.objects.get(material_number =23)) # 

	if '12.2.9' in zaaltuud_choices:
		m_names.append(TZ_material.objects.get(material_number =24)) # 

	if '12.2.10' in zaaltuud_choices:
		m_names.append(TZ_material.objects.get(material_number =25)) # 

	if '12.2.11' in zaaltuud_choices:
		m_names.append(TZ_material.objects.get(material_number =26)) # 

	if '12.2.12' in zaaltuud_choices:
		m_names.append(TZ_material.objects.get(material_number =27)) # 

	if '12.2.13' in zaaltuud_choices:
		m_names.append(TZ_material.objects.get(material_number =28)) # 

	if '12.2.14' in zaaltuud_choices:
		m_names.append(TZ_material.objects.get(material_number =29)) # 

	return m_names

def materialiud_list_function(req, baig, materials):
	materialiud_list = TZ_material_list()	
	materialiud_list.save()				# tuhain huselt deer burduuleh materialuudiin jagsaalt. End materialuudaa songono
	try:
		med_dutuu = TZ_material_status.objects.get(status = 'Мэдээлэл дутуу')	# materialiin anhnii status ni Medeelel dutuu
	except ObjectDoesNotExist:
		med_dutuu = TZ_material_status.objects.create(status = 'Мэдээлэл дутуу')
		med_dutuu.save()
	
	try:
		burdsen = TZ_material_status.objects.get(status = 'Бүрдсэн')
	except:
		burdsen = TZ_material_status.objects.create(status = 'Бүрдсэн')
		burdsen.save()

	a = req.session['user']
	user = jsonpickle.decode(a)
	for m in materials:
		if m.material_number == 1: # Байгууллагын ерөнхий мэдээлэл
			if baig.gerchilgee_picture and baig.ubd and baig.org_name  and baig.org_date  and baig.phone and baig.e_mail and baig.tax and baig.address and baig.org_type and baig.fax and baig.post and baig.reg_num: # dutuu yum baigaa esehiin shalgah heregtei:
				b = TZ_mat_status_bind.objects.create(material = m, status = burdsen, updated_datetime = datetime.datetime.now(), updated_by = user)
				materialiud_list.tz_materialiud.add(b)	# materialiig nemj baina
			else:
				b = TZ_mat_status_bind.objects.create(material = m, status = med_dutuu, updated_datetime = datetime.datetime.now(), updated_by = user)
				materialiud_list.tz_materialiud.add(b)	# materialiig nemj baina

		elif m.material_number == 2: # Аймаг орон нутгийн засаг даргын тодорхойлолт
			if ZDTodorhoilolt.objects.filter(tze = baig):
				b = TZ_mat_status_bind.objects.create(material = m, status = burdsen, updated_datetime = datetime.datetime.now(), updated_by = user)
				materialiud_list.tz_materialiud.add(b)	# materialiig nemj baina
			else:
				b = TZ_mat_status_bind.objects.create(material = m, status = med_dutuu, updated_datetime = datetime.datetime.now(), updated_by = user)
				materialiud_list.tz_materialiud.add(b)	# materialiig nemj baina

			
		elif m.material_number == 3:	# Хангагч байгууллагуудтай хийсэн гэрээ, тодорхойлолт
			if baig.tovch_taniltsuulga:
				b = TZ_mat_status_bind.objects.create(material = m, status = burdsen, updated_datetime = datetime.datetime.now(), updated_by = user)
				materialiud_list.tz_materialiud.add(b)	# materialiig nemj baina
				
			else:
				b = TZ_mat_status_bind.objects.create(material = m, status = med_dutuu, updated_datetime = datetime.datetime.now(), updated_by = user)
				materialiud_list.tz_materialiud.add(b)	# mateirialuudiig nemj baina

		else:
			b = TZ_mat_status_bind.objects.create(material = m, status = med_dutuu, updated_datetime = datetime.datetime.now(), updated_by = user)
			materialiud_list.tz_materialiud.add(b)	# mateirialuudiig nemj baina

	return materialiud_list

def tze_history_writing_func(baig):
	try:
		tze_history = TZE_history.objects.get(tze = baig, begin_time = baig.begin_time)
	except ObjectDoesNotExist:
		tze_history = TZE_history.objects.create(tze = baig)
		tze_history.reg_num = baig.reg_num
		tze_history.ubd = baig.ubd
		tze_history.org_name = baig.org_name
		tze_history.org_type = baig.org_type
		tze_history.org_date = baig.org_date
		tze_history.phone = baig.phone
		tze_history.e_mail = baig.e_mail
		tze_history.fax = baig.fax
		tze_history.post = baig.post
		tze_history.tax = baig.tax
		tze_history.city = baig.city
		tze_history.district = baig.district
		tze_history.khoroo = baig.khoroo
		tze_history.address = baig.address
		tze_history.tovch_taniltsuulga = baig.tovch_taniltsuulga
		tze_history.gerchilgee_picture = baig.gerchilgee_picture
		tze_history.begin_time = baig.begin_time
		tze_history.created_by = baig.created_by
		tze_history.status = baig.status
		# end time ni baihgui. Utga onooj ogohgui
		tze_history.save()
		return 1

	tze_history_new = TZE_history.objects.create(tze = baig)
	tze_history_new.reg_num = baig.reg_num
	tze_history_new.ubd = baig.ubd
	tze_history_new.org_name = baig.org_name
	tze_history_new.org_type = baig.org_type
	tze_history_new.org_date = baig.org_date
	tze_history_new.phone = baig.phone
	tze_history_new.e_mail = baig.e_mail
	tze_history_new.fax = baig.fax
	tze_history_new.post = baig.post
	tze_history_new.tax = baig.tax
	tze_history_new.city = baig.city
	tze_history_new.district = baig.district
	tze_history_new.khoroo = baig.khoroo
	tze_history_new.address = baig.address
	tze_history_new.tovch_taniltsuulga = baig.tovch_taniltsuulga
	tze_history_new.gerchilgee_picture = baig.gerchilgee_picture
	tze_history_new.created_by = baig.created_by
	tze_history_new.status = baig.status
	tze_history_new.begin_time = timezone.now()
	baig.begin_time = tze_history_new.begin_time
	baig.save()	# baiguullagiin begin time-iig shinechilj baina
	tze_history_new.save()

	tze_history.end_time = baig.begin_time
	tze_history.save()
	return 0
    
class Tusgai_zovshoorolView(LoginRequired, TemplateView):	###### end LoginRequired-aas udamshchihsna baigaa. Permission-ees udamshval deer
	template_name = 'tusgai_zovshoorol_menu.html'
	__user = None
	form_classes = {
	'huseltform': Huselt_gargah_Form,
	'huselt_tsutslahform': Huselt_tsutslah_Form,
	'huselt_ilgeehform': Huselt_ilgeeh_Form,
	'huselt_editform': Huselt_edit_Form,
	'sez_uzuuleltform': SEZ_uzuulelt_form,
	
	'hudagzuragform':HudagNegtsgesenBairshliinZuragForm,
	'hudagnegdsen':HudagNegdsenForm,
    'edit_hudagform': edit_guniihudagForm,
	'nasosform': NasosForm,
	'labform': LabForm,
	'sh_suljeeform': Sh_suljeeForm,
	'ts_baiguulamjform': Ts_baiguulamjForm,
	'usansanform': UsanSanForm,
	'usdamjuulahbairform': UsDamjuulahBairForm,
	'ustugeehbairform': UsTugeehBairForm,
	'watercarform': WaterCarForm,
	'bohircarform': BohirCarForm,
	'equipmentform':EquipmentForm,

	'baiguullagaaform':BaiguullagaForm,
	'zdtform':ZDTForm,
	'hangagchbaiguullagaform':HBGereeForm,
	'taxtodorhoiloltform': TaxTodorhoiloltForm,
	'auditdugneltform': AuditDugneltForm,
	'normstandartform':NormStandartForm,
	'ulsiinaktform': UlsiinAktForm,
	'uszuvshuurulform':UsZuvshuurulForm,
	'orontooform': SchemaForm,
	'sanhuutailanform': SanhuuTailanForm,
	'abbform': ABBForm,
	'uildvertechnologyform':UildverTechnologyForm,
	'mergejliinhyanaltform': MergejliinHyanaltForm,
	'ajliinbairform': AjliinBairForm,
	'hunii_nootsform': Hunii_noots_form,

	'zdt_burdel_bind_form': ZDT_burdel_bind_form,
	'han_burdel_bind_form': Hangagch_burdel_bind_form,

	'tax_burdel_bind_form': Tax_burdel_bind_form,
	'sanhuuTailan_burdel_bind_form': SanhuuTailan_burdel_bind_form,
	'audit_dugnelt_burdel_bind_form': Audit_dugnelt_burdel_bind_form,
	'oron_toonii_schemas_burdel_bind_form': Oron_toonii_schemas_burdel_bind_form,
	'norm_standarts_burdel_bind_form': Norm_standarts_burdel_bind_form,
	'ulsiin_komis_akt_burdel_bind_form': Ulsiin_komis_akt_burdel_bind_form,
	'us_ashiglah_zovshoorol_burdel_bind_form': Us_ashiglah_zovshoorol_burdel_bind_form,
	'uildver_tech_schemas_burdel_bind_form': Uildver_tech_schemas_burdel_bind_form,
	'mheg_dugnelt_burdel_bind_form': Mheg_dugnelt_burdel_bind_form,
	'ajliin_bair_dugnelts_burdel_bind_form': Ajliin_bair_dugnelts_burdel_bind_form,
	'mashin_TT_burdel_bind_form': Mashin_TT_burdel_bind_form,

	}
	success_url = '/engineering/tz_tables/'
	def dispatch(self, request, *args, **kwargs):
		a = self.request.session['user']
		self.__user = jsonpickle.decode(a)
		return super(Tusgai_zovshoorolView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(Tusgai_zovshoorolView, self).get_context_data(**kwargs)
		tz_huseltuud = TZ_Huselt.objects.filter(tze = context['baiguullaga'])
		context['tz_huseltuud'] = tz_huseltuud

		tzHuselt_warn_dic = {}
		tzHuselt_burdel = {}
		tzHuselt_burdel_history_dic = {}
		tzHuselt_medegdel_dic = {}
		for h in tz_huseltuud:
			# huselt bur deer
			warns = TZ_anhaaruulga.objects.filter(tz_huselt = h)	# tuhain huselttei holbootoi buh warninguud
			burdels = Burdel_history.objects.filter(tz_huselt = h)	# tuhain huseltiin buh burdeliin history
			medegdels = TZ_medegdel.objects.filter(tz_huselt = h) # tuhain huseltiin buh medegdeluud

			tzHuselt_burdel[h.id] = Burdel.objects.get(tz_huselt = h)	# huselted burdel gantshan shirheg baina
			tzHuselt_burdel_history_dic[h.id] = burdels
			tzHuselt_warn_dic[h.id] = warns
			tzHuselt_medegdel_dic[h.id] = medegdels
		
		context['tzHuselt_burdel'] = tzHuselt_burdel	
		context['tzHuselt_burdel_history_dic'] = tzHuselt_burdel_history_dic
		context['tzHuselt_warn_dic'] = tzHuselt_warn_dic
		context['tzHuselt_medegdel_dic'] = tzHuselt_medegdel_dic
		context['tz_certificates'] = Certificate.objects.filter(baiguullaga = context['baiguullaga'], status = True)

		context['ehudag'] = Hudag.objects.filter(tze = context['baiguullaga'],status=True)
		context['enasos'] = Nasos.objects.filter(tze = context['baiguullaga'],status=True)
		context['elab'] = Lab.objects.filter(tze = context['baiguullaga'],status=True)
		context['eusansan'] = UsanSan.objects.filter(tze = context['baiguullaga'],status=True)
		context['ewatercar'] = WaterCar.objects.filter(tze = context['baiguullaga'], status = True)
		context['ebohircar'] = BohirCar.objects.filter(tze = context['baiguullaga'], status = True)

		context['tsever_usnii_damjuulah'] = Sh_suljee.objects.filter(tze=context['baiguullaga'], shugam_torol = u'Цэвэр усны дамжуулах шугам', status=True)
		context['tsever_usnii_tugeeh'] = Sh_suljee.objects.filter(tze=context['baiguullaga'], shugam_torol = u'Цэвэр ус түгээх шугам', status=True)
		context['bohir_us_gargalgaa_shugam'] = Sh_suljee.objects.filter(tze=context['baiguullaga'], shugam_torol = u'Бохир усны гаргалгааны шугам', status=True)
		context['bohir_us_tsugluulah_shugam'] = Sh_suljee.objects.filter(tze=context['baiguullaga'], shugam_torol = u'Бохир усны цуглуулах шугам', status=True)
		context['bohir_us_tatan_zailuulah_shugam'] = Sh_suljee.objects.filter(tze=context['baiguullaga'], shugam_torol = u'Бохир ус татан зайлуулах шугам', status=True)
		context['tonog']=Equipment.objects.filter(tze = context['baiguullaga'],status=True)
		context['tseverleh_baig'] = Ts_baiguulamj.objects.filter(tze = context['baiguullaga'], status=True)
		context['usdamjuulah'] = UsDamjuulahBair.objects.filter(tze = context['baiguullaga'], status = True)

		context['baig'] = TZE.objects.filter(id=context['baiguullaga'].id)		
		context['zdt'] = ZDTodorhoilolt.objects.filter(tze = context['baiguullaga'], status = True)
		context['han'] = HangagchBaiguullaga.objects.filter(tze = context['baiguullaga'], status = True)
		context['tax'] = TaxTodorhoilolt.objects.filter(tze = context['baiguullaga'], status = True)
		context['audit'] = AuditDugnelt.objects.filter(tze = context['baiguullaga'], status = True)
		context['norm'] = NormStandart.objects.filter(tze = context['baiguullaga'], status = True)
		context['akt'] = UlsiinAkt.objects.filter(tze = context['baiguullaga'], status = True)
		context['us'] = UsZuvshuurul.objects.filter(tze = context['baiguullaga'], status = True)
		context['oron'] = OronTooniiSchema.objects.filter(tze = context['baiguullaga'], status = True)
		context['sanhuu'] = SanhuuTailan.objects.filter(tze = context['baiguullaga'], status = True)
		context['abb'] = ABB.objects.filter(tze = context['baiguullaga'], status = True)
		context['uildver'] = UildverTechnology.objects.filter(tze = context['baiguullaga'], status = True)
		context['hyanalt'] = MergejliinHyanalt.objects.filter(tze = context['baiguullaga'], status = True)
		context['ajliinbair'] = AjliinBair.objects.filter(tze = context['baiguullaga'], status = True)
		context['ustugeeh'] = UsTugeehBair.objects.filter(tze = context['baiguullaga'], status = True)
		context['aimag'] = Aimag.objects.all()
		context['sum'] = Sum.objects.all()
		context['bag'] = Bag.objects.all()

		return context

	def hudagnegdsen_form_valid(self, form):
		hudag_insert_func(self, form)
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	def hudagzuragform_form_valid(self, form):
		user = self.request.session['user']
		a = HudagNegtsgesenBairshliinZurag(tze_id = TZE.objects.get(org_name = self.request.POST.get('tze')))
		a.bairshliin_picture = form.cleaned_data['bairshliin_picture']
		a.begin_time=timezone.now()
		a.created_by=jsonpickle.decode(user)
		a.status= True
		a.save()
		aa= HudagNegtsgesenBairshliinZuragHistory(hudagnegtgesenbairshliinzurag=a)
		aa.bairshliin_picture = form.cleaned_data['bairshliin_picture']
		aa.begin_time=timezone.now()
		aa.created_by=jsonpickle.decode(user)
		aa.status= True
		aa.save()
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	def nasosform_form_valid(self, form):
		nasos_insert_func(self, form)
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)

		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	def labform_form_valid(self, form):
		lab_insert_func(self, form)
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)

	def sh_suljeeform_form_valid(self, form):
		sh_suljee_insert_func(self,form)
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	def ts_baiguulamjform_form_valid(self, form):
		user = self.request.session['user']
		ee = Ts_baiguulamj(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
		ee.huchin_chadal = form.cleaned_data['huchin_chadal']
		ee.ashiglaltand_orson_ognoo = form.cleaned_data['ashiglaltand_orson_ognoo']
		ee.mehanik = form.cleaned_data['mehanik']
		ee.biologi = form.cleaned_data['biologi']
		ee.fizik = form.cleaned_data['fizik']
		ee.technology_schema = form.cleaned_data['technology_schema']
		ee.created_by=jsonpickle.decode(user)
		ee.status = True
		ee.save()
		ts_baiguulamj_history_writing(ee)
		barilga_tonog = self.request.POST.getlist('barilga_tonog')
		huchin_chadall = self.request.POST.getlist('huchin_chadall')
		too = self.request.POST.getlist('too')
		ashiglaltand_orson_ognooo = self.request.POST.getlist('ashiglaltand_orson_ognooo')
		tailbarr = self.request.POST.getlist('tailbarr')
		if len(barilga_tonog) == len(huchin_chadall) and len(huchin_chadall) == len(too) and len(too) == len(ashiglaltand_orson_ognooo) and len(ashiglaltand_orson_ognooo) == len(tailbarr) :
			for i in range(len(huchin_chadall)):
				ab=Ts_tohooromj(ts_baiguulamj=ee, barilga_tonog= barilga_tonog[i],huchin_chadall= huchin_chadall[i],too= too[i],ashiglaltand_orson_ognooo= ashiglaltand_orson_ognooo[i],tailbarr= tailbarr[i],created_by=jsonpickle.decode(user))
				ab.save()
				ad= Ts_tohooromjHistory(Ts_tohooromj=ab,barilga_tonog= barilga_tonog[i],huchin_chadall= huchin_chadall[i],too= too[i],ashiglaltand_orson_ognooo= ashiglaltand_orson_ognooo[i],tailbarr= tailbarr[i], created_by=jsonpickle.decode(user))
				ad.save()
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	def usansanform_form_valid(self, form):
		usansan_insert_func(self, form)
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	def usdamjuulahbairform_form_valid(self, form):
		user = self.request.session['user']
		gg = UsDamjuulahBair(tze=TZE.objects.get(org_name = self.request.POST.get('tze')))
		gg.ashiglaltand_orson_ognoo = form.cleaned_data['ashiglaltand_orson_ognoo']
		gg.created_by=jsonpickle.decode(user)
		gg.status= True
		gg.tovlorson= form.cleaned_data['tovlorson']
		gg.bairiiin_uzeli= form.cleaned_data['bairiiin_uzeli']
		gg.baiguulalt_holbolt_picture = form.cleaned_data['baiguulalt_holbolt_picture']
		gg.picture = form.cleaned_data['picture']
		gg.bair_uzeli_holbolt_schema = form.cleaned_data['bair_uzeli_holbolt_schema']
		gg.save()
		tonog = self.request.POST.getlist('barilga_tonog')
		huchin_chadall = self.request.POST.getlist('huchin_chadall')
		too = self.request.POST.getlist('too')
		ognoo = self.request.POST.getlist('ognoo')
		tailbarr = self.request.POST.getlist('tailbarr')
		if len(tonog) == len(huchin_chadall) and len(huchin_chadall) == len(too) and len(too) == len(ognoo) and len(ognoo) == len(tailbarr) :
			for i in range(len(huchin_chadall)):
				ab=UsDamjuulahBairTonog(us_id=gg, tze=TZE.objects.get(org_name = self.request.POST.get('tze')), tonog= tonog[i],huchin_chadall= huchin_chadall[i],too= too[i],ognoo= ognoo[i],tailbarr= tailbarr[i],created_by=jsonpickle.decode(user))
				ab.save()
				ad= UsDamjuulahBairTonogHistory(usdamjuulahbairtonog=ab, tze=TZE.objects.get(org_name = self.request.POST.get('tze')), tonog= tonog[i],huchin_chadall= huchin_chadall[i],too= too[i],ognoo= ognoo[i],tailbarr= tailbarr[i], created_by=jsonpickle.decode(user))
				ad.save()
		us_damjuulah_history_writing(gg)	# history-d hiine bas hadgalna
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	def ustugeehbairform_form_valid(self, form):
		us_tugeeh_insert_func(self, form)
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	def watercarform_form_valid(self, form):
		user = self.request.session['user']
		jj = WaterCar(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
		jj.mark = form.cleaned_data['mark']
		jj.no = form.cleaned_data['no']
		jj.huchin_chadal = form.cleaned_data['huchin_chadal']
		jj.daats = form.cleaned_data['daats']
		jj.gerchilgee_picture = form.cleaned_data['gerchilgee_picture']
		jj.hun_am_too = form.cleaned_data['hun_am_too']
		jj.utb_too = form.cleaned_data['utb_too']
		jj.aanb_too = form.cleaned_data['aanb_too']
		jj.created_by=jsonpickle.decode(user)
		jj.status= True
		jj.save()
		watercar_history_writing(jj)
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	def bohircarform_form_valid(self, form):
		user = self.request.session['user']
		ll = BohirCar(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
		ll.mark = form.cleaned_data['mark']
		ll.no = form.cleaned_data['no']
		ll.huchin_chadal = form.cleaned_data['huchin_chadal']
		ll.daats = form.cleaned_data['daats']
		ll.gerchilgee_picture = form.cleaned_data['gerchilgee_picture']
		ll.gereet_too = form.cleaned_data['gereet_too']
		ll.duudlaga_too = form.cleaned_data['duudlaga_too']
		ll.niiluuleh_tseg = form.cleaned_data['niiluuleh_tseg']
		ll.avtomashin_tevsh = form.cleaned_data['avtomashin_tevsh']
		ll.daatgal = form.cleaned_data['daatgal']
		ll.created_by=jsonpickle.decode(user)
		ll.status= True
		ll.save()
		bohircar_history_writing(ll)
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	def equipmentform_form_valid(self, form):
		user = self.request.session['user']
		ll = Equipment(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
		ll.name = form.cleaned_data['name']
		ll.torol_id = form.cleaned_data['torol_id']
		ll.too = form.cleaned_data['too']
		ll.huchin_chadal = form.cleaned_data['huchin_chadal']
		ll.elegdliin_chanar = form.cleaned_data['elegdliin_chanar']
		ll.ashiglaltand_orson_ognoo = form.cleaned_data['ashiglaltand_orson_ognoo']
		ll.balans_une = form.cleaned_data['balans_une']
		ll.hurimtlagdsan_elegdel = form.cleaned_data['hurimtlagdsan_elegdel']
		ll.elegdel_huvi = form.cleaned_data['elegdel_huvi']
		ll.eh_uusver = form.cleaned_data['eh_uusver']
		ll.status= True
		ll.created_by=jsonpickle.decode(user)
		ll.save()
		equipment_history_writing(ll)
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	def zdtform_form_valid(self, form):
		zdt(self, form)
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	def hangagchbaiguullagaform_form_valid(self, form):
		hangagch(self, form)
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	def taxtodorhoiloltform_form_valid(self, form):
		tax(self, form)
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	def auditdugneltform_form_valid(self, form):
		audit(self, form)
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	def normstandartform_form_valid(self, form):
		norm(self, form)
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	def ulsiinaktform_form_valid(self, form):
		ulsiinakt(self, form)
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	def uszuvshuurulform_form_valid(self, form):
		uszuvshuurul(self, form)
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	def orontooform_form_valid(self, form):
		orontoo(self, form)
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	def sanhuutailanform_form_valid(self, form):
		sanhuu(self, form)
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	def abbform_form_valid(self, form):
		abb(self, form)
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)

	def uildvertechnologyform_form_valid(self, form):
		uildvertechnology(self, form)
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	def mergejliinhyanaltform_form_valid(self, form):
		mergejliinhyanalt(self, form)
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	def ajliinbairform_form_valid(self, form):
		ajliinbair(self, form)
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	
	def huselt_tsutslahform_form_valid(self, form):	# TZE huseltiig tsutslah tohioldold
		huselt_id = self.request.POST.get('huselt_id')
		tz_huselt = TZ_Huselt.objects.get(id = huselt_id)
		tsutslagdsan = TZ_huselt_yavts.objects.get(yavts_name = 'цуцлагдсан')
		tz_huselt.yavts = tsutslagdsan # huseltiin yavtsiig tsutslagdsan bolgoj solij baina
		tz_huselt.save()

		medegdel = TZ_medegdel.objects.create(tz_huselt = tz_huselt, datetime = datetime.datetime.now(), message = 'Хүсэлтийг компани цуцалсан.')
		medegdel.save()
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)

	def huselt_editform_form_valid(self, form): # TZE huseltiin zaaltiig solih tohioldold
		huselt_id = self.request.POST.get('huselt_id')
		zaaltuud_choices = self.request.POST.getlist('zaalt')	# formoos songoson zaaltuud

		tz_huselt = TZ_Huselt.objects.get(id = huselt_id)

		if zaaltuud_choices:	# if zaaltuud choices not empty
			if tz_huselt.yavts.yavts_name == u'материал бүрдүүлэлт':
				burdel = Burdel.objects.get(tz_huselt = tz_huselt)
				changed = False
				all_tzs = burdel.tz.all()
				if len(all_tzs) == len(zaaltuud_choices):	# tz-iin songoltiin too taaraad
					for z in all_tzs:
						if not z.tz in zaaltuud_choices:	# tz zaalt songolt dotor baihgui baival
							changed = True 					# zaalt oorchlogdson gesen ug
							break
				else: # songoltiin too taarahgui bol 
					changed = True 	# oorchlogdson gesen ug

				if changed:	# oorchlogdson tohioldold
					burdel.materialiud_list.tz_materialiud.all().delete() # buh tz_materialiud listiig ustgaj baina
					idtemp = burdel.materialiud_list.id
					materials = material_names(zaaltuud_choices)	# zaaltuudiin songoltoos hamaaran burduuleh materialuudaa songoj baina
					materialiud_list = materialiud_list_function(self.request, burdel.tze, materials) # burduuleh materialiudiin statusiig baiguullagiin medeellees hamaaran todorhoiloh function
					e = TZ_material_list.objects.get(id = idtemp)
					e.burdel_set.remove(burdel)
					burdel.materialiud_list = materialiud_list				

					burdel.tz.clear()	# buh zaaltuudiig arilgana
					for z in zaaltuud_choices:
						#print z
						tzzzz = TZ.objects.get(tz = z)
						burdel.tz.add(tzzzz)
					burdel.save()
					
					e.delete()
					medegdel = TZ_medegdel.objects.create(tz_huselt = tz_huselt, datetime = datetime.datetime.now(), message = 'Хүсэлтийн заалтуудад өөрчлөлт оруулсан.')
					medegdel.save()
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)

			


	def huselt_ilgeehform_form_valid(self, form):	# TZE huseltiig ilgeeh tohioldold
		huselt_id = self.request.POST.get('huselt_id')
		tz_huselt = TZ_Huselt.objects.get(id = huselt_id)
		ilgeegdsen = TZ_huselt_yavts.objects.get(yavts_name = 'хүсэлт илгээгдсэн')
		tz_huselt.yavts = ilgeegdsen # huseltiin yavtsiig tsutslagdsan bolgoj solij baina
		tz_huselt.ilgeesen_datetime = timezone.now()	# ilgeesen hugatsaag temdeglene
		tz_huselt.save()
		# burdeliiin medeelel burdel_history-d oroh yostoi
		burdel = Burdel.objects.get(tz_huselt = tz_huselt) # tuhain huselted hargalzah tsoriin gants burdel
		tze_history = TZE_history.objects.get(tze = burdel.tze, begin_time = burdel.tze.begin_time)
		burdel_history = Burdel_history.objects.create(tz_huselt = tz_huselt, tze = tze_history, materialiud_list = burdel.materialiud_list, ilgeesen_datetime = datetime.datetime.now())
		burdel_history.tz = burdel.tz.all()
		burdel_history.save()
		# burdeliiin medeelel burdel_history-d orson. Nemeh shaardlagatai

		medegdel = TZ_medegdel.objects.create(tz_huselt = tz_huselt, datetime = datetime.datetime.now(), message = 'Хүсэлтийг зохицуулах зөвлөл рүү илгээсэн.', created_by = self.__user)
		medegdel.save()

		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)
	
	def huseltform_form_valid(self, form):	# huselt shineer uuseh form
		baiguullaga_name = self.request.POST.get('baiguullaga')	# baiguullagiin ner
		zaaltuud_choices = self.request.POST.getlist('zaalt')	# formoos songoson zaaltuud
		baiguullaga = TZE.objects.get(org_name = baiguullaga_name) # baiguullaga
		yavts = TZ_huselt_yavts.objects.get(yavts_name = 'материал бүрдүүлэлт') # хүсэлтийн анхны статус
		h = TZ_Huselt.objects.create(tze=baiguullaga, yavts = yavts)
		h.created_by = self.__user
		h.begin_time = timezone.now()
		h.save()	# huselt uusne

		medegdel = TZ_medegdel.objects.create(tz_huselt = h, datetime = datetime.datetime.now(), message = 'Хүсэлт үүсэв.', created_by = self.__user)
		medegdel.save()

		materials = material_names(zaaltuud_choices)	# zaaltuudiin songoltoos hamaaran burduuleh materialuudaa songoj baina
		materialiud_list = materialiud_list_function(self.request, baiguullaga, materials) # burduuleh materialiudiin statusiig baiguullagiin medeellees hamaaran todorhoiloh function


		b = Burdel.objects.create(tz_huselt = h, tze = baiguullaga) # Burdel tuhain huselted gantshan baina
		b.materialiud_list = materialiud_list
		b.save()
		
		for z in zaaltuud_choices:
			tzzzz = TZ.objects.get(tz = z)
			b.tz.add(tzzzz)
			# end zaaltuudaa ashiglan burdeliig uusgene
		
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)



	def hunii_nootsform_form_valid(self, form):
		ajilchid_ids = self.request.POST.getlist('ajilchin') # form deer boglogdson ajilchdiin id-uudiig avna
		huselt_id = self.request.POST.get('huselt_id') # huseltiin id
		huselt = TZ_Huselt.objects.get(id = huselt_id) # huselt
		burdel = Burdel.objects.get(tz_huselt = huselt)	# tuhain huselted hargalzah burdel
		baig_ajilchid = Ajiltan.objects.filter(baiguullaga = self.request.POST.get('baiguullaga_id'), status = True) # baiguullagiin buh ajilchid
		burdel.ajiltans.clear()
		for i in ajilchid_ids:
			a = baig_ajilchid.get(id = i) # baiguullagiin buh ajilchdaas songoson ajilching avna
			burdel.ajiltans.add(a) # burdeld nemj ogno

		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)

	def zdt_burdel_bind_form_form_valid(self, form):
		zdt_ids = self.request.POST.getlist('zdt_ids')
		huselt_id = self.request.POST.get('huselt_id')
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		baig_zdts = ZDTodorhoilolt.objects.filter(tze = self.request.POST.get('baiguullaga_id'), status = True)
		burdel.zasag_dargiin_todorhoilolts.clear()
		for i in zdt_ids:
			a = baig_zdts.get(id = i)
			burdel.zasag_dargiin_todorhoilolts.add(a)

		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)

	def han_burdel_bind_form_form_valid(self, form):
		han_ids = self.request.POST.getlist('hangagch_baiguullaga_geree')
		huselt_id = self.request.POST.get('huselt_id')
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		baig_hans = HangagchBaiguullaga.objects.filter(tze = self.request.POST.get('baiguullaga_id'), status = True)
		burdel.hangagch_baigs.clear()
		for i in han_ids:
			a = baig_hans.get(id = i)
			burdel.hangagch_baigs.add(a)
			
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)

	def tax_burdel_bind_form_form_valid(self, form):
		tax_ids = self.request.POST.getlist('tax_todorhoilolt_ids')
		huselt_id = self.request.POST.get('huselt_id')
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		baig_taxs = HangagchBaiguullaga.objects.filter(tze = self.request.POST.get('baiguullaga_id'), status = True)
		burdel.tax_tods.clear()
		for i in tax_ids:
			a = baig_taxs.get(id = i)
			burdel.tax_tods.add(a)
			
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)

	def sanhuuTailan_burdel_bind_form_form_valid(self, form):
		sanhuu_tailans = self.request.POST.getlist('sanhuu_tailan_ids')
		huselt_id = self.request.POST.get('huselt_id')
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		baig_sanhuu_tailans = SanhuuTailan.objects.filter(tze = self.request.POST.get('baiguullaga_id'), status = True)
		burdel.sanhuu_tailans.clear()
		for i in sanhuu_tailans:
			a = baig_sanhuu_tailans.get(id = i)
			burdel.sanhuu_tailans.add(a)
			
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)

	def audit_dugnelt_burdel_bind_form_form_valid(self, form):
		audit_dugnelt_ids = self.request.POST.getlist('audit_dugnelt_ids')
		huselt_id = self.request.POST.get('huselt_id')
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		baig_audit_dugnelts = AuditDugnelt.objects.filter(tze = self.request.POST.get('baiguullaga_id'), status = True)
		burdel.audit_dugnelts.clear()
		for i in audit_dugnelt_ids:
			a = baig_audit_dugnelts.get(id = i)
			burdel.audit_dugnelts.add(a)
			
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)

	def oron_toonii_schemas_burdel_bind_form_form_valid(self, form):
		oron_toonii_schema_ids = self.request.POST.getlist('oron_toonii_schema_ids')
		huselt_id = self.request.POST.get('huselt_id')
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		baig_alls = OronTooniiSchema.objects.filter(tze = self.request.POST.get('baiguullaga_id'), status = True)
		burdel.oron_toonii_schemas.clear()
		for i in oron_toonii_schema_ids:
			a = baig_alls.get(id = i)
			burdel.oron_toonii_schemas.add(a)
			
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)

	def norm_standarts_burdel_bind_form_form_valid(self, form):
		norm_standart_ids = self.request.POST.getlist('norm_standart_ids')
		huselt_id = self.request.POST.get('huselt_id')
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		baig_alls = NormStandart.objects.filter(tze = self.request.POST.get('baiguullaga_id'), status = True)
		burdel.oron_toonii_schemas.clear()
		for i in norm_standart_ids:
			a = baig_alls.get(id = i)
			burdel.oron_toonii_schemas.add(a)
			
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)

	def ulsiin_komis_akt_burdel_bind_form_form_valid(self, form):
		ulsiin_komis_ids = self.request.POST.getlist('ulsiin_komis_ids')
		huselt_id = self.request.POST.get('huselt_id')
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		baig_alls = UlsiinAkt.objects.filter(tze = self.request.POST.get('baiguullaga_id'), status = True)
		burdel.ulsiin_komis_akts.clear()
		for i in ulsiin_komis_ids:
			a = baig_alls.get(id = i)
			burdel.ulsiin_komis_akts.add(a)
			
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)

	def us_ashiglah_zovshoorol_burdel_bind_form_form_valid(self, form):
		us_zovshoorol_ids = self.request.POST.getlist('us_zovshoorol_ids')
		huselt_id = self.request.POST.get('huselt_id')
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		baig_alls = UsZuvshuurul.objects.filter(tze = self.request.POST.get('baiguullaga_id'), status = True)
		burdel.us_ashiglah_zovshoorols.clear()
		for i in us_zovshoorol_ids:
			a = baig_alls.get(id = i)
			burdel.us_ashiglah_zovshoorols.add(a)
			
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)

	def uildver_tech_schemas_burdel_bind_form_form_valid(self, form):
		uildver_schema_ids = self.request.POST.getlist('uildver_schema_ids')
		huselt_id = self.request.POST.get('huselt_id')
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		baig_alls = UildverTechnology.objects.filter(tze = self.request.POST.get('baiguullaga_id'), status = True)
		burdel.uildver_tech_schemas.clear()
		for i in uildver_schema_ids:
			a = baig_alls.get(id = i)
			burdel.uildver_tech_schemas.add(a)
			
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)

	def mheg_dugnelt_burdel_bind_form_form_valid(self, form):
		mheg_dugnelt_ids = self.request.POST.getlist('mheg_dugnelt_ids')
		huselt_id = self.request.POST.get('huselt_id')
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		baig_alls = MergejliinHyanalt.objects.filter(tze = self.request.POST.get('baiguullaga_id'), status = True)
		burdel.mheg_dugnelts.clear()
		for i in mheg_dugnelt_ids:
			a = baig_alls.get(id = i)
			burdel.mheg_dugnelts.add(a)
			
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)

	def ajliin_bair_dugnelts_burdel_bind_form_form_valid(self, form):
		ajliinbair_dugnelt_ids = self.request.POST.getlist('ajliinbair_dugnelt_ids')
		huselt_id = self.request.POST.get('huselt_id')
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		baig_alls = AjliinBair.objects.filter(tze = self.request.POST.get('baiguullaga_id'), status = True)
		burdel.ajliin_bair_dugnelts.clear()
		for i in ajliinbair_dugnelt_ids:
			a = baig_alls.get(id = i)
			burdel.ajliin_bair_dugnelts.add(a)
			
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)

	def mashin_TT_burdel_bind_form_form_valid(self, form):
		mashin_TT_ids = self.request.POST.getlist('mashin_TT_ids')
		huselt_id = self.request.POST.get('huselt_id')
		huselt = TZ_Huselt.objects.get(id = huselt_id)
		burdel = Burdel.objects.get(tz_huselt = huselt)
		baig_alls = Equipment.objects.filter(tze = self.request.POST.get('baiguullaga_id'), status = True)
		burdel.mashin_tonog_tohooromjs.clear()
		for i in mashin_TT_ids:
			a = baig_alls.get(id = i)
			burdel.mashin_tonog_tohooromjs.add(a)
			
		return super(Tusgai_zovshoorolView, self).forms_valid(form, form)

###################################### UILSEE CODE END ##############################################
def us_tugeeh_history_writing(us_tugeeh_bair):
	history_new = UsTugeehBairHistory(bb = us_tugeeh_bair)
	history_new.tze = us_tugeeh_bair.tze
	history_new.huchin_chadal = us_tugeeh_bair.huchin_chadal
	history_new.ashiglaltand_orson_ognoo = us_tugeeh_bair.ashiglaltand_orson_ognoo
	history_new.tailbar = us_tugeeh_bair.tailbar
	history_new.barilga = us_tugeeh_bair.barilga
	history_new.tze = us_tugeeh_bair.tze
	history_new.dugaar = us_tugeeh_bair.dugaar
	history_new.ustugeeh_aimag = us_tugeeh_bair.ustugeeh_aimag
	history_new.ustugeeh_sum = us_tugeeh_bair.ustugeeh_sum
	history_new.ustugeeh_bag = us_tugeeh_bair.ustugeeh_bag
	history_new.ustugeeh_address = us_tugeeh_bair.ustugeeh_address
	history_new.ustugeeh_sav = us_tugeeh_bair.ustugeeh_sav
	history_new.savnii_bagtaamj = us_tugeeh_bair.savnii_bagtaamj
	history_new.borluulj_bui_us = us_tugeeh_bair.borluulj_bui_us
	history_new.hun_amiin_too = us_tugeeh_bair.hun_amiin_too
	history_new.gadna_tal_picture = str(us_tugeeh_bair.gadna_tal_picture)
	history_new.dotor_tal_picture = str(us_tugeeh_bair.dotor_tal_picture)

	try:
		history = UsTugeehBairHistory.objects.get(bb = us_tugeeh_bair, begin_time = us_tugeeh_bair.begin_time)
	except ObjectDoesNotExist:
		history_new.status = us_tugeeh_bair.status
		history_new.created_by = us_tugeeh_bair.created_by
		us_tugeeh_bair.begin_time = timezone.now()
		history_new.begin_time = us_tugeeh_bair.begin_time

		us_tugeeh_bair.save()
		history_new.save()
		return 1

	history_new.status = us_tugeeh_bair.status
	history_new.created_by = us_tugeeh_bair.created_by
	us_tugeeh_bair.begin_time = timezone.now()
	history_new.begin_time = us_tugeeh_bair.begin_time

	history.end_time = us_tugeeh_bair.begin_time

	us_tugeeh_bair.save()
	history.save()
	history_new.save()
	return 0

def bohircar_history_writing(bohir_car):
	history_new = BohirCarHistory(car = bohir_car)
	history_new.mark = bohir_car.mark
	history_new.tze = bohir_car.tze
	history_new.no = bohir_car.no
	history_new.huchin_chadal = bohir_car.huchin_chadal
	history_new.daats = bohir_car.daats
	history_new.gerchilgee_picture = bohir_car.gerchilgee_picture
	history_new.gereet_too = bohir_car.gereet_too
	history_new.duudlaga_too = bohir_car.duudlaga_too
	history_new.niiluuleh_tseg = bohir_car.niiluuleh_tseg
	history_new.avtomashin_tevsh = bohir_car.avtomashin_tevsh
	history_new.daatgal = bohir_car.daatgal

	try:
		history = BohirCarHistory.objects.get(car = bohir_car, begin_time = bohir_car.begin_time)
	except ObjectDoesNotExist:
		history_new.status = bohir_car.status
		history_new.created_by = bohir_car.created_by
		bohir_car.begin_time = timezone.now()
		history_new.begin_time = bohir_car.begin_time

		bohir_car.save()
		history_new.save()
		return 1

	history_new.status = bohir_car.status
	history_new.created_by = bohir_car.created_by
	bohir_car.begin_time = timezone.now()
	history_new.begin_time = bohir_car.begin_time
	history.end_time = bohir_car.begin_time
	bohir_car.save()
	return 0

def watercar_history_writing(water_car):
	history_new = WaterCarHistory(car = water_car)
	history_new.mark = water_car.mark
	history_new.tze = water_car.tze
	history_new.no = water_car.no
	history_new.huchin_chadal = water_car.huchin_chadal
	history_new.daats = water_car.daats
	history_new.gerchilgee_picture = water_car.gerchilgee_picture
	history_new.hun_am_too = water_car.hun_am_too
	history_new.utb_too = water_car.utb_too
	history_new.aanb_too = water_car.aanb_too

	try:
		history = WaterCarHistory.objects.get(car = water_car, begin_time = water_car.begin_time)
	except ObjectDoesNotExist:
		history_new.status = water_car.status
		history_new.created_by = water_car.created_by
		water_car.begin_time = timezone.now()
		history_new.begin_time = water_car.begin_time

		water_car.save()
		history_new.save()
		return 1

	history_new.status = water_car.status
	history_new.created_by = water_car.created_by
	water_car.begin_time = timezone.now()
	history_new.begin_time = water_car.begin_time
	history.end_time = water_car.begin_time
	water_car.save()
	return 0

def us_damjuulah_history_writing(us_damjuulah):
	history_new = UsDamjuulahBairHistory(bb = us_damjuulah)
	history_new.ashiglaltand_orson_ognoo = us_damjuulah.ashiglaltand_orson_ognoo
	history_new.tze = us_damjuulah.tze
	history_new.tovlorson = us_damjuulah.tovlorson
	history_new.bairiiin_uzeli = us_damjuulah.bairiiin_uzeli
	history_new.baiguulalt_holbolt_picture = us_damjuulah.baiguulalt_holbolt_picture
	history_new.picture = us_damjuulah.picture
	history_new.bair_uzeli_holbolt_schema = us_damjuulah.bair_uzeli_holbolt_schema

	try:
		history = UsDamjuulahBairHistory.objects.get(bb = us_damjuulah, begin_time = us_damjuulah.begin_time)
	except ObjectDoesNotExist:
		history_new.status = us_damjuulah.status
		history_new.created_by = us_damjuulah.created_by
		us_damjuulah.begin_time = timezone.now()
		history_new.begin_time = us_damjuulah.begin_time

		us_damjuulah.save()
		history_new.save()
		return 1

	history_new.status = us_damjuulah.status
	history_new.created_by = us_damjuulah.created_by
	us_damjuulah.begin_time = timezone.now()
	history_new.begin_time = us_damjuulah.begin_time
	history.end_time = us_damjuulah.begin_time
	us_damjuulah.save()
	return 0
		
def equipment_history_writing(equipment):
	history_new = EquipmentHistory(equipment = equipment)
	history_new.name = equipment.name
	history_new.tze = equipment.tze
	history_new.torol_id = equipment.torol_id
	history_new.too = equipment.too
	history_new.huchin_chadal = equipment.huchin_chadal
	history_new.elegdliin_chanar = equipment.elegdliin_chanar
	history_new.ashiglaltand_orson_ognoo = equipment.ashiglaltand_orson_ognoo
	history_new.balans_une = equipment.balans_une
	history_new.hurimtlagdsan_elegdel = equipment.hurimtlagdsan_elegdel
	history_new.elegdel_huvi = equipment.elegdel_huvi
	history_new.eh_uusver = equipment.eh_uusver

	try:
		history = EquipmentHistory.objects.get(equipment = equipment, begin_time = equipment.begin_time)
	except ObjectDoesNotExist:
		history_new.status = equipment.status
		history_new.created_by = equipment.created_by
		equipment.begin_time = timezone.now()
		history_new.begin_time = equipment.begin_time

		equipment.save()
		history_new.save()
		return 1

	history_new.status = equipment.status
	history_new.created_by = equipment.created_by
	equipment.begin_time = timezone.now()
	history_new.begin_time = equipment.begin_time
	history.end_time = equipment.begin_time
	equipment.save()
	return 0

def nasos_history_writing(nasos):
	history_new = NasosHistory(bb = nasos)
	history_new.tze = nasos.tze
	history_new.huchin_chadal = nasos.huchin_chadal
	history_new.ashiglaltand_orson_ognoo = nasos.ashiglaltand_orson_ognoo
	history_new.tailbar = nasos.tailbar
	history_new.nasos_torol = nasos.nasos_torol
	history_new.nasos_name = nasos.nasos_name
	history_new.nasos_aimag = nasos.nasos_aimag
	history_new.nasos_sum = nasos.nasos_sum
	history_new.nasos_bag = nasos.nasos_bag
	history_new.nasos_address = nasos.nasos_address
	history_new.too_hemjee = nasos.too_hemjee
	history_new.nasos_ajillagaa = nasos.nasos_ajillagaa
	history_new.zarchmiin_schema = str(nasos.zarchmiin_schema)
	history_new.zarchmiin_picture = str(nasos.zarchmiin_picture)

	try:
		history = NasosHistory.objects.get(bb = nasos, begin_time = nasos.begin_time)
	except ObjectDoesNotExist:
		history_new.status = nasos.status
		history_new.created_by = nasos.created_by
		nasos.begin_time = timezone.now()
		history_new.begin_time = nasos.begin_time

		nasos.save()
		history_new.save()
		return 1

	history_new.status = nasos.status
	history_new.created_by = nasos.created_by
	nasos.begin_time = timezone.now()
	history_new.begin_time = nasos.begin_time

	history.end_time = nasos.begin_time

	nasos.save()

	history.save()
	history_new.save()
	return 0

def lab_history_writing(lab):
	history_new = LabHistory(bb = lab)
	history_new.tze = lab.tze
	history_new.huchin_chadal = lab.huchin_chadal
	history_new.ashiglaltand_orson_ognoo = lab.ashiglaltand_orson_ognoo
	history_new.tailbar = lab.tailbar
	history_new.tsever = lab.tsever
	history_new.bohir = lab.bohir
	history_new.eronhii_hatuulag = lab.eronhii_hatuulag
	history_new.kalitsi = lab.kalitsi
	history_new.magni = lab.magni
	history_new.hlorid = lab.hlorid
	history_new.sulifat = lab.sulifat
	history_new.fosfat = lab.fosfat
	history_new.ammiak = lab.ammiak
	history_new.nitrit = lab.nitrit
	history_new.nitrat = lab.nitrat
	history_new.tomor = lab.tomor
	history_new.ftor = lab.ftor
	history_new.ongo = lab.ongo
	history_new.amt = lab.amt
	history_new.uner = lab.uner
	history_new.pH = lab.pH
	history_new.huurai_uld = lab.huurai_uld
	history_new.iseldelt = lab.iseldelt
	history_new.natri = lab.natri
	history_new.kali = lab.kali
	history_new.gidrocarbonat = lab.gidrocarbonat
	history_new.uldegdel_hlor = lab.uldegdel_hlor
	history_new.niit_hlor = lab.niit_hlor
	history_new.niit_shultleg = lab.niit_shultleg
	history_new.us_tem = lab.us_tem
	history_new.ustorogch = lab.ustorogch
	history_new.unermed = lab.unermed
	history_new.jinlegdeh = lab.jinlegdeh
	history_new.biohimi = lab.biohimi
	history_new.himiin_herertseet = lab.himiin_herertseet
	history_new.permanganat = lab.permanganat
	history_new.uussan_davs = lab.uussan_davs
	history_new.ammoniin_azot = lab.ammoniin_azot
	history_new.niitazot = lab.niitazot
	history_new.niitfosfor = lab.niitfosfor
	history_new.orgfosfor = lab.orgfosfor
	history_new.huhertus = lab.huhertus
	history_new.niittomor = lab.niittomor
	history_new.hongontsagaan = lab.hongontsagaan
	history_new.mangan = lab.mangan
	history_new.niithrom = lab.niithrom
	history_new.zurgaavalenttaihrom = lab.zurgaavalenttaihrom
	history_new.niittsianit = lab.niittsianit
	history_new.choloottsianit = lab.choloottsianit
	history_new.zes = lab.zes
	history_new.bor = lab.bor
	history_new.hartugalga = lab.hartugalga
	history_new.tsair = lab.tsair
	history_new.kadmii = lab.kadmii
	history_new.tsagaantugalga = lab.tsagaantugalga
	history_new.mongonus = lab.mongonus
	history_new.molibden = lab.molibden
	history_new.niithuntsel = lab.niithuntsel
	history_new.nikeli = lab.nikeli
	history_new.selen = lab.selen
	history_new.binder = lab.binder
	history_new.kobalit = lab.kobalit
	history_new.bari = lab.bari
	history_new.strontsi = lab.strontsi
	history_new.vanadii = lab.vanadii
	history_new.uran = lab.uran
	history_new.erdestos = lab.erdestos
	history_new.oohtos = lab.oohtos
	history_new.gadarguunidevhjil = lab.gadarguunidevhjil
	history_new.fenol = lab.fenol
	history_new.trihloretilen = lab.trihloretilen
	history_new.tetrahloretilen = lab.tetrahloretilen
	history_new.uldegdelbodis = lab.uldegdelbodis
	history_new.gedes = lab.gedes

	try:
		history = LabHistory.objects.get(bb = lab, begin_time = lab.begin_time)
	except ObjectDoesNotExist:
		history_new.status = lab.status
		history_new.created_by = lab.created_by
		lab.begin_time = timezone.now()
		history_new.begin_time = lab.begin_time
		lab.save()
		history_new.save()
		return 1

	history_new.status = lab.status
	history_new.created_by = lab.created_by
	lab.begin_time = timezone.now()
	history_new.begin_time = lab.begin_time
	lab.save()
	history_new.save()
	history.end_time = nasos.begin_time
	history.save()
	return 0

def hudag_history_writing(hudag):
	history_new= HudagHistory(bb = hudag)
	history_new.tze = hudag.tze
	history_new.huchin_chadal = hudag.huchin_chadal
	history_new.ashiglaltand_orson_ognoo = hudag.ashiglaltand_orson_ognoo
	history_new.tailbar = hudag.tailbar
	history_new.olborloj_bui_us=hudag.olborloj_bui_us
	history_new.haruul =hudag.haruul
	history_new.tsoonog= hudag.tsoonog

	history_new.status=hudag.status
	history_new.created_by=hudag.created_by

	try:
		history = HudagHistory.objects.get(bb = hudag, begin_time = hudag.begin_time)
	except ObjectDoesNotExist:
		hudag.begin_time = timezone.now()
		history_new.begin_time = hudag.begin_time
		hudag.save()
		history_new.save()
		return 1

	hudag.begin_time = timezone.now()
	history_new.begin_time = hudag.begin_time
	history.end_time = hudag.begin_time
	hudag.save()
	history.save()
	history_new.save()
	return 0

def ts_baiguulamj_history_writing(ts_baig):
	history_new= Ts_baiguulamjHistory(bb = ts_baig)
	history_new.tze = ts_baig.tze
	history_new.huchin_chadal = ts_baig.huchin_chadal
	history_new.ashiglaltand_orson_ognoo = ts_baig.ashiglaltand_orson_ognoo
	history_new.tailbar = ts_baig.tailbar
	history_new.mehanik=ts_baig.mehanik
	history_new.biologi =ts_baig.biologi
	history_new.fizik= ts_baig.fizik
	history_new.technology_schema = str(ts_baig.technology_schema)

	history_new.status=ts_baig.status
	history_new.created_by=ts_baig.created_by

	try:
		history = Ts_baiguulamjHistory.objects.get(bb = ts_baig, begin_time = ts_baig.begin_time)
	except ObjectDoesNotExist:
		ts_baig.begin_time = timezone.now()
		history_new.begin_time = ts_baig.begin_time
		ts_baig.save()
		history_new.save()
		return 1

	ts_baig.begin_time = timezone.now()
	history_new.begin_time = ts_baig.begin_time
	history.end_time = ts_baig.begin_time
	ts_baig.save()
	history.save()
	history_new.save()
	return 0

def sh_suljee_history_writing(suljee):
	history_new= Sh_suljeeHistory(bb = suljee)
	history_new.tze = suljee.tze
	history_new.huchin_chadal = suljee.huchin_chadal
	history_new.ashiglaltand_orson_ognoo = suljee.ashiglaltand_orson_ognoo
	history_new.tailbar = suljee.tailbar
	history_new.shugam_helber=suljee.shugam_helber
	history_new.shugam_torol =suljee.shugam_torol
	history_new.shugam_urt= suljee.shugam_urt
	history_new.diametr= suljee.diametr
	history_new.hudgiin_too= suljee.hudgiin_too
	history_new.gemtliin_too= suljee.gemtliin_too
	history_new.schema = str(suljee.schema)

	history_new.status=suljee.status
	history_new.created_by=suljee.created_by

	try:
		history = Sh_suljeeHistory.objects.get(bb = suljee, begin_time = suljee.begin_time)
	except ObjectDoesNotExist:
		suljee.begin_time = timezone.now()
		history_new.begin_time = suljee.begin_time
		suljee.save()
		history_new.save()
		return 1

	suljee.begin_time = timezone.now()
	history_new.begin_time = suljee.begin_time
	history.end_time = suljee.begin_time
	suljee.save()
	history.save()
	history_new.save()
	return 0

def usan_san_history_writing(usansan):
	history_new= UsanSanHistory(bb = usansan)
	history_new.tze = usansan.tze
	history_new.huchin_chadal = usansan.huchin_chadal
	history_new.ashiglaltand_orson_ognoo = usansan.ashiglaltand_orson_ognoo
	history_new.tailbar = usansan.tailbar
	history_new.usansan_helber=usansan.usansan_helber
	history_new.ner =usansan.ner
	history_new.usansan_aimag= usansan.usansan_aimag
	history_new.usansan_sum= usansan.usansan_sum
	history_new.usansan_bag= usansan.usansan_bag
	history_new.usansan_address= usansan.usansan_address
	history_new.bagtaamj= usansan.bagtaamj
	history_new.huurai_hlor= usansan.huurai_hlor
	history_new.shingen_hlor= usansan.shingen_hlor
	history_new.davsnii_uusmal= usansan.davsnii_uusmal
	history_new.usansan_haruul= usansan.usansan_haruul
	history_new.bairshiliin_schema = str(usansan.bairshiliin_schema)
	history_new.bairshiliin_photo = str(usansan.bairshiliin_photo)

	history_new.status=usansan.status
	history_new.created_by=usansan.created_by

	try:
		history = UsanSanHistory.objects.get(bb = usansan, begin_time = usansan.begin_time)
	except ObjectDoesNotExist:
		usansan.begin_time = timezone.now()
		history_new.begin_time = usansan.begin_time
		usansan.save()
		history_new.save()
		return 1

	usansan.begin_time = timezone.now()
	history_new.begin_time = usansan.begin_time
	history.end_time = usansan.begin_time
	usansan.save()
	history.save()
	history_new.save()
	return 0

class TohooromjjView(LoginRequired,MultiFormsView):
	form_classes = {
	'hudagzuragform':HudagNegtsgesenBairshliinZuragForm,
	'hudagnegdsen':HudagNegdsenForm,
    'edit_hudagform': edit_guniihudagForm,
	'nasosform': NasosForm,
	'labform': LabForm,
	'sh_suljeeform': Sh_suljeeForm,
	'ts_baiguulamjform': Ts_baiguulamjForm,
	'usansanform': UsanSanForm,
	'usdamjuulahbairform': UsDamjuulahBairForm,
	'ustugeehbairform': UsTugeehBairForm,
	'watercarform': WaterCarForm,
	'bohircarform': BohirCarForm,
	'equipmentform':EquipmentForm,
	}
	template_name = "tohooromj.html"
	success_url = '/engineering/tohooromj/'
	def get_context_data(self, **kwargs):
		context = super(TohooromjjView, self).get_context_data(**kwargs)
		#context['bb'] = BB.objects.filter(tze = context['baiguullaga'],status=True)
		#context['ehudag'] = Hudag.objects.filter(tze = context['baiguullaga'],status=True)
		#context['enasos'] = Nasos.objects.filter(tze = context['baiguullaga'],status=True)
		#context['elab'] = Lab.objects.filter(tze = context['baiguullaga'],status=True)
		#context['esuljee']= Sh_suljee.objects.filter(tze = context['baiguullaga'],status=True)
		#context['eusansan'] = UsanSan.objects.filter(tze = context['baiguullaga'],status=True)
		#context['ustugeeh']=UsTugeehBair.objects.filter(tze = context['baiguullaga'],status=True)
		#context['usdamjuulah'] =UsDamjuulahBair.objects.filter(tze = context['baiguullaga'],status=True)
		#context['ewatercar'] = WaterCar.objects.filter(tze = context['baiguullaga'],status=True)
		#context['ebohircar'] = BohirCar.objects.filter(tze = context['baiguullaga'],status=True)
		#context['car']=Car.objects.filter(tze = context['baiguullaga'],status=True)
		#context['tonog']=Equipment.objects.filter(tze = context['baiguullaga'],status=True)
		#context['tseverleh']=Ts_baiguulamj.objects.filter(tze = context['baiguullaga'],status=True)
		context['aimag'] = Aimag.objects.all()
		context['sum'] = Sum.objects.all()
		context['bag'] = Bag.objects.all()
		paginator1 = Paginator(BB.objects.filter(tze = context['baiguullaga'],status=True), 5)
		page1 = self.request.GET.get('page')
		try:
			context['bb'] = paginator1.page(page1)
		except PageNotAnInteger:
			context['bb'] = paginator1.page(1)
		except EmptyPage:
			context['bb'] = paginator1.page(paginator1.num_pages)

		paginator2 = Paginator(Hudag.objects.filter(tze = context['baiguullaga'],status=True), 5)
		page2 = self.request.GET.get('page')
		try:
			context['ehudag'] = paginator2.page(page2)
		except PageNotAnInteger:
			context['ehudag'] = paginator2.page(1)
		except EmptyPage:
			context['ehudag'] = paginator2.page(paginator2.num_pages)

		paginator3 = Paginator(Nasos.objects.filter(tze = context['baiguullaga'],status=True), 5)
		page3 = self.request.GET.get('page')
		try:
			context['enasos'] = paginator3.page(page3)
		except PageNotAnInteger:
			context['enasos'] = paginator3.page(1)
		except EmptyPage:
			context['enasos'] = paginator3.page(paginator3.num_pages)

		paginator4 = Paginator(Lab.objects.filter(tze = context['baiguullaga'],status=True), 5)
		page4 = self.request.GET.get('page')
		try:
			context['elab'] = paginator4.page(page4)
		except PageNotAnInteger:
			context['elab'] = paginator4.page(1)
		except EmptyPage:
			context['elab'] = paginator4.page(paginator4.num_pages)
			
		paginator5 = Paginator(Sh_suljee.objects.filter(tze = context['baiguullaga'],status=True), 5)
		page4 = self.request.GET.get('page')
		try:
			context['esuljee'] = paginator5.page(page4)
		except PageNotAnInteger:
			context['esuljee'] = paginator5.page(1)
		except EmptyPage:
			context['esuljee'] = paginator5.page(paginator5.num_pages)

		paginator6 = Paginator(UsanSan.objects.filter(tze = context['baiguullaga'],status=True), 5)
		page6 = self.request.GET.get('page')
		try:
			context['eusansan'] = paginator6.page(page6)
		except PageNotAnInteger:
			context['eusansan'] = paginator6.page(1)
		except EmptyPage:
			context['eusansan'] = paginator6.page(paginator6.num_pages)

		paginator7 = Paginator(UsDamjuulahBair.objects.filter(tze = context['baiguullaga'],status=True), 5)
		page7 = self.request.GET.get('page')
		try:
			context['usdamjuulah'] = paginator7.page(page7)
		except PageNotAnInteger:
			context['usdamjuulah'] = paginator7.page(1)
		except EmptyPage:
			context['usdamjuulah'] = paginator7.page(paginator7.num_pages)
			
		paginator8 = Paginator(UsTugeehBair.objects.filter(tze = context['baiguullaga'],status=True), 5)
		page8 = self.request.GET.get('page')
		try:
			context['ustugeeh'] = paginator8.page(page8)
		except PageNotAnInteger:
			context['ustugeeh'] = paginator8.page(1)
		except EmptyPage:
			context['ustugeeh'] = paginator8.page(paginator8.num_pages)	

		paginator9 = Paginator(Car.objects.filter(tze = context['baiguullaga'],status=True), 5)
		page9 = self.request.GET.get('page')
		try:
			context['car'] = paginator9.page(page9)
		except PageNotAnInteger:
			context['car'] = paginator9.page(1)
		except EmptyPage:
			context['car'] = paginator9.page(paginator9.num_pages)

		paginator10 = Paginator(WaterCar.objects.filter(tze = context['baiguullaga'],status=True), 5)
		page10 = self.request.GET.get('page')
		try:
			context['ewatercar'] = paginator10.page(page10)
		except PageNotAnInteger:
			context['ewatercar'] = paginator10.page(1)
		except EmptyPage:
			context['ewatercar'] = paginator10.page(paginator10.num_pages)
			
		paginator11 = Paginator(BohirCar.objects.filter(tze = context['baiguullaga'],status=True), 5)
		page11 = self.request.GET.get('page')
		try:
			context['ebohircar'] = paginator11.page(page11)
		except PageNotAnInteger:
			context['ebohircar'] = paginator11.page(1)
		except EmptyPage:
			context['ebohircar'] = paginator11.page(paginator11.num_pages)

		paginator11 = Paginator(Equipment.objects.filter(tze = context['baiguullaga'],status=True), 5)
		page11 = self.request.GET.get('page')
		try:
			context['tonog'] = paginator11.page(page11)
		except PageNotAnInteger:
			context['tonog'] = paginator11.page(1)
		except EmptyPage:
			context['tonog'] = paginator11.page(paginator11.num_pages)
			
		paginator12 = Paginator(Ts_baiguulamj.objects.filter(tze = context['baiguullaga'],status=True), 5)
		page12 = self.request.GET.get('page')
		try:
			context['tseverleh'] = paginator12.page(page12)
		except PageNotAnInteger:
			context['tseverleh'] = paginator12.page(1)
		except EmptyPage:
			context['tseverleh'] = paginator12.page(paginator12.num_pages)	

		paginator13 = Paginator(HudagNegtsgesenBairshliinZurag.objects.filter(tze_id = context['baiguullaga'],status=True), 5)
		page13 = self.request.GET.get('page')
		try:
			context['guniihudagnegsen'] = paginator13.page(page13)
		except PageNotAnInteger:
			context['guniihudagnegsen'] = paginator13.page(1)
		except EmptyPage:
			context['guniihudagnegsen'] = paginator13.page(paginator13.num_pages)	
		return context
	def hudagnegdsen_form_valid(self, form):
		hudag_insert_func(self, form)
		return super(TohooromjjView, self).forms_valid(form, form)
	def hudagzuragform_form_valid(self, form):
		user = self.request.session['user']
		a = HudagNegtsgesenBairshliinZurag(tze_id = TZE.objects.get(org_name = self.request.POST.get('tze')))
		a.bairshliin_picture = form.cleaned_data['bairshliin_picture']
		a.begin_time=timezone.now()
		a.created_by=jsonpickle.decode(user)
		a.status= True
		a.save()
		aa= HudagNegtsgesenBairshliinZuragHistory(hudagnegtgesenbairshliinzurag=a)
		aa.bairshliin_picture = form.cleaned_data['bairshliin_picture']
		aa.begin_time=timezone.now()
		aa.created_by=jsonpickle.decode(user)
		aa.status= True
		aa.save()
		return super(TohooromjjView, self).forms_valid(form, form)
	def nasosform_form_valid(self, form):
		nasos_insert_func(self, form)
		return super(TohooromjjView, self).forms_valid(form, form)
	def analysisform_form_valid(self, form):
		user = self.request.session['user']
		ana = Analysis(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
		ana.analysis_torol = form.cleaned_data['analysis_torol']
		ana.analysis = form.cleaned_data['analysis']
		ana.begin_time=datetime.datetime.now()
		ana.created_by=jsonpickle.decode(user)
		ana.save()
		ansa = AnalysisHistory(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
		ansa.analysis = ana
		ansa.analysis_torol = form.cleaned_data['analysis_torol']
		ansa.analysis = form.cleaned_data['analysis']
		ansa.begin_time=datetime.datetime.now()
		ansa.created_by=jsonpickle.decode(user)
		ansa.save()
		return super(TohooromjjView, self).forms_valid(form, form)
	def labform_form_valid(self, form):
		lab_insert_func(self, form)
		return super(TohooromjjView, self).forms_valid(form, form)

	def sh_suljeeform_form_valid(self, form):
		sh_suljee_insert_func(self,form)
		return super(TohooromjjView, self).forms_valid(form, form)
	def ts_baiguulamjform_form_valid(self, form):
		user = self.request.session['user']
		ee = Ts_baiguulamj(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
		ee.huchin_chadal = form.cleaned_data['huchin_chadal']
		ee.ashiglaltand_orson_ognoo = form.cleaned_data['ashiglaltand_orson_ognoo']
		ee.mehanik = form.cleaned_data['mehanik']
		ee.biologi = form.cleaned_data['biologi']
		ee.fizik = form.cleaned_data['fizik']
		ee.technology_schema = form.cleaned_data['technology_schema']
		ee.created_by=jsonpickle.decode(user)
		ee.status = True
		ee.save()
		ts_baiguulamj_history_writing(ee)
		barilga_tonog = self.request.POST.getlist('barilga_tonog')
		huchin_chadall = self.request.POST.getlist('huchin_chadall')
		too = self.request.POST.getlist('too')
		ashiglaltand_orson_ognooo = self.request.POST.getlist('ashiglaltand_orson_ognooo')
		tailbarr = self.request.POST.getlist('tailbarr')
		if len(barilga_tonog) == len(huchin_chadall) and len(huchin_chadall) == len(too) and len(too) == len(ashiglaltand_orson_ognooo) and len(ashiglaltand_orson_ognooo) == len(tailbarr) :
			for i in range(len(huchin_chadall)):
				ab=Ts_tohooromj(ts_baiguulamj=ee, barilga_tonog= barilga_tonog[i],huchin_chadall= huchin_chadall[i],too= too[i],ashiglaltand_orson_ognooo= ashiglaltand_orson_ognooo[i],tailbarr= tailbarr[i],created_by=jsonpickle.decode(user))
				ab.save()
				ad= Ts_tohooromjHistory(Ts_tohooromj=ab,barilga_tonog= barilga_tonog[i],huchin_chadall= huchin_chadall[i],too= too[i],ashiglaltand_orson_ognooo= ashiglaltand_orson_ognooo[i],tailbarr= tailbarr[i], created_by=jsonpickle.decode(user))
				ad.save()
		return super(TohooromjjView, self).forms_valid(form, form)
	def usansanform_form_valid(self, form):
		usansan_insert_func(self, form)
		return super(TohooromjjView, self).forms_valid(form, form)
	def usdamjuulahbairform_form_valid(self, form):
		user = self.request.session['user']
		gg = UsDamjuulahBair(tze=TZE.objects.get(org_name = self.request.POST.get('tze')))
		gg.ashiglaltand_orson_ognoo = form.cleaned_data['ashiglaltand_orson_ognoo']
		gg.created_by=jsonpickle.decode(user)
		gg.status= True
		gg.tovlorson= form.cleaned_data['tovlorson']
		gg.bairiiin_uzeli= form.cleaned_data['bairiiin_uzeli']
		gg.baiguulalt_holbolt_picture = form.cleaned_data['baiguulalt_holbolt_picture']
		gg.picture = form.cleaned_data['picture']
		gg.bair_uzeli_holbolt_schema = form.cleaned_data['bair_uzeli_holbolt_schema']
		gg.save()
		tonog = self.request.POST.getlist('barilga_tonog')
		huchin_chadall = self.request.POST.getlist('huchin_chadall')
		too = self.request.POST.getlist('too')
		ognoo = self.request.POST.getlist('ognoo')
		tailbarr = self.request.POST.getlist('tailbarr')
		if len(tonog) == len(huchin_chadall) and len(huchin_chadall) == len(too) and len(too) == len(ognoo) and len(ognoo) == len(tailbarr) :
			for i in range(len(huchin_chadall)):
				ab=UsDamjuulahBairTonog(us_id=gg, tze=TZE.objects.get(org_name = self.request.POST.get('tze')), tonog= tonog[i],huchin_chadall= huchin_chadall[i],too= too[i],ognoo= ognoo[i],tailbarr= tailbarr[i],created_by=jsonpickle.decode(user))
				ab.save()
				ad= UsDamjuulahBairTonogHistory(usdamjuulahbairtonog=ab, tze=TZE.objects.get(org_name = self.request.POST.get('tze')), tonog= tonog[i],huchin_chadall= huchin_chadall[i],too= too[i],ognoo= ognoo[i],tailbarr= tailbarr[i], created_by=jsonpickle.decode(user))
				ad.save()
		us_damjuulah_history_writing(gg)	# history-d hiine bas hadgalna
		return super(TohooromjjView, self).forms_valid(form, form)
	def ustugeehbairform_form_valid(self, form):
		us_tugeeh_insert_func(self, form)
		return super(TohooromjjView, self).forms_valid(form, form)
	def watercarform_form_valid(self, form):
		user = self.request.session['user']
		jj = WaterCar(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
		jj.mark = form.cleaned_data['mark']
		jj.no = form.cleaned_data['no']
		jj.huchin_chadal = form.cleaned_data['huchin_chadal']
		jj.daats = form.cleaned_data['daats']
		jj.gerchilgee_picture = form.cleaned_data['gerchilgee_picture']
		jj.hun_am_too = form.cleaned_data['hun_am_too']
		jj.utb_too = form.cleaned_data['utb_too']
		jj.aanb_too = form.cleaned_data['aanb_too']
		jj.created_by=jsonpickle.decode(user)
		jj.status= True
		jj.save()
		watercar_history_writing(jj)
		return super(TohooromjjView, self).forms_valid(form, form)
	def bohircarform_form_valid(self, form):
		user = self.request.session['user']
		ll = BohirCar(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
		ll.mark = form.cleaned_data['mark']
		ll.no = form.cleaned_data['no']
		ll.huchin_chadal = form.cleaned_data['huchin_chadal']
		ll.daats = form.cleaned_data['daats']
		ll.gerchilgee_picture = form.cleaned_data['gerchilgee_picture']
		ll.gereet_too = form.cleaned_data['gereet_too']
		ll.duudlaga_too = form.cleaned_data['duudlaga_too']
		ll.niiluuleh_tseg = form.cleaned_data['niiluuleh_tseg']
		ll.avtomashin_tevsh = form.cleaned_data['avtomashin_tevsh']
		ll.daatgal = form.cleaned_data['daatgal']
		ll.created_by=jsonpickle.decode(user)
		ll.status= True
		ll.save()
		bohircar_history_writing(ll)
		return super(TohooromjjView, self).forms_valid(form, form)
	def equipmentform_form_valid(self, form):
		user = self.request.session['user']
		ll = Equipment(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
		ll.name = form.cleaned_data['name']
		ll.torol_id = form.cleaned_data['torol_id']
		ll.too = form.cleaned_data['too']
		ll.huchin_chadal = form.cleaned_data['huchin_chadal']
		ll.elegdliin_chanar = form.cleaned_data['elegdliin_chanar']
		ll.ashiglaltand_orson_ognoo = form.cleaned_data['ashiglaltand_orson_ognoo']
		ll.balans_une = form.cleaned_data['balans_une']
		ll.hurimtlagdsan_elegdel = form.cleaned_data['hurimtlagdsan_elegdel']
		ll.elegdel_huvi = form.cleaned_data['elegdel_huvi']
		ll.eh_uusver = form.cleaned_data['eh_uusver']
		ll.status= True
		ll.created_by=jsonpickle.decode(user)
		ll.save()
		equipment_history_writing(ll)
		return super(TohooromjjView, self).forms_valid(form, form)

def ajiltan_history_writing(ajiltan):
	try:
		ajiltan_history = AjiltanHistory.objects.get(ajiltan = ajiltan, begin_time = ajiltan.begin_time)
	except ObjectDoesNotExist:
		ajiltan_history = AjiltanHistory.objects.create(baiguullaga = ajiltan.baiguullaga, ajiltan = ajiltan, position_id = ajiltan.position_id, mer_zereg = ajiltan.mer_zereg)
		ajiltan_history.emp_lname = ajiltan.emp_lname
		ajiltan_history.emp_name = ajiltan.emp_name
		ajiltan_history.emp_reg = ajiltan.emp_reg
		ajiltan_history.picture = ajiltan.picture
		ajiltan_history.emp_birth = ajiltan.emp_birth
		ajiltan_history.nas = ajiltan.nas
		ajiltan_history.ndd = ajiltan.ndd
		ajiltan_history.gender = ajiltan.gender
		ajiltan_history.zereg = ajiltan.zereg
		ajiltan_history.naj = ajiltan.naj
		ajiltan_history.tzeaj = ajiltan.tzeaj
		ajiltan_history.phone = ajiltan.phone
		ajiltan_history.e_mail = ajiltan.e_mail
		


		ajiltan.begin_time = timezone.now()	# ajiltanii begin_time iig shinechilne
		ajiltan_history.begin_time = ajiltan.begin_time
		ajiltan_history.created_by = ajiltan.created_by
		ajiltan_history.status = ajiltan.status
		
		# end time ni baihgui. Utga onooj ogohgui
		ajiltan.save()
		ajiltan_history.save()
		return 1

	ajiltan_history_new = AjiltanHistory.objects.create(baiguullaga = ajiltan.baiguullaga, ajiltan = ajiltan, position_id = ajiltan.position_id, mer_zereg = ajiltan.mer_zereg)
	ajiltan_history_new.emp_lname = ajiltan.emp_lname
	ajiltan_history_new.emp_name = ajiltan.emp_name
	ajiltan_history_new.emp_reg = ajiltan.emp_reg
	ajiltan_history_new.picture = ajiltan.picture
	ajiltan_history_new.emp_birth = ajiltan.emp_birth
	ajiltan_history_new.nas = ajiltan.nas
	ajiltan_history_new.ndd = ajiltan.ndd
	ajiltan_history_new.gender = ajiltan.gender
	ajiltan_history_new.zereg = ajiltan.zereg
	ajiltan_history_new.naj = ajiltan.naj
	ajiltan_history_new.tzeaj = ajiltan.tzeaj
	ajiltan_history_new.phone = ajiltan.phone
	ajiltan_history_new.e_mail = ajiltan.e_mail

	
	
	ajiltan_history_new.created_by = created_by
	ajiltan_history_new.status = ajiltan.status
	ajiltan.begin_time = timezone.now() # ajiltanii begin_time iig shinechilne
	ajiltan_history_new.begin_time = ajiltan.begin_time
	ajiltan.save()	# baiguullagiin begin time-iig shinechilj baina
	ajiltan_history_new.save()

	ajiltan_history.end_time = ajiltan.begin_time
	ajiltan_history.save()
	return 0

class AjiltanView(LoginRequired, FormView):
	form_class = TZEAForm
	template_name = "ajiltan.html"
	success_url = reverse_lazy('ajiltan_create')

	def get_context_data(self, **kwargs):
		context = super(AjiltanView, self).get_context_data(**kwargs)
		context['tasag'] = Tasag.objects.filter(baiguullaga = context['baiguullaga'])
		context['albantushaal'] =AlbanTushaal.objects.filter(baiguullaga = context['baiguullaga'])
		
		paginator = Paginator(Ajiltan.objects.filter(baiguullaga = context['baiguullaga']), 2)
		page = self.request.GET.get('page')
		
		try:
			context['ajiltan'] = paginator.page(page)
		except PageNotAnInteger:
			context['ajiltan'] = paginator.page(1)
		except EmptyPage:
			context['ajiltan'] = paginator.page(paginator.num_pages)

		#context['ajiltan1'] = context['ajiltan'].filter(zereg=u'Удирдах ажилтан')
		#context['ajiltan2'] = context['ajiltan'].filter(zereg=u'Инженер техникийн ажилтан')
		#context['ajiltan3'] = context['ajiltan'].filter(zereg=u'Мэргэжлийн ажилтан')
		#context['ajiltan4'] = context['ajiltan'].filter(zereg=u'Бусад')
		#context['school'] = School.objects.filter(emp = context['ajiltan'])
		#context['job'] = Job.objects.filter(emp = context['ajiltan'])
		#context['engineeringcertificate'] = EngineeringCertificate.objects.filter(emp = context['ajiltan'])
		#school_ajiltan_dic={}
		#job_ajiltan_dic={}
		#engCert_ajiltan_dic={}
		#for a in context['ajiltan']:
		#	school_ajiltan_dic[a.id] = context['school'].filter(emp = a)
		#	job_ajiltan_dic[a.id] = context['job'].filter(emp = a)
		#	engCert_ajiltan_dic[a.id] = context['engineeringcertificate'].filter(emp = a)
		#context['school_ajiltan_dic'] = school_ajiltan_dic
		#context['job_ajiltan_dic'] = job_ajiltan_dic
		#context['engCert_ajiltan_dic'] = engCert_ajiltan_dic
		return context

	def form_valid(self, form):
		user = self.request.session['user']
		employee = form.save(commit = False)
		employee.baiguullaga = Baiguullaga.objects.get(id=1)
		employee.created_by = jsonpickle.decode(user)
		employee.status = True
		if form.cleaned_data['position_id'] == AlbanTushaal.objects.get(position_name = AlbanTushaalList.objects.get(name = u'Инженер')):
			#return HttpResponse("uuganaa")
			employee.zereg = u'Инженер техникийн ажилтан'
		employee.save()
		#ajiltan_history_writing(aaaa)
		school_name = self.request.POST.getlist('school_name')
		diplom_num = self.request.POST.getlist('diplom_num')
		degree = self.request.POST.getlist('degree')
		diplom_picture = self.request.FILES.getlist('diplom_picture')
		if len(school_name) == len(diplom_num) and len(degree) ==len(diplom_picture) \
		and len(school_name) == len(degree):
			for i in range(len(school_name)):
				s1 = School(school_name = University.objects.get(id = school_name[i]), emp = employee,
					diplom_num = diplom_num[i], degree = Mer_zereg.objects.get(id = degree[i]),
					diplom_picture = diplom_picture[i], created_by= employee.created_by)
				s1.save()
				s4 = SchoolHistory(school = s1, school_name = University.objects.get(id = school_name[i]),
					emp = employee, diplom_num = diplom_num[i], degree = Mer_zereg.objects.get(id = degree[i]),
					diplom_picture = diplom_picture[i],created_by= employee.created_by)
				s4.save()

		if('mergejliin_unemleh_checkbox' in self.request.POST):
			print 'mergejliin unemleh checkbox checked'
			job_picture = self.request.FILES.getlist('job_picture')
			job_name = self.request.POST.getlist('job_name')
			if len(job_name) == len(job_picture):
				for i in range(len(job_name)):
					s2 = Job(job_name = job_name[i], emp = employee, job_picture = job_picture[i],  created_by= employee.created_by)
					s2.save()
					s5 = JobHistory(job= s2, job_name = job_name[i], emp = employee, job_picture = job_picture[i],  created_by= employee.created_by)
					s5.save()
		if('zovloh_engineer_cert_checkbox' in self.request.POST):
			print 'zovloh engineer gerchilgeee checked'
			certificate_num= self.request.POST.getlist('certificate_num')
			certificate_picture= self.request.FILES.getlist('certificate_picture')
			if len(certificate_num) == len(certificate_picture):
				for i in range(len(certificate_num)):
					s7=EngineeringCertificate(certificate_num=certificate_num[i], emp = employee, certificate_picture=certificate_picture[i], created_by= employee.created_by)
					s7.save()
					s8=EngineeringCertificateHistory(certificate=s7, emp = employee,certificate_num=certificate_num[i], certificate_picture=certificate_picture[i], created_by= employee.created_by)
					s8.save()
		return super(AjiltanView, self).form_valid(form)

class BaiguullagaaView(LoginRequired,MultiFormsView):
	form_classes = {
	'baiguullagaaform':BaiguullagaForm,
	'zdtform':ZDTForm,
	'hangagchbaiguullagaform':HBGereeForm,
	'taxtodorhoiloltform': TaxTodorhoiloltForm,
	'auditdugneltform': AuditDugneltForm,
	'normstandartform':NormStandartForm,
	'ulsiinaktform': UlsiinAktForm,
	'uszuvshuurulform':UsZuvshuurulForm,
	'orontooform': SchemaForm,
	'sanhuutailanform': SanhuuTailanForm,
	'abbform': ABBForm,
	}
	template_name = "baiguullaga.html"
	pk_id = 'pk'
	success_url = '/engineering/baiguullaga/'
	def get_context_data(self, **kwargs):
		date = []
		context = super(BaiguullagaaView, self).get_context_data(**kwargs)
		context['baig'] = TZE.objects.filter(id=context['baiguullaga'].id)		
		
		for i in range(3):
			date.append(int(timezone.now().year)-(i+1))
		context['date'] = date
		#context['zdt'] = ZDTodorhoilolt.objects.filter(tze = context['baiguullaga'], status = True)
		#context['han'] = HangagchBaiguullaga.objects.filter(tze = context['baiguullaga'], status = True)
		#context['tax'] = TaxTodorhoilolt.objects.filter(tze = context['baiguullaga'], status = True)
		#context['audit'] = AuditDugnelt.objects.filter(tze = context['baiguullaga'], status = True)
		#context['norm'] = NormStandart.objects.filter(tze = context['baiguullaga'], status = True)
		#context['akt'] = UlsiinAkt.objects.filter(tze = context['baiguullaga'], status = True)
		#context['us'] = UsZuvshuurul.objects.filter(tze = context['baiguullaga'], status = True)
		#context['oron'] = OronTooniiSchema.objects.filter(tze = context['baiguullaga'], status = True)
		#context['sanhuu'] = SanhuuTailan.objects.filter(tze = context['baiguullaga'], status = True)
		#context['abb'] = ABB.objects.filter(tze = context['baiguullaga'], status = True)

		context['aimag'] = Aimag.objects.all()
		context['sum'] = Sum.objects.all()
		context['bag'] = Bag.objects.all()

		
		paginator1 = Paginator(ZDTodorhoilolt.objects.filter(tze = context['baiguullaga'], status = True), 5)
		page1 = self.request.GET.get('page')
		try:
			context['zdt'] = paginator1.page(page1)
		except PageNotAnInteger:
			context['zdt'] = paginator1.page(1)
		except EmptyPage:
			context['zdt'] = paginator1.page(paginator1.num_pages)

		paginator2 = Paginator(HangagchBaiguullaga.objects.filter(tze = context['baiguullaga'], status = True), 5)
		page2 = self.request.GET.get('page')
		try:
			context['han'] = paginator2.page(page2)
		except PageNotAnInteger:
			context['han'] = paginator2.page(1)
		except EmptyPage:
			context['han'] = paginator2.page(paginator2.num_pages)

		paginator3 = Paginator(TaxTodorhoilolt.objects.filter(tze = context['baiguullaga'], status = True), 5)
		page3 = self.request.GET.get('page')
		try:
			context['tax'] = paginator3.page(page3)
		except PageNotAnInteger:
			context['tax'] = paginator3.page(1)
		except EmptyPage:
			context['tax'] = paginator3.page(paginator3.num_pages)

		paginator4 = Paginator(AuditDugnelt.objects.filter(tze = context['baiguullaga'], status = True), 5)
		page4 = self.request.GET.get('page')
		try:
			context['audit'] = paginator4.page(page4)
		except PageNotAnInteger:
			context['audit'] = paginator4.page(1)
		except EmptyPage:
			context['audit'] = paginator4.page(paginator4.num_pages)

		paginator5 = Paginator(NormStandart.objects.filter(tze = context['baiguullaga'], status = True), 5)
		page5 = self.request.GET.get('page')
		try:
			context['norm'] = paginator5.page(page5)
		except PageNotAnInteger:
			context['norm'] = paginator5.page(1)
		except EmptyPage:
			context['norm'] = paginator5.page(paginator5.num_pages)

		paginator6 = Paginator(UlsiinAkt.objects.filter(tze = context['baiguullaga'], status = True), 5)
		page6 = self.request.GET.get('page')
		try:
			context['akt'] = paginator6.page(page6)
		except PageNotAnInteger:
			context['akt'] = paginator6.page(1)
		except EmptyPage:
			context['akt'] = paginator6.page(paginator6.num_pages)

		paginator7 = Paginator(UsZuvshuurul.objects.filter(tze = context['baiguullaga'], status = True), 5)
		page7 = self.request.GET.get('page')
		try:
			context['us'] = paginator7.page(page7)
		except PageNotAnInteger:
			context['us'] = paginator7.page(1)
		except EmptyPage:
			context['us'] = paginator7.page(paginator7.num_pages)

		paginator8 = Paginator(OronTooniiSchema.objects.filter(tze = context['baiguullaga'], status = True), 5)
		page8 = self.request.GET.get('page')
		try:
			context['oron'] = paginator8.page(page8)
		except PageNotAnInteger:
			context['oron'] = paginator8.page(1)
		except EmptyPage:
			context['oron'] = paginator8.page(paginator8.num_pages)

		paginator9 = Paginator(SanhuuTailan.objects.filter(tze = context['baiguullaga'], status = True), 5)
		page9 = self.request.GET.get('page')
		try:
			context['sanhuu'] = paginator9.page(page9)
		except PageNotAnInteger:
			context['sanhuu'] = paginator9.page(1)
		except EmptyPage:
			context['sanhuu'] = paginator9.page(paginator9.num_pages)

		paginator10 = Paginator(ABB.objects.filter(tze = context['baiguullaga'], status = True), 5)
		page10 = self.request.GET.get('page')
		try:
			context['abb'] = paginator10.page(page10)
		except PageNotAnInteger:
			context['abb'] = paginator10.page(1)
		except EmptyPage:
			context['abb'] = paginator10.page(paginator10.num_pages)

		return context
	def get_baiguullagaaform_initial(self):
		initial = super(BaiguullagaaView, self).get_initial('')
		context = self.get_context_data()
		if TZE.objects.filter(id=context['baig']):
			a = TZE.objects.get(id=context['baig'])
			initial['reg_num'] = a.reg_num 
			initial['ubd'] = a.ubd 
			initial['org_name'] = a.org_name 
			initial['org_type'] = a.org_type 
			initial['org_date'] = a.org_date
			initial['phone'] = a.phone
			initial['e_mail'] = a.e_mail
			initial['fax'] = a.fax
			initial['post'] = a.post
			initial['tax'] = a.tax
			initial['city'] = a.city
			initial['district'] = a.district
			initial['khoroo'] = a.khoroo
			initial['address'] = a.address
			initial['tovch_taniltsuulga'] = a.tovch_taniltsuulga
			initial['gerchilgee_picture'] = a.gerchilgee_picture
		return initial
	def baiguullagaaform_form_valid(self, form):
		user = self.request.session['user']
		dd = TZE.objects.get(id=self.request.POST.get('id'))
		dd.reg_num = form.cleaned_data['reg_num']
		dd.ubd = form.cleaned_data['ubd']
		dd.org_name = form.cleaned_data['org_name']	
		dd.org_type = form.cleaned_data['org_type']	
		dd.org_date = form.cleaned_data['org_date']
		dd.phone = form.cleaned_data['phone']
		dd.e_mail = form.cleaned_data['e_mail']
		dd.fax = form.cleaned_data['fax']
		dd.post = form.cleaned_data['post']
		dd.tax = form.cleaned_data['tax']	
		dd.city = form.cleaned_data['city']	
		dd.district = form.cleaned_data['district']
		dd.khoroo = form.cleaned_data['khoroo']
		dd.address = form.cleaned_data['address']
		dd.tovch_taniltsuulga = form.cleaned_data['tovch_taniltsuulga']
		dd.gerchilgee_picture = form.cleaned_data['gerchilgee_picture']
		dd.status=True
		dd.created_by=jsonpickle.decode(user)
		dd.save()
		tze_history_writing_func(dd)
		return super(BaiguullagaaView, self).forms_valid(form, form)
	def zdtform_form_valid(self, form):
		zdt(self, form)
		return super(BaiguullagaaView, self).forms_valid(form, form)
	def hangagchbaiguullagaform_form_valid(self, form):
		hangagch(self, form)
		return super(BaiguullagaaView, self).forms_valid(form, form)
	def taxtodorhoiloltform_form_valid(self, form):
		tax(self, form)
		return super(BaiguullagaaView, self).forms_valid(form, form)
	def auditdugneltform_form_valid(self, form):
		audit(self, form)
		return super(BaiguullagaaView, self).forms_valid(form, form)
	def normstandartform_form_valid(self, form):
		norm(self, form)
		return super(BaiguullagaaView, self).forms_valid(form, form)
	def ulsiinaktform_form_valid(self, form):
		ulsiinakt(self, form)
		return super(BaiguullagaaView, self).forms_valid(form, form)
	def uszuvshuurulform_form_valid(self, form):
		uszuvshuurul(self, form)
		return super(BaiguullagaaView, self).forms_valid(form, form)
	def orontooform_form_valid(self, form):
		orontoo(self, form)
		return super(BaiguullagaaView, self).forms_valid(form, form)
	def sanhuutailanform_form_valid(self, form):
		sanhuu(self, form)
		return super(BaiguullagaaView, self).forms_valid(form, form)
	def abbform_form_valid(self, form):
		abb(self, form)
		return super(BaiguullagaaView, self).forms_valid(form, form)

class uamedeeView(LoginRequired,MultiFormsView):
	form_classes = {
	'analysiswaterform':AnalysisWaterForm,
	'analysisbohirform':AnalysisBohirForm,
	}
	template_name = "uamedee.html"
	success_url = '/engineering/uamedee/'
	def get_context_data(self, **kwargs):
		context = super(uamedeeView, self).get_context_data(**kwargs)
		context['water'] = AnalysisWater.objects.filter(tze = context['baiguullaga'])
		context['bohir'] = AnalysisBohir.objects.filter(tze = context['baiguullaga'])
		return context
	def analysiswaterform_form_valid(self, form):
		user = self.request.session['user']
		ana = Analysis(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
		ana.analysis_torol = form.cleaned_data['analysis_torol']
		ana.analysis = form.cleaned_data['analysis']
		ana.begin_time=datetime.datetime.now()
		ana.created_by=jsonpickle.decode(user)
		ana.save()
		ansa = AnalysisHistory(tze = TZE.objects.get(org_name = self.request.POST.get('tze')))
		ansa.analysis = ana
		ansa.analysis_torol = form.cleaned_data['analysis_torol']
		ansa.analysis = form.cleaned_data['analysis']
		ansa.begin_time=datetime.datetime.now()
		ansa.created_by=jsonpickle.decode(user)
		ansa.save()
		return super(TohooromjjView, self).forms_valid(form, form)
	
class uatailanView(LoginRequired,MultiFormsView):
	form_classes = {
	'baiguullagaaform':BaiguullagaForm,
	'zdtform':ZDTForm,
	'hangagchbaiguullagaform':HBGereeForm,
	'taxtodorhoiloltform': TaxTodorhoiloltForm,
	'auditdugneltform': AuditDugneltForm,
	'normstandartform':NormStandartForm,
	'ulsiinaktform': UlsiinAktForm,
	'uszuvshuurulform':UsZuvshuurulForm,
	'orontooform': SchemaForm,
	'sanhuutailanform': SanhuuTailanForm,
	'abbform': ABBForm,
	}
	template_name = "uatailan.html"

def zdtDelete(request, id):
	try:
		note = get_object_or_404(ZDTodorhoilolt, pk=id)
		note.end_time = timezone.now()
		note.created_by = jsonpickle.decode(request.session['user'])
		note.status = False
		note.save()

		note = get_object_or_404(ZDTodorhoiloltHistory, pk=id)
		note.end_time = timezone.now()
		note.created_by = jsonpickle.decode(request.session['user'])
		note.status = False
		note.save()
	except:
		raise Http404
	return HttpResponseRedirect("/engineering/baiguullaga/")

def hanDelete(request, id):
	try:
		note = get_object_or_404(HangagchBaiguullaga, pk=id)
		note.end_time = timezone.now()
		note.created_by = jsonpickle.decode(request.session['user'])
		note.status = False
		note.save()
		note = get_object_or_404(HangagchBaiguullagaHistory, pk=id)
		note.end_time = timezone.now()
		note.created_by = jsonpickle.decode(request.session['user'])
		note.status = False
		note.save()
	except:
		raise Http404
	return HttpResponseRedirect("/engineering/baiguullaga/")

def taxDelete(request, id):
	try:
		note = get_object_or_404(TaxTodorhoilolt, pk=id)
		note.end_time = timezone.now()
		note.created_by = jsonpickle.decode(request.session['user'])
		note.status = False
		note.save()
		note = get_object_or_404(TaxTodorhoiloltHistory, pk=id)
		note.end_time = timezone.now()
		note.created_by = jsonpickle.decode(request.session['user'])
		note.status = False
		note.save()
	except:
		raise Http404
	return HttpResponseRedirect("/engineering/baiguullaga/")

def auditDelete(request, id):
	try:
		note = get_object_or_404(AuditDugnelt, pk=id)
		note.end_time = timezone.now()
		note.created_by = jsonpickle.decode(request.session['user'])
		note.status = False
		note.save()
		note = get_object_or_404(AuditDugneltHistory, pk=id)
		note.end_time = timezone.now()
		note.created_by = jsonpickle.decode(request.session['user'])
		note.status = False
		note.save()
	except:
		raise Http404
	return HttpResponseRedirect("/engineering/baiguullaga/")

def aktDelete(request, id):
	try:
		note = get_object_or_404(UlsiinAkt, pk=id)
		note.end_time = timezone.now()
		note.created_by = jsonpickle.decode(request.session['user'])
		note.status = False
		note.save()
		note = get_object_or_404(UlsiinAktHistory, pk=id)
		note.end_time = timezone.now()
		note.created_by = jsonpickle.decode(request.session['user'])
		note.status = False
		note.save()
	except:
		raise Http404
	return HttpResponseRedirect("/engineering/baiguullaga/")

def usDelete(request, id):
	try:
		note = get_object_or_404(UsZuvshuurul, pk=id)
		note.end_time = timezone.now()
		note.created_by = jsonpickle.decode(request.session['user'])
		note.status = False
		note.save()
		note = get_object_or_404(UsZuvshuurulHistory, pk=id)
		note.end_time = timezone.now()
		note.created_by = jsonpickle.decode(request.session['user'])
		note.status = False
		note.save()
	except:
		raise Http404
	return HttpResponseRedirect("/engineering/baiguullaga/")

def sanDelete(request, id):
	try:
		note = get_object_or_404(SanhuuTailan, pk=id)
		note.end_time = timezone.now()
		note.created_by = jsonpickle.decode(request.session['user'])
		note.status = False
		note.save()
		note = get_object_or_404(SanhuuTailanHistory, pk=id)
		note.end_time = timezone.now()
		note.created_by = jsonpickle.decode(request.session['user'])
		note.status = False
		note.save()
	except:
		raise Http404
	return HttpResponseRedirect("/engineering/baiguullaga/")

def oronDelete(request, id):
	try:
		note = get_object_or_404(OronTooniiSchema, pk=id)
		note.end_time = timezone.now()
		note.created_by = jsonpickle.decode(request.session['user'])
		note.status = False
		note.save()
		note = get_object_or_404(OronTooniiSchemaHistory, pk=id)
		note.end_time = timezone.now()
		note.created_by = jsonpickle.decode(request.session['user'])
		note.status = False
		note.save()
	except:
		raise Http404
	return HttpResponseRedirect("/engineering/baiguullaga/")

def carDelete(request, id):
	try:
		note = get_object_or_404(Car, pk=id)
		note.end_time = timezone.now()
		note.created_by = jsonpickle.decode(request.session['user'])
		note.status = False
		note.save()
		notee = get_object_or_404(CarHistory, car=note)
		notee.end_time = timezone.now()
		notee.created_by = jsonpickle.decode(request.session['user'])
		notee.status = False
		notee.save()
	except:
		raise Http404
	return HttpResponseRedirect("/engineering/tohooromj/")

def bbDelete(request, id):
	try:
		note = get_object_or_404(BB, pk=id)
		note.end_time = timezone.now()
		note.created_by = jsonpickle.decode(request.session['user'])
		note.status = False
		note.save()
		notee = get_object_or_404(BBHistory, bb=note)
		notee.end_time = timezone.now()
		notee.created_by = jsonpickle.decode(request.session['user'])
		notee.status = False
		notee.save()
	except:
		raise Http404
	return HttpResponseRedirect("/engineering/tohooromj/")

def tonogDelete(request, id):
	try:
		note = get_object_or_404(Equipment, pk=id)
		note.end_time = timezone.now()
		note.created_by = jsonpickle.decode(request.session['user'])
		note.status = False
		note.save()
		notee = get_object_or_404(EquipmentHistory, equipment=note)
		notee.end_time = timezone.now()
		notee.created_by = jsonpickle.decode(request.session['user'])
		notee.status = False
		notee.save()
	except:
		raise Http404
	return HttpResponseRedirect("/engineering/tohooromj/")
	
def ajiltanDelete(request, id):
	try:
		note = get_object_or_404(Ajiltan, pk=id)
		note.end_time = timezone.now()
		note.created_by = jsonpickle.decode(request.session['user'])
		note.status = False
		note.save()
		note = get_object_or_404(Ajiltan, pk=id)
		note.end_time = timezone.now()
		note.created_by = jsonpickle.decode(request.session['user'])
		note.status = False
		note.save()
	except:
		raise Http404
	return HttpResponseRedirect("/engineering/baiguullaga/")

def delete_ajiltan(request, id):
	user = request.session['user']
	aaaa = Ajiltan.objects.get(id = id)
	aaaa.created_by=jsonpickle.decode(user)
	aaaa.status= False
	aaaa.save()
	ajiltan_history_writing(aaaa)
	return HttpResponseRedirect('/engineering/ajiltan/')

class AjiltanUpdateView(AjaxTemplateMixin, UpdateView):
	template_name = 'emp_update.html'
	model = Ajiltan
	form_class = AjiltanForm
	success_url = reverse_lazy('ajiltan_create')

	def get_context_data(self, *args, **kwargs):
		context = super(AjiltanUpdateView, self).get_context_data(*args, **kwargs)
		context['schools'] = School.objects.filter(emp = self.object)
		context['certificate'] = EngineeringCertificate.objects.filter(emp = self.object)
		context['job'] = Job.objects.filter(emp = self.object)
		context['university'] = University.objects.all()
		return context

	def form_valid(self, form):
		employee_school_id = self.request.POST.getlist('employee_school_id')
		employee_diplom_num = self.request.POST.getlist('employee_diplom_num')
		employee_university = self.request.POST.getlist('university')
		if len(employee_school_id) == len(employee_diplom_num):
			for too, i in enumerate(employee_school_id):
				school = School.objects.get(id = i)
				school.diplom_num = employee_diplom_num[too]
				school.school_name = University.objects.get(university = employee_university[too])
				school.save()
		school_name = self.request.POST.getlist('school_name')
		diplom_num = self.request.POST.getlist('diplom_num')
		degree = self.request.POST.getlist('degree')
		diplom_picture = self.request.FILES.getlist('diplom_picture')
		if len(school_name) == len(diplom_num) and len(degree) ==len(diplom_picture) \
		and len(school_name) == len(degree):
			for i in range(len(school_name)):
				s1 = School(school_name = University.objects.get(id = school_name[i]), emp = self.object,
					diplom_num = diplom_num[i], degree = Mer_zereg.objects.get(id = degree[i]),
					diplom_picture = diplom_picture[i], created_by= self.object.created_by)
				s1.save()
				s4 = SchoolHistory(school = s1, school_name = University.objects.get(id = school_name[i]),
					emp = self.object, diplom_num = diplom_num[i], degree = Mer_zereg.objects.get(id = degree[i]),
					diplom_picture = diplom_picture[i],created_by= self.object.created_by)
				s4.save()
		return  super(AjiltanUpdateView, self).form_valid(form)

class HudagUpdateView(AjaxTemplateMixin, UpdateView):
	template_name = 'tonog_tohooromj_update/hudag_update.html'
	model = Hudag
	form_class = HudagNegdsenForm
	success_url = '/engineering/tohooromj/'

class UsansanUpdateView(AjaxTemplateMixin, UpdateView):
	template_name = 'tonog_tohooromj_update/usansan_update.html'
	model = UsanSan
	form_class = UsanSanForm
	success_url = '/engineering/tohooromj/'

class NasosUpdateView(AjaxTemplateMixin, UpdateView):
	template_name = 'tonog_tohooromj_update/nasos_update.html'
	model = Nasos
	form_class = NasosForm
	success_url = '/engineering/tohooromj/'

class LabUpdateView(AjaxTemplateMixin, UpdateView):
	template_name = 'tonog_tohooromj_update/lab_update.html'
	model = Lab
	form_class = LabForm
	success_url = '/engineering/tohooromj/'

class SuljeeUpdateView(AjaxTemplateMixin, UpdateView):
	template_name = 'tonog_tohooromj_update/suljee_update.html'
	model = Sh_suljee
	form_class = Sh_suljeeForm
	success_url = '/engineering/tohooromj/'

class Ts_baiguulamjUpdateView(AjaxTemplateMixin, UpdateView):
	template_name = 'tonog_tohooromj_update/ts_baiguulamj_update.html'
	model = Ts_baiguulamj
	form_class = Ts_baiguulamjForm
	success_url = '/engineering/tohooromj/'

class WatercarUpdateView(AjaxTemplateMixin, UpdateView):
	template_name = 'tonog_tohooromj_update/watercar_update.html'
	model = WaterCar
	form_class = WaterCarForm
	success_url = '/engineering/tohooromj/'

class BohircarUpdateView(AjaxTemplateMixin, UpdateView):
	template_name = 'tonog_tohooromj_update/bohircar_update.html'
	model = BohirCar
	form_class = BohirCarForm
	success_url = '/engineering/tohooromj/'

class UsdamjuulahUpdateView(AjaxTemplateMixin, UpdateView):
	template_name = 'tonog_tohooromj_update/us_damjuulah_update.html'
	model = UsDamjuulahBair
	form_class = UsDamjuulahBairForm
	success_url = '/engineering/tohooromj/'

class UstugeehUpdateView(AjaxTemplateMixin, UpdateView):
	template_name = 'tonog_tohooromj_update/us_tugeeh_update.html'
	model = UsTugeehBair
	form_class = UsTugeehBairForm
	success_url = '/engineering/tohooromj/'

class EquipmentUpdateView(AjaxTemplateMixin, UpdateView):
	template_name = 'tonog_tohooromj_update/equipment_update.html'
	model = Equipment
	form_class = EquipmentForm
	success_url = '/engineering/tohooromj/'

def city(request, id = 0):
	response_data = []
	for i in Sum.objects.filter(aimag_id = Aimag.objects.get(id = id)):
		response_data.append( { "key":i.id ,"values":i.Sum } )

	return HttpResponse(
		json.dumps(response_data),
    	content_type="application/json"
    	)

def district(request, city_id = 0, district_id = 0):
	response_data = []
	sum_num = Sum.objects.get(id = district_id).sum_num
	for i in Bag.objects.filter(aimag_id = Aimag.objects.get(id = city_id),sum_id = sum_num):
		response_data.append( { "key":i.id ,"values":i.Bag } )

	return HttpResponse(
		json.dumps(response_data),
    	content_type="application/json"
    	)

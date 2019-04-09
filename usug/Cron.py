# -*- coding:utf-8 -*-
from django_cron import CronJobBase, Schedule
from applications.app.models import *
from applications.director.models import *
from django.utils import timezone

class TailanEhleh(CronJobBase):
	RUN_EVERY_MINS = 0.1

	schedule = Schedule(run_every_mins = RUN_EVERY_MINS)
	code = 'tailan_ehleh.log'
	
	def do(self):
		a = timezone.now().year
		b = timezone.now().month - 1
		for i in Certificate.objects.values('tze').distinct():
			if not SariinTailan.objects.filter(tze = TZE.objects.get(id = i.values()[0]), year = a, month = b):
				z = Zardal.objects.create(status = True)
				o = Orlogo.objects.create(status = True)
				s = SariinTailan.objects.create(tze = TZE.objects.get(id = i.values()[0]), orlogo = o, zardal = z, tailan_status = True,  status = True, yvts = u'Хийгдэж байна', year = a, month = b)
				if TariffAll.objects.filter(tze = TZE.objects.get(id = i.values()[0]), name = 0):
					s.tariff_hereglegch.add(TariffAll.objects.filter(tze = TZE.objects.get(id = i.values()[0]), name = 0).last())

class TailanDuusah(CronJobBase):
	RUN_EVERY_MINS = 1

	schedule = Schedule(run_every_mins = RUN_EVERY_MINS)
	code = 'tailan_duusah.log'
	def do(self):
		name = '%s оны %s сарын санхүүгийн мэдээ' %(timezone.now().year, timezone.now().month)
		for i in Certificate.objects.values('baiguullaga').distinct():
			s = SariinTailan.objects.get(tze = TZE.objects.get(id = i.values()[0]), name = name)
			s.yvts = u'Илгээсэн'
			#s.status = False
			s.save()

class UAtailanIlgeeh(CronJobBase):
	RUN_EVERY_MINS = 1

	schedule = Schedule(run_every_mins = RUN_EVERY_MINS)
	code = 'tailan_hiigdeh.log'
	def do(self):
		#for i in Certificate.objects.values('tze').distinct():
		#	for x in range(1,13):
		z = Zardal.objects.create(status = True)
		o = Orlogo.objects.create(status = True)
		s = SariinTailan.objects.create(tze = TZE.objects.get(reg_num = 2000075), orlogo = o, zardal = z, status = True, yvts = u'Хийгдэж байна', year = 2015, month = 2)

class TailanUusgeh(CronJobBase):
	RUN_EVERY_MINS = 1

	schedule = Schedule(run_every_mins = RUN_EVERY_MINS)
	code = 'tailan_hiigdeh.log'
	def do(self):
		for x in range(1,13):
			z = Zardal.objects.create(status = True)
			o = Orlogo.objects.create(status = True)
			s = SariinTailan.objects.create(tze = TZE.objects.get(reg_num = 2777401), orlogo = o, zardal = z, status = True, yvts = u'Хийгдэж байна', year = 2015, month = x)
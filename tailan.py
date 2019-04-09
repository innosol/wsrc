# -*- coding:utf-8 -*-
from applications.app.models import *
from applications.director.models import *

for i in Certificate.objects.values('tze').distinct():
	for x in range(1,12):
		z = Zardal.objects.create(status = True)
		o = Orlogo.objects.create(status = True)
		s = SariinTailan.objects.create(tze__id = i.values()[0], orlogo = o, zardal = z, status = True, yvts = u'Хийгдэж байна', year = 2015, month = x)
# -*- coding: utf-8 -*-

from django import forms as f
from applications.app.models import TZE, ZZ, TZ
from applications.app.models import Tasag, AlbanTushaal
from applications.app.models import Ajiltan



class HZM_tze_filter(f.ModelForm):
	tza_mergejilten = f.ChoiceField()
	uta_mergejilten = f.ChoiceField()
	class Meta:
		model = TZE
		fields=['city', 'district', 'khoroo']
		
	def __init__(self, *args, **kwargs):
		super(HZM_tze_filter, self).__init__(*args, **kwargs)
		zz = ZZ.objects.all()[0]
		tasag_tza = Tasag.objects.get(baiguullaga = zz, dep_name = 'Тусгай зөвшөөрлийн алба')
		tasag_uta = Tasag.objects.get(baiguullaga = zz, dep_name = 'Үнэ тарифын алба')
		tza = AlbanTushaal.objects.filter(dep_id = tasag_tza, position_name__icontains = 'мэргэжилтэн')
		uta = AlbanTushaal.objects.filter(dep_id = tasag_uta, position_name__icontains = 'мэргэжилтэн')
		self.fields['tza_mergejilten'] = f.ModelChoiceField(label = 'ТЗА мэргэжилтэн', queryset = Ajiltan.objects.filter(baiguullaga = zz, status = True, alban_tushaal = tza), required = False)
		self.fields['uta_mergejilten'] = f.ModelChoiceField(label = 'ҮТА мэргэжилтэн', queryset = Ajiltan.objects.filter(baiguullaga = zz, status = True, alban_tushaal = uta), required = False)
		self.fields['tz'] = f.ModelMultipleChoiceField(label = 'Тусгай зөвшөөрөл', queryset = TZ.objects.all(), widget = f.CheckboxSelectMultiple())
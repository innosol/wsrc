# -*- coding: utf-8 -*-

from django import forms as f
from applications.app.models import TZE, ZZ
from applications.app.models import Tasag, AlbanTushaal
from applications.app.models import Ajiltan
import django_filters
from applications.app.models import TZ_Huselt, TZ

class TZ_Huselt_filter(django_filters.FilterSet):
	class Meta:
		model = TZ_Huselt
		fields = ['yavts']

class TZE_uta_darga_filter(f.ModelForm):
	uta_mergejilten = f.ChoiceField()
	class Meta:
		model = TZE
		fields=['city', 'district', 'khoroo']
	def __init__(self, *args, **kwargs):
		super(TZE_uta_darga_filter, self).__init__(*args, **kwargs)
		zz = ZZ.objects.all()[0]
		tasag_uta = Tasag.objects.get(baiguullaga = zz, dep_name = 'Үнэ тарифын алба')
		uta = AlbanTushaal.objects.filter(dep_id = tasag_uta, position_name__icontains = 'мэргэжилтэн')
		self.fields['uta_mergejilten'] = f.ModelChoiceField(label = 'ҮТА мэргэжилтэн',queryset = Ajiltan.objects.filter(baiguullaga = zz, status = True, alban_tushaal = uta), required = False)

class TZE_uta_mergejilten_filter(f.ModelForm):
	uta_mergejilten = f.ChoiceField()
	class Meta:
		model = TZE
		fields=['city', 'district', 'khoroo']

""" tusgai zovshoorliin huselt huvaarilah filter """
class TZ_huselt_huvaarilah_uta_filter(f.Form):
	tze_baig = f.CharField(label="ТЗЭ-ийн нэр")
	uta_mergejilten = f.ChoiceField()
	tz = f.ModelMultipleChoiceField(label = 'Тусгай зөвшөөрөл', queryset = TZ.objects.all(), widget = f.CheckboxSelectMultiple())
	def __init__(self, *args, **kwargs):
		super(TZ_huselt_huvaarilah_uta_filter, self).__init__(*args, **kwargs)
		zz = ZZ.objects.all()[0]
		tasag_uta = Tasag.objects.get(baiguullaga = zz, dep_name = 'Үнэ тарифын алба')
		uta = AlbanTushaal.objects.filter(dep_id = tasag_uta, position_name__icontains = 'мэргэжилтэн')
		self.fields['uta_mergejilten'] = f.ModelChoiceField(label = 'ҮТА мэргэжилтэн',queryset = Ajiltan.objects.filter(baiguullaga = zz, status = True, alban_tushaal = uta), required = False)
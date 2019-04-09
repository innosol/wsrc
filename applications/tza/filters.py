# -*- coding: utf-8 -*-

from django import forms as f
from applications.app.models import TZE, ZZ, TZ
from applications.app.models import Tasag, AlbanTushaal
from applications.app.models import Ajiltan, Hudag, UsanSan, NasosStants, Lab, Sh_suljee, Ts_baiguulamj
from applications.app.models import BohirCar, WaterCar, UsDamjuulahBair, UsTugeehBair, Burdel
import django_filters
from applications.app.models import UAT_yavts, BB, Equipment, Car, AnalysisWater, AnalysisBohir

class TZE_tza_darga_filter(f.ModelForm):
	tza_mergejilten = f.ChoiceField()
	class Meta:
		model = TZE
		fields=['city', 'district', 'khoroo']

	def __init__(self, *args, **kwargs):
		super(TZE_tza_darga_filter, self).__init__(*args, **kwargs)
		zz = ZZ.objects.all()[0]
		tasag_tza = Tasag.objects.get(baiguullaga = zz, dep_name = 'Тусгай зөвшөөрлийн алба')
		tza = AlbanTushaal.objects.filter(dep_id = tasag_tza, position_name__icontains = 'мэргэжилтэн')
		self.fields['tza_mergejilten'] = f.ModelChoiceField(label = 'ТЗА мэргэжилтэн', queryset = Ajiltan.objects.filter(baiguullaga = zz, status = True, alban_tushaal = tza), required = False)
		self.fields['tz'] = f.ModelMultipleChoiceField(label = 'Тусгай зөвшөөрөл', queryset = TZ.objects.all(), widget = f.CheckboxSelectMultiple())

class TZE_tza_mergejilten_filter(f.ModelForm):
	tz = f.ModelMultipleChoiceField(label = 'Тусгай зөвшөөрөл', queryset = TZ.objects.all(), widget = f.CheckboxSelectMultiple())
	class Meta:
		model = TZE
		fields=['city', 'district', 'khoroo', 'tz']


class TZE_search(f.Form):
	#search_type = f.ChoiceField(choices = search_choices, label='Хайх төрөл', required=False)
	search = f.CharField(max_length = 127, required = False, label='Хайх утга', widget = f.TextInput(attrs = {'placeholder':'РД, УБД, нэр оруулна уу.'}))

class TZE_search_by_name(f.Form):
	#search_type = f.ChoiceField(choices = search_choices, label='Хайх төрөл', required=False)
	search = f.CharField(max_length = 127, required = False, label='Хайх утга', widget = f.TextInput(attrs = {'placeholder':'ТЗЭ-ийн нэр оруулна уу.'}))

class Ajiltan_filter(f.ModelForm):
	tze_baig = f.CharField(label="ТЗЭ-ийн нэр", max_length=127)
	alban_tushaal = f.CharField(label="Албан тушаал", max_length=127)
	class Meta:
		model = Ajiltan
		fields=['tze_baig','zereg']



class UAT_yavts_filter(django_filters.FilterSet):
	on = django_filters.RangeFilter()
	class Meta:
		model = UAT_yavts
		fields = ['on', 'tze']

	def __init__(self, *args, **kwargs):
		super(UAT_yavts_filter, self).__init__(*args, **kwargs)
		self.filters['tze'].label = 'Тусгай зөвшөөрөл эзэмшигч'
		self.filters['on'].label = 'Хугацааны интервал'


""" tusgai zovshoorliin huselt huvaarilah filter """
class TZ_huselt_huvaarilah_tza_filter(f.Form):
	tze_baig = f.CharField(label="ТЗЭ-ийн нэр")
	tza_mergejilten = f.ChoiceField()
	tz = f.ModelMultipleChoiceField(label = 'Тусгай зөвшөөрөл', queryset = TZ.objects.all(), widget = f.CheckboxSelectMultiple())
	def __init__(self, *args, **kwargs):
		super(TZ_huselt_huvaarilah_tza_filter, self).__init__(*args, **kwargs)
		zz = ZZ.objects.all()[0]
		tasag_tza = Tasag.objects.get(baiguullaga = zz, dep_name = 'Тусгай зөвшөөрлийн алба')
		tza = AlbanTushaal.objects.filter(dep_id = tasag_tza, position_name__icontains = 'мэргэжилтэн')
		self.fields['tza_mergejilten'] = f.ModelChoiceField(label = 'ТЗА мэргэжилтэн', queryset = Ajiltan.objects.filter(baiguullaga = zz, status = True, alban_tushaal = tza), required = False)
class TZ_huselt_tza_filter(f.Form):
	tze_baig = f.CharField(label="ТЗЭ-ийн нэр")
	tz = f.ModelMultipleChoiceField(label = 'Тусгай зөвшөөрөл', queryset = TZ.objects.all(), widget = f.CheckboxSelectMultiple())


""" tonog tohooromj filters """
class Hudag_filter(f.ModelForm):
	class Meta:
		model = Hudag
		fields = [
		'city',
		'district',
		'khoroo',
		]
class UsanSan_filter(f.ModelForm):
	class Meta:
		model = UsanSan
		fields = [
		'city',
		'district',
		'khoroo',
		]
class NasosStants_filter(f.ModelForm):
	class Meta:
		model = NasosStants
		fields = [
		'city',
		'district',
		'khoroo',
		]
class Lab_filter(f.ModelForm):
	class Meta:
		model = Lab
		fields = [
		'torol',
		]
class Sh_suljee_filter(f.ModelForm):
	class Meta:
		model = Sh_suljee
		fields = [
		'shugam_helber',
		]

class UsTugeehBair_filter(f.ModelForm):
	class Meta:
		model = UsTugeehBair
		fields = [
		'city',
		'district',
		'khoroo',
		]

class TZ_Gerchilgee_filter(f.Form):
	tze_baig = f.CharField(label="ТЗЭ-ийн нэр")
	tz = f.ModelMultipleChoiceField(label = 'Тусгай зөвшөөрөл', queryset = TZ.objects.all(), widget = f.CheckboxSelectMultiple())





""" shinjilgee filters """
class Analysis_water_filter(f.ModelForm):
	tze_baig = f.CharField(label="ТЗЭ-ийн нэр")
	class Meta:
		model = AnalysisWater
		fields = [
		'tze_baig',
		'ognoo',
		]
class AnalysisBohir_filter(f.ModelForm):
	tze_baig = f.CharField(label="ТЗЭ-ийн нэр")
	class Meta:
		model = AnalysisBohir
		fields = [
		'tze_baig',
		'ognoo',
		]

class DateFilter(f.Form):
	date = f.DateField(label="Огноо:", widget = f.TextInput(attrs={'placeholder': '2015-12-20'}))
	time = f.TimeField(label="Цаг:", widget = f.TextInput(attrs={'placeholder': '10:30'}), required=False)

	def is_valid(self):
		ret = super(DateFilter, self).is_valid()
		for f in self.errors:
			self.fields[f].widget.attrs.update({'class': self.fields[f].widget.attrs.get('class', '') + ' input_error'})
		return ret
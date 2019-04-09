# -*- coding:utf-8 -*-

from django import forms as f
from applications.app.models import Aimag, Sum, ZZ, Tasag, AlbanTushaal, Ajiltan, Certificate
from applications.app.models import TZ_Huselt, Rel_baig_zz_ajilchid

class TZ_huselt_uta_huvaarilahForm(f.ModelForm):
	def __init__(self, *args, **kwargs):
		super(TZ_huselt_uta_huvaarilahForm, self).__init__(*args, **kwargs)
		zz = ZZ.objects.all()[0]
		tasag_uta = Tasag.objects.get(baiguullaga = zz, dep_name = 'Үнэ тарифын алба')
		uta = AlbanTushaal.objects.filter(dep_id = tasag_uta, position_name__icontains = 'мэргэжилтэн')
		self.fields['uta_mergejilten'] = f.ModelChoiceField(label = 'ҮТА мэргэжилтэн',queryset = Ajiltan.objects.filter(baiguullaga = zz, status = True, alban_tushaal = uta))

	class Meta:
		model = TZ_Huselt
		fields = ['uta_mergejilten']

class Baiguullaga_huvaarilalt_uta_Form(f.ModelForm):
	def __init__(self, *args, **kwargs):
		super(Baiguullaga_huvaarilalt_uta_Form, self).__init__(*args, **kwargs)
		zz = ZZ.objects.all()[0]
		tasag_uta = Tasag.objects.get(baiguullaga = zz, dep_name = 'Үнэ тарифын алба')
		uta = AlbanTushaal.objects.filter(dep_id = tasag_uta, position_name__icontains = 'мэргэжилтэн')
		self.fields['uta_mergejilten'] = f.ModelChoiceField(label = 'ҮТА мэргэжилтэн',queryset = Ajiltan.objects.filter(baiguullaga = zz, status = True, alban_tushaal = uta))
	class Meta:
		model = Rel_baig_zz_ajilchid
		fields = ['uta_mergejilten']

class MessageForm(f.Form):

	subject = f.CharField()
	body = f.CharField(widget =f.Textarea())

class BaiguullagaFilterForm(f.Form):
	name = f.CharField()
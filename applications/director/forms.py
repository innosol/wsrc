# -*- coding:utf-8 -*-

from django import forms
from .models import *
from applications.app.models import *

__all__ = ['SezForm', 'OlborloltForm' , 'ZardalForm1', 'ZardalForm16', 'Tehnik_nohtsolForm', 'BusadOrlogoForm']

class SezForm(forms.Form):
	def __init__(self, number, attr, integer, *args, **kwargs):
		super(SezForm, self).__init__(*args, **kwargs)
		self.number = number
		self.attr = attr
		self.integer = integer
		for index in range(self.number):
			if not self.integer:
				self.fields[self.attr %index] = forms.FloatField(widget = forms.TextInput(attrs = {'class': 'input-small zar', 'required': 'True'}))
			else:
				self.fields[self.attr %index] = forms.IntegerField(widget = forms.NumberInput(attrs = {'class': 'input-small zar', 'required': 'True'}))
			self.fields[self.attr %index].initial = 0

class ZardalForm16(forms.Form):
	z16_0 = forms.CharField(required = False, widget = forms.TextInput(attrs = {'class': 'input-small'}))
	def __init__(self, *args, **kwargs):
		super(ZardalForm16, self).__init__(*args, **kwargs)
		for index in range(7):
			self.fields['z16_%s' %str(index+1)] = forms.CharField(required = False,widget = forms.TextInput(attrs = {'class': 'input-small zar'}))

class OlborloltForm(forms.ModelForm):
	class Meta:
		model = Olborlolt
		exclude = ['tze']
		widgets ={
		'torol1' : forms.CheckboxInput(),
		'torol2' : forms.CheckboxInput(),
		'tsever': forms.NumberInput(attrs={'class': 'input-medium zar'}),
		'bohir': forms.NumberInput(attrs={'class': 'input-medium zar'}),
		}
	def __init__(self, *args, **kwargs):
		super(OlborloltForm, self).__init__(*args, **kwargs)
		self.fields['tsever'].required = False
		self.fields['bohir'].required = False
		self.fields['tsever'].initial = 0
		self.fields['bohir'].initial = 0

	def clean(self):
		cleaned_data = super(OlborloltForm, self).clean()
		if self.is_valid():
			if not cleaned_data['torol1'] and not cleaned_data['torol2']:
				raise forms.ValidationError(u'Сонголт буруу байна', code='invalid')
		return cleaned_data

	def clean_tsever(self):
		data = self.cleaned_data['tsever']
		if self.cleaned_data['torol2']:
			if data == None:
				raise forms.ValidationError(u'Энэ талбарыг бөглөнө үү')
		return data

	def clean_bohir(self):
		data = self.cleaned_data['bohir']
		if self.cleaned_data['torol2']:
			if data == None:
				raise forms.ValidationError(u'Энэ талбарыг бөглөнө үү')
		return data

class BusadOrlogoForm(forms.ModelForm):

	class Meta:
		model = BusadOrlogo
		exclude = ['status', 'created_by', 'yvts']

	def __init__(self, *args, **kwargs):
		super(BusadOrlogoForm, self).__init__(*args, **kwargs)
		self.fields['unt'].initial = 0
		for i in range(6):
			self.fields['unt%s' %i].initial = 0
			self.fields['unt%s' %i].required = True

class Tehnik_nohtsolForm(forms.Form):
	tn_0 = forms.IntegerField(widget = forms.NumberInput(attrs = {'class': 'input-small zar', 'required': 'True'}))
	tn_1 = forms.FloatField(widget = forms.TextInput(attrs = {'class': 'input-small zar', 'required': 'True'}))
	tn_2 = forms.IntegerField(widget = forms.NumberInput(attrs = {'class': 'input-small zar', 'required': 'True'}))
	tn_3 = forms.FloatField(widget = forms.TextInput(attrs = {'class': 'input-small zar', 'required': 'True'}))
			
	def __init__(self, *args, **kwargs):
		super(Tehnik_nohtsolForm, self).__init__(*args, **kwargs)
		for index in range(4):
			self.fields['tn_%s' %index].initial = 0
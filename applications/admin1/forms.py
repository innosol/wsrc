# -*- coding:utf-8-*-
from applications.app.models import *
from django import forms
from applications.app.validate import *

class ZZAForm(forms.ModelForm):
	class Meta:
		model = Ajiltan
		exclude = ['created_by', 'status', 'baiguullaga', 'picture', 'emp_birth', 'ndd', 'nas', 'gender', 'zereg', 'naj', 'tzeaj']
		
	def __init__(self, baiguullaga = None, *args, **kwargs):
		super(ZZAForm, self).__init__(*args, **kwargs)
		if baiguullaga:
			self.baiguullaga = baiguullaga
			self.fields['position_id'].queryset = AlbanTushaal.objects.filter(baiguullaga = baiguullaga)

	def save(self, commit = False):
		employee = super(ZZAForm, self).save(commit)
		reg = self.cleaned_data['emp_reg']
		emp_birth = u'19%s-%s-%s' %(reg[2:4], reg[4:6], reg[6:8])
		nas = timezone.now().year - int('19%s' %reg[2:4])
		if int(reg[8:9])%2 == 1:
			gender = u'Эр'
		else:
			gender = u'Эм'
		employee.emp_birth = emp_birth
		employee.nas = nas
		employee.gender = gender
		employee.status = True
		return employee

	def clean_emp_reg(self):
		data = self.cleaned_data['emp_reg']
		clean_reg(data)
		return data

	def clean_emp_name(self):
		data = self.cleaned_data['emp_name']
		kirill(data)
		return data

	def clean_emp_lname(self):
		data = self.cleaned_data['emp_lname']
		kirill(data)
		return data

	#def clean_e_mail(self):
	#	data = self.cleaned_data['e_mail']
	#	if Ajiltan.objects.filter(e_mail = self.cleaned_data['e_mail']):
	#		raise forms.ValidationError(u'Системд бүртгэлтэй байна')
	#	return data

	def clean_phone(self):
		data = self.cleaned_data['phone']
		if Ajiltan.objects.filter(e_mail = data):
			raise forms.ValidationError(u"Системд бүртгэлтэй байна")
		return data

class BaiguullagaTasagForm(f.ModelForm):
	dep_name = forms.CharField(label = u'Тасгийн нэр:')
	class Meta:
		model = Tasag
		fields = ['phone', 'mail']

	def clean_dep_name(self):
		data = self.cleaned_data['dep_name']
		if Tasag.objects.filter(dep_name__in =  TasagList.objects.filter(name = data)):
			raise forms.ValidationError(u"Системд бүртгэлтэй байна")
		return data

class TushaalForm(f.ModelForm):
	position_name = forms.CharField(label = 'Албан тушаалын нэр:')
	class Meta:
		model = AlbanTushaal
		exclude = ['baiguullaga','begin_time', 'end_time','created_by', 'status', 'position_name']

	def __init__(self, baiguullaga = None, *args, **kwargs):
		super(TushaalForm, self).__init__(*args, **kwargs)
		if baiguullaga:
			self.baiguullaga = baiguullaga
			self.fields['dep_id'].queryset = Tasag.objects.filter(baiguullaga = baiguullaga)
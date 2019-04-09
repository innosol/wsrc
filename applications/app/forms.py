#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
from django import forms as f
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from captcha.fields import CaptchaField
from . import validate
from .models import *
from django.contrib.auth import authenticate


class LoginForm(f.Form):
	username = f.CharField(label = u"Нэвтрэх нэр",widget = f.TextInput(attrs = {'class':'span12', 'placeholder':'нэвтрэх нэр' }))
	password = f.CharField(label = u"Нууц үг",widget = f.PasswordInput(attrs = {'class':'span12', 'placeholder':'нууц үг'}))

	def clean(self):
		cleaned_data = super(LoginForm, self).clean()
		if self.is_valid():
			a = cleaned_data['username']
			b = cleaned_data['password']
			user = authenticate(username=a, password=b)
			if user is not None:
				if not user.is_active:
					raise f.ValidationError(_(u'Хэрэглэгчид хандах эрх олгогдоогүй байна'), code='invalid')
			else:
				raise f.ValidationError(_(u'Хэрэглэгчийн нэр эсвэл нууц үг буруу байна'), code='invalid')
		return cleaned_data

class BaiguullagaForm(f.ModelForm):
	reg_num = f.CharField(label = 'Байгууллагын РД')
	ubd = f.CharField(label = 'Байгууллагын улсын бүртгэлийн дугаар')
	org_name = f.CharField(label = 'Байгууллагын нэр')
	
	class Meta:
		model = Baiguullaga

		exclude = ['reg_num','ubd','org_name','begin_time','end_time', 'created_by',  'status']
		          
		widgets = {
		'org_type': f.Select(attrs={'class':'input-large', }),
		'org_date': f.DateInput(attrs={'class':'input-large', 'placeholder':'2016-1-1'}),
		'phone': f.TextInput(attrs={'class':'input-large', }),
		'e_mail': f.EmailInput(attrs={'class':'input-large', }),
		'fax': f.TextInput(attrs={'class':'input-large', }),
		'post': f.TextInput(attrs={'class':'input-large', }),
		'tax': f.Select(attrs={'class':'input-large', }),
		'city': f.Select(attrs={'class':'input-large', }),
		'district': f.Select(attrs={'class':'input-large', }),
		'khoroo': f.Select(attrs={'class':'input-large', }),
		'address': f.TextInput(attrs={'class':'input-large', }),
		'tovch_taniltsuulga': f.Textarea(attrs = {'class':'org_description'}),
		}
class TZE_updateForm(f.ModelForm):
	class Meta:
		model = TZE
		exclude = ['reg_num', 'ubd', 'org_name', 'org_type', 'begin_time', 'end_time', 'created_by', 'status']

		widgets = {
		'org_date': f.DateInput(attrs={'class':'input-large', 'placeholder':'2016-1-1'}),
		'phone': f.TextInput(attrs={'class':'input-large', }),
		'e_mail': f.EmailInput(attrs={'class':'input-large', }),
		'fax': f.TextInput(attrs={'class':'input-large', }),
		'post': f.TextInput(attrs={'class':'input-large', }),
		'tax': f.Select(attrs={'class':'input-large', }),
		'address': f.TextInput(attrs={'class':'input-large', }),
		'tovch_taniltsuulga': f.Textarea(attrs = {'class':'org_description', 'placeholder':'Байгууллагын товч танилцуулга оруулна уу.', 'style':'width: 80%;'}),
		}
class TZEForm(f.ModelForm):
	ovog = f.CharField(label = u'Захирлын овог:', help_text = u'Кириллээр бичнэ үү!', widget = f.TextInput(attrs = {'class':'input-large'}))
	ner = f.CharField(label = u'Захирлын нэр:', help_text = u'Кириллээр бичнэ үү!', widget = f.TextInput(attrs = {'class':'input-large'}))
	register = f.CharField(label = u'Захирлын РД:', help_text = u'Регистерийн дугаараа оруулна уу!', widget = f.TextInput(attrs = {'class':'input-large'}), required = False)
	mail = f.EmailField(label = u'Захирал э-мэйл:', help_text = u'Э-мэйл хаягаа оруулна уу!', widget = f.EmailInput(attrs = {'class':'input-large'}), required = False)

	class Meta:
		model = TZE
		fields = ['reg_num', 'ubd', 'org_name', 'org_type']
		help_texts = {
		'reg_num': _('7 оронтой тоо оруулна уу!'),
		'org_name': _('Кириллээр бичнэ үү!'),
		}
		widgets = {
		'reg_num':f.TextInput(attrs = {'class' : 'input-large', 'maxlength':5}),
		'ubd':f.TextInput(attrs = {'class' : 'input-large'}),
		'org_name':f.TextInput(attrs = {'class' : 'input-large'}),
		}

	#def clean_register(self):
	#	data = self.cleaned_data['register']
	#	validate.clean_reg(data)
	#	if Ajiltan.objects.filter(status = True, emp_reg = data).count() > 0:
	#		raise f.ValidationError(u'Системд бүртгэлтэй байна')
	#	return data
	def clean_ovog(self):
		data = self.cleaned_data['ovog']
		validate.kirill(data)
		return data

	def clean_ner(self):
		data = self.cleaned_data['ner']
		validate.kirill(data)
		return data

	def clean_reg_num(self):
		data = self.cleaned_data['reg_num']
		if TZE.objects.filter(reg_num = data).count() > 0:
			raise f.ValidationError(u'Системд бүртгэлтэй байна')
		return data

	def clean_ubd(self):
		data = self.cleaned_data['ubd']
		if TZE.objects.filter(ubd = data).count() > 0:
			raise f.ValidationError(u'Системд бүртгэлтэй байна')
		return data

	def clean_org_name(self):
		data = self.cleaned_data['org_name']
		if TZE.objects.filter(org_name = data).count() > 0:
			raise f.ValidationError(u'Системд бүртгэлтэй байна')
		return data

	

	def save(self):
		baiguullaga = super(TZEForm, self).save()
		baiguullaga.status = True
		baiguullaga.save()
		
		tasag = Tasag.objects.create(baiguullaga = baiguullaga, dep_name = 'Захиргаа, удирдлагын хэлтэс', status = True)
		at1 = AlbanTushaal.objects.create(dep_id = tasag, position_name = 'Захирал', status = True)

		reg = self.cleaned_data['register']
		#emp_birth = u'19%s-%s-%s' %(reg[2:4], reg[4:6], reg[6:8])
		#nas = timezone.now().year - int('19%s' %reg[2:4])
		#if int(reg[8:9])%2 == 1:
		#	gender = u'Эр'
		#else:
		#	gender = u'Эм'
		z = Ajiltan.objects.create(
			baiguullaga = baiguullaga,
			alban_tushaal = at1,
			emp_name = self.cleaned_data['ner'],
			emp_lname = self.cleaned_data['ovog'],
			emp_reg = reg,
			e_mail = self.cleaned_data['mail'],
		#	emp_birth = emp_birth,
			tasag = tasag,
		#	gender = gender,
			zereg = u'Удирдах ажилтан',
			status = True
			)
		return { 'baiguullaga':baiguullaga, 'z':z }


class TZE_handah_huselt_form(TZEForm):
	capfield = CaptchaField(label = 'Captcha')

	def clean_mail(self):
		data = self.cleaned_data['mail']
		if Ajiltan.objects.filter(e_mail = data).count() > 0:
			raise f.ValidationError(u'Системд бүртгэлтэй байна')
		return data

class ZZForm(BaiguullagaForm):
	class Meta(BaiguullagaForm.Meta):
		model = ZZ
		
class AlbanTushaalForm(f.Form):
	name = f.CharField()
	dep = f.CharField()
	status = f.BooleanField(required = False)

class EngineeringCertificateForm(f.ModelForm):
	class Meta:
		model = EngineeringCertificate
		exclude = ['emp','begin_time', 'end_time','created_by', 'status']

class AccountForm(f.ModelForm):
	hide = f.IntegerField(widget = f.HiddenInput())
	class Meta:
		model = User
		fields = '__all__'

	def clean(self):
		cleaned_data = super(AccountForm, self).clean()
		a = cleaned_data['hide']
		c = Ajiltan.objects.get(id = a)
		b = User.objects.filter(user_id = c)
		if b:
			raise ValidationError(_(u'Хэрэглэгч бүртгэгдсэн байна'), code='invalid')
		return self.cleaned_data

class TusgaiZuvshuurulForm(f.ModelForm):
	class Meta:
		model = TZ
		exclude = ['begin_time', 'end_time','created_by', 'status']
		widgets = {
		}



class TZPictureForm(f.ModelForm):
	class Meta:
		model = TZPicture
		exclude = ['tze', 'tz']

''' Цэвэр усны шинжилгээ'''
class AnalysisWaterForm(f.ModelForm):
	class Meta:
		model = AnalysisWater
		exclude = ['tze','begin_time', 'end_time','created_by', 'status']
		widgets = {
		'ognoo': f.TextInput(attrs={'placeholder':'2005-10-04'}),
		}
	def save(self, commit=True):
		m=super(AnalysisWaterForm, self).save(commit=False)
		if commit:
			m.save()
		return m
class UA_water_analysisForm(f.ModelForm):
	class Meta:
		model = UA_water_analysis
		exclude = ['tze','begin_time', 'end_time','created_by', 'status']
		widgets = {
		'ognoo': f.TextInput(attrs={'placeholder':'2005-10-04'}),
		}	
	def save(self, commit=True):
		m=super(UA_water_analysisForm, self).save(commit=False)
		if commit:
			m.save()
		return m

class TZ_huselt_water_analysisForm(f.ModelForm):
	class Meta:
		model = TZ_huselt_water_analysis
		exclude = ['tze','begin_time', 'end_time','created_by', 'status']
		widgets = {
		'ognoo': f.TextInput(attrs={'placeholder':'2005-10-04'}),
		}	
	def save(self, commit=True):
		m=super(TZ_huselt_water_analysisForm, self).save(commit=False)
		if commit:
			m.save()
		return m


''' Бохир усны шинжилгээ'''
class AnalysisBohirForm(f.ModelForm):
	class Meta:
		model = AnalysisBohir
		exclude = ['tze','begin_time', 'end_time','created_by', 'status']
		widgets = {
		'ognoo': f.TextInput(attrs={'placeholder':'2005-10-04'}),
		}
	def save(self, commit=True):
		m=super(AnalysisBohirForm, self).save(commit=False)
		if commit:
			m.save()
		return m	

class TZ_huselt_bohir_analysisForm(f.ModelForm):
	class Meta:
		model = TZ_huselt_bohir_analysis
		exclude = ['tze', 'begin_time', 'end_time', 'created_by', 'status']
		widgets = {
			'ognoo': f.TextInput(attrs={'placeholder':'2005-10-04'}),
		}
	def save(self, commit=True):
		m=super(TZ_huselt_bohir_analysisForm, self).save(commit=False)
		if commit:
			m.save()
		return m




''' baiguullaga menu deer ashiglagdah formuud '''
''' Орон тооны бүтцийн схем form  '''
class SchemaForm(f.ModelForm):
	class Meta:
		model = OronTooniiSchema
		exclude = ['tze','begin_time', 'end_time','created_by', 'status']
		help_texts = {
			'schema': 'pdf, doc, jpg, jpeg, png өргөтгөлтэй, 5MB-аас бага хэмжээтэй зурган файл сонгоно уу.',
		}
''' Хангагч байгуулагын гэрээ form '''
class HBGereeForm(f.ModelForm):
	class Meta:
		model = HangagchBaiguullaga
		exclude = ['tze','begin_time', 'end_time','created_by', 'status']
''' Засаг даргын тодорхойлолт form '''
class ZDTForm(f.ModelForm):
	class Meta:
		model = ZDTodorhoilolt
		exclude = ['tze','begin_time', 'end_time','created_by', 'status']
	def clean_todorhoilolt_picture(self):
		data = self.cleaned_data['todorhoilolt_picture']
		validate.validate_file_extension(data)
		return data
''' Татварын тодорхойлолт form '''
class TaxTodorhoiloltForm(f.ModelForm):
	class Meta:
		model = TaxTodorhoilolt
		exclude = ['tze','begin_time', 'end_time','created_by', 'status']
''' Аудит дүгнэлт form '''
class AuditDugneltForm(f.ModelForm):
	class Meta:
		model = AuditDugnelt
		exclude = ['tze','begin_time', 'end_time','created_by', 'status']
''' Норм стандарт форм '''

''' Улсын Акт form '''
class UlsiinAktForm(f.ModelForm):
	class Meta:
		model = UlsiinAkt
		exclude = ['tze','begin_time', 'end_time','created_by', 'status']
'''Ашиглалтыг нь хариуцаж байгаа барилга байгууламж '''
class ABBForm(f.ModelForm):
	class Meta:
		model = ABB
		#exclude = ['tze','begin_time', 'end_time','created_by', 'status']
		fields = ['city', 'district', 'khoroo', 'address','barilga_ner', 'niit', 'tooluurjilt_too', 'aan_too', 'tooluurjilt_too_aan', 'photo', 'ulsiinakt', 'geree',]
		widgets = {
			'niit': f.TextInput(),
			'tooluurjilt_too': f.TextInput(),
			'aan_too': f.TextInput(),
			'tooluurjilt_too_aan': f.TextInput(),
		}
		help_texts = {
			'photo': 'jpg, jpeg, png, gif өргөтгөлтэй, 5MB-аас бага хэмжээтэй зурган файл сонгоно уу.',
			'ulsiinakt': 'pdf, doc, jpg, jpeg, png өргөтгөлтэй, 5MB-аас бага хэмжээтэй зурган файл сонгоно уу.',
			'geree': 'pdf, doc, jpg, jpeg, png өргөтгөлтэй, 5MB-аас бага хэмжээтэй зурган файл сонгоно уу.',
		}

	def clean(self):
		cleaned_data = super(ABBForm, self).clean()
		if self.is_valid():
			b = cleaned_data['city']
			c = cleaned_data['district']
			d = cleaned_data['khoroo']
			e = cleaned_data['address']
			h = cleaned_data['barilga_ner']
		#	if aa < a
		#		raise f.ValidationError(u'Тоолууржилтын тоо хэтэрсэн байна')		
			if ABB.objects.filter(city = b, district=c, khoroo=d, barilga_ner=h, status = True).count()>0:
				raise f.ValidationError(_(u'Барилга системд бүртгэлтэй байна'))
			return cleaned_data

	'''Гүний худгийн форм'''













''' hunii noots menu deer ashiglagdah formuud '''
class TZEAForm(f.ModelForm):
		
	class Meta:
		model = Ajiltan
		fields = ['baiguullaga','emp_lname', 'emp_name', 'emp_reg','picture', 'emp_birth', 'ndd', 'gender', 'tasag',
		          'alban_tushaal', 'naj', 'bolovsroliin_tuvshin','tzeaj', 'phone', 'e_mail', 'zereg']
		widgets = {
		'baiguullaga': f.TextInput(attrs={'style': 'display:none;', 'readonly':'True'}),
		'emp_lname': f.TextInput(attrs={'class' : 'input-long', 'placeholder':u'Бат'}),
		'emp_name' : f.TextInput(attrs={'class' : 'input-long','placeholder':u'Дорж'}),
		'emp_reg' : f.TextInput(attrs={'class' : 'input-medium','placeholder':u'АА77121201', 'onchange':'update()'}),
		'emp_birth' : f.DateInput(attrs={'class' : 'input-small','placeholder':'2015-12-1', 'readonly':'true'}),
		'ndd' : f.TextInput(attrs={'class' : 'input-medium','placeholder':'1234567'}),
		'gender' : f.TextInput(attrs={'class' : 'input-mini', 'readonly': True}),
		#'alban_tushaal' : f.Select(attrs={'class' : 'chained'}),
		'bolovsroliin_tuvshin' : f.Select(attrs={'class' : 'input-medium', 'onchange':'update_mer_zereg()'}),
		'naj' : f.TextInput(attrs={'class' : 'input-medium','placeholder':'1'}),
		'tzeaj' : f.TextInput(attrs={'class' : 'input-medium','placeholder':'1'}),
		'phone' : f.TextInput(attrs={'class' : 'input-medium','placeholder':'99887766'}),
		'e_mail' : f.EmailInput(attrs={'class' : 'input-medium','placeholder':'email@gmail.com'}),
		}
		help_texts = {
			'picture': 'jpg, jpeg, png, gif өргөтгөлтэй, 5MB-аас бага хэмжээтэй зурган файл сонгоно уу.',
		}
	def __init__(self, user_id = None, *args, **kwargs):
		super(TZEAForm, self).__init__(*args, **kwargs)
		self.fields['bolovsroliin_tuvshin'].required = False
		self.fields['naj'].required = True
		self.fields['tzeaj'].required = True
		self.fields['ndd'].required = True
		

	def clean_emp_reg(self):
		data = self.cleaned_data['emp_reg']
		validate.clean_reg(data)
		if Ajiltan.objects.filter(emp_reg = self.cleaned_data['emp_reg']):
			raise f.ValidationError(u'Системд бүртгэлтэй байна')
		return data

	def clean_emp_name(self):
		data = self.cleaned_data['emp_name']
		validate.kirill(data)
		return data

	def clean_emp_lname(self):
		data = self.cleaned_data['emp_lname']
		validate.kirill(data)
		return data

	def clean_ndd(self):
		data = self.cleaned_data['ndd']
		if Ajiltan.objects.filter(ndd = self.cleaned_data['ndd']):
			raise f.ValidationError(u'Системд бүртгэлтэй байна')
		return data

	def clean_e_mail(self):
		data = self.cleaned_data['e_mail']
		if Ajiltan.objects.filter(e_mail = self.cleaned_data['e_mail']):
			if data:
				raise f.ValidationError(u'Системд бүртгэлтэй байна')
		return data

	def clean_school_name(self):
		data = self.cleaned_data['school_name']
		if self.cleaned_data['mer_zereg']:
			if not data:
				raise f.ValidationError("Энэ талбарыг бөглөнө үү")
		return data

	def clean_diplom_num(self):
		data = self.cleaned_data['diplom_num']
		if self.cleaned_data['mer_zereg']:
			if not data:
				raise f.ValidationError("Энэ талбарыг бөглөнө үү")
		return data

	def clean_degree(self):
		data = self.cleaned_data['degree']
		if self.cleaned_data['mer_zereg']:
			if not data:
				raise f.ValidationError("Энэ талбарыг бөглөнө үү")
		return data

	def clean_diplom_picture(self):
		data = self.cleaned_data['diplom_picture']
		if self.cleaned_data.get('mer_zereg'):
			if not data:
				raise f.ValidationError(u"Энэ талбарыг бөглөнө үү")
		return data

	def clean_job_name(self):
		data = self.cleaned_data.get('job_name')
		if 'mergejliin_unemleh_checkbox' in self.data:
			if not data:
				raise f.ValidationError(u'Энэ талбарыг бөглөнө үү')
		return data

	def clean_job_picture(self):
		data = self.cleaned_data.get('job_picture')
		if 'mergejliin_unemleh_checkbox' in self.data:
			if not data:
				raise f.ValidationError("Энэ талбарыг бөглөнө үү")
		return data

	def clean_certificate_num(self):
		data = self.cleaned_data.get('certificate_num')
		if 'zovloh_engineer_cert_checkbox' in self.data:
			if not data:
				raise f.ValidationError("Энэ талбарыг бөглөнө үү")
		return data

	def clean_certificate_picture(self):
		data = self.cleaned_data.get('certificate_picture')
		if 'zovloh_engineer_cert_checkbox' in self.data:
			if not data:
				raise f.ValidationError("Энэ талбарыг бөглөнө үү")
		return data
	def save(self, commit=True):
		m=super(TZEAForm, self).save(commit=False)
		if commit:
			m.save()
		return m
class TZEAUpdateForm(TZEAForm):


	def __init__(self, user_id = None, *args, **kwargs):
		super(TZEAUpdateForm, self).__init__(*args, **kwargs)
		self.__user = user_id

	def clean_emp_reg(self):
		a = Ajiltan.objects.exclude(id = self.__user)
		return self.cleaned_data['emp_reg']

	def clean_ndd(self):
		return self.cleaned_data['ndd']

	def clean_e_mail(self):
		return self.cleaned_data['e_mail']

	def clean_diplom_num(self):
		return self.cleaned_data['diplom_num']

	def clean_diplom_picture(self):
		return self.cleaned_data['diplom_picture']

	def clean_degree(self):
		return self.cleaned_data['degree']

	def clean_school_name(self):
		return self.cleaned_data['school_name']

	def clean_job_name(self):
		return self.cleaned_data['job_name']

	def clean_job_picture(self):
		return self.cleaned_data['job_picture']

	def clean_certificate_num(self):
		return self.cleaned_data['certificate_num']

	def clean_certificate_picture(self):
		return self.cleaned_data['certificate_picture']












''' tonog tohooromj menu deer ashiglagdah formuud '''
class Gunii_Hudag_insertForm(f.ModelForm):
	class Meta:
		model = Hudag
		fields=[
			'city',
			'district',
			'khoroo',
			'hudag_address',
			'ashiglaltand_orson_ognoo',
			'huchin_chadal',
			'mark',
			'country',
			'nasos_ognoo',
			'olborloj_bui_us',
			'tsoonog',
			'haruul',
			'tailbar',
			'outside_picture',
			'inside_picture',
		]
		widgets = {
		'ashiglaltand_orson_ognoo' : f.TextInput(attrs={'class' : 'input-small','placeholder':'2016'}),
		'tsoonog' : f.TextInput(),
		'huchin_chadal': f.TextInput(),
		'olborloj_bui_us': f.TextInput(),
		}
		help_texts = {
			'outside_picture': 'jpg, jpeg, png, gif өргөтгөлтэй, 5MB-аас бага хэмжээтэй зурган файл сонгоно уу.',
			'inside_picture': 'jpg, jpeg, png, gif өргөтгөлтэй, 5MB-аас бага хэмжээтэй зурган файл сонгоно уу.',
		}
class NasosForm(f.ModelForm):
	class Meta:
		model = NasosStants
		fields=[
			'nasos_torol',
			'nasos_name',
			'city',
			'district',
			'khoroo',
			'nasos_address',
			'ashiglaltand_orson_ognoo',
			'nasos_ajillagaa',
			'picture_outside',
			'picture_inside'
		]
		widgets = {
		'ashiglaltand_orson_ognoo' : f.TextInput(attrs={'class' : 'input-small','placeholder':'2016'}),
		}
		help_texts = {
			'picture_inside': 'jpg, jpeg, png, gif өргөтгөлтэй, 5MB-аас бага хэмжээтэй зурган файл сонгоно уу.',
			'picture_outside': 'jpg, jpeg, png, gif өргөтгөлтэй, 5MB-аас бага хэмжээтэй зурган файл сонгоно уу.',
		}
	
	def clean(self):
		cleaned_data = self.cleaned_data
		if self.is_valid():
             
			a = cleaned_data['nasos_torol']
			b = cleaned_data['nasos_name']
			c = cleaned_data['city']
			d = cleaned_data['district']
			e = cleaned_data['khoroo']
			h = cleaned_data['nasos_address']

			if NasosStants.objects.filter(nasos_torol= a, nasos_name = b, city=c, district=d, khoroo=e, nasos_address=h).count()>0:
			
				raise f.ValidationError(_(u'Системд бүртгэлтэй байна'))
			return cleaned_data
	
	def save(self, commit=True):
		m=super(NasosForm, self).save(commit=False)
		if commit:
			m.save()
		return m
class Ts_baiguulamjForm(f.ModelForm):
	class Meta:
		model = Ts_baiguulamj
		fields = [
			'torol',
			'mehanik',
			'biologi',
			'fizik',
			'huchin_chadal',
			'ashiglaltand_orson_ognoo',
			'technology_schema',
		]
		widgets = {
		'ashiglaltand_orson_ognoo' : f.TextInput(attrs={'class' : 'input-small','placeholder':'2016'}),
		'huchin_chadal': f.TextInput(),
		}
		help_texts = {
			'technology_schema': 'jpg, jpeg, png, gif өргөтгөлтэй, 5MB-аас бага хэмжээтэй зурган файл сонгоно уу.',
		}
class UsanSanForm(f.ModelForm):
	class Meta:
		model = UsanSan
		fields= [
			'usansan_helber',
			'city',
			'district',
			'khoroo',
			'usansan_address',
			'ashiglaltand_orson_ognoo',
			'bagtaamj',
			'huurai_hlor',
			'shingen_hlor',
			'davsnii_uusmal',
			'usansan_haruul',
			]
	
		widgets = {
		'ashiglaltand_orson_ognoo' : f.TextInput(attrs={'class' : 'input-small','placeholder':'2016'}),
		'bagtaamj': f.TextInput(),
		}
	def clean(self):

		cleaned_data = self.cleaned_data
		if self.is_valid():
			a = cleaned_data['usansan_helber']
			c = cleaned_data['city']
			d = cleaned_data['district']
			e = cleaned_data['khoroo']
			h = cleaned_data['usansan_address']

			if UsanSan.objects.filter(usansan_helber= a, city=c, district=d, khoroo=e, usansan_address=h).count()>0:
			
				raise f.ValidationError(_(u'Тухайн байршилд усан сан бүртгэлтэй байна'))
			return cleaned_data
class UsDamjuulahBairForm(f.ModelForm):
	class Meta:
		model = UsDamjuulahBair
		fields = ['torol', 'ashiglaltand_orson_ognoo','picture','bair_uzeli_holbolt_schema',]
		widgets = {
		'ashiglaltand_orson_ognoo' : f.TextInput(attrs={'class' : 'input-small','placeholder':'2016'}),
		}
		help_texts = {
			'picture': 'jpg, jpeg, png, gif өргөтгөлтэй, 5MB-аас бага хэмжээтэй зурган файл сонгоно уу.',
			'bair_uzeli_holbolt_schema': 'jpg, jpeg, png, gif өргөтгөлтэй, 5MB-аас бага хэмжээтэй зурган файл сонгоно уу.',
		}
	
class UsTugeehBairForm(f.ModelForm):
	class Meta:
		model = UsTugeehBair
		fields = [
			'barilga',
			'dugaar',
			'city',
			'district',
			'khoroo',
			'ustugeeh_address',
			'ashiglaltand_orson_ognoo',
			'ustugeeh_sav',
			'savnii_bagtaamj',
			'borluulj_bui_us',
			'hun_amiin_too',
			'gadna_tal_picture',
			'dotor_tal_picture'
			]
		widgets = {
		'ustugeeh_sav': f.CheckboxInput(attrs={'onchange':'ustugeeh_sav_check_changed()'}),
		'ashiglaltand_orson_ognoo' : f.TextInput(attrs={'class' : 'input-small','placeholder':'2016'}),
		'hun_amiin_too': f.TextInput(),
		'borluulj_bui_us': f.TextInput(),
		'dugaar': f.TextInput(),
		'savnii_bagtaamj': f.TextInput(),
		}
		help_texts = {
			'gadna_tal_picture': 'jpg, jpeg, png, gif өргөтгөлтэй, 5MB-аас бага хэмжээтэй зурган файл сонгоно уу.',
			'dotor_tal_picture': 'jpg, jpeg, png, gif өргөтгөлтэй, 5MB-аас бага хэмжээтэй зурган файл сонгоно уу.',
		}

	def save(self, commit=True):
		m=super(UsTugeehBairForm, self).save(commit=False)
		if m.ustugeeh_sav == False:
			m.savnii_bagtaamj = None
		if commit:
			m.save()
		return m
	def clean(self):
		cleaned_data = self.cleaned_data
		if self.is_valid():
			a = cleaned_data['barilga']
			b = cleaned_data['dugaar']
			c = cleaned_data['city']
			d = cleaned_data['district']
			e = cleaned_data['khoroo']
			h = cleaned_data['ustugeeh_address']

			if UsTugeehBair.objects.filter(barilga= a, dugaar = b, city=c, district=d, khoroo=e, ustugeeh_address=h).count()>0:
				raise f.ValidationError(_(u'Системд бүртгэлтэй байна'))
			return cleaned_data
	def clean_savnii_bagtaamj(self):
		if self.cleaned_data['ustugeeh_sav'] and not self.cleaned_data['savnii_bagtaamj']:
				raise f.ValidationError(_(u'Ус нөөцлөх савны багтаамжийг оруулна уу.'))
		return self.cleaned_data['savnii_bagtaamj']
class LabForm(f.ModelForm):
	class Meta:
		model = Lab
		exclude = ['tze','begin_time', 'end_time','created_by', 'status', 'approved']
		widgets = {
		'ashiglaltand_orson_ognoo' : f.TextInput(attrs={'class' : 'input-small','placeholder':'2016'}),
		'tailbar' : f.TextInput(attrs={'placeholder':'Дутуу ажиллагааны тайлбар'}),
		'shinjilgee_count': f.TextInput(),
		}
		
	def save(self, commit=True):
		m=super(LabForm, self).save(commit=False)
		if commit:
			m.save()
		return m
	def clean_tailbar(self):
		tailbar = self.cleaned_data['tailbar']
		try:
			ajillagaa = self.cleaned_data['ajillagaa']
		except KeyError:
			return tailbar
		if not tailbar and ajillagaa != u'Бүрэн ажиллагаатай':
			raise f.ValidationError(u'Энэ талбарыг бөглөнө үү.')
		return tailbar
class Sh_suljeeForm(f.ModelForm):
	class Meta:
		model = Sh_suljee
		fields = ['shugam_helber','shugam_torol','shugam_urt','hudgiin_too', 'gemtliin_too', 'schema',]
		widgets = {
			'shugam_torol': f.Select(attrs = {'id': 'torol'}),
			'shugam_urt': f.TextInput(),
			'hudgiin_too': f.TextInput(),
			'gemtliin_too': f.TextInput(),
		}
		help_texts = {
			'schema': 'jpg, jpeg, png, gif өргөтгөлтэй, 5MB-аас бага хэмжээтэй зурган файл сонгоно уу.',
		}
class CarForm(f.ModelForm):
	class Meta:
		model = Car
		exclude = ['tze','begin_time', 'end_time','created_by', 'status']
class WaterCarForm(f.ModelForm):
	class Meta:
		model = WaterCar
		exclude = ['tze','begin_time', 'end_time','created_by', 'status']
		widgets = {
			'hun_am_too': f.TextInput(),
			'utb_too': f.TextInput(),
			'aanb_too': f.TextInput(),
			'daats': f.TextInput(),
			'us': f.TextInput(),
		}
		help_texts = {
			'gerchilgee_picture': 'jpg, jpeg, png, gif өргөтгөлтэй, 5MB-аас бага хэмжээтэй зурган файл сонгоно уу.',
		}

	def clean_no(self):
		data = self.cleaned_data['no']
		if Car.objects.filter(no = self.cleaned_data['no']):
			raise f.ValidationError(u'Машины дугаар системд бүртгэлтэй байна')
		return data
class BohirCarForm(f.ModelForm):
	class Meta:
		model = BohirCar
		exclude = ['tze','begin_time', 'end_time','created_by', 'status']
		widgets = {
			'gereet_too': f.TextInput(),
			'duudlaga_too': f.TextInput(),
			'daats': f.TextInput(),
			'us': f.TextInput(),
		}
		help_texts = {
			'gerchilgee_picture': 'jpg, jpeg, png, gif өргөтгөлтэй, 5MB-аас бага хэмжээтэй зурган файл сонгоно уу.',
			'avtomashin_tevsh': 'jpg, jpeg, png, gif өргөтгөлтэй, 5MB-аас бага хэмжээтэй зурган файл сонгоно уу.',
		}

	def clean_no(self):
		data = self.cleaned_data['no']
		if Car.objects.filter(no = self.cleaned_data['no']):
			raise f.ValidationError(u'Машины дугаар системд бүртгэлтэй байна')
		return data
class EquipmentForm(f.ModelForm):
	class Meta:
		model = Equipment
		exclude = ['tze','begin_time', 'end_time','created_by', 'status']
		widgets = {
			'too': f.TextInput(),
			'huchin_chadal': f.TextInput(),
			'balans_une': f.TextInput(),
			'elegdel_huvi': f.TextInput(),
		}
	def clean_elegdel_huvi(self):
		data = self.cleaned_data['elegdel_huvi']
		if data >= 101 :
			raise f.ValidationError(u'100 % хүртэлх тоо бичнэ үү')
		return data

class NasosUpdateForm(NasosForm):
	def __init__(self, *args, **kwargs):
		super(NasosUpdateForm, self).__init__(*args, **kwargs)
		self.__nasos = kwargs['instance']

	def clean(self):
		cleaned_data = self.cleaned_data
		if self.is_valid():
			aa = cleaned_data['nasos_torol']
			b = cleaned_data['nasos_name']
			c = cleaned_data['city']
			d = cleaned_data['district']
			e = cleaned_data['khoroo']
			h = cleaned_data['nasos_address']
			a = NasosStants.objects.exclude(id = self.__nasos.id).filter(status=True)
			if a.filter(nasos_torol= aa, nasos_name = b, city=c, district=d, khoroo=e, nasos_address=h):
				raise f.ValidationError(u'Системд бүртгэлтэй байна')
			return cleaned_data
class UsanSanUpdateForm(UsanSanForm):
	def __init__(self, usansan_id = None, *args, **kwargs):
		super(UsanSanUpdateForm, self).__init__(*args, **kwargs)
		self.__usansan = usansan_id

	def clean(self):
		cleaned_data = self.cleaned_data
		if self.is_valid():
			a = cleaned_data['usansan_helber']
			c = cleaned_data['city']
			d = cleaned_data['district']
			e = cleaned_data['khoroo']
			h = cleaned_data['usansan_address']
			aa = UsanSan.objects.exclude(id = self.__usansan)
			if aa.filter(usansan_helber= a, city=c, district=d, khoroo=e, usansan_address=h):
				raise f.ValidationError(u'Системд бүртгэлтэй байна')
			return cleaned_data
class UsTugeehBairUpdateForm(UsTugeehBairForm):
	def __init__(self, ustugeeh_id = None, *args, **kwargs):
		super(UsTugeehBairUpdateForm, self).__init__(*args, **kwargs)
		self.__ustugeeh = ustugeeh_id

	def clean(self):
		cleaned_data = self.cleaned_data
		if self.is_valid():
			a = cleaned_data['barilga']
			b = cleaned_data['dugaar']
			c = cleaned_data['city']
			d = cleaned_data['district']
			e = cleaned_data['khoroo']
			h = cleaned_data['ustugeeh_address']
			aa = UsTugeehBair.objects.exclude(id = self.__ustugeeh)
			if aa.filter(barilga= a, dugaar = b, city=c, district=d, khoroo=e, ustugeeh_address=h):
				raise f.ValidationError(u'Системд бүртгэлтэй байна')
			return cleaned_data
class WaterCarUpdateForm(WaterCarForm):
	def __init__(self, watercar_id = None, *args, **kwargs):
		super(WaterCarUpdateForm, self).__init__(*args, **kwargs)
		self.__watercar = watercar_id

	def clean_no(self):
		data = self.cleaned_data['no']
		a = Car.objects.exclude(id = self.__watercar)
		if a.filter(no = self.cleaned_data['no']):
			raise f.ValidationError(u'Машины дугаар системд бүртгэлтэй байна')
		return data
class BohirCarUpdateForm(BohirCarForm):
	def __init__(self, bohircar_id = None, *args, **kwargs):
		super(BohirCarUpdateForm, self).__init__(*args, **kwargs)
		self.__bohircar = bohircar_id

	def clean_no(self):
		data = self.cleaned_data['no']
		a = Car.objects.exclude(id = self.__bohircar)
		if a.filter(no = self.cleaned_data['no']):
			raise f.ValidationError(u'Машины дугаар системд бүртгэлтэй байна')
		return data


''' Бүх гүний худгуудыг нэгтгэсэн байршлын схем зураг '''
class HudagNegtsgesenBairshliinZuragForm(f.ModelForm):
	class Meta:
		model = HudagNegtsgesenBairshliinZurag
		fields = ['comments','bairshliin_picture']
		widgets = {
		'comments': f.Textarea(attrs={'style': 'width: 340px;', 'placeholder': 'Зургийн тайлбараа оруулна уу.(250)'})
		}
		help_texts = {
		'bairshliin_picture': 'jpg, jpeg, png, gif өргөтгөлтэй, 5MB-аас бага хэмжээтэй зурган файл сонгоно уу.',
		}












''' tusgai zovshoorol menu deer ashiglagdah formuud '''
''' Үйлдвэрийн технологийн схем form '''
class UildverTechnologyForm(f.ModelForm):
	class Meta:
		model = UildverTechnology
		exclude = ['tze','begin_time', 'end_time','created_by', 'status']

''' Ажлын байр form '''
class AjliinBairForm(f.ModelForm):
	class Meta:
		model = AjliinBair
		exclude = ['tze','begin_time', 'end_time','created_by', 'status']

''' Байгууллагын лабораторийн шинжилгээнд өгсөн Мэргэжлийн Хяналтын Газрын дүгнэлт form '''
class MergejliinHyanaltForm(f.ModelForm):
	class Meta:
		model = MergejliinHyanalt
		exclude = ['tze','begin_time', 'end_time','created_by', 'status']

''' Ус ашиглах зөвшөөрөл '''
class UsZuvshuurulForm(f.ModelForm):
	class Meta:
		model = UsZuvshuurul
		exclude = ['tze','begin_time', 'end_time','created_by', 'status']
		help_texts = {
			'dugnelt': 'pdf, doc, jpg, jpeg, png өргөтгөлтэй, 5MB-аас бага хэмжээтэй зурган файл сонгоно уу.',
			'zuvshuurul': 'pdf, doc, jpg, jpeg, png өргөтгөлтэй, 5MB-аас бага хэмжээтэй зурган файл сонгоно уу.',
			'geree': 'pdf, doc, jpg, jpeg, png өргөтгөлтэй, 5MB-аас бага хэмжээтэй зурган файл сонгоно уу.',
		}
''' Санхүүгийн тайлан '''
class SanhuuTailanForm(f.ModelForm):
	class Meta:
		model = SanhuuTailan
		exclude = ['tze','begin_time', 'end_time','created_by', 'status']
		help_texts = {
			'tailan': 'pdf, doc, jpg, jpeg, png өргөтгөлтэй, 5MB-аас бага хэмжээтэй зурган файл сонгоно уу.',
		}

















''' handah erh menu deer ashiglagdah formuud '''
''' uil ajillagaanii tailan menu deer ashiglagdah formuud '''
''' sanhuugiin medee menu deer ashiglagdah formuud '''
''' sanhuugiin tailan menu deer ashiglagdah formuud '''
''' GSHUT menu deer ashiglagdah formuud '''







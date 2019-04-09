# -*- coding:utf-8 -*-
from django import forms as f
from applications.app.models import Aimag, Sum, ZZ, Tasag, AlbanTushaal, Ajiltan, Certificate
from applications.app.models import Rel_baig_zz_ajilchid, TZ_Huselt, GShU, BB, Car, ABB, Equipment

# uilsee code 

class TZ_huselt_tza_huvaarilahForm(f.ModelForm):
	def __init__(self, *args, **kwargs):
		super(TZ_huselt_tza_huvaarilahForm, self).__init__(*args, **kwargs)
		zz = ZZ.objects.all()[0]
		tasag_tza = Tasag.objects.get(baiguullaga = zz, dep_name = 'Тусгай зөвшөөрлийн алба')
		tza = AlbanTushaal.objects.filter(dep_id = tasag_tza, position_name__icontains = 'мэргэжилтэн')
		self.fields['tza_mergejilten'] = f.ModelChoiceField(label = 'ТЗА мэргэжилтэн', queryset = Ajiltan.objects.filter(baiguullaga = zz, status = True, alban_tushaal = tza), required = True)

	class Meta:
		model = TZ_Huselt
		fields = ['tza_mergejilten']


class TZ_huselt_hural_tovlohForm(f.Form):
	hural_date = f.DateField(label = 'Хурал болох огноо', widget=f.TextInput(attrs={'placeholder':'2016-02-20'}))

class Ajliin_heseg_date_tovlohForm(f.Form):
	date = f.DateField(label = 'Ажлын хэсэг очиж шалгах огноо', widget=f.TextInput(attrs={'placeholder':'2016-02-20'}))

class ShalgajDuussanForm(f.Form):
	check = f.BooleanField(label='Бүх бичиг баримтуудыг шалгаж дууслаа.')


class Material_check_form(f.Form):
	CHOICES=[('zovshoorson','Зөвшөөрсөн'),
		('hangaltgui','Хангалтгүй')]
	
	status = f.ChoiceField(choices=CHOICES, widget=f.RadioSelect(), label = 'Статус')
	tailbar = f.CharField(max_length = 200, widget=f.Textarea(attrs={'placeholder':'Компанийг материалаа зөв бүрдүүлэхэд туслахын тулд татгалзах болсон шалтгаанаа оруулна уу.',
																		'rows': 2,
                              											'cols': 50,
                              											'style': 'width:300px; height:100px;'}),
																label = 'Тайлбар',required=False)

class TZ_gerchilgee_change_tolov(f.ModelForm):
	class Meta:
		model = Certificate
		fields = ['tolov']
		labels = {
			'tolov': 'Төлөв'
		}

class TZ_gerchilgee_sungah_Form(f.ModelForm):
	class Meta:
		model = Certificate
		fields = [
				'togtool_date',
				'togtool_number',
				'certificate_end_date',
				'tz_id'
				]
		widgets = {
			'tz_id': f.CheckboxSelectMultiple(),
		}
		labels = {
			'tz_id': 'Тусгай зөвшөөрлийн заалтууд:'
		}


"""
class Baiguullaga_huvaarilaltForm(f.ModelForm):
	def __init__(self, *args, **kwargs):
		super(Baiguullaga_huvaarilaltForm, self).__init__(*args, **kwargs)
		zz = ZZ.objects.all()[0]
		tasag_tza_name = TasagList.objects.get(name = 'Тусгай зөвшөөрлийн алба')
		tasag_uta_name = TasagList.objects.get(name = 'Үнэ тарифын алба')
		tasag_tza = Tasag.objects.get(baiguullaga = zz, dep_name = tasag_tza_name)
		tasag_uta = Tasag.objects.get(baiguullaga = zz, dep_name = tasag_uta_name)
		mergejilten = AlbanTushaalList.objects.get(name = 'Мэргэжилтэн')
		ahlah_mergejilten = AlbanTushaalList.objects.get(name = 'Ахлах мэргэжилтэн')
		tza = AlbanTushaal.objects.filter(baiguullaga = zz, dep_id = tasag_tza, position_name = mergejilten) | AlbanTushaal.objects.filter(baiguullaga = zz, dep_id = tasag_tza, position_name = ahlah_mergejilten)
		uta = AlbanTushaal.objects.filter(baiguullaga = zz, dep_id = tasag_uta, position_name = mergejilten) | AlbanTushaal.objects.filter(baiguullaga = zz, dep_id = tasag_uta, position_name = ahlah_mergejilten)
		self.fields['tza_mergejilten'] = f.ModelChoiceField(label = 'ТЗА мэргэжилтэн', queryset = Ajiltan.objects.filter(baiguullaga = zz, status = True, alban_tushaal = tza), required = False)
		self.fields['uta_mergejilten'] = f.ModelChoiceField(label = 'ҮТА мэргэжилтэн',queryset = Ajiltan.objects.filter(baiguullaga = zz, status = True, alban_tushaal = uta), required = False)
	class Meta:
		model = Rel_baig_zz_ajilchid
		fields = ['tze', 'tza_mergejilten', 'uta_mergejilten']

	def save(self, commit = True):
		m=super(Baiguullaga_huvaarilaltForm, self).save(commit=False)
		if commit:
			m.save()
		return m
"""
class Baiguullaga_huvaarilalt_tza_Form(f.ModelForm):
	def __init__(self, *args, **kwargs):
		super(Baiguullaga_huvaarilalt_tza_Form, self).__init__(*args, **kwargs)
		zz = ZZ.objects.all()[0]
		tasag_tza = Tasag.objects.get(baiguullaga = zz, dep_name = 'Тусгай зөвшөөрлийн алба')
		tza = AlbanTushaal.objects.filter(dep_id = tasag_tza, position_name__icontains = 'мэргэжилтэн')
		self.fields['tza_mergejilten'] = f.ModelChoiceField(label = 'ТЗА мэргэжилтэн', queryset = Ajiltan.objects.filter(baiguullaga = zz, status = True, alban_tushaal = tza), required = True)
	class Meta:
		model = Rel_baig_zz_ajilchid
		fields = ['tza_mergejilten']

class Certificate_giving_Form(f.ModelForm):
	def __init__(self, *args, **kwargs):
		self.tz_choices = kwargs.pop('tz_choices', None)
		super(Certificate_giving_Form, self).__init__(*args, **kwargs)
		self.fields['tz_id'] = f.ModelMultipleChoiceField(queryset=self.tz_choices, widget = f.CheckboxSelectMultiple())
		self.fields['tz_id'].label = "Тусгай зөвшөөрлийн заалт:"

	class Meta:
		model = Certificate
		fields = ['cert_number', 'togtool_date', 'togtool_number', 'certificate_end_date', 'tz_id', 'cert_file']
		labels = {
            "tz_id": "Тусгай зөвшөөрлийн заалт:",
            "cert_number": "Гэрчилгээний дугаар:",
            "togtool_number": "Гэрчилгээ олгосон тогтоолын дугаар:",
        }
		widgets = {
        'togtool_date': f.TextInput(attrs={'placeholder':'2016-03-27'}),
        'certificate_end_date': f.TextInput(attrs={'placeholder':'2016-03-27'}),
        }
	def save(self, commit = True):
		m=super(Certificate_giving_Form, self).save(commit=False)
		if commit:
			m.save()
		return m

class Certificate_huulbar_insert_Form(f.ModelForm):
	class Meta:
		model = Certificate
		fields = ['cert_file']

class Hurliin_shiidver_Form(Certificate_giving_Form):
	hurliin_shiidver_choices=[('1', 'Тусгай зөвшөөрлийн гэрчилгээ олгоно.'),
								('2', 'Тусгай зөвшөөрлийн гэрчилгээ олгохгүй')]
	shiidver = f.ChoiceField(label="Хурлын шийдвэр сонгоно уу.",
							choices = hurliin_shiidver_choices,
							widget = f.RadioSelect())
	class Meta:
		model = Certificate
		fields = ['shiidver', 'tolov', 'cert_number', 'togtool_date', 'togtool_number', 'certificate_end_date', 'tz_id']
		labels = {
            "tz_id": "Тусгай зөвшөөрлийн заалт:",
            "cert_number": "Гэрчилгээний дугаар:",
            "togtool_number": "Гэрчилгээ олгосон тогтоолын дугаар:",
            "tolov": "Гэрчилгээний төлөв:",
        }
		widgets = {
        'togtool_date': f.TextInput(attrs={'placeholder':'2016-03-27'}),
        'certificate_end_date': f.TextInput(attrs={'placeholder':'2016-03-27'}),
        }
		

	def is_valid(self):
		super(Hurliin_shiidver_Form, self).is_valid()
		if self.cleaned_data['shiidver'] == '2':
			return True
		else:
			return super(Hurliin_shiidver_Form, self).is_valid()


class Baig_huvaarilalt_bundleForm(f.Form):
	CHOICES=[('1','ТЗА'),
	('2','ҮТА')]

	tza_check = f.BooleanField(label='ТЗА-ны ажилтанд оноох')
	uta_check = f.BooleanField(label='ҮТА-ны ажилтанд оноох')
	def __init__(self, *args, **kwargs):
		super(Baig_huvaarilalt_bundleForm, self).__init__(*args, **kwargs)
		zz = ZZ.objects.all()[0]
		tasag_tza_name = TasagList.objects.get(name = 'Тусгай зөвшөөрлийн алба')
		tasag_uta_name = TasagList.objects.get(name = 'Үнэ тарифын алба')
		tasag_tza = Tasag.objects.get(baiguullaga = zz, dep_name = tasag_tza_name)
		tasag_uta = Tasag.objects.get(baiguullaga = zz, dep_name = tasag_uta_name)
		mergejilten = AlbanTushaalList.objects.get(name = 'Мэргэжилтэн')
		ahlah_mergejilten = AlbanTushaalList.objects.get(name = 'Ахлах мэргэжилтэн')
		tza = AlbanTushaal.objects.filter(dep_id = tasag_tza, position_name = mergejilten) | AlbanTushaal.objects.filter(dep_id = tasag_tza, position_name = ahlah_mergejilten)
		uta = AlbanTushaal.objects.filter(dep_id = tasag_uta, position_name = mergejilten) | AlbanTushaal.objects.filter(dep_id = tasag_uta, position_name = ahlah_mergejilten)
		self.fields['tza_mergejilten'] = f.ModelChoiceField(label = 'ТЗА мэргэжилтэн', queryset = Ajiltan.objects.filter(baiguullaga = zz, status = True, alban_tushaal = tza), required = False)
		self.fields['uta_mergejilten'] = f.ModelChoiceField(label = 'ҮТА мэргэжилтэн',queryset = Ajiltan.objects.filter(baiguullaga = zz, status = True, alban_tushaal = uta), required = False)
# uilsee code ends



gshu_check_choices = (
	(u'Хүлээн авсан', u'Хүлээн авсан'),
	(u'Буцаасан', u'Буцаасан'),
	)
class TZA_gshu_check_form(f.ModelForm):
	class Meta:
		model = GShU
		fields = ['tolov']
	def __init__(self, *args, **kwargs):
		super(TZA_gshu_check_form, self).__init__(*args, **kwargs)
		self.fields['tolov'] = f.ChoiceField(choices=gshu_check_choices, label = 'Төлөв:')

class BB_tze_update_form(f.ModelForm):
	class Meta:
		model=BB
		fields=['tze']
		labels = {
				'tze': 'Тусгай зөвшөөрөл эзэмшигч'
			}

class Car_tze_update_form(f.ModelForm):
	class Meta:
		model=Car
		fields=['tze']
		labels = {
				'tze': 'Тусгай зөвшөөрөл эзэмшигч'
			}

class ABB_tze_update_form(f.ModelForm):
	class Meta:
		model=ABB
		fields=['tze']
		labels = {
				'tze': 'Тусгай зөвшөөрөл эзэмшигч'
			}

class Equipment_tze_update_form(f.ModelForm):
	class Meta:
		model=Equipment
		fields=['tze']
		labels = {
				'tze': 'Тусгай зөвшөөрөл эзэмшигч'
			}
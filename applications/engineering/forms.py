# -*- coding: utf-8 -*-
from django import forms as f
from applications.app.models import Baiguullaga, Tasag, AlbanTushaal, Nasoss, Hooloi, Ts_tohooromj, UsDamjuulahBairTonog
from applications.app.models import Certificate, Burdel, School, EngineeringCertificate, UsanSanUgaalga, UsTugeehBairSavUgaalga, LabBagaj, Lab_orgotgol
from applications.app.models import GShU, TZ
from django.forms import modelformset_factory
from django.utils.translation import ugettext_lazy as _

class EmptyForm(f.Form):
	pass

def get_gshu_form_class(field_list = ['__all__']):
	widget_dic = {}
	for i in field_list:
		widget_dic[i] = f.TextInput(attrs = {'class': 'input-small'})
	class GShU_Form(f.ModelForm):
		class Meta:
			model = GShU
			fields = field_list
			widgets = widget_dic
	return GShU_Form



class Handah_erh_oorchloh_Form(f.Form):
	ovog = f.CharField(label = 'Овог', max_length = 30)
	ner = f.CharField(label = 'Нэр', max_length = 30)
	email = f.EmailField(label = 'E-mail')

class New_TZ_Huselt_Form(f.ModelForm):
	huselt_angilal = f.TypedChoiceField(required=True, label=u'Хүсэлтийн ангилал',choices=Burdel.tz_huselt_angilal, widget=f.RadioSelect())
	tz_choices_hodoo_oron_nutag = f.ModelMultipleChoiceField(label='Тусгай зөвшөөрлийн заалтуудаас сонгоно уу.', 
								queryset=TZ.objects.all(), widget=f.CheckboxSelectMultiple, required=False, to_field_name='tz')

	tz_choices_oron_suuts = f.ModelMultipleChoiceField(label='Тусгай зөвшөөрлийн заалтуудаас сонгоно уу.',
								queryset=TZ.objects.filter(tz='12.2.1')|TZ.objects.filter(tz='12.2.2')|TZ.objects.filter(tz='12.2.3'),
								widget=f.CheckboxSelectMultiple(), required=False)
	
	def __init__(self, *args, **kwargs):



		super(New_TZ_Huselt_Form, self).__init__(*args, **kwargs)
	#	if tze.get_sungah_bolomjtoi_certs():
	#		self.fields['cert'] = f.ModelChoiceField(label='Сунгах тусгай зөвшөөрлийн гэрчилгээ', queryset = tze.get_sungah_bolomjtoi_certs(), required=False)
	#	else:
	#		del self.fields['cert']

	#	self.fields['tz'] = f.ModelMultipleChoiceField(label='Тусгай зөвшөөрлийн заалтуудаас сонгоно уу',
	#						queryset = tze.get_possible_tz_choices() | huselt_tzs, widget=f.CheckboxSelectMultiple)
		

	class Meta:
		model = Burdel
		fields = ['huselt_angilal' ,'cert']
		#widgets = {'tz': f.CheckboxSelectMultiple(),}

	def save(self, commit=True):
		m=super(New_TZ_Huselt_Form, self).save(commit=False)
		if commit:
			m.save()
		return m
	def clean_tz_choices_hodoo_oron_nutag(self):
		if 'huselt_angilal' in self.cleaned_data:
			if self.cleaned_data['huselt_angilal'] == u'Хөдөө орон нутаг':
				if not self.cleaned_data['tz_choices_hodoo_oron_nutag']:
					raise f.ValidationError(_(u'Тусгай зөвшөөрлийн заалтыг сонгоно уу.'))
		return self.cleaned_data['tz_choices_hodoo_oron_nutag']



class Huselt_ilgeeh_Form(f.Form):
	check = f.BooleanField(label="Бүрдүүлсэн бичиг баримтууд үнэн зөв болохыг баталж байна.", required = True)



class Material_Burdsen_Check_Form(f.Form):
	check = f.BooleanField(label="Материал бүрдсэн гэж үзвэл сонгоно уу.", required=False)

class Alba_tasag_form(f.ModelForm):
	class Meta:
		model = Tasag
		fields = ['dep_name', 'phone', 'mail']

	def save(self, commit=True):
		m=super(Alba_tasag_form, self).save(commit=False)
		if commit:
			m.save()
		return m
class AlbanTushaal_form(f.ModelForm):
	class Meta:
		model = AlbanTushaal
		fields = ['position_name']


AlbanTushaal_formset = modelformset_factory(AlbanTushaal, fields=['position_name'], can_delete = True)

School_formset = modelformset_factory(
	School,
	fields = 
		[
		'school_name',
		'diplom_num',
		'mergejil',
		'degree', 
		'diplom_picture',
		 ],
	widgets = 
		{
		'school_name': f.TextInput(attrs={'class' : 'input-medium',}),
		'diplom_num' : f.TextInput(attrs={'class' : 'input-small',}),
		'mergejil' : f.TextInput(attrs={'class' : 'input-small'}),
		'degree' : f.Select(attrs={'class' : 'input-small', }),
		'diplom_picture' : f.FileInput(attrs={'class' : 'input-small'}),
		},
	can_delete = True
)



EngineeringCertificate_formset = modelformset_factory(
	EngineeringCertificate,
	fields =
		[
		'zergiin_huree',
		'certificate_num',
		'certificate_picture',
		],
	widgets =
		{
		'zergiin_huree': f.TextInput(attrs={'placeholder': 'Жнь: Ус хангамжийн ашиглалт',}),
		},
	can_delete = True
	)

Nasoss_formset = modelformset_factory(
	Nasoss,
	fields =
		[
		'mark',
		'country',
		'huchin_chadal',
		'too',
		'ashiglaltand_orson_ognoo'
		],
	widgets =
		{
		'huchin_chadal': f.TextInput(attrs={'class': 'input-small',}),
		'too': f.TextInput(attrs={'class': 'input-small',}),
		'ashiglaltand_orson_ognoo': f.TextInput(attrs={'class': 'input-small',}),
		},
	can_delete = True
	)

Hooloi_formset = modelformset_factory(
	Hooloi,
	fields =
		[
		'torol',
		'diametr',
		'urt',
		'ashiglaltand_orson_ognoo'
		],
	can_delete = True,
	widgets =
		{
		'diametr': f.TextInput(),
		'urt': f.TextInput(),
		}
	)

Ts_tohooromj_formset = modelformset_factory(
	Ts_tohooromj,
	fields =
		[
		'barilga_tonog',
		'huchin_chadal',
		'ajillaj_bui_huchin_chadal',
		'too',
		'ashiglaltand_orson_ognoo',
		'tailbar',
		],
	
	widgets = {
		'barilga_tonog': f.Select(attrs={'class' : 'input-small',}),
		'huchin_chadal' : f.TextInput(attrs={'class' : 'input-small',}),
		'ajillaj_bui_huchin_chadal' : f.TextInput(attrs={'class' : 'input-small',}),
		'too' : f.TextInput(attrs={'class' : 'input-small', }),
		'ashiglaltand_orson_ognoo' : f.TextInput(attrs={'class' : 'input-small', }),
		},
	can_delete = True
	)

UsDamjuulahBairTonog_formset = modelformset_factory(
	UsDamjuulahBairTonog,
	fields =
		[
		'tonog',
		'huchin_chadal',
		'too',
		'ognoo',
		'tailbar',
		],

	widgets = {
	'tonog': f.Select(attrs={'class' : 'input-small',}),
	'huchin_chadal' : f.TextInput(attrs={'class' : 'input-small',}),
	'too' : f.TextInput(attrs={'class' : 'input-small', }),
	'ognoo' : f.TextInput(attrs={'class' : 'input-small', }),
	},
	can_delete = True
	)

UsanSanUgaalga_formset = modelformset_factory(
	UsanSanUgaalga,
	fields = 
	[
	'ognoo',
	'akt'
	],
	can_delete = True
	)

UsTugeehBairSavUgaalga_formset = modelformset_factory(
	UsTugeehBairSavUgaalga,
	fields =
	[
	'ugaalga_ognoo'
	],
	can_delete = True
	)

LabBagaj_formset = modelformset_factory(
	LabBagaj,
	fields =
	[
	'bagaj'
	],
	can_delete = True
	)

Lab_orgotgol_formset = modelformset_factory(
	Lab_orgotgol,
	fields =
	[
	'horongo_uusver',
	'ognoo'
	],
	can_delete=True
	)





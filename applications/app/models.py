#!/usr/bin/env python
# -*- coding: utf-8 -*-
import jsonpickle

from django.db import models
from applications.app.validate import *
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_unicode
from django.utils import six
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.db.models import Sum
from smart_selects.db_fields import ChainedForeignKey 
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User as SystemUser
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
#from django.contrib.auth.models import AbstractUser


def user_directory_path(instance, filename):
	return u'{0}/base/{1}'.format(instance.tze, filename)
def ajiltan_directory_path(instance, filename):
	return u'{0}/ajiltan/{1}'.format(instance.baiguullaga, filename)
def ajiltan_directory_path_school_and_others(instance, filename):
	return u'{0}/ajiltan/{1}'.format(instance.emp.baiguullaga, filename)
def nasos_directory_path(instance, filename):
	return u'{0}/tonog/{1}'.format(instance.tze, filename)
def nasoszurag_directory_path(instance, filename):
	return u'{0}/tonog/{1}'.format(instance.nasos_id.tze, filename)
def hudag_directory_path(instance, filename):
	return u'{0}/tonog/{1}'.format(instance.tze, filename)
def usansan_directory_path(instance, filename):
	return u'{0}/tonog/{1}'.format(instance.tze, filename)
def usansanakt_directory_path(instance, filename):
	return u'{0}/tonog/{1}'.format(instance.usansan_id.tze, filename)
def car_directory_path(instance, filename):
	return u'{0}/car/{1}'.format(instance.tze, filename)
def hudag_negdsen_directory_path(instance, filename):
	return u'{0}/tonog/{1}'.format(instance.tze_id, filename)


def lcm(*values):
	""" hamgiin baga yoronhii huvaagdagchiig oloh function """
	values = set([abs(int(v)) for v in values])
	if values and 0 not in values:
		n = n0 = max(values)
		values.remove(n)
		while any( n % m for m in values ):
			n += n0
		return n
	return 0


class History_operations(object):
	def get_history_object(self, date_time):
		try:
			obj = self.history.as_of(date_time)
		except:
			return False
		return obj

	def get_sub_objects(self, subclass_name, subclass_field_name, date_time=timezone.now()):
		### jishee ni NasosStantsiin date_time hugatsaan dahi nasoss-uudiig butsaah function
		### status == True -g butsaana
		obj_history = self.get_history_object(date_time)
		if obj_history:
			sub_objects = []
			sub_objects_all = subclass_name.objects.all()
			for i in sub_objects_all:
				i_history = i.get_history_object(date_time)
				if i_history:
					t = getattr(i_history, subclass_field_name)
					if t.id == self.id and i_history.status==True:
						sub_objects.append(i_history)
			return sub_objects
		return False
	@classmethod
	def export_to_excel(self, worksheet, row_start, col_start, queryset, date_time=timezone.now()):
		""" object-iin queryset-iig avna. Tuhain queryset-iin date_time uy deh data-g excel export hiine """
		if queryset:
			[row_write, col_write] = self.excel_write_header_and_format(worksheet, row_start, col_start)
			for q in queryset:
				# object_excel_write function---date_time uyiin history objectiig excel -ruu horvuulne
				[row_write, col_write] = q.object_excel_write(worksheet, row_write, col_write, date_time=date_time)
		else:
			worksheet.write_string(row_start, col_start, u'Мэдээлэл байхгүй')
	@classmethod
	def export_to_excel_without_header(self, worksheet, row_start, col_start, queryset, date_time=timezone.now()):
		row_write = row_start
		col_write = col_start
		if queryset:
			for q in queryset:
				[row_write, col_write] = q.object_excel_write(worksheet, row_write, col_write, date_time=date_time)
		return [row_write, col_write]


	@classmethod
	def get_history_queryset(self, queryset, date_time):
		### queryset deh objectuudiin date_time hugatsaandahi history-nuudiin
		### listiig butsaah function
		qs = []
		for q in queryset:
			q_history = q.get_history_object(date_time)
			if q_history:
				qs.append(q_history)
		return qs
	@classmethod
	def get_history_queryset_with_status(self, queryset, date_time, status):
		### queryset deh objectuudiin date_time hugatsaandahi history-nuudiin
		### listiig butsaah function
		### status ni True or False baina
		### statusaar ni filterdej ur dung butsaana
		qs = []
		for q in queryset:
			q_history = q.get_history_object(date_time)
			if q_history and q_history.status == status:
				qs.append(q_history)
		return qs




class GlobalPermissionManager(models.Manager):
	def get_query_set(self):
		return super(GlobalPermissionManager, self).get_query_set().filter(content_type__name='global_permission')


class GlobalPermission(Permission):
	"""A global permission, not attached to a model"""

	objects = GlobalPermissionManager()

	class Meta:
		proxy = True
		verbose_name = "global_permission"
		permissions = (('tze_baiguullaga_menu_view', 'TZE baiguullaga menu view'),
					('tze_hunii_noots_menu_view', 'TZE hunii noots menu view'),
					('tze_tonog_tohooromj_menu_view', 'TZE tonog tohooromj menu view'),
					('tze_tusgai_zovshoorol_menu_view', 'TZE tusgai zovshoorol menu view'),
					('tze_handah_erh_menu_view', 'TZE handah erh menu view'),
					('tze_ua_tailan_menu_view', 'TZE ua tailan menu view'),
					('tze_sanhuu_medee_menu_view', 'TZE sanhuu medee menu view'),
					('tze_sanhuu_tailan_menu_view', 'TZE sanhuu tailan menu view'),
					('tze_gshu_tailan_menu_view', 'TZE gshu tailan menu view'),

					('tze_handah_erh_change_view', 'TZE handah erh change view'),
					('tze_tz_huselt_ilgeeh_view', 'TZE TZ huselt ilgeeh view'),
					('tze_tz_huselt_uusgeh_view', 'TZE TZ huselt uusgeh view'),
					
					('tza_tur_zuur_permission', 'TZA tur zuuriin permission'),
					('tza_darga_permission', 'TZA darga permission'),
					('tza_mergejilten_permission', 'TZA mergejilten permission'),

					('uta_darga_permission', 'UTA darga permission'),
					('uta_mergejilten_permission', 'UTA mergejilten permission'),

					('hzm_mergejilten_permission', 'HZM mergejilten permission'),
					
					)


	def save(self, *args, **kwargs):
		ct, created = ContentType.objects.get_or_create(
			model=self._meta.verbose_name, app_label=self._meta.app_label,
		)
		self.content_type = ct
		super(GlobalPermission, self).save(*args)


class Create(models.Model):
	begin_time = models.DateTimeField(db_index = True ,auto_now_add = True, verbose_name = 'Эхлэх хугацаа:')
	end_time = models.DateTimeField(db_index = True, auto_now = True, verbose_name = 'Дуусах хугацаа:')
	created_by= models.ForeignKey('User', null = True, blank = True)
	status = models.BooleanField(verbose_name = 'Төлөв:', default = False)

	class Meta:
		abstract = True
		ordering = ['-id']

	def __unicode__(self):
		return unicode(self.created_by)

class Aimag(models.Model):
	aimag_name = models.CharField(verbose_name ='Аймаг, Хот',max_length = 250)

	class Meta:
		verbose_name_plural = 'Аймаг, Хот'

	def __unicode__(self):
		return self.aimag_name
class Sum(models.Model):
	aimag_id = models.ForeignKey(Aimag, verbose_name = 'Аймаг ID:')
	sum_name = models.CharField(verbose_name = 'Сум, Дүүрэг:',max_length = 250)
	

	class Meta:
		verbose_name_plural = 'Сум, Дүүрэг'

	def __unicode__(self):
		return self.sum_name
class Bag(models.Model):
	aimag_id = models.ForeignKey(Aimag, verbose_name = 'Аймаг ID:')
	sum_id = ChainedForeignKey(Sum, verbose_name = 'Сум ID:', chained_field = 'aimag_id', chained_model_field = 'aimag_id')
	bag_name = models.CharField(verbose_name = 'Баг, Хороо:',max_length = 250)
	
	

	class Meta:
		verbose_name_plural = 'Баг, Хороо'

	def __unicode__(self):
		return self.bag_name

class Tax(models.Model):
	tax= models.CharField(verbose_name='Харьяалагдах татварын алба:',max_length = 250)

	class Meta:
		verbose_name_plural = 'Харьяалагдах татварын алба'

	def __unicode__(self):
		return self.tax

''' Байгууллагын бүртгэл '''
class Baiguullaga(Create, History_operations):
	type_choices = (
		(u'ХХК', 'ХХК'),
		(u'ТӨХК', 'ТӨХК'),
		(u'ОНӨААТҮГ', 'ОНӨААТҮГ'),
		(u'ОНӨҮГ', 'ОНӨҮГ'),
		(u'ОНӨХК', 'ОНӨХК'),
		(u'ОНӨХХК', 'ОНӨХХК'),
		(u'ТӨААТҮГ', 'ТӨААТҮГ'),
		(u'ОНТҮГ', 'ОНТҮГ'),
		(u'ХК', 'ХК'),
		(u'ХНН', 'ХНН'),
        (u'ТББ','ТББ'),
		)
	reg_num = models.CharField(max_length =7 ,verbose_name = 'Байгууллагын РД:', validators = [Validate])
	ubd = models.CharField(max_length =12 ,verbose_name = 'Байгууллагын улсын бүртгэлийн дугаар:')
	org_name = models.CharField(verbose_name = 'Байгууллагын нэр:',max_length=250)
	org_type = models.CharField(verbose_name = 'Байгууллагын хэлбэр:', max_length = 50, choices = type_choices, null = True, blank = True)
	org_date = models.DateField(verbose_name = 'Байгуулагдсан огноо:', null = True, blank = True)
	phone = models.CharField(max_length = 11, verbose_name = 'Утас:', validators=[validate_phone], null = True, blank = True)
	e_mail = models.EmailField(verbose_name = 'И-мэйл:', null = True, blank = True)
	fax = models.CharField(max_length = 50, verbose_name = 'Факс:', null = True, blank = True)
	post = models.CharField(max_length = 50, verbose_name = 'Шуудангийн хайрцаг:', null = True, blank = True)
	tax = models.ForeignKey(Tax, verbose_name = 'Харьяалагдах татварын алба:', null = True, blank = True)
	city = models.ForeignKey(Aimag, verbose_name = 'Аймаг, Хот:', null = True, blank = True)
	district = ChainedForeignKey(Sum, verbose_name = 'Сум, Дүүрэг:', null = True, blank = True, chained_field = 'city', chained_model_field = 'aimag_id')
	khoroo = ChainedForeignKey(Bag, verbose_name = 'Баг, Хороо:', null = True, blank = True, chained_field = 'district', chained_model_field = 'sum_id')
	address = models.CharField(verbose_name = 'Хаяг:',max_length = 500, null = True, blank = True)
	tovch_taniltsuulga=models.CharField(verbose_name = 'Товч танилцуулга:',max_length = 5000, null = True, blank = True)
	gerchilgee_picture= models.ImageField(verbose_name = 'Улсын бүртгэлийн гэрчилгээний зураг урд тал:', null = True, blank = True, upload_to=user_directory_path)
	gerchilgee_picture1= models.ImageField(verbose_name = 'Улсын бүртгэлийн гэрчилгээний зураг ар тал:', null = True, blank = True, upload_to=user_directory_path)
	history = HistoricalRecords(inherit = True)
	class Meta:
		verbose_name_plural = 'Байгууллагын бүртгэл'

	def __unicode__(self):
		return unicode(self.reg_num)

	
class Tasag(Create, History_operations):
	baiguullaga = models.ForeignKey(Baiguullaga, verbose_name = 'Байгууллага')
	dep_name = models.CharField(max_length = 250, verbose_name = u'Алба хэлтсийн нэр:')
	phone = models.CharField(max_length = 12, verbose_name = 'Утас:', validators = [validate_phone])
	mail = models.EmailField(verbose_name = 'И-мэйл:', null = True, blank = True)
	history = HistoricalRecords()
	class Meta:
		verbose_name_plural = 'Байгууллагын хэлтсийн мэдээ'

	def __unicode__(self):
		return "%s" %(six.text_type(self.dep_name))
	def get_alban_tushaal_queryset(self):
		return AlbanTushaal.objects.filter(dep_id = self, status = True)
	def get_alban_tushaal_count(self):
		qs = self.get_alban_tushaal_queryset()
		return qs.count()
	def get_ajiltan_queryset(self):
		alban_tushaal_qs = self.get_alban_tushaal_queryset()
		ajiltan_qs = Ajiltan.objects.filter(alban_tushaal__in = alban_tushaal_qs, status = True)
		return ajiltan_qs
	def get_ajiltan_count(self):
		ajiltan_qs = self.get_ajiltan_queryset()
		return ajiltan_qs.count()
class AlbanTushaal(Create, History_operations):
	dep_id = models.ForeignKey(Tasag, verbose_name = 'Байгууллагын хэлтэс:')
	position_name = models.CharField(max_length = 250, verbose_name = 'Албан тушаал:')
	history = HistoricalRecords()
	
	class Meta:
		verbose_name_plural = 'Албан тушаал'

	def __unicode__(self):
		return unicode(self.position_name)
	def get_ajiltan_count(self):
		ajiltan_qs = Ajiltan.objects.filter(alban_tushaal = self, status = True)
		return ajiltan_qs.count()

zereg_choices = (
		(u'Удирдах ажилтан', u'Удирдах ажилтан'),
		(u'Инженер техникийн ажилтан',u'Инженер техникийн ажилтан'),
		(u'Мэргэжлийн ажилтан',u'Мэргэжлийн ажилтан'),
		(u'Бусад', u'Бусад')
		)

bolovsroliin_tuvshin_choices = (
		(u'Дээд', u'Дээд'),
		(u'Дунд', u'Дунд'),
		(u'Бүрэн дунд', u'Бүрэн дунд'),
		(u'Тусгай дунд', u'Тусгай дунд'),
		(u'Бүрэн бус дунд', u'Бүрэн бус дунд'),
		(u'Бага', u'Бага'),
		)



		
# Ажилтаны бүртгэл
class Ajiltan(Create, History_operations):
	gender_choices = (
		(u'Эр', u'Эр'),
		(u'Эм', u'Эм')
		)
	baiguullaga = models.ForeignKey(Baiguullaga, verbose_name = 'Байгууллага:')
	emp_lname = models.CharField(max_length = 50, verbose_name = 'Овог:')
	emp_name = models.CharField(max_length = 50, verbose_name = 'Нэр:')
	emp_reg = models.CharField(max_length = 10, verbose_name = 'РД:', null=True, blank=True)
	picture= models.ImageField(verbose_name = 'Иргэний үнэмлэхний зураг:', null = True, blank = True, upload_to=ajiltan_directory_path, validators=[validate_file_extension, validate_file_size])
	emp_birth = models.DateField(verbose_name = 'Төрсөн огноо:', null=True)
	ndd = models.CharField(max_length = 7, verbose_name = 'НДД:', null = True, blank = True)
	gender = models.CharField(max_length=7, verbose_name = 'Хүйс:', choices = gender_choices, null=True)
	tasag = ChainedForeignKey(Tasag, verbose_name = 'Алба хэлтэс:', chained_field='baiguullaga', chained_model_field='baiguullaga')
	alban_tushaal = ChainedForeignKey(AlbanTushaal, verbose_name = 'Албан тушаал:', chained_field='tasag', chained_model_field='dep_id')
	zereg = models.CharField(max_length = 250, choices = zereg_choices, null = True, blank = True, verbose_name = 'Албан тушаалын ангилал:')
	naj = models.IntegerField(verbose_name = 'Нийт ажилласан жил:', null = True, blank = True)
	tzeaj = models.IntegerField(verbose_name = 'ТЗЭ-д ажилласан жил:', null = True, blank = True)
	phone = models.CharField(verbose_name = 'Утас:', max_length = 11, validators = [validate_phone], null = True, blank = True)
	e_mail = models.EmailField(verbose_name = 'И-мэйл:', null=True, blank=True)
	bolovsroliin_tuvshin=models.CharField(max_length = 15, verbose_name= 'Боловсролын түвшин:', choices = bolovsroliin_tuvshin_choices, null = True, blank = True)
	history = HistoricalRecords()
	
	def calculate_nas(self):
		if self.emp_birth:
			nas = timezone.now().date().year - self.emp_birth.year
		else:
			nas = ''
		return nas
	class Meta:
		verbose_name_plural = 'Байгууллагын ажилтны бүртгэл'

	def __unicode__(self):
		return unicode(self.emp_name)

	@classmethod
	def get_history_queryset_with_status_and_zereg(self, queryset, date_time, status, zereg):
		qs = []
		for q in queryset:
			q_history = q.get_history_object(date_time)
			if q_history and q_history.status == status and q_history.zereg == zereg:
				qs.append(q_history)
		return qs

	@classmethod
	def excel_write_header_and_format(self, worksheet, row_start, col_start):
		worksheet.merge_range(row_start, col_start, row_start+1, col_start,u'ТЗЭ')
		worksheet.merge_range(row_start, col_start+1, row_start+1, col_start+1,u'Овог')
		worksheet.merge_range(row_start, col_start+2, row_start+1, col_start+2,u'Нэр')
		worksheet.merge_range(row_start, col_start+3, row_start+1, col_start+3,u'Хүйс')
		worksheet.merge_range(row_start, col_start+4, row_start+1, col_start+4,u'Нас')
		worksheet.merge_range(row_start, col_start+5, row_start+1, col_start+5,u'Регистрийн дугаар')
		worksheet.merge_range(row_start, col_start+6, row_start+1, col_start+6,u'Төрсөн огноо')
		worksheet.merge_range(row_start, col_start+7, row_start+1, col_start+7,u'НДД')
		worksheet.merge_range(row_start, col_start+8, row_start+1, col_start+8,u'Албан тушаалын ангилал')
		worksheet.merge_range(row_start, col_start+9, row_start+1, col_start+9,u'Алба хэлтэс')
		worksheet.merge_range(row_start, col_start+10, row_start+1, col_start+10,u'Албан тушаал')
		worksheet.merge_range(row_start, col_start+11, row_start+1, col_start+11,u'Нийт ажилласан жил')
		worksheet.merge_range(row_start, col_start+12, row_start+1, col_start+12,u'ТЗЭ-д ажилласан жил')
		worksheet.merge_range(row_start, col_start+13, row_start+1, col_start+13,u'Утас')
		worksheet.merge_range(row_start, col_start+14, row_start+1, col_start+14,u'И-мэйл')
		worksheet.merge_range(row_start, col_start+15, row_start+1, col_start+15,u'Боловсролын түвшин')


		worksheet.merge_range(row_start, col_start+16, row_start, col_start+19, u'Төгссөн сургууль')
		worksheet.write_string(row_start+1, col_start+16, u'Төгссөн сургуулийн нэр')
		worksheet.write_string(row_start+1, col_start+17, u'Эзэмшсэн мэргэжил')
		worksheet.write_string(row_start+1, col_start+18, u'Диплом, мэргэжлийн үнэмлэхний дугаар')
		worksheet.write_string(row_start+1, col_start+19, u'Боловсролын зэрэг')


		worksheet.merge_range(row_start, col_start+20, row_start, col_start+21, u'Мэргэшсэн болон зөвлөх зэргийн гэрчилгээ')
		worksheet.write_string(row_start+1, col_start+20, u'Зэргийн хүрээ')
		worksheet.write_string(row_start+1, col_start+21, u'Гэрчилгээний дугаар')

		return [row_start+2, col_start]
		

	def object_excel_write(self, worksheet, row_start, col_start, **kwargs):
		date_time = kwargs['date_time']
		hist_obj = self.get_history_object(date_time)

		if hist_obj:
			if hist_obj.status==True:
				school_count = self.get_school_count(date_time)
				eng_cert_count = self.get_eng_cert_count(date_time)

				if school_count == 0:
					school_count=1
				if eng_cert_count == 0:
					eng_cert_count = 1

				least_common_multiply = lcm(school_count, eng_cert_count)

				if least_common_multiply>1:
					worksheet.merge_range(row_start, col_start, row_start+least_common_multiply-1, col_start, hist_obj.baiguullaga.org_name + ' ' + hist_obj.baiguullaga.org_type)
					worksheet.merge_range(row_start, col_start+1, row_start+least_common_multiply-1, col_start+1, hist_obj.emp_lname)
					worksheet.merge_range(row_start, col_start+2, row_start+least_common_multiply-1, col_start+2, hist_obj.emp_name)
					worksheet.merge_range(row_start, col_start+3, row_start+least_common_multiply-1, col_start+3, hist_obj.gender)
					worksheet.merge_range(row_start, col_start+4, row_start+least_common_multiply-1, col_start+4, u'нас')
					worksheet.merge_range(row_start, col_start+5, row_start+least_common_multiply-1, col_start+5, hist_obj.emp_reg)
					worksheet.merge_range(row_start, col_start+6, row_start+least_common_multiply-1, col_start+6, hist_obj.emp_birth)
					worksheet.merge_range(row_start, col_start+7, row_start+least_common_multiply-1, col_start+7, hist_obj.ndd)
					worksheet.merge_range(row_start, col_start+8, row_start+least_common_multiply-1, col_start+8, hist_obj.zereg)
					worksheet.merge_range(row_start, col_start+9, row_start+least_common_multiply-1, col_start+9, hist_obj.tasag.dep_name)
					worksheet.merge_range(row_start, col_start+10, row_start+least_common_multiply-1, col_start+10, hist_obj.alban_tushaal.position_name)
					worksheet.merge_range(row_start, col_start+11, row_start+least_common_multiply-1, col_start+11, hist_obj.naj)
					worksheet.merge_range(row_start, col_start+12, row_start+least_common_multiply-1, col_start+12, hist_obj.tzeaj)
					worksheet.merge_range(row_start, col_start+13, row_start+least_common_multiply-1, col_start+13, hist_obj.phone)
					worksheet.merge_range(row_start, col_start+14, row_start+least_common_multiply-1, col_start+14, hist_obj.e_mail)
					worksheet.merge_range(row_start, col_start+15, row_start+least_common_multiply-1, col_start+15, hist_obj.bolovsroliin_tuvshin)


				else:
					worksheet.write_string(row_start, col_start, hist_obj.baiguullaga.org_name + ' ' + hist_obj.baiguullaga.org_type)
					worksheet.write(row_start, col_start+1, hist_obj.emp_lname)
					worksheet.write(row_start, col_start+2, hist_obj.emp_name)
					worksheet.write(row_start, col_start+3, hist_obj.gender)
					worksheet.write(row_start, col_start+4, u'нас')
					worksheet.write(row_start, col_start+5, hist_obj.emp_reg)
					worksheet.write(row_start, col_start+6, hist_obj.emp_birth)
					worksheet.write(row_start, col_start+7, hist_obj.ndd)
					worksheet.write(row_start, col_start+8, hist_obj.zereg)
					worksheet.write(row_start, col_start+9, hist_obj.tasag.dep_name)
					worksheet.write(row_start, col_start+10, hist_obj.alban_tushaal.position_name)
					worksheet.write(row_start, col_start+11, hist_obj.naj)
					worksheet.write(row_start, col_start+12, hist_obj.tzeaj)
					worksheet.write(row_start, col_start+13, hist_obj.phone)
					worksheet.write(row_start, col_start+14, hist_obj.e_mail)
					worksheet.write(row_start, col_start+15, hist_obj.bolovsroliin_tuvshin)

				# bagaj export
				if school_count != 1:
					schools = self.get_sub_objects(School, 'emp', date_time)
					School.export_to_excel(worksheet, row_start, col_start+16, least_common_multiply/len(schools), schools)
				else:
					schools = self.get_sub_objects(School, 'emp', date_time)
					if len(schools) == 1:
						School.export_to_excel(worksheet, row_start, col_start+16, least_common_multiply/len(schools), schools)
					else:
						# bagaj baihgui uyd
						worksheet.merge_range(row_start, col_start+16, row_start+least_common_multiply-1, col_start+19, u'Бүртгэгдсэн мэдээлэл байхгүй')


				# orgotgol export
				if eng_cert_count != 1:
					eng_certs = self.get_sub_objects(EngineeringCertificate, 'emp', date_time)
					EngineeringCertificate.export_to_excel(worksheet, row_start, col_start+20, least_common_multiply/len(eng_certs), eng_certs)
				else:
					eng_certs = self.get_sub_objects(EngineeringCertificate, 'emp', date_time)
					if len(eng_certs) == 1:
						EngineeringCertificate.export_to_excel(worksheet, row_start, col_start+20, least_common_multiply/len(eng_certs), eng_certs)
					else:
						# orgotgol baihgui uyd
						worksheet.merge_range(row_start, col_start+20, row_start+least_common_multiply-1, col_start+21, u'Бүртгэгдсэн мэдээлэл байхгүй')

				return [row_start+least_common_multiply, col_start] # daraagiin object bichih coordinatiig butsaana
			else:
				# history object status==False uyd
				return [row_start, col_start]
		else:
			# history object baihgui uyd
			return [row_start, col_start]

	def get_school_count(self, date_time=timezone.now()):
		list_school = self.get_sub_objects(School, 'emp', date_time)
		return len(list_school)
	def get_eng_cert_count(self, date_time=timezone.now()):
		list_eng_cert = self.get_sub_objects(EngineeringCertificate, 'emp', date_time)
		return len(list_eng_cert)


bolovsroliin_zereg_choices = (
	(None, '------------'),
	(u'Бүрэн дунд', u'Бүрэн дунд'),
	(u'Тусгай дунд', u'Тусгай дунд'),
	(u'Бүрэн бус дунд', u'Бүрэн бус дунд'),
	(u'Бакалавр', u'Бакалавр'),
	(u'Магистр', u'Магистр'),
	(u'Доктор', u'Доктор'),
	)
''' Төгссөн сургууль '''
class School(Create, History_operations):
	school_name = models.CharField(max_length = 256,verbose_name = 'Төгссөн сургуулийн нэр:')
	emp = models.ForeignKey(Ajiltan, verbose_name = 'Ажилтан:')
	diplom_num = models.CharField(max_length =100, verbose_name = 'Диплом, мэргэжлийн үнэмлэхний дугаар:')
	mergejil = models.CharField(max_length = 64, verbose_name = 'Эзэмшсэн мэргэжил:')
	degree = models.CharField(max_length = 32, verbose_name = ' Боловсролын зэрэг:', choices = bolovsroliin_zereg_choices, null=True, blank=True)
	diplom_picture = models.FileField(verbose_name = 'Диплом, мэргэжлийн үнэмлэхний хуулбар:', validators = [validate_diplom_extension, validate_file_size], upload_to=ajiltan_directory_path_school_and_others) #upload_to=ajiltan_directory_path, 
	history = HistoricalRecords()

	@classmethod
	def export_to_excel(self, worksheet, row_start, col_start, row_step, queryset):
		row_write = row_start
		col_write = col_start
		for q in queryset:
			[row_write, col_write] = q.object_excel_write(worksheet, row_write, col_write, row_step = row_step)

	def object_excel_write(self, worksheet, row_start, col_start, **kwargs):
		row_step = kwargs['row_step']
		if row_step == 1:
			worksheet.write_string(row_start, col_start, self.school_name)
			worksheet.write_string(row_start, col_start+1, self.mergejil)
			worksheet.write_string(row_start, col_start+2, self.diplom_num)
			worksheet.write_string(row_start, col_start+3, self.degree)
		else:
			worksheet.merge_range(row_start, col_start, row_start+row_step-1, col_start, self.school_name)
			worksheet.merge_range(row_start, col_start+1, row_start+row_step-1, col_start+1, self.mergejil)
			worksheet.merge_range(row_start, col_start+2, row_start+row_step-1, col_start+2, self.diplom_num)
			worksheet.merge_range(row_start, col_start+3, row_start+row_step-1, col_start+3, self.degree)
		return [row_start+row_step, col_start]
	
	class Meta:
		verbose_name_plural = 'Төгссөн сургууль:'

	def __unicode__(self):
		return self.school_name
''' Мэргэшсэн болон зөвлөх зэргийн гэрчилгээ: '''
class EngineeringCertificate(Create, History_operations):
	zergiin_huree = models.CharField(max_length=256, verbose_name='Зэргийн хүрээ', null=True)
	certificate_num = models.CharField(max_length=32, verbose_name = 'Гэрчилгээний дугаар:')
	certificate_picture = models.ImageField(verbose_name = 'Гэрчилгээний зураг:', upload_to=ajiltan_directory_path_school_and_others)
	emp = models.ForeignKey(Ajiltan)

	@classmethod
	def export_to_excel(self, worksheet, row_start, col_start, row_step, queryset):
		row_write = row_start
		col_write = col_start
		for q in queryset:
			[row_write, col_write] = q.object_excel_write(worksheet, row_write, col_write, row_step = row_step)

	def object_excel_write(self, worksheet, row_start, col_start, **kwargs):
		row_step = kwargs['row_step']
		if row_step == 1:
			worksheet.write_string(row_start, col_start, self.zergiin_huree)
			worksheet.write_string(row_start, col_start+1, self.certificate_num)
		else:
			worksheet.merge_range(row_start, col_start, row_start+row_step-1, col_start, self.zergiin_huree)
			worksheet.merge_range(row_start, col_start+1, row_start+row_step-1, col_start+1, self.certificate_num)
		return [row_start+row_step, col_start]

	class Meta:
		verbose_name_plural = 'Мэргэшсэн болон зөвлөх зэргийн гэрчилгээ:'
	def __unicode__(self):
		return self.emp.emp_name




''' Системийн Хэрэглэгч '''
class User(SystemUser):
	user_id = models.OneToOneField(Ajiltan)
	created_by= models.ForeignKey('User', null = True, blank = True)

	def is_tza_alba(self):
		result = False
		if ZZ.objects.filter(id = self.user_id.baiguullaga.id):
			if self.user_id.tasag.dep_name == u'Тусгай зөвшөөрлийн алба':
				result = True
		return result
	def is_uta_alba(self):
		result = False
		if ZZ.objects.filter(id = self.user_id.baiguullaga.id):
			if self.user_id.tasag.dep_name == u'Үнэ тарифын алба':
				result = True
		return result
	def is_hzm_alba(self):
		result = False
		if ZZ.objects.filter(id = self.user_id.baiguullaga.id):
			if self.user_id.tasag.dep_name == u'Эрх зүй, мэдээлэл, захиргааны алба':
				result = True
		return result
	
	def has_tza_darga_permission(self):
		has_permission = False
		perm = Permission.objects.get(codename = 'tza_darga_permission')
		if perm in self.user.user_permissions.all():
			has_permission = True
		for group in self.user.groups.all():
			if perm in group.permissions.all():
				has_permission = True
		return has_permission

	def has_uta_darga_permission(self):
		has_permission = False
		perm = Permission.objects.get(codename = 'uta_darga_permission')
		if perm in self.user.user_permissions.all():
			has_permission = True
		for group in self.user.groups.all():
			if perm in group.permissions.all():
				has_permission = True
		return has_permission

	class Meta:
		verbose_name_plural = 'Хэрэглэгчийн бүртгэл'

	def __unicode__(self):
		return u"%s" %(self.username)

class User_change_history(Create):
	baiguullaga = models.ForeignKey(Baiguullaga)
	user_id = models.ForeignKey(Ajiltan)
	change_name = models.CharField(max_length=25)

''' Тусгай зөвшөөрлийн заалт '''
class TZ(Create):
	tz =models.CharField(max_length = 10,unique = True, verbose_name = 'Тусгай зөвшөөрлийн ID:')
	name = models.CharField(max_length = 500, verbose_name = 'Тусгай зөвшөөрлийн нэр:')
	description = models.CharField(max_length = 250, verbose_name = 'Тусгай зөвшөөрлийн тайлбар:')

	class Meta:
		verbose_name_plural = 'Тусгай зөвшөөрлийн бүртгэл'

	def __unicode__(self):
		return unicode(self.tz + "-"+ self.name)

''' Тусгай зөвшөөрөл эзэмшигчийн бүртгэл '''
class TZE(Baiguullaga):
	phone_dispetcher = models.CharField(max_length = 15, verbose_name = 'Диспетчерийн утас:', null=True, blank=True)

	def get_possible_tz_choices(self):
		# tz huselt gargaj boloh bolomjtoi tz zaaltuudiin listiig butsaana
		sungah_bolomjtoi_certs = self.get_sungah_bolomjtoi_certs()
		huchintei_certs = self.get_huchintei_certificates()
		certs = huchintei_certs.exclude(id = sungah_bolomjtoi_certs)

		all_tzs = self.get_tzs_of_huselts() | self.get_tzs_of_certificates(certs)
		possible_tzs = TZ.objects.exclude(id__in = all_tzs)
		return possible_tzs

	def get_tzs_of_huselts(self):
		yavts_tsutslagdsan = u'Цуцлагдсан'
		yavts_huselt_huleen_avaagui = u'Хүсэлтийг хүлээн аваагүй'
		yavts_huselt_zovshoorson = 'Хүсэлтийг зөвшөөрсөн'
		tz_huselts = TZ_Huselt.objects.filter(tze = self).exclude(yavts = yavts_tsutslagdsan).exclude(yavts=yavts_huselt_huleen_avaagui).exclude(yavts=yavts_huselt_zovshoorson)
		all_tzs = TZ.objects.none()
		for t in tz_huselts:
			all_tzs = all_tzs | t.burdel.tz.all()
		return all_tzs
	def get_tzs_of_certificates(self, certificates):
		all_tzs = TZ.objects.none()
		for c in certificates:
			all_tzs = all_tzs | c.tz_id.all()
		return all_tzs

	def get_huchintei_certificates(self):
		# huchintei tusgai zovshoorliin gerchilgeenuudiin querysetiig butsaana
		olgogdson, created = Certificate_tolov.objects.get_or_create(tolov = u'Хүчинтэй')
		qs = Certificate.objects.filter(tze = self, status = True, tolov = olgogdson)
		return qs
	def get_sungah_bolomjtoi_certs(self):
		certs = self.get_huchintei_certificates()
		sungah_bolomjtoi_cert_ids = []
		for c in certs:
			if c.is_sungah_bolomjtoi():
				sungah_bolomjtoi_cert_ids.append(c.id)
		qs = certs.filter(id__in = sungah_bolomjtoi_cert_ids)
		return qs

	def get_huchintei_zaaltuud(self):
		# huchintei tusgai zovshoorliin zaaltuudiin listiig butsaana
		zaaltuud = []
		for i in self.get_huchintei_certificates():
			for j in i.tz_id.all():
				zaaltuud.append(j.tz)
		return zaaltuud

	def get_tailan_names(self):
		# zaaltuudaas hamaaran uil ajillagaanii tailangiin nersiin listiig butsaana
		zaaltuud = self.get_huchintei_zaaltuud()
		if zaaltuud:
			m_names = [
					UAT.objects.get(material_number = 15),	# 
			]	# end buh huselted zaaval baih materialuudiin nersiig hiij ogno


			if '12.2.1' in zaaltuud:
				m_names.append(UAT.objects.get(material_number =1)) # 
				

			if '12.2.2' in zaaltuud:
				m_names.append(UAT.objects.get(material_number =2)) # 
				m_names.append(UAT.objects.get(material_number =3)) # 
				m_names.append(UAT.objects.get(material_number =4)) # 
				m_names.append(UAT.objects.get(material_number =5)) # 

			if '12.2.3' in zaaltuud:
				m_names.append(UAT.objects.get(material_number =6)) # 

			if '12.2.4' in zaaltuud:
				if not '12.2.3' in zaaltuud:
					m_names.append(UAT.objects.get(material_number =6)) # 

			if '12.2.5' in zaaltuud:
				m_names.append(UAT.objects.get(material_number =7)) # 
				m_names.append(UAT.objects.get(material_number =8)) #

			if '12.2.6' in zaaltuud:
				if not '12.2.5' in zaaltuud:
					m_names.append(UAT.objects.get(material_number =7)) #
					m_names.append(UAT.objects.get(material_number =8)) #

			if '12.2.7' in zaaltuud:
				m_names.append(UAT.objects.get(material_number =9)) # 

			if '12.2.8' in zaaltuud:
				if not '12.2.7' in zaaltuud:
					m_names.append(UAT.objects.get(material_number =9)) #

			if '12.2.9' in zaaltuud:
				if not '12.2.8' in zaaltuud and not '12.2.7' in zaaltuud:
					m_names.append(UAT.objects.get(material_number =9)) #

			if '12.2.10' in zaaltuud:
				m_names.append(UAT.objects.get(material_number =10)) # 
				m_names.append(UAT.objects.get(material_number =11)) # 

			if '12.2.11' in zaaltuud:
				pass

			if '12.2.12' in zaaltuud:
				m_names.append(UAT.objects.get(material_number =12)) # 

			if '12.2.13' in zaaltuud:
				m_names.append(UAT.objects.get(material_number =13)) # 

			if '12.2.14' in zaaltuud:
				m_names.append(UAT.objects.get(material_number =14)) # 

			return m_names
		else:
			return []

	def __unicode__(self):
		return unicode(self.org_name)

	def get_gshu_uzuulelt_num_list(self):
		zaaltuud = self.get_huchintei_zaaltuud()
		uzuulelt_num_list = []
		if zaaltuud:
			uzuulelt_num_list = [9, 10, 11, 12, 13, 14]
			if '12.2.1' in zaaltuud:
				uzuulelt_num_list.append(1)
				uzuulelt_num_list.append(2)
				uzuulelt_num_list.append(3)
			if '12.2.2' in zaaltuud:
				uzuulelt_num_list.append(4)
			if '12.2.3' in zaaltuud:
				uzuulelt_num_list.append(5)
				uzuulelt_num_list.append(6)
				uzuulelt_num_list.append(7)
			if '12.2.4' in zaaltuud and '12.2.3' not in zaaltuud:
				uzuulelt_num_list.append(5)
				uzuulelt_num_list.append(6)
				uzuulelt_num_list.append(7)
			if '12.2.10' in zaaltuud:
				uzuulelt_num_list.append(8)

		return uzuulelt_num_list


	def get_gshu_fields(self):
		uzuulelt_num_list = self.get_gshu_uzuulelt_num_list()
		fields=[]
		if uzuulelt_num_list:
			if 1 in uzuulelt_num_list:
				fields.append('Pasdws')
				fields.append('Nmean')
			if 2 in uzuulelt_num_list:
				fields.append('Q1')
				fields.append('Qr')
			if 3 in uzuulelt_num_list:
				fields.append('Q2')
				fields.append('Ec')
			if 4 in uzuulelt_num_list:
				fields.append('Nb')
				fields.append('Na')
			if 5 in uzuulelt_num_list:
				fields.append('Qn')
				fields.append('Qs1')
			if 6 in uzuulelt_num_list:
				fields.append('Qm')
				fields.append('Qs2')
			if 7 in uzuulelt_num_list:
				fields.append('Nn')
				fields.append('Ln')
			if 8 in uzuulelt_num_list:
				fields.append('BOD5input')
				fields.append('BOD5output')
				fields.append('COD5input')
				fields.append('COD5output')
				fields.append('SSinput')
				fields.append('SSoutput')
			if 9 in uzuulelt_num_list:
				fields.append('Ne1')
				fields.append('N1')
			if 10 in uzuulelt_num_list:
				fields.append('N1')
				fields.append('C')
			if 11 in uzuulelt_num_list:
				fields.append('BOsh')
				fields.append('BOshb')
			if 12 in uzuulelt_num_list:
				fields.append('O')
				fields.append('Z')
			if 13 in uzuulelt_num_list:
				fields.append('TsQs')
				fields.append('ZTsU')
				fields.append('BQs')
				fields.append('ZBU')
			if 14 in uzuulelt_num_list:
				fields.append('M')
				fields.append('B')

		return fields

class TZE_Users_bind(Create, History_operations):
	tze = models.OneToOneField(TZE)
	user_zahiral = models.OneToOneField(User, 	related_name = 'zahiral')
	user_engineer = models.OneToOneField(User, related_name = 'engineer', null=True, blank=True)
	user_account = models.OneToOneField(User, related_name = 'account', null=True, blank=True)
	history = HistoricalRecords()

class Handah_huselt_yavts(models.Model):
	yavts_name = models.CharField(verbose_name ='Явц',max_length = 250)

	class Meta:
		verbose_name_plural = 'Явц'

	def __unicode__(self):
		return unicode(self.yavts_name)
''' Хандах Хүсэлт '''
class Handah_huselt(Create):
	tze = models.ForeignKey(TZE)
	yavts=models.ForeignKey(Handah_huselt_yavts, verbose_name = 'Явц ID:')
	class Meta:
		pass

	def __unicode__(self):
		return unicode(self.tze.org_name)

class Tailbar(Create, History_operations):
	name = models.CharField(max_length = 250, verbose_name = u'Нэр', null = True, blank = True)

	class Meta:
		abstract = True

''' Аймаг орон нутгийн засаг даргын тодорхойлолт'''
class ZDTodorhoilolt(Tailbar):
	tze = models.ForeignKey(TZE)
	todorhoilolt_picture = models.FileField(verbose_name=u'Аймаг орон нутгийн засаг даргын тодорхойлолт', validators=[validate_file_extension], upload_to=user_directory_path)
	history = HistoricalRecords()

''' Хангагч байгууллага '''
class HangagchBaiguullaga(Tailbar):
	tze = models.ForeignKey(TZE)
	h_b_todorhoilolt = models.FileField(verbose_name=u'Хангагч байгууллагын тодорхойлолт',validators=[validate_file_extension], upload_to=user_directory_path)
	baiguulsan_geree = models.FileField(verbose_name=u'Хангагч байгууллагатай хийсэн гэрээ', validators=[validate_file_extension], upload_to=user_directory_path)
	history = HistoricalRecords()

''' Татварын тодорхойлолт '''
class TaxTodorhoilolt(Tailbar):
	tze = models.ForeignKey(TZE)
	todorhoilolt = models.FileField(verbose_name=u'Татварын тодорхойлолт' , validators=[validate_file_extension], upload_to=user_directory_path)
	history = HistoricalRecords()

''' Аудитын дүгнэлт '''
class AuditDugnelt(Tailbar):
	tze = models.ForeignKey(TZE)
	dugnelt = models.FileField(verbose_name=u'Аудитын дүгнэлт',  validators=[validate_file_extension], upload_to=user_directory_path)
	history = HistoricalRecords()

''' Санхүүгийн тайлан '''
class SanhuuTailan(Tailbar):
	tze = models.ForeignKey(TZE)
	tailan = models.FileField(verbose_name=u'Санхүүгийн баланс' , validators=[validate_file_extension], upload_to=user_directory_path)
	history = HistoricalRecords()

class Standart(models.Model):
	code = models.CharField(verbose_name='Стандартын код', max_length = 64)
	standart_name = models.CharField(verbose_name = 'Стандартын нэр:', max_length= 500)

	class Meta:
		verbose_name_plural = 'Стандартууд:'

	def __unicode__(self):
		return self.standart_name

class Huuli_durem_norm(models.Model):
	code = models.CharField(verbose_name='БНбД-ийн код:', max_length=128)
	name = models.CharField(verbose_name='БНбД-ийн нэр', max_length = 512)

''' Норм ба стандарт, техник баримт бичгийн жагсаалт '''
class NormStandart(Create, History_operations):
	tze = models.ForeignKey(TZE, verbose_name = 'Байгууллага')
	standart = models.ForeignKey(Standart, verbose_name = 'Стандарт:')
	history = HistoricalRecords()
	
class Baig_huuli_durem(Create, History_operations):
	tze = models.ForeignKey(TZE)
	durem = models.ForeignKey(Huuli_durem_norm)
	history = HistoricalRecords()

''' Ус ашиглах дүгнэлт зөвшөөрөл '''
class UsZuvshuurul(Create, History_operations):
	tze = models.ForeignKey(TZE)
	name = models.CharField(max_length = 250, verbose_name = u'Тайлбар', null = True, blank = True)
	dugnelt = models.FileField(verbose_name=u'Ус ашиглуулах дүгнэлт', null= True , validators=[validate_file_extension], upload_to=user_directory_path)
	zuvshuurul = models.FileField(verbose_name=u'Ус ашиглуулах зөвшөөрөл',null= True, validators=[validate_file_extension], upload_to=user_directory_path)
	geree = models.FileField(verbose_name=u'Ус ашиглуулах гэрээ', null= True , validators=[validate_file_extension], upload_to=user_directory_path)
	history = HistoricalRecords()

''' Улсын комиссын акт '''
class UlsiinAkt(Create, History_operations):
	tze = models.ForeignKey(TZE)
	akt = models.FileField(verbose_name=u'Улсын комиссын акт',validators=[validate_file_extension], upload_to=user_directory_path)
	history = HistoricalRecords()

'''Орон тооны бүтцийн схем'''
class OronTooniiSchema(Create, History_operations):
	tze =models.ForeignKey(TZE)
	name = models.CharField(max_length = 250, null = True, blank = True, verbose_name = u'Тайлбар')
	schema = models.FileField(verbose_name=u'Орон тооны бүтцийн схем' , validators=[validate_file_extension], upload_to=user_directory_path)
	history = HistoricalRecords()
	
''' Үйлдвэрийн технологийн схем зураг '''
class UildverTechnology(Create, History_operations):
	tze = models.ForeignKey(TZE)
	schema = models.FileField(verbose_name=u'Үйлдвэрийн технологийн схем зураг',validators=[validate_file_extension], upload_to=user_directory_path)
	history = HistoricalRecords()

''' Байгууллагын лабораторийн шинжилгээнд өгсөн Мэргэжлийн Хяналтын Газрын дүгнэлт '''
class MergejliinHyanalt(Create, History_operations):
	tze = models.ForeignKey(TZE)
	dugnelt = models.FileField(verbose_name=u'Байгууллагын лабораторийн шинжилгээнд өгсөн Мэргэжлийн Хяналтын Газрын дүгнэлт',validators=[validate_file_extension], upload_to=user_directory_path)
	history = HistoricalRecords()

''' Ажлын байрны дүгнэлт '''
class AjliinBair(Create, History_operations):
	tze = models.ForeignKey(TZE)
	dugnelt = models.FileField(verbose_name=u'Ажлын байрны дүгнэлт',validators=[validate_file_extension], upload_to=user_directory_path)
	history = HistoricalRecords()

''' Тухайн оны үйл ажиллагааны орлогын төлөвлөгөө '''
class OrlogiinTolovlogoo(Create, History_operations):	
	tze = models.ForeignKey(TZE)
	tolovlogoo = models.FileField(validators=[validate_file_extension], upload_to=user_directory_path)
	history = HistoricalRecords()

''' Тусгай зөвшөөрлийн зураг '''
class TZPicture(Create, History_operations):
	tze = models.ForeignKey(TZE)
	tz = models.ForeignKey(TZ)
	picture = models.FileField(validators=[validate_file_extension], upload_to=user_directory_path)
	history = HistoricalRecords()

''' Зохицуулах зөвлөлийн бүртгэл '''
class ZZ(Baiguullaga):
	pass



class Certificate_tolov(models.Model):
	tolov = models.CharField(max_length = 15, verbose_name = 'Төлөв:')

	class Meta:
		verbose_name_plural = u'Гэрчилгээний төлвийн жагсаалт'

	def __unicode__(self):
		return unicode(self.tolov)

''' Ашиглалтыг нь хариуцаж байгаа барилга байгууламж '''
class ABB(Create, History_operations):
	tze = models.ForeignKey(TZE)
	barilga_ner = models.CharField(max_length = 500, verbose_name = 'Барилгын нэр, дугаар')
	niit = models.IntegerField( verbose_name = 'Нийт өрхийн тоо')
	tooluurjilt_too = models.IntegerField( verbose_name = 'Тоолууртай өрхийн тоо')
	aan_too = models.IntegerField(verbose_name = 'Аж ахуй нэгжийн тоо')
	tooluurjilt_too_aan = models.IntegerField(verbose_name = 'Тоолууртай ААН-ийн тоо')
	photo = models.ImageField( verbose_name = 'Зураг',validators=[validate_picture_extension, validate_file_size], upload_to=user_directory_path)
	city = models.ForeignKey(Aimag, verbose_name = 'Аймаг, Хот:',)
	district = ChainedForeignKey(Sum, verbose_name = 'Сум, Дүүрэг:', chained_field = 'city', chained_model_field = 'aimag_id')
	khoroo = ChainedForeignKey(Bag, verbose_name = 'Баг, Хороо:', chained_field = 'district', chained_model_field = 'sum_id')
	address = models.CharField(max_length = 500,verbose_name = "Барилгын байршил дэлгэрэнгүй")
	ulsiinakt = models.FileField(verbose_name=u'Улсын комиссын акт',validators=[validate_file_extension, validate_file_size], upload_to=user_directory_path)
	geree  = models.FileField(verbose_name=u'Гэрээ', validators=[validate_file_extension, validate_file_size], upload_to=user_directory_path)
	approved = models.BooleanField(default=False)
	history = HistoricalRecords()

	@classmethod
	def excel_write_header_and_format(self, worksheet, row_start, col_start):
		worksheet.write_string(row_start, col_start, u'ТЗЭ')
		worksheet.write_string(row_start, col_start+1, u'Аймаг,хот')
		worksheet.write_string(row_start, col_start+2, u'Сум, дүүрэг')
		worksheet.write_string(row_start, col_start+3, u'Баг, хороо')
		worksheet.write_string(row_start, col_start+4, u'Байрлал')
		worksheet.write_string(row_start, col_start+5, u'Барилгын нэр дугаар')
		worksheet.write_string(row_start, col_start+6, u'Нийт өрхийн тоо')
		worksheet.write_string(row_start, col_start+7, u'Тоолууртай өрхийн тоо')
		worksheet.write_string(row_start, col_start+8, u'Аж ахуй нэгжийн тоо')
		worksheet.write_string(row_start, col_start+9, u'Тоолууртай ААН-ийн тоо')


		return [row_start+1, col_start]

	def object_excel_write(self, worksheet, row_start, col_start, **kwargs):
		date_time=kwargs['date_time']
		hist_obj = self.get_history_object(date_time)

		if hist_obj:
			if hist_obj.status==True:
				worksheet.write_string(row_start, col_start, hist_obj.tze.org_name + ' ' + hist_obj.tze.org_type)
				worksheet.write_string(row_start, col_start+1, hist_obj.city.aimag_name)
				worksheet.write_string(row_start, col_start+2, hist_obj.district.sum_name)
				worksheet.write_string(row_start, col_start+3, hist_obj.khoroo.bag_name)
				worksheet.write_string(row_start, col_start+4, hist_obj.address)
				worksheet.write_string(row_start, col_start+5, hist_obj.barilga_ner)
				worksheet.write_number(row_start, col_start+6, hist_obj.niit)
				worksheet.write_number(row_start, col_start+7, hist_obj.tooluurjilt_too)
				worksheet.write_number(row_start, col_start+8, hist_obj.aan_too)
				worksheet.write_number(row_start, col_start+9, hist_obj.tooluurjilt_too_aan)
				return [row_start+1, col_start] # daraagiin object bichih coordinatiig butsaana
			else:
				# history ni status=False baina
				return [row_start, col_start]
		else:
			# history object doesn't exist
			return [row_start, col_start]
		


# Барилга байгууламж
class BB(Create, History_operations):
	tze = models.ForeignKey(TZE)
	approved = models.BooleanField(default=False)
	history = HistoricalRecords(inherit = True)

equipment_torol = (
		(u'Тээврийн хэрэгсэл хүнд машин механизм', 'Тээврийн хэрэгсэл хүнд машин механизм'),
		(u'Технологийн тоног төхөөрөмж, багаж хэрэгсэл', 'Технологийн тоног төхөөрөмж, багаж хэрэгсэл'),
		(u'Хэмжүүр ба хяналт шалгалтын багаж схем', 'Хэмжүүр ба хяналт шалгалтын багаж схем'),
		(u'Хөдөлмөр хамгааллын багаж хэрэгсэл', 'Хөдөлмөр хамгааллын багаж хэрэгсэл'),
		)
omchiin_helber = (
	(u'Байгууллагынх', u'Байгууллагынх'),
	(u'Түрээсийнх', u'Түрээсийнх'),
	(u'Бусад', u'Бусад'),
	)
''' Тоног төхөөрөмж '''
class Equipment(Create, History_operations):
	tze = models.ForeignKey(TZE, verbose_name = 'Байгууллага:')
	name = models.CharField(max_length = 400, null = True, verbose_name = 'Тоног төхөөрөмжийн нэр:')
	torol_id = models.CharField(max_length = 50, choices = equipment_torol, verbose_name = 'Төхөөрөмжийн төрөл:')
	too = models.IntegerField(verbose_name = 'Тоо:')
	huchin_chadal = models.FloatField(verbose_name = 'Хүчин чадал:')
	elegdliin_chanar = models.CharField(max_length = 50, verbose_name = 'Элэгдлийн чанар:')
	ashiglaltand_orson_ognoo = models.CharField(max_length = 4, verbose_name = 'Ашиглалтанд орсон он:', validators = [validate_year])
	balans_une = models.IntegerField(verbose_name = 'Баланс үнэ (төг):')
	hurimtlagdsan_elegdel = models.CharField(max_length = 4000, verbose_name = 'Хуримтлагдсан элэгдэл (төг):')
	elegdel_huvi = models.IntegerField(verbose_name = 'Элэгдлийн хувь/%/:')
	eh_uusver = models.CharField(max_length = 30, verbose_name = 'Өмчийн хэлбэр:', choices = omchiin_helber)
	approved = models.BooleanField(default=False)
	history = HistoricalRecords()


	@classmethod
	def excel_write_header_and_format(self, worksheet, row_start, col_start):
		worksheet.write_string(row_start, col_start, u'ТЗЭ')
		worksheet.write_string(row_start, col_start+1, u'Тоног төхөөрөмжийн нэр')
		worksheet.write_string(row_start, col_start+2, u'Тоног төхөөрөмжийн төрөл')
		worksheet.write_string(row_start, col_start+3, u'Тоо')
		worksheet.write_string(row_start, col_start+4, u'Хүчин чадал')
		worksheet.write_string(row_start, col_start+5, u'Элэгдлийн чанар')
		worksheet.write_string(row_start, col_start+6, u'Ашиглалтанд орсон он')
		worksheet.write_string(row_start, col_start+7, u'Баланс үнэ')
		worksheet.write_string(row_start, col_start+8, u'Хуримтлагдсан элэгдэл')
		worksheet.write_string(row_start, col_start+9, u'Элэгдлийн хувь /%/')
		worksheet.write_string(row_start, col_start+10, u'Өмчийн хэлбэр')
		return [row_start+1, col_start]
		
	def object_excel_write(self, worksheet, row_start, col_start, **kwargs):
		date_time=kwargs['date_time']
		hist_obj = self.get_history_object(date_time)

		if hist_obj:
			if hist_obj.status==True:
				worksheet.write_string(row_start, col_start, hist_obj.tze.org_name + ' ' + hist_obj.tze.org_type)
				worksheet.write_string(row_start, col_start+1, hist_obj.name)
				worksheet.write_string(row_start, col_start+2, hist_obj.torol_id)
				worksheet.write_number(row_start, col_start+3, hist_obj.too)
				worksheet.write_number(row_start, col_start+4, hist_obj.huchin_chadal)
				worksheet.write_string(row_start, col_start+5, hist_obj.elegdliin_chanar)
				worksheet.write_string(row_start, col_start+6, hist_obj.ashiglaltand_orson_ognoo)
				worksheet.write_number(row_start, col_start+7, hist_obj.balans_une)
				worksheet.write_string(row_start, col_start+8, hist_obj.hurimtlagdsan_elegdel)
				worksheet.write_number(row_start, col_start+9, hist_obj.elegdel_huvi)
				worksheet.write_string(row_start, col_start+10, hist_obj.eh_uusver)
				return [row_start+1, col_start] # daraagiin object bichih coordinatiig butsaana
			else:
				# history ni status=False baina
				return [row_start, col_start]
		else:
			# history object doesn't exist
			return [row_start, col_start]


	class Meta:
		verbose_name_plural = 'Машин тоног төхөөрөмжийн жагсаалт:'

	def __unicode__(self):
		return unicode(self.torol_id)

# Лаб
lab_torol_choices = (
	(u'Цэвэр усны лаборатори', u'Цэвэр усны лаборатори'),
	(u'Бохир усны лаборатори', u'Бохир усны лаборатори'),
	)
lab_ajillagaa_choices = (
	(u'Бүрэн ажиллагаатай', u'Бүрэн ажиллагаатай'),
	(u'Хагас ажиллагаатай', u'Хагас ажиллагаатай'),
	(u'Ажиллахгүй байгаа', u'Ажиллахгүй байгаа'),
	)

class Lab(BB):
	torol = models.CharField(max_length = 64, verbose_name='Лабораторийн төрөл:', choices=lab_torol_choices)
	ajillagaa = models.CharField(max_length=64, verbose_name='Ажиллагаа:', choices=lab_ajillagaa_choices)
	tailbar = models.CharField(max_length=256, verbose_name='Тайлбар:', null=True, blank = True)
	shinjilgee_count = models.IntegerField(verbose_name='Шинжилгээний тоо:')
	ashiglaltand_orson_ognoo = models.CharField(max_length = 4, verbose_name = 'Ашиглалтанд орсон он:', validators = [validate_year])

	@classmethod
	def excel_write_header_and_format(self, worksheet, row_start, col_start):
		worksheet.merge_range(row_start, col_start, row_start+1, col_start,u'ТЗЭ')
		worksheet.merge_range(row_start, col_start+1, row_start+1, col_start+1,u'Лабораторийн төрөл')
		worksheet.merge_range(row_start, col_start+2, row_start+1, col_start+2,u'Шинжилгээний тоо')
		worksheet.merge_range(row_start, col_start+3, row_start+1, col_start+3,u'Ажиллагаа')
		worksheet.merge_range(row_start, col_start+4, row_start+1, col_start+4,u'Тайлбар')
		worksheet.merge_range(row_start, col_start+5, row_start+1, col_start+5,u'Ашиглалтанд орсон он')


		worksheet.write_string(row_start, col_start+6, u'Лабораторийн багаж, төхөөрөмж')
		worksheet.write_string(row_start+1, col_start+6, u'Багаж, Тоног төхөөрөмжийн нэр')


		worksheet.merge_range(row_start, col_start+7, row_start, col_start+8, u'Лабораторийн өргөтгөл')
		worksheet.write_string(row_start+1, col_start+7, u'Хөрөнгө оруулалтын эх үүсвэр')
		worksheet.write_string(row_start+1, col_start+8, u'Өргөтгөл хийсэн он')

		return [row_start+2, col_start]
		

	def object_excel_write(self, worksheet, row_start, col_start, **kwargs):
		date_time = kwargs['date_time']
		hist_obj = self.get_history_object(date_time)

		if hist_obj:
			if hist_obj.status==True:
				bagaj_count = self.get_bagaj_count(date_time)
				orgotgol_count = self.get_orgotgol_count(date_time)

				if bagaj_count == 0:
					bagaj_count=1
				if orgotgol_count == 0:
					orgotgol_count = 1

				least_common_multiply = lcm(bagaj_count, orgotgol_count)

				if least_common_multiply>1:
					worksheet.merge_range(row_start, col_start, row_start+least_common_multiply-1, col_start, hist_obj.tze.org_name + ' ' + hist_obj.tze.org_type)
					worksheet.merge_range(row_start, col_start+1, row_start+least_common_multiply-1, col_start+1, hist_obj.torol)
					worksheet.merge_range(row_start, col_start+2, row_start+least_common_multiply-1, col_start+2, hist_obj.shinjilgee_count)
					worksheet.merge_range(row_start, col_start+3, row_start+least_common_multiply-1, col_start+3, hist_obj.ajillagaa)
					worksheet.merge_range(row_start, col_start+4, row_start+least_common_multiply-1, col_start+4, hist_obj.tailbar)
					worksheet.merge_range(row_start, col_start+5, row_start+least_common_multiply-1, col_start+5, hist_obj.ashiglaltand_orson_ognoo)

				else:
					worksheet.write_string(row_start, col_start, hist_obj.tze.org_name + ' ' + hist_obj.tze.org_type)
					worksheet.write_string(row_start, col_start+1, hist_obj.torol)
					worksheet.write_number(row_start, col_start+2, hist_obj.shinjilgee_count)
					worksheet.write_string(row_start, col_start+3, hist_obj.ajillagaa)
					worksheet.write_string(row_start, col_start+4, hist_obj.tailbar)
					worksheet.write_string(row_start, col_start+5, hist_obj.ashiglaltand_orson_ognoo)

				# bagaj export
				if bagaj_count != 1:
					bagajs = self.get_sub_objects(LabBagaj, 'lab_id', date_time)
					LabBagaj.export_to_excel(worksheet, row_start, col_start+6, least_common_multiply/len(bagajs), bagajs)
				else:
					bagajs = self.get_sub_objects(LabBagaj, 'lab_id', date_time)
					if len(bagajs) == 1:
						LabBagaj.export_to_excel(worksheet, row_start, col_start+6, least_common_multiply/len(bagajs), bagajs)
					else:
						# bagaj baihgui uyd
						if least_common_multiply == 1:
							worksheet.write_string(row_start, col_start+6, u'Бүртгэгдсэн багаж төхөөрөмж байхгүй')
						else:
							worksheet.merge_range(row_start, col_start+6, row_start+least_common_multiply-1, col_start+6, u'Бүртгэгдсэн багаж төхөөрөмж байхгүй')


				# orgotgol export
				if orgotgol_count != 1:
					orgotgols = self.get_sub_objects(Lab_orgotgol, 'lab_id', date_time)
					Lab_orgotgol.export_to_excel(worksheet, row_start, col_start+7, least_common_multiply/len(orgotgols), orgotgols)
				else:
					orgotgols = self.get_sub_objects(Lab_orgotgol, 'lab_id', date_time)
					if len(orgotgols) == 1:
						Lab_orgotgol.export_to_excel(worksheet, row_start, col_start+7, least_common_multiply/len(orgotgols), orgotgols)
					else:
						# orgotgol baihgui uyd
						worksheet.merge_range(row_start, col_start+7, row_start+least_common_multiply-1, col_start+8, u'Бүртгэгдсэн мэдээлэл байхгүй')

				return [row_start+least_common_multiply, col_start] # daraagiin object bichih coordinatiig butsaana
			else:
				# history object status==False uyd
				return [row_start, col_start]
		else:
			# history object baihgui uyd
			return [row_start, col_start]


	def get_shinjilgee_list_names(self):
		verbose_names = []
		exclude_fields = ['tze_id', 'status', 'created_by_id']
		for field_name, val in self:
			if field_name not in exclude_fields and val == True:
				verbose_names.append(self._meta.get_field(field_name).verbose_name)
		return verbose_names
	def get_shinjilgee_count(self):
		return self.shinjilgee_count
	def __iter__(self):
		for field_name in self._meta.get_all_field_names():
			value = getattr(self, field_name, None)
			yield (field_name, value)
	def get_bagaj_count(self, date_time=timezone.now()):
		list_bagaj = self.get_sub_objects(LabBagaj, 'lab_id', date_time)
		return len(list_bagaj)
	def get_orgotgol_count(self, date_time=timezone.now()):
		list_orgotgol = self.get_sub_objects(Lab_orgotgol, 'lab_id', date_time)
		return len(list_orgotgol)

# Лабын багаж
class LabBagaj(Create, History_operations):
	lab_id=models.ForeignKey(Lab)
	bagaj = models.CharField(max_length=500,verbose_name=u'Багаж, тоног төхөөрөмжийн нэр')
	history = HistoricalRecords()

	@classmethod
	def export_to_excel(self, worksheet, row_start, col_start, row_step, queryset):
		row_write = row_start
		col_write = col_start
		for q in queryset:
			[row_write, col_write] = q.object_excel_write(worksheet, row_write, col_write, row_step = row_step)

	def object_excel_write(self, worksheet, row_start, col_start, **kwargs):
		row_step = kwargs['row_step']
		if row_step == 1:
			worksheet.write_string(row_start, col_start, self.bagaj)
		else:
			worksheet.merge_range(row_start, col_start, row_start+row_step-1, col_start, self.bagaj)
		return [row_start+row_step, col_start]
class Lab_orgotgol(Create, History_operations):
	lab_id = models.ForeignKey(Lab)
	horongo_uusver = models.CharField(max_length=256, verbose_name='Хөрөнгө оруулалтын эх үүсвэр:')
	ognoo = models.CharField(max_length = 4, verbose_name = 'Өргөтгөл хийсэн он:', validators = [validate_year])
	history = HistoricalRecords()

	@classmethod
	def export_to_excel(self, worksheet, row_start, col_start, row_step, queryset):
		row_write = row_start
		col_write = col_start
		for q in queryset:
			[row_write, col_write] = q.object_excel_write(worksheet, row_write, col_write, row_step = row_step)

	def object_excel_write(self, worksheet, row_start, col_start, **kwargs):
		row_step = kwargs['row_step']
		if row_step == 1:
			worksheet.write_string(row_start, col_start, self.horongo_uusver)
			worksheet.write_string(row_start, col_start+1, self.ognoo)
		else:
			worksheet.merge_range(row_start, col_start, row_start+row_step-1, col_start, self.horongo_uusver)
			worksheet.merge_range(row_start, col_start+1, row_start+row_step-1, col_start+1, self.ognoo)
		return [row_start+row_step, col_start]

# Насос
class NasosStants(BB):
	ca = ((u'Автомат' , u'Автомат' ),
		(u'Хагас автомат' , u'Хагас автомат' ),
		(u'Механик', u'Механик'),
		)
	cb = ((u'Цэвэр усны насос станц', u'Цэвэр усны насос станц' ),
		(u'Бохир усны насос станц', u'Бохир усны насос станц'),
		)
	ashiglaltand_orson_ognoo = models.CharField(max_length = 4, verbose_name = 'Ашиглалтанд орсон он:', validators = [validate_year])
	nasos_torol= models.CharField(choices=cb,max_length = 100, verbose_name=u'Насосны станцын төрөл')
	nasos_name= models.CharField(max_length = 500, verbose_name=u'Насос станцын нэр',null= True, blank=True)
	city = models.ForeignKey(Aimag, verbose_name = 'Насос станцын байршил/Аймаг, хот/:',)
	district = ChainedForeignKey(Sum, verbose_name = 'Насос станцын байршил/Сум, дүүрэг/:', chained_field = 'city', chained_model_field = 'aimag_id')
	khoroo = ChainedForeignKey(Bag, verbose_name = 'Насос станцын байршил/Баг, хороо/:', chained_field = 'district', chained_model_field = 'sum_id')
	nasos_address= models.CharField(max_length = 1000, verbose_name=u'Насос станцын байршил',null= True, blank=True)
	nasos_ajillagaa= models.CharField(choices=ca, max_length = 100,verbose_name=u'Насос станцын ажиллагаа')
	picture_outside = models.ImageField(verbose_name=u'Насос станцын гадна талын зураг',validators=[validate_picture_extension, validate_file_size], upload_to=nasos_directory_path)
	picture_inside = models.ImageField(verbose_name=u'Насос станцын дотор талын зураг',validators=[validate_picture_extension, validate_file_size], upload_to=nasos_directory_path)
	class Meta:
		permissions = (("can_view_nasosStants", "Can view NasosStants"),)

	def get_nasos_count(self, date_time=timezone.now()):
		list_nasoss = self.get_sub_objects(Nasoss, 'nasos_stants', date_time)
		if list_nasoss:
			return len(list_nasoss)
		else:
			return 0
	def get_huchin_chadal(self):
		huchin_chadal = 0
		nasoses = Nasoss.objects.filter(nasos_stants = self, status=True)
		for nasos in nasoses:
			huchin_chadal = nasos.huchin_chadal + huchin_chadal
		return huchin_chadal

	def is_davhtssan(self):
		qs = NasosStants.objects.filter(city=self.city, district=self.district, khoroo=self.khoroo, nasos_name=self.nasos_name ,approved=True, status=True,).exclude(id=self.id)
		if qs:
			return True
		else:
			return False

	@classmethod
	def excel_write_header_and_format(self, worksheet, row_start, col_start):
		worksheet.merge_range(row_start, col_start, row_start+1, col_start,u'ТЗЭ')
		worksheet.merge_range(row_start, col_start+1, row_start+1, col_start+1,u'Насос станцын төрөл')
		worksheet.merge_range(row_start, col_start+2, row_start+1, col_start+2,u'Насос станцын нэр')
		worksheet.merge_range(row_start, col_start+3, row_start+1, col_start+3,u'Аймаг, хот')
		worksheet.merge_range(row_start, col_start+4, row_start+1, col_start+4,u'Сум, дүүрэг')
		worksheet.merge_range(row_start, col_start+5, row_start+1, col_start+5,u'Баг, хороо')
		worksheet.merge_range(row_start, col_start+6, row_start+1, col_start+6,u'Байршил')
		worksheet.merge_range(row_start, col_start+7, row_start+1, col_start+7,u'Насос станцын ажиллагаа')


		worksheet.merge_range(row_start, col_start+8, row_start, col_start+12, u'Насос')
		worksheet.write_string(row_start+1, col_start+8, u'Марк')
		worksheet.write_string(row_start+1, col_start+9, u'Хүчин чадал м3/хоног')
		worksheet.write_string(row_start+1, col_start+10, u'Үйлдвэрлэсэн улс')
		worksheet.write_string(row_start+1, col_start+11, u'Тоо')
		worksheet.write_string(row_start+1, col_start+12, u'Ашиглалтанд орсон он')

		return [row_start+2, col_start]
		

	def object_excel_write(self, worksheet, row_start, col_start, **kwargs):
		date_time = kwargs['date_time']
		hist_obj = self.get_history_object(date_time)

		if hist_obj:
			if hist_obj.status==True:
				nasos_count = self.get_nasos_count(date_time)
				if nasos_count>1:
					worksheet.merge_range(row_start, col_start, row_start+nasos_count-1, col_start, hist_obj.tze.org_name + ' ' + hist_obj.tze.org_type)
					worksheet.merge_range(row_start, col_start+1, row_start+nasos_count-1, col_start+1, hist_obj.nasos_torol)
					worksheet.merge_range(row_start, col_start+2, row_start+nasos_count-1, col_start+2, hist_obj.nasos_name)
					worksheet.merge_range(row_start, col_start+3, row_start+nasos_count-1, col_start+3, hist_obj.city.aimag_name)
					worksheet.merge_range(row_start, col_start+4, row_start+nasos_count-1, col_start+4, hist_obj.district.sum_name)
					worksheet.merge_range(row_start, col_start+5, row_start+nasos_count-1, col_start+5, hist_obj.khoroo.bag_name)
					worksheet.merge_range(row_start, col_start+6, row_start+nasos_count-1, col_start+6, hist_obj.nasos_address)
					worksheet.merge_range(row_start, col_start+7, row_start+nasos_count-1, col_start+7, hist_obj.nasos_ajillagaa)

					nasosnuud = self.get_sub_objects(Nasoss, 'nasos_stants', date_time)
					Nasoss.export_to_excel(worksheet, row_start, col_start+8, nasosnuud)
				else:
					worksheet.write_string(row_start, col_start, hist_obj.tze.org_name + ' ' + hist_obj.tze.org_type)
					worksheet.write_string(row_start, col_start+1, hist_obj.nasos_torol)
					worksheet.write_string(row_start, col_start+2, hist_obj.nasos_name)
					worksheet.write_string(row_start, col_start+3, hist_obj.city.aimag_name)
					worksheet.write_string(row_start, col_start+4, hist_obj.district.sum_name)
					worksheet.write_string(row_start, col_start+5, hist_obj.khoroo.bag_name)
					worksheet.write_string(row_start, col_start+6, hist_obj.nasos_address)
					worksheet.write_string(row_start, col_start+7, hist_obj.nasos_ajillagaa)
					if nasos_count == 1:
						nasosnuud = self.get_sub_objects(Nasoss, 'nasos_stants', date_time)
						Nasoss.export_to_excel(worksheet, row_start, col_start+8, nasosnuud)
					else:
						# hervee shugam suljee hooloigui baival
						worksheet.merge_range(row_start, col_start+8, row_start, col_start+12, u'Бүртгэгдсэн насос байхгүй')
						return [row_start+1, col_start]
						
				return [row_start+nasos_count, col_start] # daraagiin object bichih coordinatiig butsaana
			else:
				# history object status==False uyd
				return [row_start, col_start]
		else:
			# history object baihgui uyd
			return [row_start, col_start]
uildverlesen_uls_choices = (
	(u'АНУ', u'АНУ'),
	(u'БНХАУ', u'БНХАУ'),
	(u'ОХУ', u'ОХУ'),
	(u'Герман', u'Герман'),
	(u'Бусад', u'Бусад'),
	)
class Nasoss(Create, History_operations):
	nasos_stants = models.ForeignKey(NasosStants)
	huchin_chadal = models.IntegerField(verbose_name=u'Хүчин чадал (м3/хон)')
	too = models.IntegerField(verbose_name=u'Тоо')
	mark = models.CharField(max_length = 30, verbose_name=u'Насосны марк')
	country = models.CharField(max_length = 20, verbose_name=u'Үйлдвэрлэсэн улс', choices = uildverlesen_uls_choices)
	ashiglaltand_orson_ognoo = models.CharField(max_length = 4, verbose_name = 'Ашиглалтанд орсон он:', validators = [validate_year])
	history = HistoricalRecords()
	
	@classmethod
	def export_to_excel(self, worksheet, row_start, col_start, queryset):
		row_write = row_start
		col_write = col_start
		for q in queryset:
			[row_write, col_write] = q.object_excel_write(worksheet, row_write, col_write)

	def object_excel_write(self, worksheet, row_start, col_start, **kwargs):
		worksheet.write_number(row_start, col_start, self.huchin_chadal)
		worksheet.write_string(row_start, col_start+1, self.mark)
		worksheet.write_string(row_start, col_start+2, self.country)
		worksheet.write_number(row_start, col_start+3, self.too)
		worksheet.write_string(row_start, col_start+4, self.ashiglaltand_orson_ognoo)

		return [row_start+1, col_start]

# Гүний худаг
class Hudag(BB):
	ca = ((u'Энгийн', u'Энгийн' ),
		(u'Гэрээт', u'Гэрээт'),
		(u'Онцгой', u'Онцгой'),
		)
	city = models.ForeignKey(Aimag, verbose_name = 'Худгийн байршил/Аймаг, хот/:', null=True)
	district = ChainedForeignKey(Sum, verbose_name = 'Худгийн байршил/Сум, дүүрэг/:', chained_field = 'city', chained_model_field = 'aimag_id', null=True)
	khoroo = ChainedForeignKey(Bag, verbose_name = 'Худгийн байршил/Баг, хороо/:', chained_field = 'district', chained_model_field = 'sum_id', null=True)
	hudag_address= models.CharField(max_length = 1000, verbose_name=u'Худгийн байршил',null= True, blank=True)
	ashiglaltand_orson_ognoo = models.CharField(max_length = 4, verbose_name = 'Худгийн ашиглалтанд орсон он:', validators = [validate_year])
	huchin_chadal = models.FloatField(verbose_name=u'Насосны хүчин чадал (м3/хон)', null = True, blank = True)
	mark = models.CharField(max_length = 30, verbose_name=u'Насосны марк')
	country = models.CharField(max_length = 20, verbose_name=u'Үйлдвэрлэсэн улс', choices = uildverlesen_uls_choices)
	nasos_ognoo = models.CharField(max_length = 4, verbose_name = 'Насосны ашиглалтанд орсон он:', validators = [validate_year])
	olborloj_bui_us = models.FloatField(verbose_name=u'Олборлож буй ус(м3/хон)')
	tsoonog = models.FloatField(verbose_name=u'Гүний худгийн цооногийн гүн(м)',null= True, blank=True)
	haruul = models.CharField(max_length = 4000,choices=ca, verbose_name=u'Эх үүсвэрийн харуул хамгаалалтын тухай')
	tailbar = models.CharField(max_length = 500, verbose_name=u'Тайлбар/ажиллаж байгаа эсэх/', null = True, blank = True)
	outside_picture = models.ImageField(verbose_name=u'Гадна талын фото зураг',validators=[validate_picture_extension, validate_file_size], upload_to=hudag_directory_path)
	inside_picture = models.ImageField(verbose_name=u'Дотор талын фото зураг',validators=[validate_picture_extension, validate_file_size], upload_to=hudag_directory_path)

	@classmethod
	def excel_write_header_and_format(self, worksheet, row_start, col_start):
		worksheet.write_string(row_start, col_start, u'ТЗЭ')
		worksheet.write_string(row_start, col_start+1, u'Аймаг,хот')
		worksheet.write_string(row_start, col_start+2, u'Сум, дүүрэг')
		worksheet.write_string(row_start, col_start+3, u'Баг, хороо')
		worksheet.write_string(row_start, col_start+4, u'Байрлал')
		worksheet.write_string(row_start, col_start+5, u'Ашиглалтанд орсон огноо')
		worksheet.write_string(row_start, col_start+6, u'Цооногийн гүн (м)')
		worksheet.write_string(row_start, col_start+7, u'Насосны марк')
		worksheet.write_string(row_start, col_start+8, u'Насос үйлдвэрлэсэн улс')
		worksheet.write_string(row_start, col_start+9, u'Насосны хүчин чадал м3/хон')
		worksheet.write_string(row_start, col_start+10, u'Насосны ашиглалтанд орсон огноо')
		worksheet.write_string(row_start, col_start+11, u'Олборлож буй ус')

		return [row_start+1, col_start]

		
	def object_excel_write(self, worksheet, row_start, col_start, **kwargs):
		date_time=kwargs['date_time']
		hist_obj = self.get_history_object(date_time)

		if hist_obj:
			if hist_obj.status==True:
				worksheet.write_string(row_start, col_start, hist_obj.tze.org_name + ' ' + hist_obj.tze.org_type)
				worksheet.write_string(row_start, col_start+1, hist_obj.city.aimag_name)
				worksheet.write_string(row_start, col_start+2, hist_obj.district.sum_name)
				worksheet.write_string(row_start, col_start+3, hist_obj.khoroo.bag_name)
				worksheet.write_string(row_start, col_start+4, hist_obj.hudag_address)
				worksheet.write_string(row_start, col_start+5, hist_obj.ashiglaltand_orson_ognoo)
				worksheet.write_number(row_start, col_start+6, hist_obj.tsoonog)
				worksheet.write_string(row_start, col_start+7, hist_obj.mark)
				worksheet.write_string(row_start, col_start+8, hist_obj.country)
				worksheet.write_number(row_start, col_start+9, hist_obj.huchin_chadal)
				worksheet.write_string(row_start, col_start+10, hist_obj.nasos_ognoo)
				worksheet.write_number(row_start, col_start+11, hist_obj.olborloj_bui_us)
				return [row_start+1, col_start] # daraagiin object bichih coordinatiig butsaana
			else:
				# history ni status=False baina
				return [row_start, col_start]
		else:
			# history object doesn't exist
			return [row_start, col_start]
#Бүх гүний худгуудыг нэгтгэсэн байршлын схем зураг
class HudagNegtsgesenBairshliinZurag(Create, History_operations):
	tze=models.ForeignKey(TZE)
	comments = models.CharField(max_length = 250, verbose_name = u'Тайлбар:', null = True, blank = True)
	bairshliin_picture = models.ImageField(verbose_name=u'Ус хангамжийн системийн схем зураг',validators=[validate_picture_extension, validate_file_size], upload_to=hudag_negdsen_directory_path)
	history = HistoricalRecords()
	

# Шугам сүлжээ
class Sh_suljee(BB):
	shugam_helber = ((u'Цэвэр усны шугам сүлжээ', u'Цэвэр усны шугам сүлжээ' ),
		(u'Бохир усны шугам сүлжээ', u'Бохир усны шугам сүлжээ'),
		)
	shugam_choices = (
		(u'Эх үүсвэрийн цуглуулах',u'Эх үүсвэрийн цуглуулах'),
		(u'Цэвэр усны дамжуулах шугам',u'Цэвэр усны дамжуулах шугам'),
		(u'Цэвэр ус түгээх шугам', u'Цэвэр ус түгээх шугам'),
		(u'Бохир усны гаргалгааны шугам', u'Бохир усны гаргалгааны шугам'),
		(u'Бохир усны цуглуулах шугам', u'Бохир усны цуглуулах шугам'),
		(u'Бохир ус татан зайлуулах шугам', u'Бохир ус татан зайлуулах шугам'),
		)
	shugam_helber = models.CharField(max_length = 250,choices= shugam_helber, verbose_name=u'Шугам сүлжээний ангилал')
	shugam_torol  = models.CharField(max_length = 250, choices = shugam_choices, verbose_name=u'Шугам сүлжээний төрөл')
	shugam_urt = models.FloatField(verbose_name=u'Шугамын нийт урт (м)')
	hudgiin_too = models.IntegerField(verbose_name=u'Шугам сүлжээн дээрх хяналтын худгийн тоо')
	gemtliin_too = models.IntegerField(verbose_name=u'Жилд гарсан гэмтлийн тоо')
	schema = models.ImageField(verbose_name=u'Шугам сүлжээний схем зураг',validators=[validate_picture_extension, validate_file_size], upload_to=user_directory_path)


	def get_hooloi_count(self, date_time=timezone.now()):
		list_hooloi = self.get_sub_objects(Hooloi, 'sh_suljee', date_time)
		if list_hooloi:
			return len(list_hooloi)
		else:
			return 0

	@classmethod
	def excel_write_header_and_format(self, worksheet, row_start, col_start):
		worksheet.set_column(col_start, col_start, 25)
		worksheet.set_column(col_start+1, col_start+1, 25)
		worksheet.set_column(col_start+2, col_start+2, 25)
		worksheet.set_column(col_start+6, col_start+6, 30)
		worksheet.set_column(col_start+9, col_start+9, 30)


		worksheet.merge_range(row_start, col_start, row_start+1, col_start,u'ТЗЭ')
		worksheet.merge_range(row_start, col_start+1, row_start+1, col_start+1,u'Шугам сүлжээний ангилал')
		worksheet.merge_range(row_start, col_start+2, row_start+1, col_start+2,u'Шугам сүлжээний төрөл')
		worksheet.merge_range(row_start, col_start+3, row_start+1, col_start+3,u'Шугам сүлжээний урт')
		worksheet.merge_range(row_start, col_start+4, row_start+1, col_start+4,u'Шугам сүлжээний худгийн тоо')
		worksheet.merge_range(row_start, col_start+5, row_start+1, col_start+5,u'Шугам сүлжээний гэмтлийн тоо')


		worksheet.merge_range(row_start, col_start+6, row_start, col_start+9, u'Хоолой')
		worksheet.write_string(row_start+1, col_start+6, u'Хоолойн төрөл')
		worksheet.write_string(row_start+1, col_start+7, u'Диаметр')
		worksheet.write_string(row_start+1, col_start+8, u'Урт')
		worksheet.write_string(row_start+1, col_start+9, u'Ашиглалтанд орсон он')

		return [row_start+2, col_start]

	def object_excel_write(self, worksheet, row_start, col_start, **kwargs):
		date_time = kwargs['date_time']
		hist_obj = self.get_history_object(date_time)

		if hist_obj:
			if hist_obj.status==True:
				hooloi_count = self.get_hooloi_count(date_time)
				if hooloi_count>1:
					worksheet.merge_range(row_start, col_start, row_start+hooloi_count-1, col_start, hist_obj.tze.org_name + ' ' + hist_obj.tze.org_type)
					worksheet.merge_range(row_start, col_start+1, row_start+hooloi_count-1, col_start+1, hist_obj.shugam_helber)
					worksheet.merge_range(row_start, col_start+2, row_start+hooloi_count-1, col_start+2, hist_obj.shugam_torol)
					worksheet.merge_range(row_start, col_start+3, row_start+hooloi_count-1, col_start+3, hist_obj.shugam_urt)
					worksheet.merge_range(row_start, col_start+4, row_start+hooloi_count-1, col_start+4, hist_obj.hudgiin_too)
					worksheet.merge_range(row_start, col_start+5, row_start+hooloi_count-1, col_start+5, hist_obj.gemtliin_too)

					hooloinuud = self.get_sub_objects(Hooloi, 'sh_suljee', date_time)
					Hooloi.export_to_excel(worksheet, row_start, col_start+6, hooloinuud)
				else:
					worksheet.write_string(row_start, col_start, hist_obj.tze.org_name + ' ' + hist_obj.tze.org_type)
					worksheet.write_string(row_start, col_start+1, hist_obj.shugam_helber)
					worksheet.write_string(row_start, col_start+2, hist_obj.shugam_torol)
					worksheet.write_number(row_start, col_start+3, hist_obj.shugam_urt)
					worksheet.write_number(row_start, col_start+4, hist_obj.hudgiin_too)
					worksheet.write_number(row_start, col_start+5, hist_obj.gemtliin_too)
					if hooloi_count == 1:
						hooloinuud = self.get_sub_objects(Hooloi, 'sh_suljee', date_time)
						Hooloi.export_to_excel(worksheet, row_start, col_start+6, hooloinuud)
					else:
						# hervee shugam suljee hooloigui baival
						worksheet.merge_range(row_start, col_start+6, row_start, col_start+9, u'Бүртгэгдсэн хоолой байхгүй')
						return [row_start+1, col_start]						
				return [row_start+hooloi_count, col_start] # daraagiin object bichih coordinatiig butsaana
			else:
				# history object status==False uyd
				return [row_start, col_start]
		else:
			# history object baihgui uyd
			return [row_start, col_start]

hooloi_choices = (
	(u'Ган', u'Ган'),
	(u'Хуванцар', u'Хуванцар'),
	(u'Ширэм', u'Ширэм'),
	(u'Ваар', u'Ваар'),
	(u'Төмөр бетон', u'Төмөр бетон'),
	(u'Шөрмөсөн чулуун', u'Шөрмөсөн чулуун'),
	(u'Бусад', u'Бусад'),
	)
class Hooloi(Create, History_operations):
	sh_suljee = models.ForeignKey(Sh_suljee)
	torol = models.CharField(max_length = 25, verbose_name=u'Шугам хоолойн төрөл', choices = hooloi_choices)
	diametr = models.FloatField(verbose_name=u'Хоолойн диаметр (мм)')
	urt = models.FloatField(verbose_name=u'Хоолойн урт (м)')
	ashiglaltand_orson_ognoo = models.CharField(max_length = 4, verbose_name = 'Ашиглалтанд орсон он:', validators = [validate_year])
	history = HistoricalRecords()

	@classmethod
	def export_to_excel(self, worksheet, row_start, col_start, queryset):
		row_write = row_start
		col_write = col_start
		for q in queryset:
			[row_write, col_write] = q.object_excel_write(worksheet, row_write, col_write)

	def object_excel_write(self, worksheet, row_start, col_start, **kwargs):
		worksheet.write_string(row_start, col_start, self.torol)
		worksheet.write_number(row_start, col_start+1, self.diametr)
		worksheet.write_number(row_start, col_start+2, self.urt)
		worksheet.write_string(row_start, col_start+3, self.ashiglaltand_orson_ognoo)

		return [row_start+1, col_start]


ts_baiguulamj_choices=(
	(u'Цэвэр усны', u'Цэвэр усны'),
	(u'Бохир усны', u'Бохир усны'),
	)
# Цэвэрлэх байгууламж
class Ts_baiguulamj(BB):
	torol = models.CharField(max_length = 32, choices = ts_baiguulamj_choices, verbose_name = 'Төрөл:')
	ashiglaltand_orson_ognoo = models.CharField(max_length = 4, verbose_name = 'Ашиглалтанд орсон он:', validators = [validate_year])
	huchin_chadal = models.FloatField(verbose_name=u'Хүчин чадал (м3/хон)', null = True, blank = True)
	mehanik= models.BooleanField(verbose_name = 'Механик', default = False)
	biologi= models.BooleanField(verbose_name = 'Биологи', default = False)
	fizik= models.BooleanField(verbose_name = 'Физик хими, Хими', default = False)
	technology_schema = models.ImageField(verbose_name=u'Технологийн схем',validators=[validate_picture_extension, validate_file_size], upload_to=user_directory_path)
	def get_tohooromj_queryset(self):
		return Ts_tohooromj.objects.filter(ts_baiguulamj = self, status=True)
	def get_tohooromj_count(self, date_time=timezone.now()):
		list_ts_tohooromj = self.get_sub_objects(Ts_tohooromj, 'ts_baiguulamj', date_time)
		if list_ts_tohooromj:
			return len(list_ts_tohooromj)
		else:
			return 0

	@classmethod
	def excel_write_header_and_format(self, worksheet, row_start, col_start):
		worksheet.merge_range(row_start, col_start, row_start+1, col_start,u'ТЗЭ')
		worksheet.merge_range(row_start, col_start+1, row_start+1, col_start+1,u'Төрөл')
		worksheet.merge_range(row_start, col_start+2, row_start+1, col_start+2,u'Хүчин чадал (м3/хон)')
		worksheet.merge_range(row_start, col_start+3, row_start+1, col_start+3,u'Механик')
		worksheet.merge_range(row_start, col_start+4, row_start+1, col_start+4,u'Биологи')
		worksheet.merge_range(row_start, col_start+5, row_start+1, col_start+5,u'Физик хими, Хими')
		worksheet.merge_range(row_start, col_start+6, row_start+1, col_start+6,u'Ашиглалтанд орсон он')



		worksheet.merge_range(row_start, col_start+7, row_start, col_start+12, u'Цэвэрлэх төхөөрөмж')
		worksheet.write_string(row_start+1, col_start+7, u'Төрөл')
		worksheet.write_string(row_start+1, col_start+8, u'Хүчин чадал (м3/хон)')
		worksheet.write_string(row_start+1, col_start+9, u'Ажиллаж буй хүчин чадал (м3/хон)')
		worksheet.write_string(row_start+1, col_start+10, u'Тоо хэмжээ')
		worksheet.write_string(row_start+1, col_start+11, u'Ашиглалтанд орсон он')
		worksheet.write_string(row_start+1, col_start+12, u'Тайлбар /ажиллаж байгаа эсэх/')

		return [row_start+2, col_start]
		

	def object_excel_write(self, worksheet, row_start, col_start, **kwargs):
		date_time = kwargs['date_time']
		hist_obj = self.get_history_object(date_time)

		if hist_obj:
			if hist_obj.status==True:
				ts_tohooromj_count = self.get_tohooromj_count(date_time)
				if ts_tohooromj_count>1:
					worksheet.merge_range(row_start, col_start, row_start+ts_tohooromj_count-1, col_start, hist_obj.tze.org_name + ' ' + hist_obj.tze.org_type)
					worksheet.merge_range(row_start, col_start+1, row_start+ts_tohooromj_count-1, col_start+1, hist_obj.torol)
					worksheet.merge_range(row_start, col_start+2, row_start+ts_tohooromj_count-1, col_start+2, hist_obj.huchin_chadal)
					if hist_obj.mehanik:
						worksheet.merge_range(row_start, col_start+3, row_start+ts_tohooromj_count-1, col_start+3, u'Тийм')
					else:
						worksheet.merge_range(row_start, col_start+3, row_start+ts_tohooromj_count-1, col_start+3, u'Үгүй')
					if hist_obj.biologi:
						worksheet.merge_range(row_start, col_start+4, row_start+ts_tohooromj_count-1, col_start+4, u'Тийм')
					else:
						worksheet.merge_range(row_start, col_start+4, row_start+ts_tohooromj_count-1, col_start+4, u'Үгүй')
					if hist_obj.fizik:
						worksheet.merge_range(row_start, col_start+5, row_start+ts_tohooromj_count-1, col_start+5, u'Тийм')
					else:
						worksheet.merge_range(row_start, col_start+5, row_start+ts_tohooromj_count-1, col_start+5, u'Үгүй')
					worksheet.merge_range(row_start, col_start+6, row_start+ts_tohooromj_count-1, col_start+6, hist_obj.ashiglaltand_orson_ognoo)

					ts_tohooromjs = self.get_sub_objects(Ts_tohooromj, 'ts_baiguulamj', date_time)
					Ts_tohooromj.export_to_excel(worksheet, row_start, col_start+7, ts_tohooromjs)
				else:
					worksheet.write_string(row_start, col_start, hist_obj.tze.org_name + ' ' + hist_obj.tze.org_type)
					worksheet.write_string(row_start, col_start+1, hist_obj.torol)
					worksheet.write_number(row_start, col_start+2, hist_obj.huchin_chadal)

					if hist_obj.mehanik:
						worksheet.write_string(row_start, col_start+3, u'Тийм')
					else:
						worksheet.write_string(row_start, col_start+3, u'Үгүй')
					if hist_obj.biologi:
						worksheet.write_string(row_start, col_start+4, u'Тийм')
					else:
						worksheet.write_string(row_start, col_start+4, u'Үгүй')
					if hist_obj.fizik:
						worksheet.write_string(row_start, col_start+5, u'Тийм')
					else:
						worksheet.write_string(row_start, col_start+5, u'Үгүй')

					worksheet.write_string(row_start, col_start+6, hist_obj.ashiglaltand_orson_ognoo)
					if ts_tohooromj_count == 1:
						ts_tohooromjs = self.get_sub_objects(Ts_tohooromj, 'ts_baiguulamj', date_time)
						Ts_tohooromj.export_to_excel(worksheet, row_start, col_start+7, ts_tohooromjs)
					else:
						# hervee shugam suljee hooloigui baival
						worksheet.merge_range(row_start, col_start+7, row_start, col_start+12, u'Бүртгэгдсэн цэвэрлэх төхөөрөмж байхгүй')
						return [row_start+1, col_start]
						
				return [row_start+ts_tohooromj_count, col_start] # daraagiin object bichih coordinatiig butsaana
			else:
				# history object status==False uyd
				return [row_start, col_start]
		else:
			# history object baihgui uyd
			return [row_start, col_start]
barilga_tonog_torol = (
		(u'Сараалж, м3/цаг', u'Сараалж, м3/цаг'),
		(u'Элс тогтоогуур', u'Элс тогтоогуур'),
		(u'Тунгаагуур', u'Тунгаагуур'),
		(u'Жигдрүүлэх сан', u'Жигдрүүлэх сан'),
		(u'Механик шүүлтүүр', u'Механик шүүлтүүр'),
		(u'Шүүх талбай', u'Шүүх талбай'),
		(u'Усалгаат талбай', u'Усалгаат талбай'),
		(u'Биоцөөрөм', u'Биоцөөрөм'),
		(u'Исэлдүүлэх суваг', u'Исэлдүүлэх суваг'),
		(u'Исэлдүүлэх цөөрөм', u'Исэлдүүлэх цөөрөм'),
		(u'Агааржуулах сав', u'Агааржуулах сав'),
		(u'Биошүүлтүүр', u'Биошүүлтүүр'),
		(u'Элсэн шүүлтүүр', u'Элсэн шүүлтүүр'),
		(u'Хүрдэн шүүлтүүр', u'Хүрдэн шүүлтүүр'),
		(u'Аноксик байгууламж', u'Аноксик байгууламж'),
		(u'2-р тунгаагуур', u'2-р тунгаагуур'),
		(u'Экстраци', u'Экстраци'),
		(u'Адсорбци', u'Адсорбци'),
		(u'Флотаци', u'Флотаци'),
		(u'Ион солилцоо', u'Ион солилцоо'),
		(u'Диализ', u'Диализ'),
		(u'Бүлэгнүүлэх', u'Бүлэгнүүлэх'),
		(u'Тунадасжуулах', u'Тунадасжуулах'),
		(u'Каогулент', u'Каогулент'),
		(u'Хлоржуулах', u'Хлоржуулах'),
		(u'Озонжуулах', u'Озонжуулах'),
		(u'Саармагжуулах', u'Саармагжуулах'),
		(u'Хэт ягаан туяагаар шарах', u'Хэт ягаан туяагаар шарах'),
		)

# Цэвэрлэх төхөөрөмж
class Ts_tohooromj(Create, History_operations):
	ts_baiguulamj = models.ForeignKey(Ts_baiguulamj)
	barilga_tonog = models.CharField(max_length = 250, choices=barilga_tonog_torol, verbose_name=u'Төрөл')
	huchin_chadal = models.FloatField(verbose_name=u'Хүчин чадал (м3/хон)', null = True, blank = True)
	ajillaj_bui_huchin_chadal = models.FloatField(verbose_name=u'Ажиллаж буй хүчин чадал (м3/хон)', null = True, blank = True)
	too = models.IntegerField(verbose_name=u'Тоо хэмжээ')
	ashiglaltand_orson_ognoo = models.CharField(max_length = 4, verbose_name = 'Ашиглалтанд орсон он:', validators = [validate_year])
	tailbar = models.CharField(max_length = 500, verbose_name=u'Тайлбар/ажиллаж байгаа эсэх/', null = True, blank = True)
	history = HistoricalRecords()

	@classmethod
	def export_to_excel(self, worksheet, row_start, col_start, queryset):
		row_write = row_start
		col_write = col_start
		for q in queryset:
			[row_write, col_write] = q.object_excel_write(worksheet, row_write, col_write)

	def object_excel_write(self, worksheet, row_start, col_start, **kwargs):
		worksheet.write_string(row_start, col_start, self.barilga_tonog)
		worksheet.write_number(row_start, col_start+1, self.huchin_chadal)
		worksheet.write_number(row_start, col_start+2, self.ajillaj_bui_huchin_chadal)
		worksheet.write_number(row_start, col_start+3, self.too)
		worksheet.write_string(row_start, col_start+4, self.ashiglaltand_orson_ognoo)
		worksheet.write_string(row_start, col_start+5, self.tailbar)

		return [row_start+1, col_start]

''' Усан сан '''
class UsanSan(BB):
	usansan_helber_choices = ((u'Эзэлхүүнт' , u'Эзэлхүүнт' ),
		(u'Даралтат буюу цамхагт', u'Даралтат буюу цамхагт'),
		)
	usansan_haruul_choices = (
		(u'Энгийн',u'Энгийн'),
		(u'Гэрээт',u'Гэрээт'),
		(u'Онцгой', u'Онцгой'),
		)
	ashiglaltand_orson_ognoo = models.CharField(max_length = 4, verbose_name = 'Ашиглалтанд орсон он:', validators = [validate_year])
	usansan_helber = models.CharField(max_length = 50, choices= usansan_helber_choices, verbose_name=u'Усан сангийн төрөл')
	city = models.ForeignKey(Aimag, verbose_name = 'Усан сангийн байршил/Аймаг, хот/:')
	district = ChainedForeignKey(Sum, verbose_name = 'Усан сангийн байршил/Сум, дүүрэг/:', chained_field = 'city', chained_model_field = 'aimag_id')
	khoroo = ChainedForeignKey(Bag, verbose_name = 'Усан сангийн байршил/Баг, хороо/:', chained_field = 'district', chained_model_field = 'sum_id')
	usansan_address= models.CharField(max_length = 1000, verbose_name=u'Усан сангийн байршил',null= True, blank=True)
	bagtaamj= models.FloatField(verbose_name=u'Усан сангийн багтаамж (м3)')
	huurai_hlor= models.BooleanField(verbose_name = 'Хуурай хлор', default = False)
	shingen_hlor= models.BooleanField(verbose_name = 'Шингэн хлор', default = False)
	davsnii_uusmal= models.BooleanField(verbose_name = 'Давсны уусмал', default = False)
	usansan_haruul  = models.CharField(max_length = 250, choices = usansan_haruul_choices, verbose_name=u'Усан сангийн харуул, хамгаалалт')

	def get_wash_count(self):
		queryset = UsanSanUgaalga.objects.filter(usansan_id = self, status = True)
		return queryset.count()

	@classmethod
	def excel_write_header_and_format(self, worksheet, row_start, col_start):
		worksheet.write_string(row_start, col_start, u'ТЗЭ')
		worksheet.write_string(row_start, col_start+1, u'Аймаг,хот')
		worksheet.write_string(row_start, col_start+2, u'Сум, дүүрэг')
		worksheet.write_string(row_start, col_start+3, u'Баг, хороо')
		worksheet.write_string(row_start, col_start+4, u'Байрлал')
		worksheet.write_string(row_start, col_start+5, u'Усан сангийн төрөл')
		worksheet.write_string(row_start, col_start+6, u'Ашиглалтанд орсон он')
		worksheet.write_string(row_start, col_start+7, u'Усан сангийн багтаамж (м3)')
		worksheet.write_string(row_start, col_start+8, u'Хуурай хлор')
		worksheet.write_string(row_start, col_start+9, u'Шингэн хлор')
		worksheet.write_string(row_start, col_start+10, u'Давсны уусмал')
		worksheet.write_string(row_start, col_start+11, u'Усан сангийн харуул, хамгаалалт')
		return [row_start+1, col_start]

		
	def object_excel_write(self, worksheet, row_start, col_start, **kwargs):
		date_time=kwargs['date_time']
		hist_obj = self.get_history_object(date_time)

		if hist_obj:
			if hist_obj.status==True:
				worksheet.write_string(row_start, col_start, hist_obj.tze.org_name + ' ' + hist_obj.tze.org_type)
				worksheet.write_string(row_start, col_start+1, hist_obj.city.aimag_name)
				worksheet.write_string(row_start, col_start+2, hist_obj.district.sum_name)
				worksheet.write_string(row_start, col_start+3, hist_obj.khoroo.bag_name)
				worksheet.write_string(row_start, col_start+4, hist_obj.usansan_address)
				worksheet.write_string(row_start, col_start+5, hist_obj.usansan_helber)
				worksheet.write_string(row_start, col_start+6, hist_obj.ashiglaltand_orson_ognoo)
				worksheet.write_number(row_start, col_start+7, hist_obj.bagtaamj)

				if hist_obj.huurai_hlor:
					worksheet.write_string(row_start, col_start+8, u'Тийм')
				else:
					worksheet.write_string(row_start, col_start+8, u'Үгүй')

				if hist_obj.shingen_hlor:
					worksheet.write_string(row_start, col_start+9, u'Тийм')
				else:
					worksheet.write_string(row_start, col_start+9, u'Үгүй')

				if hist_obj.davsnii_uusmal:
					worksheet.write_string(row_start, col_start+10, u'Тийм')
				else:
					worksheet.write_string(row_start, col_start+10, u'Үгүй')

				worksheet.write_string(row_start, col_start+11, hist_obj.usansan_haruul)
				return [row_start+1, col_start] # daraagiin object bichih coordinatiig butsaana
			else:
				# history ni status=False baina
				return [row_start, col_start]
		else:
			# history object doesn't exist
			return [row_start, col_start]
''' Усан сангийн угаалга '''
class UsanSanUgaalga(Create, History_operations):
	usansan_id = models.ForeignKey(UsanSan)
	ognoo = models.DateField(null = True, blank = True, verbose_name = 'Он, сар, өдөр')
	akt= models.ImageField(verbose_name=u'Ажлын акт, баримт/Зураг/',validators=[validate_picture_extension, validate_file_size], upload_to=usansanakt_directory_path)
	history = HistoricalRecords()

us_damjuulah_torol_choices = (
		(u'Төвлөрсөн ус, дулаан дамжуулах төв', u'Төвлөрсөн ус, дулаан дамжуулах төв'),
		(u'Байрын ус, дулаан дамжуулах төв', u'Байрын ус, дулаан дамжуулах төв'),
		)
''' Ус дамжуулах байр '''
class UsDamjuulahBair(BB):
	ashiglaltand_orson_ognoo = models.CharField(max_length = 4, verbose_name = 'Ашиглалтанд орсон он:', validators = [validate_year])
	torol = models.CharField(max_length = 40, verbose_name = 'Ус, дулаан дамжуулах төвийн төрөл', choices = us_damjuulah_torol_choices)
	picture = models.ImageField(verbose_name=u'Тоног төхөөрөмжийн зураг',validators=[validate_picture_extension, validate_file_size], upload_to=user_directory_path)
	bair_uzeli_holbolt_schema = models.ImageField(verbose_name=u'Байр узель холболтын зураг',validators=[validate_picture_extension, validate_file_size], upload_to=user_directory_path)

	def get_tohooromj_count(self, date_time=timezone.now()):
		list_tonog = self.get_sub_objects(UsDamjuulahBairTonog, 'us_id', date_time)
		if list_tonog:
			return len(list_tonog)
		else:
			return 0

	@classmethod
	def excel_write_header_and_format(self, worksheet, row_start, col_start):
		worksheet.merge_range(row_start, col_start, row_start+1, col_start,u'ТЗЭ')
		worksheet.merge_range(row_start, col_start+1, row_start+1, col_start+1,u'Ус, дулаан дамжуулах төвийн төрөл')
		worksheet.merge_range(row_start, col_start+2, row_start+1, col_start+2,u'Ашиглалтанд орсон он')


		worksheet.merge_range(row_start, col_start+3, row_start, col_start+7, u'Ус, дулаан дамжуулах байрны тоног төхөөрөмж')
		worksheet.write_string(row_start+1, col_start+3, u'Төхөөрөмж')
		worksheet.write_string(row_start+1, col_start+4, u'Хүчин чадал')
		worksheet.write_string(row_start+1, col_start+5, u'Тоо')
		worksheet.write_string(row_start+1, col_start+6, u'Ашиглалтанд орсон он')
		worksheet.write_string(row_start+1, col_start+7, u'Тайлбар /ажиллаж байгаа эсэх/')

		return [row_start+2, col_start]
		

	def object_excel_write(self, worksheet, row_start, col_start, **kwargs):
		date_time = kwargs['date_time']
		hist_obj = self.get_history_object(date_time)

		if hist_obj:
			if hist_obj.status==True:
				tonog_count = self.get_tohooromj_count(date_time)
				if tonog_count>1:
					worksheet.merge_range(row_start, col_start, row_start+tonog_count-1, col_start, hist_obj.tze.org_name + ' ' + hist_obj.tze.org_type)
					worksheet.merge_range(row_start, col_start+1, row_start+tonog_count-1, col_start+1, hist_obj.torol)
					worksheet.merge_range(row_start, col_start+2, row_start+tonog_count-1, col_start+2, hist_obj.ashiglaltand_orson_ognoo)

					tonog_tohooromjs = self.get_sub_objects(UsDamjuulahBairTonog, 'us_id', date_time)
					UsDamjuulahBairTonog.export_to_excel(worksheet, row_start, col_start+3, tonog_tohooromjs)
				else:
					worksheet.write_string(row_start, col_start, hist_obj.tze.org_name + ' ' + hist_obj.tze.org_type)
					worksheet.write_string(row_start, col_start+1, hist_obj.torol)
					worksheet.write_string(row_start, col_start+2, hist_obj.ashiglaltand_orson_ognoo)

					if tonog_count == 1:
						tonog_tohooromjs = self.get_sub_objects(UsDamjuulahBairTonog, 'us_id', date_time)
						UsDamjuulahBairTonog.export_to_excel(worksheet, row_start, col_start+3, tonog_tohooromjs)
					else:
						# hervee shugam suljee hooloigui baival
						worksheet.merge_range(row_start, col_start+3, row_start, col_start+7, u'Бүртгэгдсэн тоног төхөөрөмж байхгүй')
						return [row_start+1, col_start]
						
				return [row_start+tonog_count, col_start] # daraagiin object bichih coordinatiig butsaana
			else:
				# history object status==False uyd
				return [row_start, col_start]
		else:
			# history object baihgui uyd
			return [row_start, col_start]
us_damjuulah_bair_torol = (
		(u'Халаалтын бойлер, кВт', u'Халаалтын бойлер, кВт'),
		(u'Хэрэглээний халуун усны бойлер, кВт', u'Хэрэглээний халуун усны бойлер, кВт'),
		(u'Салхивчийн системийн бойлер, кВт', u'Салхивчийн системийн бойлер, кВт'),
		(u'Халаалтын насос, м3/ц', u'Халаалтын насос, м3/ц'),
		(u'Хэрэглээний халуун усны насос, м3/ц', u'Хэрэглээний халуун усны насос, м3/ц'),
		(u'Цэвэр усны өргөлтийн насос, кВт', u'Цэвэр усны өргөлтийн насос, кВт'),
		)
''' Ус дамжуулах байрны тоног төхөөрөмж '''
class UsDamjuulahBairTonog(Create, History_operations):
	us_id=models.ForeignKey(UsDamjuulahBair)
	tze = models.ForeignKey(TZE)
	huchin_chadal = models.FloatField(verbose_name=u'Хүчин чадал', null = True, blank = True)
	ognoo = models.CharField(max_length = 4, verbose_name = 'Ашиглалтанд орсон он:', validators = [validate_year])
	tonog = models.CharField(max_length = 100,choices= us_damjuulah_bair_torol, verbose_name=u'Тоног төхөөрөмж')
	too= models.IntegerField(verbose_name=u'Тоо хэмжээ')
	tailbar = models.CharField(max_length = 500, verbose_name=u'Тайлбар/ажиллаж байгаа эсэх/', null = True, blank = True)
	history = HistoricalRecords()

	@classmethod
	def export_to_excel(self, worksheet, row_start, col_start, queryset):
		row_write = row_start
		col_write = col_start
		for q in queryset:
			[row_write, col_write] = q.object_excel_write(worksheet, row_write, col_write)

	def object_excel_write(self, worksheet, row_start, col_start, **kwargs):
		worksheet.write_string(row_start, col_start, self.tonog)
		worksheet.write_number(row_start, col_start+1, self.huchin_chadal)
		worksheet.write_number(row_start, col_start+2, self.too)
		worksheet.write_string(row_start, col_start+3, self.ashiglaltand_orson_ognoo)
		worksheet.write_string(row_start, col_start+4, self.tailbar)

		return [row_start+1, col_start]
	


	
barilga_choice = (
	(u'Гүний эх үүсвэртэй ус түгээх байр', u'Гүний эх үүсвэртэй ус түгээх байр'),
	(u'Зөөврийн эх үүсвэртэй ус түгээх байр', u'Зөөврийн эх үүсвэртэй ус түгээх байр'),
	(u'Төвлөрсөн шугамаас тэжээгддэг ус түгээх байр', u'Төвлөрсөн шугамаас тэжээгддэг ус түгээх байр'),
	)
''' Ус түгээх байр '''
class UsTugeehBair(BB):
	ashiglaltand_orson_ognoo = models.CharField(max_length = 4, verbose_name = 'Ашиглалтанд орсон он:', validators = [validate_year])
	barilga = models.CharField(max_length = 250, choices = barilga_choice, verbose_name=u'Ус түгээх байрны төрөл')
	dugaar = models.IntegerField(  verbose_name=u'Ус түгээх байрны дугаар (нэр)')
	city = models.ForeignKey(Aimag, verbose_name = 'Ус түгээх байрны байршил/Аймаг, хот/:',)
	district = ChainedForeignKey(Sum, verbose_name = 'Ус түгээх байрны байршил/Сум, дүүрэг/:', chained_field = 'city', chained_model_field = 'aimag_id')
	khoroo = ChainedForeignKey(Bag, verbose_name = 'Ус түгээх байрны байршил/Баг, хороо/:', chained_field = 'district', chained_model_field = 'sum_id')
	ustugeeh_address= models.CharField(max_length = 1000, verbose_name=u'Ус түгээх байрны байршил',null= True, blank=True)
	ustugeeh_sav= models.BooleanField(verbose_name = 'Ус нөөцлөх сав байгаа эсэх', default = False)
	savnii_bagtaamj=models.FloatField(verbose_name=u'Савны багтаамж (м3)', null=True, blank=True)
	borluulj_bui_us = models.FloatField(verbose_name=u'УТБ-р борлуулж буй ус (м3/хон)')
	hun_amiin_too = models.IntegerField(verbose_name=u'УТБ-р үйлчлүүлж буй айл өрхийн тоо')
	gadna_tal_picture = models.ImageField(verbose_name=u'Байрны гадна талын зураг',validators=[validate_picture_extension, validate_file_size], upload_to=user_directory_path)
	dotor_tal_picture = models.ImageField(verbose_name=u' Байрны дотор талын зураг',validators=[validate_picture_extension, validate_file_size], upload_to=user_directory_path)

	@classmethod
	def excel_write_header_and_format(self, worksheet, row_start, col_start):
		worksheet.write_string(row_start, col_start, u'ТЗЭ')
		worksheet.write_string(row_start, col_start+1, u'Аймаг,хот')
		worksheet.write_string(row_start, col_start+2, u'Сум, дүүрэг')
		worksheet.write_string(row_start, col_start+3, u'Баг, хороо')
		worksheet.write_string(row_start, col_start+4, u'Байрлал')
		worksheet.write_string(row_start, col_start+5, u'Ус түгээх байрны дугаар (нэр)')
		worksheet.write_string(row_start, col_start+6, u'Ус түгээх байрны төрөл')
		worksheet.write_string(row_start, col_start+7, u'Ус нөөцлөх савтай эсэх')
		worksheet.write_string(row_start, col_start+8, u'Савны багтаамж')
		worksheet.write_string(row_start, col_start+9, u'УТБ-р борлуулж буй ус(м3/хон)')
		worksheet.write_string(row_start, col_start+10, u'УТБ-р үйлчлүүлж буй хүн амын тоо')
		worksheet.write_string(row_start, col_start+11, u'Ашиглалтанд орсон он')

		return [row_start+1, col_start]
		

	def object_excel_write(self, worksheet, row_start, col_start, **kwargs):
		date_time=kwargs['date_time']
		hist_obj = self.get_history_object(date_time)

		if hist_obj:
			if hist_obj.status==True:
				worksheet.write_string(row_start, col_start, hist_obj.tze.org_name + ' ' + hist_obj.tze.org_type)
				worksheet.write_string(row_start, col_start+1, hist_obj.city.aimag_name)
				worksheet.write_string(row_start, col_start+2, hist_obj.district.sum_name)
				worksheet.write_string(row_start, col_start+3, hist_obj.khoroo.bag_name)
				worksheet.write_string(row_start, col_start+4, hist_obj.ustugeeh_address)
				worksheet.write_number(row_start, col_start+5, hist_obj.dugaar)
				worksheet.write_string(row_start, col_start+6, hist_obj.barilga)
				if hist_obj.ustugeeh_sav:
					worksheet.write_string(row_start, col_start+7, u'Тийм')
					if hist_obj.savnii_bagtaamj:
						worksheet.write_number(row_start, col_start+8, hist_obj.savnii_bagtaamj)
				else:
					worksheet.write_string(row_start, col_start+7, u'Үгүй')

				
				worksheet.write_number(row_start, col_start+9, hist_obj.borluulj_bui_us)
				worksheet.write_number(row_start, col_start+10, hist_obj.hun_amiin_too)
				worksheet.write_string(row_start, col_start+11, hist_obj.ashiglaltand_orson_ognoo)
				return [row_start+1, col_start] # daraagiin object bichih coordinatiig butsaana
			else:
				# history ni status=False baina
				return [row_start, col_start]
		else:
			# history object doesn't exist
			return [row_start, col_start]
''' Ус түгээх байрны ус нөөцлөх савны угаалга'''
class UsTugeehBairSavUgaalga(Create, History_operations):
	ussav_id= models.ForeignKey(UsTugeehBair)
	ugaalga_ognoo = models.DateField(null = True, blank = True, verbose_name = 'Cавыг угааж, халдваргүйжүүлсэн он, сар, өдөр')
	history = HistoricalRecords()
	

''' Цэвэр усны шинжилгээний стандарт үзүүлэлт '''
class AnalysisWaterStandart(Create):
	hatuulag= models.CharField(max_length = 50, verbose_name=u'Ерөнхий хатуулаг:')
	magni= models.CharField(max_length = 50, verbose_name=u'Магни:')
	kalitsi= models.CharField(max_length = 50, verbose_name=u'Кальци:')
	hlorid= models.CharField(max_length = 50, verbose_name=u'Хлорид:')
	sulifat= models.CharField(max_length = 50, verbose_name=u'Сульфат:')
	ph= models.CharField(max_length = 50, verbose_name=u'pH:')
	ammiak= models.CharField(max_length = 50, verbose_name=u'Аммиак:')
	nitrit= models.CharField(max_length = 50, verbose_name=u'Нитрит:')
	amt= models.CharField(max_length = 50, verbose_name=u'Амт:')
	uner= models.CharField(max_length = 50, verbose_name=u'Үнэр:')
	nyan= models.CharField(max_length = 50, verbose_name=u'Нийт нянгийн тоо:')
''' Цэвэр усны шинжилгээ '''
class AnalysisWater(Create):
	water_analysis_types = (
		('1', 'Савласан цэвэр ус'),
		('2', 'Савласан эрдэслэг ус'),
		('3', 'Ундны ус'),
		)

	tze = models.ForeignKey(TZE)
	torol = models.CharField(max_length=3, choices=water_analysis_types, verbose_name=u'Төрөл')
	ognoo=models.DateField(verbose_name=u'Он, сар, өдөр:')
	hatuulag= models.FloatField(verbose_name=u'Ерөнхий хатуулаг:', null=True, blank=True)
	kalitsi= models.FloatField(verbose_name=u'Кальци:', null=True, blank=True)
	magni= models.FloatField(verbose_name=u'Магни:', null=True, blank=True)
	hlorid= models.FloatField(verbose_name=u'Хлорид:', null=True, blank=True)
	sulifat= models.FloatField(verbose_name=u'Сульфат:', null=True, blank=True)
	fosfat= models.FloatField(verbose_name=u'Фосфат:', null=True, blank=True)
	ammiak= models.FloatField(verbose_name=u'Аммиак:', null=True, blank=True)
	nitrit= models.FloatField(verbose_name=u'Нитрит:', null=True, blank=True)
	nitrat= models.FloatField(verbose_name=u'Нитрат:', null=True, blank=True)
	tomor= models.FloatField(verbose_name=u'Төмөр:', null=True, blank=True)
	ftor= models.FloatField(verbose_name=u'Фтор:', null=True, blank=True)
	ongo= models.FloatField(verbose_name=u'Өнгө:', null=True, blank=True)
	amt= models.FloatField(verbose_name=u'Амт:', null=True, blank=True)
	uner= models.FloatField(verbose_name=u'Үнэр:', null=True, blank=True)
	ph= models.FloatField(verbose_name=u'pH:', null=True, blank=True)
	huurai_uldegdel= models.FloatField(verbose_name=u'Хуурай үлдэгдэл:', null=True, blank=True)
	iseldelt= models.FloatField(verbose_name=u'Исэлдэлт:', null=True, blank=True)
	natri= models.FloatField(verbose_name=u'Натри:', null=True, blank=True)
	kali= models.FloatField(verbose_name=u'Кали:', null=True, blank=True)
	gidro_carbonat= models.FloatField(verbose_name=u'Гидрокарбонат:', null=True, blank=True)
	uldegdel_hlor= models.FloatField(verbose_name=u'Үлдэгдэл хлор:', null=True, blank=True)
	niit_hlor= models.FloatField(verbose_name=u'Нийт хлор:', null=True, blank=True)
	niit_shultleg= models.FloatField(verbose_name=u'Нийт шүлтлэг:', null=True, blank=True)
	mheg_dugnelt= models.FileField(verbose_name= u'Шинжилгээний талаар МХЕГ-ын дүгнэлт:', validators=[validate_picture_extension, validate_file_size], upload_to=user_directory_path)
	nyan_1ml_us = models.IntegerField(verbose_name='1 мл усан дахь нийт нянгийн тоо:', null=True, blank=True)
	nyan_haluund_tesvertei_100ml = models.IntegerField(verbose_name='100 мл усан дахь халуунд тэсвэртэй гэдэсний бүлгийн нянгийн тоо', null=True, blank=True)
	e_coli_100ml_us = models.IntegerField(verbose_name='100 мл усан дахь E.coli-ийн тоо', null=True, blank=True)

	def torol_char(self):
		if self.torol == '1':
			return 'Савласан цэвэр ус'
		elif self.torol == '2':
			return 'Савласан эрдэслэг ус'
		elif self.torol == '3':
			return 'Ундны ус'
class UA_water_analysis(AnalysisWater):
	pass
class TZ_huselt_water_analysis(AnalysisWater):
	pass
	


''' Бохир усны шинжилгээний стандарт үзүүлэлт '''
class AnalysisBohirStandart(Create):
	umbuur= models.CharField(max_length = 50, verbose_name=u'Умбуур бодисын тоо, мг/л:')
	bhh= models.CharField(max_length = 50, verbose_name=u'БХХ мг/л O2:')
	hhh= models.CharField(max_length = 50, verbose_name=u'ХХХ мг/л O2:')
''' Бохир усны шинжилгээ '''
class AnalysisBohir(Create):
	tze = models.ForeignKey(TZE)

	temperature_input = models.IntegerField(verbose_name=u'Усны температур:', null=True, blank=True)
	orchin_input = models.IntegerField(verbose_name=u'Усны орчин:', null=True, blank=True)
	uner_input = models.FloatField(verbose_name=u'Үнэр:', null=True, blank=True)
	umbuuro_input= models.FloatField(verbose_name=u'Умбуур бодисын тоо, мг/л:', null=True, blank=True)
	bhho_input= models.FloatField(verbose_name=u'БХХ мг/л O2:', null=True, blank=True)
	hhho_input= models.FloatField(verbose_name=u'ХХХ мг/л O2:', null=True, blank=True)
	pich_input = models.FloatField(verbose_name=u'Перманганатын исэлдэх чанар:', null=True, blank=True)
	davs_input = models.FloatField(verbose_name=u'Ууссан давс/эрдэсжилт/:', null=True, blank=True)
	niit_azot_input = models.FloatField(verbose_name=u'Нийт азот:', null=True, blank=True)
	niit_phosphor_input = models.FloatField(verbose_name=u'Нийт фосфор:', null=True, blank=True)
	huhert_ustorogch_input = models.FloatField(verbose_name=u'Хүхэрт устөрөгч:', null=True, blank=True)
	uldegdel_hlor_input = models.FloatField(verbose_name=u'Үлдэгдэл хлор:', null=True, blank=True)
	barii_input = models.FloatField(verbose_name=u'Барий:', null=True, blank=True)
	binder_input = models.FloatField(verbose_name=u'Биндэр:', null=True, blank=True)
	bor_input = models.FloatField(verbose_name=u'Бор:', null=True, blank=True)
	vanadii_input = models.FloatField(verbose_name=u'Ванадий:', null=True, blank=True)
	zes_input = models.FloatField(verbose_name=u'Зэс:', null=True, blank=True)
	kadmi_input = models.FloatField(verbose_name=u'Кадми:', null=True, blank=True)
	kobalt_input = models.FloatField(verbose_name=u'Кобальт:', null=True, blank=True)
	mangan_input = models.FloatField(verbose_name=u'Манган:', null=True, blank=True)
	anzan_input = models.FloatField(verbose_name=u'Анзан/Молибден:', null=True, blank=True)
	mongon_us_input = models.FloatField(verbose_name=u'Мөнгөн ус:', null=True, blank=True)
	nikel_input = models.FloatField(verbose_name=u'Никель:', null=True, blank=True)
	selen_input = models.FloatField(verbose_name=u'Селен:', null=True, blank=True)
	strontsi_input = models.FloatField(verbose_name=u'Стронций:', null=True, blank=True)
	tomor_input = models.FloatField(verbose_name=u'Нийт төмөр:', null=True, blank=True)
	uran_input = models.FloatField(verbose_name=u'Уран:', null=True, blank=True)
	har_tugalga_input = models.FloatField(verbose_name=u'Хар тугалга:', null=True, blank=True)
	niit_hrom_input = models.FloatField(verbose_name=u'Нийт хром:', null=True, blank=True)
	valent_6_hrom_input = models.FloatField(verbose_name=u'6 валенттай хром:', null=True, blank=True)
	hongon_tsagaan_input = models.FloatField(verbose_name=u'Хөнгөн цагаан:', null=True, blank=True)
	huntsel_input = models.FloatField(verbose_name=u'Хүнцэл:', null=True, blank=True)
	tsair_input = models.FloatField(verbose_name=u'Цайр:', null=True, blank=True)
	tsagaan_tugalga_input = models.FloatField(verbose_name=u'Цагаан тугалга:', null=True, blank=True)
	niit_tsianid_input = models.FloatField(verbose_name=u'Нийт цианид:', null=True, blank=True)
	choloot_tsianid_input = models.FloatField(verbose_name=u'Чөлөөт цианид:', null=True, blank=True)
	phenol_input = models.FloatField(verbose_name=u'Фенол:', null=True, blank=True)
	benza_piren_input= models.FloatField(verbose_name=u'Бенза(а)пирен:', null=True, blank=True)
	ooh_tos_input = models.FloatField(verbose_name=u'Өөх тос:', null=True, blank=True)
	erdes_tos_input = models.FloatField(verbose_name=u'Эрдэс тос:', null=True, blank=True)
	ugaagch_bodis_input = models.FloatField(verbose_name=u'Бүх төрлийн угаагч бодис:', null=True, blank=True)
	trichlor_ethylen_input = models.FloatField(verbose_name=u'Трихлорэтилен:', null=True, blank=True)
	tetrachlor_ethylen_input = models.FloatField(verbose_name=u'Тетрахлорэтилен:', null=True, blank=True)
	gedes_nyan_input = models.FloatField(verbose_name=u'Гэдэсний бүлгийн эмгэг төрөгч нян:', null=True, blank=True)

	temperature_output = models.IntegerField(verbose_name=u'Усны температур:', null=True, blank=True)
	orchin_output = models.IntegerField(verbose_name=u'Усны орчин:', null=True, blank=True)
	uner_output = models.FloatField(verbose_name=u'Үнэр:', null=True, blank=True)
	umbuuro_output= models.FloatField(verbose_name=u'Умбуур бодисын тоо, мг/л:', null=True, blank=True)
	bhho_output= models.FloatField(verbose_name=u'БХХ мг/л O2:', null=True, blank=True)
	hhho_output= models.FloatField(verbose_name=u'ХХХ мг/л O2:', null=True, blank=True)
	pich_output = models.FloatField(verbose_name=u'Перманганатын исэлдэх чанар:', null=True, blank=True)
	davs_output = models.FloatField(verbose_name=u'Ууссан давс/эрдэсжилт/:', null=True, blank=True)
	niit_azot_output = models.FloatField(verbose_name=u'Нийт азот:', null=True, blank=True)
	niit_phosphor_output = models.FloatField(verbose_name=u'Нийт фосфор:', null=True, blank=True)
	huhert_ustorogch_output = models.FloatField(verbose_name=u'Хүхэрт устөрөгч:', null=True, blank=True)
	uldegdel_hlor_output = models.FloatField(verbose_name=u'Үлдэгдэл хлор:', null=True, blank=True)
	barii_output = models.FloatField(verbose_name=u'Барий:', null=True, blank=True)
	binder_output = models.FloatField(verbose_name=u'Биндэр:', null=True, blank=True)
	bor_output = models.FloatField(verbose_name=u'Бор:', null=True, blank=True)
	vanadii_output = models.FloatField(verbose_name=u'Ванадий:', null=True, blank=True)
	zes_output = models.FloatField(verbose_name=u'Зэс:', null=True, blank=True)
	kadmi_output = models.FloatField(verbose_name=u'Кадми:', null=True, blank=True)
	kobalt_output = models.FloatField(verbose_name=u'Кобальт:', null=True, blank=True)
	mangan_output = models.FloatField(verbose_name=u'Манган:', null=True, blank=True)
	anzan_output = models.FloatField(verbose_name=u'Анзан/Молибден:', null=True, blank=True)
	mongon_us_output = models.FloatField(verbose_name=u'Мөнгөн ус:', null=True, blank=True)
	nikel_output = models.FloatField(verbose_name=u'Никель:', null=True, blank=True)
	selen_output = models.FloatField(verbose_name=u'Селен:', null=True, blank=True)
	strontsi_output = models.FloatField(verbose_name=u'Стронций:', null=True, blank=True)
	tomor_output = models.FloatField(verbose_name=u'Нийт төмөр:', null=True, blank=True)
	uran_output = models.FloatField(verbose_name=u'Уран:', null=True, blank=True)
	har_tugalga_output = models.FloatField(verbose_name=u'Хар тугалга:', null=True, blank=True)
	niit_hrom_output = models.FloatField(verbose_name=u'Нийт хром:', null=True, blank=True)
	valent_6_hrom_output = models.FloatField(verbose_name=u'6 валенттай хром:', null=True, blank=True)
	hongon_tsagaan_output = models.FloatField(verbose_name=u'Хөнгөн цагаан:', null=True, blank=True)
	huntsel_output = models.FloatField(verbose_name=u'Хүнцэл:', null=True, blank=True)
	tsair_output = models.FloatField(verbose_name=u'Цайр:', null=True, blank=True)
	tsagaan_tugalga_output = models.FloatField(verbose_name=u'Цагаан тугалга:', null=True, blank=True)
	niit_tsianid_output = models.FloatField(verbose_name=u'Нийт цианид:', null=True, blank=True)
	choloot_tsianid_output = models.FloatField(verbose_name=u'Чөлөөт цианид:', null=True, blank=True)
	phenol_output = models.FloatField(verbose_name=u'Фенол:', null=True, blank=True)
	benza_piren_output= models.FloatField(verbose_name=u'Бенза(а)пирен:', null=True, blank=True)
	ooh_tos_output = models.FloatField(verbose_name=u'Өөх тос:', null=True, blank=True)
	erdes_tos_output = models.FloatField(verbose_name=u'Эрдэс тос:', null=True, blank=True)
	ugaagch_bodis_output = models.FloatField(verbose_name=u'Бүх төрлийн угаагч бодис:', null=True, blank=True)
	trichlor_ethylen_output = models.FloatField(verbose_name=u'Трихлорэтилен:', null=True, blank=True)
	tetrachlor_ethylen_output = models.FloatField(verbose_name=u'Тетрахлорэтилен:', null=True, blank=True)
	gedes_nyan_output = models.FloatField(verbose_name=u'Гэдэсний бүлгийн эмгэг төрөгч нян:', null=True, blank=True)
	
	ognoo=models.DateField(verbose_name=u'Он, сар, өдөр:')
	mheg_dugnelt= models.ImageField(verbose_name= u'Шинжилгээний талаар МХЕГ-ын дүгнэлт:', validators=[validate_file_extension, validate_file_size], upload_to=user_directory_path)


class TZ_huselt_bohir_analysis(Create):
	tze = models.ForeignKey(TZE)

	temperature_input = models.IntegerField(verbose_name=u'Усны температур:', null=True, blank=True)
	orchin_input = models.IntegerField(verbose_name=u'Усны орчин:', null=True, blank=True)
	uner_input = models.FloatField(verbose_name=u'Үнэр:', null=True, blank=True)
	umbuuro_input= models.FloatField(verbose_name=u'Умбуур бодисын тоо, мг/л:', null=True, blank=True)
	bhho_input= models.FloatField(verbose_name=u'БХХ мг/л O2:', null=True, blank=True)
	hhho_input= models.FloatField(verbose_name=u'ХХХ мг/л O2:', null=True, blank=True)
	pich_input = models.FloatField(verbose_name=u'Перманганатын исэлдэх чанар:', null=True, blank=True)
	davs_input = models.FloatField(verbose_name=u'Ууссан давс/эрдэсжилт/:', null=True, blank=True)
	niit_azot_input = models.FloatField(verbose_name=u'Нийт азот:', null=True, blank=True)
	niit_phosphor_input = models.FloatField(verbose_name=u'Нийт фосфор:', null=True, blank=True)
	huhert_ustorogch_input = models.FloatField(verbose_name=u'Хүхэрт устөрөгч:', null=True, blank=True)
	uldegdel_hlor_input = models.FloatField(verbose_name=u'Үлдэгдэл хлор:', null=True, blank=True)
	barii_input = models.FloatField(verbose_name=u'Барий:', null=True, blank=True)
	binder_input = models.FloatField(verbose_name=u'Биндэр:', null=True, blank=True)
	bor_input = models.FloatField(verbose_name=u'Бор:', null=True, blank=True)
	vanadii_input = models.FloatField(verbose_name=u'Ванадий:', null=True, blank=True)
	zes_input = models.FloatField(verbose_name=u'Зэс:', null=True, blank=True)
	kadmi_input = models.FloatField(verbose_name=u'Кадми:', null=True, blank=True)
	kobalt_input = models.FloatField(verbose_name=u'Кобальт:', null=True, blank=True)
	mangan_input = models.FloatField(verbose_name=u'Манган:', null=True, blank=True)
	anzan_input = models.FloatField(verbose_name=u'Анзан/Молибден:', null=True, blank=True)
	mongon_us_input = models.FloatField(verbose_name=u'Мөнгөн ус:', null=True, blank=True)
	nikel_input = models.FloatField(verbose_name=u'Никель:', null=True, blank=True)
	selen_input = models.FloatField(verbose_name=u'Селен:', null=True, blank=True)
	strontsi_input = models.FloatField(verbose_name=u'Стронций:', null=True, blank=True)
	tomor_input = models.FloatField(verbose_name=u'Нийт төмөр:', null=True, blank=True)
	uran_input = models.FloatField(verbose_name=u'Уран:', null=True, blank=True)
	har_tugalga_input = models.FloatField(verbose_name=u'Хар тугалга:', null=True, blank=True)
	niit_hrom_input = models.FloatField(verbose_name=u'Нийт хром:', null=True, blank=True)
	valent_6_hrom_input = models.FloatField(verbose_name=u'6 валенттай хром:', null=True, blank=True)
	hongon_tsagaan_input = models.FloatField(verbose_name=u'Хөнгөн цагаан:', null=True, blank=True)
	huntsel_input = models.FloatField(verbose_name=u'Хүнцэл:', null=True, blank=True)
	tsair_input = models.FloatField(verbose_name=u'Цайр:', null=True, blank=True)
	tsagaan_tugalga_input = models.FloatField(verbose_name=u'Цагаан тугалга:', null=True, blank=True)
	niit_tsianid_input = models.FloatField(verbose_name=u'Нийт цианид:', null=True, blank=True)
	choloot_tsianid_input = models.FloatField(verbose_name=u'Чөлөөт цианид:', null=True, blank=True)
	phenol_input = models.FloatField(verbose_name=u'Фенол:', null=True, blank=True)
	benza_piren_input= models.FloatField(verbose_name=u'Бенза(а)пирен:', null=True, blank=True)
	ooh_tos_input = models.FloatField(verbose_name=u'Өөх тос:', null=True, blank=True)
	erdes_tos_input = models.FloatField(verbose_name=u'Эрдэс тос:', null=True, blank=True)
	ugaagch_bodis_input = models.FloatField(verbose_name=u'Бүх төрлийн угаагч бодис:', null=True, blank=True)
	trichlor_ethylen_input = models.FloatField(verbose_name=u'Трихлорэтилен:', null=True, blank=True)
	tetrachlor_ethylen_input = models.FloatField(verbose_name=u'Тетрахлорэтилен:', null=True, blank=True)
	gedes_nyan_input = models.FloatField(verbose_name=u'Гэдэсний бүлгийн эмгэг төрөгч нян:', null=True, blank=True)

	temperature_output = models.IntegerField(verbose_name=u'Усны температур:', null=True, blank=True)
	orchin_output = models.IntegerField(verbose_name=u'Усны орчин:', null=True, blank=True)
	uner_output = models.FloatField(verbose_name=u'Үнэр:', null=True, blank=True)
	umbuuro_output= models.FloatField(verbose_name=u'Умбуур бодисын тоо, мг/л:', null=True, blank=True)
	bhho_output= models.FloatField(verbose_name=u'БХХ мг/л O2:', null=True, blank=True)
	hhho_output= models.FloatField(verbose_name=u'ХХХ мг/л O2:', null=True, blank=True)
	pich_output = models.FloatField(verbose_name=u'Перманганатын исэлдэх чанар:', null=True, blank=True)
	davs_output = models.FloatField(verbose_name=u'Ууссан давс/эрдэсжилт/:', null=True, blank=True)
	niit_azot_output = models.FloatField(verbose_name=u'Нийт азот:', null=True, blank=True)
	niit_phosphor_output = models.FloatField(verbose_name=u'Нийт фосфор:', null=True, blank=True)
	huhert_ustorogch_output = models.FloatField(verbose_name=u'Хүхэрт устөрөгч:', null=True, blank=True)
	uldegdel_hlor_output = models.FloatField(verbose_name=u'Үлдэгдэл хлор:', null=True, blank=True)
	barii_output = models.FloatField(verbose_name=u'Барий:', null=True, blank=True)
	binder_output = models.FloatField(verbose_name=u'Биндэр:', null=True, blank=True)
	bor_output = models.FloatField(verbose_name=u'Бор:', null=True, blank=True)
	vanadii_output = models.FloatField(verbose_name=u'Ванадий:', null=True, blank=True)
	zes_output = models.FloatField(verbose_name=u'Зэс:', null=True, blank=True)
	kadmi_output = models.FloatField(verbose_name=u'Кадми:', null=True, blank=True)
	kobalt_output = models.FloatField(verbose_name=u'Кобальт:', null=True, blank=True)
	mangan_output = models.FloatField(verbose_name=u'Манган:', null=True, blank=True)
	anzan_output = models.FloatField(verbose_name=u'Анзан/Молибден:', null=True, blank=True)
	mongon_us_output = models.FloatField(verbose_name=u'Мөнгөн ус:', null=True, blank=True)
	nikel_output = models.FloatField(verbose_name=u'Никель:', null=True, blank=True)
	selen_output = models.FloatField(verbose_name=u'Селен:', null=True, blank=True)
	strontsi_output = models.FloatField(verbose_name=u'Стронций:', null=True, blank=True)
	tomor_output = models.FloatField(verbose_name=u'Нийт төмөр:', null=True, blank=True)
	uran_output = models.FloatField(verbose_name=u'Уран:', null=True, blank=True)
	har_tugalga_output = models.FloatField(verbose_name=u'Хар тугалга:', null=True, blank=True)
	niit_hrom_output = models.FloatField(verbose_name=u'Нийт хром:', null=True, blank=True)
	valent_6_hrom_output = models.FloatField(verbose_name=u'6 валенттай хром:', null=True, blank=True)
	hongon_tsagaan_output = models.FloatField(verbose_name=u'Хөнгөн цагаан:', null=True, blank=True)
	huntsel_output = models.FloatField(verbose_name=u'Хүнцэл:', null=True, blank=True)
	tsair_output = models.FloatField(verbose_name=u'Цайр:', null=True, blank=True)
	tsagaan_tugalga_output = models.FloatField(verbose_name=u'Цагаан тугалга:', null=True, blank=True)
	niit_tsianid_output = models.FloatField(verbose_name=u'Нийт цианид:', null=True, blank=True)
	choloot_tsianid_output = models.FloatField(verbose_name=u'Чөлөөт цианид:', null=True, blank=True)
	phenol_output = models.FloatField(verbose_name=u'Фенол:', null=True, blank=True)
	benza_piren_output= models.FloatField(verbose_name=u'Бенза(а)пирен:', null=True, blank=True)
	ooh_tos_output = models.FloatField(verbose_name=u'Өөх тос:', null=True, blank=True)
	erdes_tos_output = models.FloatField(verbose_name=u'Эрдэс тос:', null=True, blank=True)
	ugaagch_bodis_output = models.FloatField(verbose_name=u'Бүх төрлийн угаагч бодис:', null=True, blank=True)
	trichlor_ethylen_output = models.FloatField(verbose_name=u'Трихлорэтилен:', null=True, blank=True)
	tetrachlor_ethylen_output = models.FloatField(verbose_name=u'Тетрахлорэтилен:', null=True, blank=True)
	gedes_nyan_output = models.FloatField(verbose_name=u'Гэдэсний бүлгийн эмгэг төрөгч нян:', null=True, blank=True)
	
	ognoo=models.DateField(verbose_name=u'Он, сар, өдөр:')
	mheg_dugnelt= models.ImageField(verbose_name= u'Шинжилгээний талаар МХЕГ-ын дүгнэлт:', validators=[validate_file_extension, validate_file_size], upload_to=user_directory_path)
	

#Автомашин
class Car(Create, History_operations):
	tze = models.ForeignKey(TZE)
	mark = models.CharField(max_length = 500, verbose_name=u'Автомашины марк')
	no = models.CharField(max_length = 10,verbose_name=u'Автомашины улсын дугаар')
	daats = models.FloatField(verbose_name=u'Даац(тонн)')
	gerchilgee_picture = models.ImageField(verbose_name=u'Гэрчилгээний зураг',validators=[validate_picture_extension, validate_file_size], upload_to=car_directory_path)
	us= models.FloatField(verbose_name=u'Зөөвөрлөх усны хэмжээ(м3/хон)', null= True, blank= True)
	approved = models.BooleanField(default=False)
	history = HistoricalRecords(inherit = True)
# Зөөврийн усны машин
class WaterCar(Car):
	hun_am_too = models.IntegerField(verbose_name=u'Айл өрхийн тоо')
	utb_too = models.IntegerField(verbose_name=u'УТБ-ны тоо')
	aanb_too = models.IntegerField(verbose_name=u'ААНБ-ын тоо')

	@classmethod
	def excel_write_header_and_format(self, worksheet, row_start, col_start):
		worksheet.write_string(row_start, col_start, u'ТЗЭ')
		worksheet.write_string(row_start, col_start+1, u'Автомашины марк')
		worksheet.write_string(row_start, col_start+2, u'Автомашины улсын дугаар')
		worksheet.write_string(row_start, col_start+3, u'Даац(тонн)')
		worksheet.write_string(row_start, col_start+4, u'Зөөвөрлөх усны хэмжээ(м3/хон)')
		worksheet.write_string(row_start, col_start+5, u'Айл өрхийн тоо')
		worksheet.write_string(row_start, col_start+6, u'УТБ-ны тоо')
		worksheet.write_string(row_start, col_start+7, u'ААНБ-ын тоо')


		return [row_start+1, col_start]
		
	def object_excel_write(self, worksheet, row_start, col_start, **kwargs):
		date_time=kwargs['date_time']
		hist_obj = self.get_history_object(date_time)

		if hist_obj:
			if hist_obj.status==True:
				worksheet.write_string(row_start, col_start, hist_obj.tze.org_name + ' ' + hist_obj.tze.org_type)
				worksheet.write_string(row_start, col_start+1, hist_obj.mark)
				worksheet.write_string(row_start, col_start+2, hist_obj.no)
				worksheet.write_number(row_start, col_start+3, hist_obj.daats)
				worksheet.write_number(row_start, col_start+4, hist_obj.us)
				worksheet.write_number(row_start, col_start+5, hist_obj.hun_am_too)
				worksheet.write_number(row_start, col_start+6, hist_obj.utb_too)
				worksheet.write_number(row_start, col_start+7, hist_obj.aanb_too)
				return [row_start+1, col_start] # daraagiin object bichih coordinatiig butsaana
			else:
				# history ni status=False baina
				return [row_start, col_start]
		else:
			# history object doesn't exist
			return [row_start, col_start]

# Бохир усны машин
class BohirCar(Car):
	gereet_too = models.IntegerField(verbose_name=u'Гэрээт үйлчлүүлэгчдийн тоо')
	duudlaga_too = models.IntegerField(verbose_name=u'Дуудлагаар үйлчлүүлэгчдийн тоо')
	niiluuleh_tseg = models.CharField(max_length = 250,verbose_name=u'Бохир ус нийлүүлэх цэгийн байршил')
	avtomashin_tevsh = models.ImageField(verbose_name=u'Автомашины фото зураг',validators=[validate_picture_extension, validate_file_size], upload_to=car_directory_path)

	@classmethod
	def excel_write_header_and_format(self, worksheet, row_start, col_start):
		worksheet.write_string(row_start, col_start, u'ТЗЭ')
		worksheet.write_string(row_start, col_start+1, u'Автомашины марк')
		worksheet.write_string(row_start, col_start+2, u'Автомашины улсын дугаар')
		worksheet.write_string(row_start, col_start+3, u'Даац(тонн)')
		worksheet.write_string(row_start, col_start+4, u'Зөөвөрлөх усны хэмжээ(м3/хон)')
		worksheet.write_string(row_start, col_start+5, u'Гэрээт үйлчлүүлэгчдийн тоо')
		worksheet.write_string(row_start, col_start+6, u'Дуудлагаар үйлчлүүлэгчдийн тоо')
		worksheet.write_string(row_start, col_start+7, u'Бохир ус нийлүүлэх цэгийн байршил')


		return [row_start+1, col_start]
		
	def object_excel_write(self, worksheet, row_start, col_start, **kwargs):
		date_time=kwargs['date_time']
		hist_obj = self.get_history_object(date_time)

		if hist_obj:
			if hist_obj.status==True:
				worksheet.write_string(row_start, col_start, hist_obj.tze.org_name + ' ' + hist_obj.tze.org_type)
				worksheet.write_string(row_start, col_start+1, hist_obj.mark)
				worksheet.write_string(row_start, col_start+2, hist_obj.no)
				worksheet.write_number(row_start, col_start+3, hist_obj.daats)
				worksheet.write_number(row_start, col_start+4, hist_obj.us)
				worksheet.write_number(row_start, col_start+5, hist_obj.gereet_too)
				worksheet.write_number(row_start, col_start+6, hist_obj.duudlaga_too)
				worksheet.write_string(row_start, col_start+7, hist_obj.niiluuleh_tseg)
				return [row_start+1, col_start] # daraagiin object bichih coordinatiig butsaana
			else:
				# history ni status=False baina
				return [row_start, col_start]
		else:
			# history object doesn't exist
			return [row_start, col_start]

class UAT(models.Model):	# materialiin ner
	material_name = models.CharField(max_length = 250)
	material_number = models.IntegerField(unique = True, blank = False, null = True)	# materialiin modal-iig yalgaj gargahiin tuld ene talbar hereg bolj baina
	url = models.CharField(max_length = 50, blank = False, null = True)

class UAT_yavts(Create):	# materialiin ner
	songolt = (
		(u'Илгээсэн', u'Илгээсэн'),
		(u'Зөвшөөрсөн', u'Зөвшөөрсөн'),
		(u'Цуцалсан', u'Цуцалсан'),
		)
	tze= models.ForeignKey(TZE)
	on= models.IntegerField(verbose_name=u'Он')
	uat=models.ManyToManyField(UAT)
	yavts = models.CharField(max_length = 30, choices= songolt)	# materialiin status types
	
class Message(Create):
	doc_names = (
		(u'Үйл ажиллагааны тайлан', u'Үйл ажиллагааны тайлан'),
		(u'Тусгай зөвшөөрлийн хүсэлт', u'Тусгай зөвшөөрлийн хүсэлт'),
		(u'Санхүү эдийн засгийн тайлан', u'Санхүү эдийн засгийн тайлан'),
		(u'Гүйцэтгэл шалгуур үзүүлэлтийн тайлан', u'Гүйцэтгэл шалгуур үзүүлэлтийн тайлан'),
		)
	tolov_songolt = (
		(u'Илгээсэн', u'Илгээсэн'),
		(u'Үзсэн', u'Үзсэн'),
		)
	tze= models.ForeignKey(TZE)
	doc= models.CharField(max_length= 150, choices= doc_names)
	message= models.CharField(max_length=5000, verbose_name= u'Та энд мэдэгдлээ бичнэ үү!')
	tolov= models.CharField(max_length =30 , choices= tolov_songolt)
	to= models.ForeignKey(User, related_name= 'receiver')


''' Гүйцэтгэлийн шалгуур үзүүлэлтийн тайлан '''
gshu_status = (
	(u'Илгээсэн', u'Илгээсэн'),
	(u'Мэдээлэл дутуу', u'Мэдээлэл дутуу'),
	(u'Буцаасан', u'Буцаасан'),
	(u'Хүлээн авсан', u'Хүлээн авсан'),
	)
class GShU(Create):
	tze = models.ForeignKey(TZE)
	tailan_date = models.DateField(verbose_name="Тайлангийн огноо")
	tolov = models.CharField(max_length=32, choices=gshu_status, default=u"Мэдээлэл дутуу")

	uzuulelt_1 = models.BooleanField(default=False)
	uzuulelt_2 = models.BooleanField(default=False)
	uzuulelt_3 = models.BooleanField(default=False)
	uzuulelt_4 = models.BooleanField(default=False)
	uzuulelt_5 = models.BooleanField(default=False)
	uzuulelt_6 = models.BooleanField(default=False)
	uzuulelt_7 = models.BooleanField(default=False)
	uzuulelt_8 = models.BooleanField(default=False)
	uzuulelt_9 = models.BooleanField(default=False)
	uzuulelt_10 = models.BooleanField(default=False)
	uzuulelt_11 = models.BooleanField(default=False)
	uzuulelt_12 = models.BooleanField(default=False)
	uzuulelt_13 = models.BooleanField(default=False)
	uzuulelt_14 = models.BooleanField(default=False)

	''' Гүйцэтгэлийн шалгуур үзүүлэлт Үйлчилгээний хүртээмж '''
	Pasdws = models.IntegerField(verbose_name = "ТЗЭ-ээр үйлчлүүлж буй хүн амын тоо (жилийн эцсээр)", null=True)
	Nmean = models.IntegerField(verbose_name="Тухайн орон нутгийн хүн амын тоо (жилийн эцсээр)", null=True)
	''' Боловсон хүчний үзүүлэлт '''
	Ne1 = models.IntegerField(verbose_name="Боловсролтой ажилтны тоо", null=True)
	N1 = models.IntegerField(verbose_name="Нийт ажилтны тоо", null=True)
	C = models.IntegerField(verbose_name="Нийт хэрэглэгчдийн тоо", null=True)

	''' Цэвэр ус олборлолт '''
	Q1 = models.FloatField(verbose_name="Олборлосон усны хэмжээ (м3/хоног)", null=True)
	Qr = models.FloatField(verbose_name = "Тогтоогдсон нөөц (м3/хоног)", null=True)
	Q2 = models.IntegerField(verbose_name="Олборлосон усны хэмжээ", null=True)
	Ec = models.IntegerField(verbose_name="Нийт зарцуулсан эрчим хүч (кВт.ц)", null=True)
	Na = models.IntegerField(verbose_name="Авсан шинжилгээний тоо", null=True)
	Nb = models.IntegerField(verbose_name = "Стандартад нийцээгүй дүнгийн тоо", null=True)

	''' Цэвэр ус түгээлт '''
	Qn = models.IntegerField(verbose_name="Нийлүүлсэн усны хэмжээ (мян.шоо метр)", null=True)
	Qs1 = models.IntegerField(verbose_name="Нийт борлуулсан усны хэмжээ (мян.шоо метр)", null=True)
	Qm = models.IntegerField(verbose_name="Тоолууртай хэрэглэгчдийн тоо", null=True)
	Qs2 = models.IntegerField(verbose_name="Нийт хэрэглэгчдийн тоо", null=True)
	Nn = models.IntegerField(verbose_name="Нийт гэмтлийн тоо", null=True)
	Ln = models.IntegerField(verbose_name="Нийт шугамын урт", null=True)

	''' Гүйцэтгэлийн шалгуур үзүүлэлт цэвэрлэх байгууламж '''
	BOD5input = models.FloatField(verbose_name="Цэвэрлэх байгууламж руу орох усны биологийн хэрэгцээт хүчилтөрөгч 5 хоног, мг\л ", null=True)
	BOD5output = models.FloatField(verbose_name="Цэвэрлэх байгууламжаас гарч буй биологийн хэрэгцээт хүчилтөрөгч 5 хоног", null=True)
	COD5input = models.FloatField(verbose_name="Цэвэрлэх байгууламж руу орж буй бохир усны химийн хэрэгцээт хүчилтөрөгч, мг\л", null=True)
	COD5output = models.FloatField(verbose_name="Цэвэрлэх байгууламжаас гарч буй усны химийн хэрэгцээт хүчилтөрөгч", null=True)
	SSinput = models.FloatField(verbose_name="Цэвэрлэх байгууламж руу орж буй усан дах умбуур бодисын агууламж", null=True)
	SSoutput = models.FloatField(verbose_name="Цэвэрлэх байгууламжаас гарч буй усан дах умбуур бодисын агууламж", null=True)

	''' Гүйцэтгэлийн шалгуур үзүүлэлтийн тайлан санхүүгийн үзүүлэлт '''
	BOsh = models.FloatField(verbose_name = "Гүйцэтгэлээр гарсан нийт зардал", null=True)
	BOshb = models.FloatField(verbose_name="Тогтоолоор батлагдсан БОш", null=True)

	O = models.FloatField(verbose_name="Нийт орлого", null=True)
	Z = models.FloatField(verbose_name = "Нийт зардал", null=True)

	TsQs = models.FloatField(verbose_name="Нийт борлуулсан цэвэр усны хэмжээ", null=True)
	ZTsU = models.FloatField(verbose_name="Цэвэр усны үйл ажиллагааны нийт зардал", null=True)

	BQs = models.FloatField(verbose_name="Нийт бохир усны хэмжээ", null=True)
	ZBU = models.FloatField(verbose_name="Бохир усны үйл ажиллагааны нийт зардал", null=True)

	M = models.FloatField(verbose_name="Бэлэн мөнгөний орлого", null=True)
	B = models.FloatField(verbose_name="Борлуулалтын нийт орлого", null=True)

	def can_edit(self):
		if self.tolov == u'Мэдээлэл дутуу' or self.tolov == u'Буцаасан':
			return True
		else:
			return False
	def change_tolov_to_ilgeesen(self):
		self.tolov = u'Илгээсэн'
		self.save()

	
	
''' Хөрөнгө оруулалт '''
class HorongoOruulalt(Create):
	tze = models.ForeignKey(TZE)
	on = models.DateField()
	ajil = models.CharField(max_length = 500)
	eh_uusver = models.CharField(max_length = 500)
	ehleh = models.DateField()
	duusah = models.DateField()
	orlog = models.IntegerField()
	guitsetgel = models.IntegerField()
	
# Системийн лог
class Log(models.Model):
	user_id = models.ForeignKey(User)	
	begin_time = models.DateTimeField(null = True, blank = True, verbose_name = 'Эхлэх хугацаа:')
	end_time = models.DateTimeField(null = True, blank = True, verbose_name = 'Дуусах хугацаа:')
	status = models.BooleanField(verbose_name = 'Төлөв:', default = False)


# Системийн лог-дутууы
class Medegdel(models.Model):
	user_id = models.ForeignKey(User)	
	begin_time = models.DateTimeField(null = True, blank = True, verbose_name = 'Эхлэх хугацаа:')
	end_time = models.DateTimeField(null = True, blank = True, verbose_name = 'Дуусах хугацаа:')

	status = models.BooleanField(verbose_name = 'Төлөв:', default = False)


########## uilsee nemsen start ##############


''' Тусгай зөвшөөрлийн гэрчилгээ '''
class Certificate(Create, History_operations):
	tz_id = models.ManyToManyField(TZ)
	tze = models.ForeignKey(TZE)
	cert_number = models.CharField(max_length = 5, unique = True)
	tolov = models.ForeignKey(Certificate_tolov)	# gerchilgeenii tolov: huchintei, huchingui, tutgelzuulsen
	togtool_date = models.DateField(verbose_name='Тогтоолын он, сар, өдөр:', null=True)
	togtool_number = models.IntegerField(verbose_name='Тогтоолын дугаар:', null=True)
	certificate_end_date = models.DateField(verbose_name='Гэрчилгээний хүчинтэй хугацаа он, сар, өдөр (хүртэл):', null=True)
	cert_file = models.FileField(verbose_name=u'Гэрчилгээний хуулбар:', null=True, validators=[validate_pdf_extension, validate_file_size])
	history = HistoricalRecords()
	def change_tolov_to_olgogdson(self):
		tolov, created = Certificate_tolov.objects.get_or_create(tolov = u'Хүчинтэй')
		self.tolov = tolov
		self.save()
	def get_sungaltuud(self):
		return Certificate_sungalt.objects.filter(certificate=self)
	def is_sungah_bolomjtoi(self):
		if self.is_left_less_than_90_days():
			sungaltuud = Certificate_sungalt.objects.filter(certificate = self)
			if sungaltuud.count() < 1:
				return True
			else:
				return False
		else:
			return False
	def is_left_less_than_90_days(self):
		if self.is_tolov_huchintei():
			delta = self.certificate_end_date - timezone.datetime.now().date()
			if delta.days < 90:
				return True
			else:
				return False
		else:
			return False
	def is_tolov_huchintei(self):
		if self.tolov.tolov == u'Хүчинтэй':
			return True
		else:
			return False
	def is_tolov_huchingui(self):
		if self.tolov.tolov == u'Хүчингүй':
			return True
		else:
			return False
	def is_tolov_tutgelzsen(self):
		if self.tolov.tolov == u'Түтгэлзсэн':
			return True
		else:
			return False

	def __unicode__(self):
		return "%s" %(self.cert_number)
class Certificate_sungalt(Create, History_operations):
	certificate = models.ForeignKey(Certificate, verbose_name=u'Тусгай зөвшөөрлийн гэрчилгээ')
	ognoo = models.DateField(verbose_name=u'Сунгалтын огноо')

class Rel_baig_zz_ajilchid(Create, History_operations):
	tze = models.OneToOneField(TZE)
	uta_mergejilten = models.ForeignKey(Ajiltan, related_name = 'une_tarifiin_albanii_mergejilten', null = True, blank = True)
	tza_mergejilten = models.ForeignKey(Ajiltan, related_name = 'tz_albanii_mergejilten', null = True, blank = True)
	history = HistoricalRecords()

''' Тусгай зөвшөөрөл авах хүсэлт'''

class TZ_medegdel(models.Model):
	tz_huselt = models.ForeignKey('TZ_Huselt')
	datetime = models.DateTimeField()
	message = models.CharField(max_length = 500)
	created_by = models.ForeignKey('User')


class TZ_anhaaruulga(models.Model):	# tusgai zovshooroliin huselttei holbootoi anhaaruulgiig haruuldag baina. Ogogdliin sangaas shuud ustagadag baina.
	tz_huselt = models.ForeignKey('TZ_Huselt')
	warning_message = models.CharField(max_length = 250)

class TZ_material(models.Model):	# materialiin ner
	#tz = models.ForeignKey(TZ)
	material_name = models.CharField(max_length = 250)
	material_number = models.IntegerField(unique = True, blank = False, null = True)	# materialiin modal-iig yalgaj gargahiin tuld ene talbar hereg bolj baina
	# div id ni material_number - aas burdsen temdegt mor baina
	material_angilal = models.IntegerField()
	# 3 hzm-nii material
	# 1 tza-nii materila
	# 2 uta-nii material

	def __unicode__(self):
		t = self.material_name + ' ' + str(self.material_number)
		return t



material_statuses = (
	(u'Мэдээлэл дутуу', u'Мэдээлэл дутуу'),
	(u'Шаардлага хангаагүй', u'Шаардлага хангаагүй'),
	(u'Шаардлага хангасан', u'Шаардлага хангасан'),
	(u'Бүрдсэн', u'Бүрдсэн'),
	)

class TZ_mat_status_bind(models.Model):	# materialiin neriig statustai holboh class
	material = models.ForeignKey(TZ_material)
	status = models.CharField(max_length = 32, choices=material_statuses)
	tatgalzsan_tailbar = models.CharField(max_length = 200, null=True, blank=True)
	updated_datetime = models.DateTimeField()	# hamgiin suuld zasagdsan ognoo. Ug materialtai hamaaraltai classiin medeelel soligdohod ene fieldiig shinechilne
	updated_by = models.ForeignKey('User', null= True, blank=True) #user baina

	def __unicode__(self):
		return "%s | %s" %(six.text_type(self.material), six.text_type(self.status))
	def copy_object(self):
		# ooriigoo huulbarlah function
		obj_copy = TZ_mat_status_bind(material = self.material, 
										status = self.status, 
										tatgalzsan_tailbar = self.tatgalzsan_tailbar,
										updated_datetime = self.updated_datetime,
										updated_by = self.updated_by
										)
		obj_copy.save()
		return obj_copy

	def change_status_to_burdsen(self, time_now, user=None):
		self.status = u'Бүрдсэн'
		self.updated_datetime = time_now
		self.updated_by = user
		self.save()
		return 0

	def change_status_to_med_dutuu(self, time_now, user=None):
		self.status = u'Мэдээлэл дутуу'
		self.updated_datetime = time_now
		self.updated_by = user
		self.save()
		return 0

	def change_status_to_hangaltgui(self, time_now, user=None):
		self.status = u'Шаардлага хангаагүй'
		self.updated_datetime = time_now
		self.updated_by = user
		self.save()
		return 0

	def change_status_to_zovshoorson(self, time_now, user=None):
		self.status = u'Шаардлага хангасан'
		self.updated_datetime = time_now
		self.updated_by = user
		self.save()
		return 0


tz_huselt_yavts_choices = (
	(u'Материал бүрдүүлэлт', u'Материал бүрдүүлэлт'),
	(u'Буцаагдсан', u'Буцаагдсан'),
	(u'Цуцлагдсан', u'Цуцлагдсан'),
	(u'Бичиг баримтыг хүлээн авсан', u'Бичиг баримтыг хүлээн авсан'),
	(u'Хүсэлт илгээгдсэн', u'Хүсэлт илгээгдсэн'),
	(u'Материал бүрдсэн', u'Материал бүрдсэн'),
	)

class TZ_Huselt(Create):
	tze = models.ForeignKey(TZE)
	yavts=models.CharField(choices = tz_huselt_yavts_choices, max_length = 64, verbose_name = 'Явц ID:')
	huuli_mergejilten = models.ForeignKey(Ajiltan, null=True, verbose_name = 'Хариуцсан хууль зүйн мэргэжилтэн:', related_name = 'hz_mergejilten', blank = True)
	tza_mergejilten = models.ForeignKey(Ajiltan, null=True, verbose_name = 'Хариуцсан ТЗА-ны мэргэжилтэн:', related_name = 'tz_mergejilten', blank = True)
	uta_mergejilten = models.ForeignKey(Ajiltan, null=True, verbose_name = 'Хариуцсан ҮТА-ны мэргэжилтэн:', related_name = 'ut_mergejilten', blank = True)
	ajliin_heseg_date = models.DateField(null = True, blank = True, verbose_name = 'Ажлын хэсэг очих өдөр:')
	hurliin_date = models.DateField(null = True, blank = True, verbose_name = 'Хурлаар хэлэлцэх өдөр:')
	ilgeesen_datetime = models.DateTimeField(null=True, verbose_name = 'Хүсэлтийг илгээсэн хугацаа:')

	
	huleen_avsan = models.BooleanField(default = False)
	

	def change_yavts_to_tz_olgoson(self):
		self.yavts = u'ТЗ олгосон'
		self.save()
	def change_yavts_to_tz_olgoogui(self):
		self.yavts = u'ТЗ олгоогүй'
		self.save()
	def change_yavts_to_butsaagdsan(self):
		self.yavts = u'Буцаагдсан'
		self.save() # butsaagdsan hugatsaag temdegledeg baihuu???
	def change_yavts_to_bichig_barimt_OK(self):
		self.yavts = u'Бичиг баримтыг хүлээн авсан'
		self.save() # butsaagdsan hugatsaag temdegledeg baihuu???
	def change_yavts_to_material_burduulelt(self):
		self.yavts = u'Материал бүрдүүлэлт'
		self.save() # butsaagdsan hugatsaag temdegledeg baihuu???
	def change_yavts_to_huselt_ilgeegdsen(self):
		self.yavts = u'Хүсэлт илгээгдсэн'
		self.save() # butsaagdsan hugatsaag temdegledeg baihuu??
	def change_yavts_to_huseltiig_huleen_avsan(self):
		self.yavts = u'Хүсэлтийг хүлээн авсан'
		self.save()
	def change_yavts_to_huseltiig_huleen_avaagui(self):
		self.yavts = u'Хүсэлтийг хүлээн аваагүй'
		self.save()
	def change_yavts_to_tsutslagdsan(self):
		self.yavts = u'Цуцлагдсан'
		self.save() # butsaagdsan hugatsaag temdegledeg baihuu???
	def change_yavts_to_material_burdsen(self):
		self.yavts = u'Материал бүрдсэн'
		self.save() # butsaagdsan hugatsaag temdegledeg baihuu???

	def is_yavts_material_burduulelt(self):
		return self.yavts == u'Материал бүрдүүлэлт'
	def is_yavts_ilgeegdsen(self):
		return self.yavts == u'Хүсэлт илгээгдсэн'
	def is_yavts_butsaagdsan(self):
		return self.yavts == u'Буцаагдсан'
	def is_yavts_tsutslagdsan(self):
		return self.yavts == u'Цуцлагдсан'
	def is_yavts_bichig_barimt_OK(self):
		return self.yavts == u'Бичиг баримтыг хүлээн авсан'
	def is_yavts_tz_olgoson(self):
		return self.yavts == u'ТЗ олгосон'
	def is_yavts_tz_olgoogui(self):
		return self.yavts == u'ТЗ олгоогүй'

	def is_ajliin_heseg_tovloh_bolomjtoi(self):
		bolomjtoi = True
		if self.is_yavts_bichig_barimt_OK():
			bolomjtoi = True
		else:
			bolomjtoi = False
		return bolomjtoi
	def is_hural_tovloh_bolomjtoi(self):
		bolomjtoi = True
		if not self.ajliin_heseg_date:
			bolomjtoi=False
		return bolomjtoi

	def huselt_ilgeeh(self):
		self.ilgeesen_datetime = timezone.now()
		self.burdel.huselt_ilgeeh()
		self.change_yavts_to_huselt_ilgeegdsen()

	def __unicode__(self):
		t = self.tze.org_name
		return t


class Burdel(models.Model):	# material dotorh medeelluudiig uusgeh classuud
	tz_huselt_angilal = (
		(u'1', u'Орон нутгийн ус хангамж ариутгах татуургын ашиглалт, үйлчилгээ эрхлэх тусгай зөвшөөрөл'),
		(u'2', u'Орон сууцны барилгын ус хангамж ариутгах татуургын ашиглалт, үйлчилгээ эрхлэх тусгай зөвшөөрөл'),
		(u'3', u'Цэвэр ус олборлон цэвэршүүлэх байгууламжийн ашиглалт, үйлчилгээ эрхлэх тусгай зөвшөөрөл'),
		(u'4', u'Бохир усыг тусгай зориулалтын автомашинаар зөөвөрлөх үйлчилгээ эрхлэх тусгай зөвшөөрөл'),
	)

	# huselt angilal: Хөдөө орон нутаг, Ус олборлолт, орон сууц, Бохир ус зөөвөрлөх
	huselt_angilal = models.CharField(max_length = 16, choices = tz_huselt_angilal, null=True)

	tz_huselt = models.OneToOneField(TZ_Huselt) # huselted burdel gantshan baina
	tz = models.ManyToManyField(TZ)		# tusgai zovshoorliin zaaltuud
	tze = models.ForeignKey(TZE, null=True) # TZE
	materialiud_list = models.ManyToManyField(TZ_mat_status_bind, verbose_name = 'материалуудын жагсаалт:')
	cert = models.ForeignKey(Certificate, null=True, verbose_name=u'Сунгах тусгай зөвшөөрлийн гэрчилгээ', blank=True)

	tza_check_finished = models.BooleanField(default = False)
	uta_check_finished = models.BooleanField(default = False)
	hzm_check_finished = models.BooleanField(default = False)
	
	ajiltans = models.ManyToManyField(Ajiltan)
	#zasag_dargiin_todorhoilolts = models.ManyToManyField(ZDTodorhoilolt)
	#hangagch_baigs = models.ManyToManyField(HangagchBaiguullaga)
	#tax_tods = models.ManyToManyField(TaxTodorhoilolt)
	sanhuu_tailans = models.ManyToManyField(SanhuuTailan)
	#audit_dugnelts = models.ManyToManyField(AuditDugnelt)
	oron_toonii_schemas = models.ManyToManyField(OronTooniiSchema)
	#norm_standarts = models.ManyToManyField(NormStandart)
	#ulsiin_komis_akts = models.ManyToManyField(UlsiinAkt)
	us_ashiglah_zovshoorols = models.ManyToManyField(UsZuvshuurul)
	#uildver_tech_schemas = models.ManyToManyField(UildverTechnology)
	#mheg_dugnelts = models.ManyToManyField(MergejliinHyanalt)
	#ajliin_bair_dugnelts = models.ManyToManyField(AjliinBair)
	#mashin_tonog_tohooromjs = models.ManyToManyField(Equipment)

	us_shinjilgee = models.ForeignKey(TZ_huselt_water_analysis, null=True)
	bohir_shinjilgee = models.ForeignKey(TZ_huselt_bohir_analysis, null=True)

	# class-uudiin history
	# ilgeesen datetime
	# uussen datetime
	def is_possible_send(self):
		check = False
		if self.tz_huselt.is_yavts_material_burduulelt() or self.tz_huselt.is_yavts_butsaagdsan():
			check = True

		for i in self.materialiud_list.all():
			if i.status == u'Шаардлага хангаагүй' or i.status == u'Мэдээлэл дутуу':
				check = False
		return check

	def is_hzm_tza_uta_checked_OK(self):
		if self.tza_checked_OK and self.uta_checked_OK and self.hzm_checked_OK:
			return True
		else:
			return False

	def get_material_1(self):
		mat1 = get_object_or_404(TZ_material, material_number = 1)
		d = self.materialiud_list.get(material = mat1)
		return d

	def get_list_of_TZ_materials(self):
		m_names = [
					TZ_material.objects.get(material_number = 1),	# 
					TZ_material.objects.get(material_number = 5),	# 
					TZ_material.objects.get(material_number = 7),	# 
					TZ_material.objects.get(material_number = 8),	# 
					TZ_material.objects.get(material_number = 9),	# 
					TZ_material.objects.get(material_number = 14),	# 
					TZ_material.objects.get(material_number = 15),	# 
					TZ_material.objects.get(material_number = 30),	# 
					
		]	# end buh huselted zaaval baih materialuudiin nersiig hiij ogno
		#if '12.2.3' in zaaltuud_choices or '12.2.4' in zaaltuud_choices or '12.2.5' in zaaltuud_choices or '12.2.6' in zaaltuud_choices or '12.2.7' in zaaltuud_choices or '12.2.8' in zaaltuud_choices or '12.2.9' in zaaltuud_choices or '12.2.10' in zaaltuud_choices or '12.2.11' in zaaltuud_choices or '12.2.12' in zaaltuud_choices or '12.2.13' in zaaltuud_choices:
		#	TZ_material.objects.get(material_number =24), # Хангагч байгууллагын тодорхойлолт
		#	TZ_material.objects.get(material_number =25), # Хангагч байгууллагатай байгуулсан гэрээ

		#if '12.2.1' in zaaltuud_choices or '12.2.2' in zaaltuud_choices:
		#	m_names.append(TZ_material.objects.get(material_number =10)) # Шугам сүлжээ барилга байгууламжийн зураг, технологийн схем
		
		tz_list_all = TZ.objects.all()
		for i in self.tz.all():
			if i == tz_list_all.get(tz = '12.2.1'):
				#m_names.append(TZ_material.objects.get(material_number =11)) # Усны чанарын шинжилгээний дүн, дүгнэлт
				#m_names.append(TZ_material.objects.get(material_number =12)) # Лабораторийн шинжилгээнд МХГ-ын дүгнэлт
				#m_names.append(TZ_material.objects.get(material_number =13)) # Байгаль орчны асуудал эрхэлсэн төрийн захиргааны төв байгууллагын ус ашиглалтын дүгнэлт, ус ашиглах зөвшөөрөл, гэрээ
				m_names.append(TZ_material.objects.get(material_number =16)) # Гүний худаг
				

			elif i == tz_list_all.get(tz = '12.2.2'):
				if not tz_list_all.get(tz = '12.2.1') in self.tz.all():
					pass
					#m_names.append(TZ_material.objects.get(material_number =11)) # Үйлдвэрийн технологи, түүний схем зураг, тайлбар
					#m_names.append(TZ_material.objects.get(material_number =12)) # Усны чанарын шинжилгээний дүн, дүгнэлт
					#m_names.append(TZ_material.objects.get(material_number =13)) # Лабораторийн шинжилгээнд МХГ-ын дүгнэлт
					#m_names.append(TZ_material.objects.get(material_number =22)) # Байгаль орчны асуудал эрхэлсэн төрийн захиргааны төв байгууллагын ус ашиглалтын дүгнэлт, ус ашиглах зөвшөөрөл, гэрээ
				m_names.append(TZ_material.objects.get(material_number =17)) # 
				m_names.append(TZ_material.objects.get(material_number =18)) # 
				m_names.append(TZ_material.objects.get(material_number =19)) # 
				m_names.append(TZ_material.objects.get(material_number =23)) # Усны шинжилгээ
				m_names.append(TZ_material.objects.get(material_number =26)) # Цэвэршүүлэх байгууламж

			elif i == tz_list_all.get(tz = '12.2.3'):
				a = TZ_material.objects.get(material_number =18)
				if a not in m_names:
					m_names.append(a) # 

			elif i == tz_list_all.get(tz = '12.2.4'):
				a = TZ_material.objects.get(material_number =19)
				if a not in m_names:
					m_names.append(a) # 

			elif i == tz_list_all.get(tz = '12.2.5'):
				m_names.append(TZ_material.objects.get(material_number =20)) # 
				m_names.append(TZ_material.objects.get(material_number =21)) # 
				m_names.append(TZ_material.objects.get(material_number =22)) # 
				#m_names.append(TZ_material.objects.get(material_number =9)) #

			elif i == tz_list_all.get(tz = '12.2.6'):
				#m_names.append(TZ_material.objects.get(material_number =21)) # 
				pass

			elif i == tz_list_all.get(tz = '12.2.7'):
				#m_names.append(TZ_material.objects.get(material_number =22)) # 
				pass

			elif i == tz_list_all.get(tz = '12.2.8'):
				#m_names.append(TZ_material.objects.get(material_number =23)) # 
				pass

			elif i == tz_list_all.get(tz = '12.2.9'):
				#m_names.append(TZ_material.objects.get(material_number =24)) # 
				pass

			elif i == tz_list_all.get(tz = '12.2.10'):
				m_names.append(TZ_material.objects.get(material_number =24)) # Бохир усны шинжилгээ (оролт гаралт)
				m_names.append(TZ_material.objects.get(material_number =25)) # Цэвэрлэх байгууламж

			elif i == tz_list_all.get(tz = '12.2.11'):
				pass
				#m_names.append(TZ_material.objects.get(material_number =26)) # 

			elif i == tz_list_all.get(tz = '12.2.12'):
				m_names.append(TZ_material.objects.get(material_number =27)) # 

			elif i == tz_list_all.get(tz = '12.2.13'):
				m_names.append(TZ_material.objects.get(material_number =28)) # 

			elif i == tz_list_all.get(tz = '12.2.14'):
				m_names.append(TZ_material.objects.get(material_number =29)) # Бохир усны машин

		return m_names

	def change_materialiud_list(self):
		self.materialiud_list.clear()
		materials = self.get_list_of_TZ_materials()
		for m in materials:
			if m.material_number == 1: # Байгууллагын ерөнхий мэдээлэл
				if self.tze.gerchilgee_picture and self.tze.ubd and self.tze.org_name  and self.tze.org_date  and self.tze.phone and self.tze.e_mail and self.tze.tax and self.tze.address and self.tze.org_type and self.tze.fax and self.tze.post and self.tze.reg_num: # dutuu yum baigaa esehiin shalgah heregtei:
					b = TZ_mat_status_bind(material = m)
					b.change_status_to_burdsen(timezone.now())
					self.materialiud_list.add(b)	# materialiig nemj baina
				else:
					b = TZ_mat_status_bind(material = m)
					b.change_status_to_med_dutuu(timezone.now())
					self.materialiud_list.add(b)	# materialiig nemj baina

			elif m.material_number == 2: # Аймаг орон нутгийн засаг даргын тодорхойлолт			
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# materialiig nemj baina

				
			elif m.material_number == 3:	# Хангагч байгууллагуудтай хийсэн гэрээ, тодорхойлолт
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 4: # Татварын тодорхойлолт
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 5: # Санхүүгийн тайлан
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 6: # Аудитын дүгнэлт
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 7: # Байгууллагын орон тооны бүтцийн схем
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 8: # Норм стандартууд
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 9: # Улсын комиссын акт
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 10: # Ус ашиглах зөвшөөрөл, дүгнэлт гэрээ
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 11: # Үйлдвэрийн технологи, түүний схем зураг тайлбар
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 12: # МХЕГ-ын байгууллагын лабораторын шинжилгээнд өгсөн дүгнэлт
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 13: # Ажлын байрын дүгнэлт
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 14: # Хүний нөөц
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 15: # Машин тоног төхөөрөмж
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 16: # 12.2.1
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 17: # 12.2.2
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 18: # 12.2.3
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 19: # 12.2.4
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 20: # 12.2.5
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 21: # 12.2.6
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 22: # 12.2.7
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 23: # 12.2.8
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 24: # 12.2.9
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 25: # 12.2.10
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 26: # 12.2.11
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 27: # 12.2.12
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 28: # 12.2.13
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 29: # 12.2.14
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina

			elif m.material_number == 30:  # Санхүү эдийн засгийн үзүүлэлт
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina
			
			else:
				b = TZ_mat_status_bind(material = m)
				b.change_status_to_med_dutuu(timezone.now())
				self.materialiud_list.add(b)	# mateirialuudiig nemj baina
		return 0
	def material_butsaah_function(self):
		# burduulsen material butsaagdah uyd ene function duudagdana
		materials = self.materialiud_list.all()
		copies = []
		for i in materials:
			i_copy = i.copy_object()
			copies.append(i_copy)
		self.materialiud_list.clear()
		for i in copies:
			self.materialiud_list.add(i)

		self.tz_huselt.hzm_checked_OK = False
		self.tz_huselt.uta_checked_OK = False
		self.tz_huselt.tza_checked_OK = False
		return 0

	def huselt_ilgeeh(self):
		burdel_history = Burdel_history(tz_huselt = self.tz_huselt, tze = self.tze)
		burdel_history.ilgeesen_datetime = timezone.now()
		burdel_history.cert = self.cert

		burdel_history.us_shinjilgee = self.us_shinjilgee
		burdel_history.bohir_shinjilgee = self.bohir_shinjilgee
		burdel_history.huselt_angilal = self.huselt_angilal

		burdel_history.save()
		burdel_history.tz = self.tz.all()
		burdel_history.materialiud_list = self.materialiud_list.all()

		

		burdel_history.ajiltans = self.ajiltans.all()
		#burdel_history.zasag_dargiin_todorhoilolts = self.zasag_dargiin_todorhoilolts.all()
		#burdel_history.hangagch_baigs = self.hangagch_baigs.all()
		#burdel_history.tax_tods = self.tax_tods.all()
		burdel_history.sanhuu_tailans = self.sanhuu_tailans.all()
		#burdel_history.audit_dugnelts = self.audit_dugnelts.all()
		burdel_history.oron_toonii_schemas = self.oron_toonii_schemas.all()
		#burdel_history.norm_standarts = self.norm_standarts.all()
		#burdel_history.ulsiin_komis_akts = self.ulsiin_komis_akts.all()
		burdel_history.us_ashiglah_zovshoorols = self.us_ashiglah_zovshoorols.all()
		#burdel_history.uildver_tech_schemas = self.uildver_tech_schemas.all()
		#burdel_history.mheg_dugnelts = self.mheg_dugnelts.all()
		#burdel_history.ajliin_bair_dugnelts = self.ajliin_bair_dugnelts.all()
		#burdel_history.mashin_tonog_tohooromjs = self.mashin_tonog_tohooromjs.all()

		burdel_history.hudags = Hudag.objects.filter(tze = self.tze, status = True)
		burdel_history.usansans = UsanSan.objects.filter(tze = self.tze, status = True)
		burdel_history.nasosStantss = NasosStants.objects.filter(tze = self.tze, status = True)
		burdel_history.labs = Lab.objects.filter(tze = self.tze, status = True)
		burdel_history.shugam_suljees = Sh_suljee.objects.filter(tze = self.tze, status = True)
		burdel_history.ts_baiguulamjs = Ts_baiguulamj.objects.filter(tze = self.tze, status = True)
		burdel_history.us_damjuulah_tovs = UsDamjuulahBair.objects.filter(tze = self.tze, status = True)
		burdel_history.us_tugeeh_bairs = UsTugeehBair.objects.filter(tze = self.tze, status = True)
		burdel_history.abbs = ABB.objects.filter(tze = self.tze, status = True)
		burdel_history.water_cars = WaterCar.objects.filter(tze = self.tze, status = True)
		burdel_history.bohir_cars = BohirCar.objects.filter(tze = self.tze, status = True)
		burdel_history.norm_standarts = NormStandart.objects.filter(tze=self.tze, status=True)
		burdel_history.huuli_durems = Baig_huuli_durem.objects.filter(tze=self.tze, status=True)
		burdel_history.mashin_tonog_tohooromjs = Equipment.objects.filter(tze=self.tze, status=True)





class Burdel_history(models.Model):

	huselt_angilal = models.CharField(max_length = 128, null=True)

	tz_huselt = models.ForeignKey(TZ_Huselt)
	tz = models.ManyToManyField(TZ)
	tze = models.ForeignKey(TZE) # TZE_history baih yostoi
	materialiud_list = models.ManyToManyField(TZ_mat_status_bind, verbose_name = 'материалуудын жагсаалт:')
	ilgeesen_datetime = models.DateTimeField(null = True, verbose_name = 'Илгээсэн хугацаа:')
	cert = models.ForeignKey(Certificate, null=True, verbose_name=u'Сунгах тусгай зөвшөөрлийн гэрчилгээ', blank=True)

	now_checking = models.BooleanField(default = True)
	tza_check_finished = models.BooleanField(default = False)
	uta_check_finished = models.BooleanField(default = False)
	hzm_check_finished = models.BooleanField(default = False)

	ajiltans = models.ManyToManyField(Ajiltan)
	#zasag_dargiin_todorhoilolts = models.ManyToManyField(ZDTodorhoilolt)
	#hangagch_baigs = models.ManyToManyField(HangagchBaiguullaga)
	#tax_tods = models.ManyToManyField(TaxTodorhoilolt)
	sanhuu_tailans = models.ManyToManyField(SanhuuTailan)
	#audit_dugnelts = models.ManyToManyField(AuditDugnelt)
	oron_toonii_schemas = models.ManyToManyField(OronTooniiSchema)
	norm_standarts = models.ManyToManyField(NormStandart)
	#ulsiin_komis_akts = models.ManyToManyField(UlsiinAkt)
	us_ashiglah_zovshoorols = models.ManyToManyField(UsZuvshuurul)
	#uildver_tech_schemas = models.ManyToManyField(UildverTechnology)
	#mheg_dugnelts = models.ManyToManyField(MergejliinHyanalt)
	#ajliin_bair_dugnelts = models.ManyToManyField(AjliinBair)
	huuli_durems = models.ManyToManyField(Baig_huuli_durem)
	mashin_tonog_tohooromjs = models.ManyToManyField(Equipment)

	hudags = models.ManyToManyField(Hudag)
	usansans = models.ManyToManyField(UsanSan)
	nasosStantss = models.ManyToManyField(NasosStants)
	labs = models.ManyToManyField(Lab)
	shugam_suljees = models.ManyToManyField(Sh_suljee)
	ts_baiguulamjs = models.ManyToManyField(Ts_baiguulamj)
	us_damjuulah_tovs = models.ManyToManyField(UsDamjuulahBair)
	us_tugeeh_bairs = models.ManyToManyField(UsTugeehBair)
	abbs = models.ManyToManyField(ABB)
	water_cars = models.ManyToManyField(WaterCar)
	bohir_cars = models.ManyToManyField(BohirCar)

	us_shinjilgee = models.ForeignKey(TZ_huselt_water_analysis, null=True)
	bohir_shinjilgee = models.ForeignKey(TZ_huselt_bohir_analysis, null=True)



	def is_hurliin_shiidver_oruulah_bolomjtoi(self):
		bolomjtoi = True
		if self.tz_huselt.is_yavts_bichig_barimt_OK() and self.tz_huselt.hurliin_date:
			if timezone.now().date() >= self.tz_huselt.hurliin_date:
				bolomjtoi=True
			else:
				bolomjtoi=False
		else:
			bolomjtoi=False
		return bolomjtoi


	def is_all_zovshoorson(self):
		check = True
		for i in self.materialiud_list.all():
			if i.status != u'Шаардлага хангасан':
				check = False
		return check
	def is_hzm_materialiud_zovshoorson(self):
		check = True
		mat_for_ajiltan = TZ_material.objects.filter(material_angilal = 3)
		for i in self.materialiud_list.filter(material = mat_for_ajiltan):
			if i.status != u'Шаардлага хангасан':
				check = False
		return check
	def is_tza_materialiud_zovshoorson(self):
		check = True
		mat_for_ajiltan = TZ_material.objects.filter(material_angilal = 1)
		for i in self.materialiud_list.filter(material = mat_for_ajiltan):
			if i.status != u'Шаардлага хангасан':
				check = False
		return check
	def is_uta_materialiud_zovshoorson(self):
		check = True
		mat_for_ajiltan = TZ_material.objects.filter(material_angilal = 2)
		for i in self.materialiud_list.filter(material = mat_for_ajiltan):
			if i.status != u'Шаардлага хангасан':
				check = False
		return check
	def is_hzm_checked_all_material(self):
		check = True
		mat_for_ajiltan = TZ_material.objects.filter(material_angilal = 3)
		for i in self.materialiud_list.filter(material = mat_for_ajiltan):
			if i.status == u'Шаардлага хангасан' or i.status == u'Шаардлага хангаагүй':
				pass
			else:
				check = False
		return check
	def is_tza_checked_all_material(self):
		check = True
		mat_for_ajiltan = TZ_material.objects.filter(material_angilal = 1)
		for i in self.materialiud_list.filter(material = mat_for_ajiltan):
			if i.status == u'Шаардлага хангасан' or i.status == u'Шаардлага хангаагүй':
				pass
			else:
				check = False
		return check
	def is_uta_checked_all_material(self):
		check = True
		mat_for_ajiltan = TZ_material.objects.filter(material_angilal = 2)
		for i in self.materialiud_list.filter(material = mat_for_ajiltan):
			if i.status == u'Шаардлага хангасан' or i.status == u'Шаардлага хангаагүй':
				pass
			else:
				check = False
		return check
	def materialiud_of_hzm(self):
		mats = TZ_material.objects.filter(material_angilal = 3)
		queryset = self.materialiud_list.filter(material = mats)
		return queryset
	def materialiud_of_uta(self):
		mats = TZ_material.objects.filter(material_angilal = 2)
		queryset = self.materialiud_list.filter(material = mats)
		return queryset
	def materialiud_of_tza(self):
		mats = TZ_material.objects.filter(material_angilal = 1)
		queryset = self.materialiud_list.filter(material = mats)
		return queryset



########## uilsee nemsen end ##############



class UATailan_Gunii_Hudag(Create):
	tze = models.ForeignKey(TZE, verbose_name = 'Тусгай зөвшөөрөл эзэмшигч:')
	hudags = models.ManyToManyField(Hudag, verbose_name = 'Гүний худгууд:')
	tailan_date = models.DateField(verbose_name = 'Тайлангийн огноо:')
	def get_tailan_objects(self):
		objects = Hudag.objects.filter(tze = self.tze, status = True)
		for h in objects:
			self.hudags.add(h)
class UATailan_Tsevershuuleh(Create):
	tze = models.ForeignKey(TZE, verbose_name = 'Тусгай зөвшөөрөл эзэмшигч:')
	tsevershuuleh = models.ManyToManyField(Ts_baiguulamj, verbose_name = 'Цэвэршүүлэх байгууламж:')
	tailan_date = models.DateField(verbose_name = 'Тайлангийн огноо:')
	def get_tailan_objects(self):
		objects = Ts_baiguulamj.objects.filter(tze = self.tze, status = True, torol = u'Цэвэр усны')
		for h in objects:
			self.tsevershuuleh.add(h)
class UATailan_Tseverleh(Create):
	tze = models.ForeignKey(TZE, verbose_name = 'Тусгай зөвшөөрөл эзэмшигч:')
	tseverleh = models.ManyToManyField(Ts_baiguulamj, verbose_name = 'Цэвэрлэх байгууламж:')
	tailan_date = models.DateField(verbose_name = 'Тайлангийн огноо:')
	def get_tailan_objects(self):
		objects = Ts_baiguulamj.objects.filter(tze = self.tze, status = True, torol=u'Бохир усны')
		for h in objects:
			self.tseverleh.add(h)
class UATailan_UsanSan(Create):
	tze = models.ForeignKey(TZE, verbose_name = 'Тусгай зөвшөөрөл эзэмшигч:')
	usan_sans = models.ManyToManyField(UsanSan, verbose_name = 'Усан сан:')
	tailan_date = models.DateField(verbose_name = 'Тайлангийн огноо:')
	def get_tailan_objects(self):
		objects = UsanSan.objects.filter(tze = self.tze, status = True)
		for h in objects:
			self.usan_sans.add(h)
class UATailan_Tsever_Nasos_stants(Create):
	tze = models.ForeignKey(TZE, verbose_name = 'Тусгай зөвшөөрөл эзэмшигч:')
	nasos_stantss = models.ManyToManyField(NasosStants, verbose_name = 'Насос станц:')
	tailan_date = models.DateField(verbose_name = 'Тайлангийн огноо:')
	def get_tailan_objects(self):
		objects = NasosStants.objects.filter(tze = self.tze, status = True, nasos_torol = u'Цэвэр усны насос станц')
		for h in objects:
			self.nasos_stantss.add(h)
class UATailan_Bohir_Nasos_stants(Create):
	tze = models.ForeignKey(TZE, verbose_name = 'Тусгай зөвшөөрөл эзэмшигч:')
	nasos_stantss = models.ManyToManyField(NasosStants, verbose_name = 'Насос станц:')
	tailan_date = models.DateField(verbose_name = 'Тайлангийн огноо:')
	def get_tailan_objects(self):
		objects = NasosStants.objects.filter(tze = self.tze, status = True, nasos_torol = u'Бохир усны насос станц')
		for h in objects:
			self.nasos_stantss.add(h)
class UATailan_Lab(Create):
	tze = models.ForeignKey(TZE, verbose_name = 'Тусгай зөвшөөрөл эзэмшигч:')
	labs = models.ManyToManyField(Lab, verbose_name = 'Лаборатори:')
	tailan_date = models.DateField(verbose_name = 'Тайлангийн огноо:')
	def get_tailan_objects(self):
		objects = Lab.objects.filter(tze = self.tze, status = True)
		for h in objects:
			self.labs.add(h)
class UATailan_tsever_usnii_shugam(Create):
	tze = models.ForeignKey(TZE, verbose_name = 'Тусгай зөвшөөрөл эзэмшигч:')
	sh_suljees = models.ManyToManyField(Sh_suljee, verbose_name = 'Цэвэр усны шугам сүлжээ:')
	tailan_date = models.DateField(verbose_name = 'Тайлангийн огноо:')
	def get_tailan_objects(self):
		objects = Sh_suljee.objects.filter(tze = self.tze, status = True, shugam_helber = u'Цэвэр усны шугам сүлжээ')
		for h in objects:
			self.sh_suljees.add(h)
class UATailan_bohir_usnii_shugam(Create):
	tze = models.ForeignKey(TZE, verbose_name = 'Тусгай зөвшөөрөл эзэмшигч:')
	sh_suljees = models.ManyToManyField(Sh_suljee, verbose_name = 'Бохир усны шугам сүлжээ:')
	tailan_date = models.DateField(verbose_name = 'Тайлангийн огноо:')
	def get_tailan_objects(self):
		objects = Sh_suljee.objects.filter(tze = self.tze, status = True, shugam_helber = u'Бохир усны шугам сүлжээ')
		for h in objects:
			self.sh_suljees.add(h)
class UATailan_ABB(Create):
	tze = models.ForeignKey(TZE, verbose_name = 'Тусгай зөвшөөрөл эзэмшигч:')
	abbs = models.ManyToManyField(ABB, verbose_name = 'Ашиглалтыг хариуцаж буй барилга байгууламж, орон сууц:')
	tailan_date = models.DateField(verbose_name = 'Тайлангийн огноо:')
	def get_tailan_objects(self):
		objects = ABB.objects.filter(tze = self.tze, status = True)
		for h in objects:
			self.abbs.add(h)
class UATailan_UsTugeeh(Create):
	tze = models.ForeignKey(TZE, verbose_name = 'Тусгай зөвшөөрөл эзэмшигч:')
	us_tugeeh_bairs = models.ManyToManyField(UsTugeehBair, verbose_name = 'Ус түгээх байр:')
	tailan_date = models.DateField(verbose_name = 'Тайлангийн огноо:')
	def get_tailan_objects(self):
		objects = UsTugeehBair.objects.filter(tze = self.tze, status = True)
		for h in objects:
			self.us_tugeeh_bairs.add(h)
class UATailan_WaterCar(Create):
	tze = models.ForeignKey(TZE, verbose_name = 'Тусгай зөвшөөрөл эзэмшигч:')
	water_cars = models.ManyToManyField(WaterCar, verbose_name = 'Цэвэр ус зөөвөрлөх автомашин:')
	tailan_date = models.DateField(verbose_name = 'Тайлангийн огноо:')
	def get_tailan_objects(self):
		objects = WaterCar.objects.filter(tze = self.tze, status = True)
		for h in objects:
			self.water_cars.add(h)
class UATailan_BohirCar(Create):
	tze = models.ForeignKey(TZE, verbose_name = 'Тусгай зөвшөөрөл эзэмшигч:')
	bohir_cars = models.ManyToManyField(BohirCar, verbose_name = 'Бохир ус зөөвөрлөх автомашин:')
	tailan_date = models.DateField(verbose_name = 'Тайлангийн огноо:')
	def get_tailan_objects(self):
		objects = BohirCar.objects.filter(tze = self.tze, status = True)
		for h in objects:
			self.bohir_cars.add(h)
class UATailan_ajiltan(Create):
	tze = models.ForeignKey(TZE, verbose_name = 'Тусгай зөвшөөрөл эзэмшигч:')
	ajiltans = models.ManyToManyField(Ajiltan, verbose_name = 'Ажилтан:')
	tailan_date = models.DateField(verbose_name = 'Тайлангийн огноо:')
	def get_tailan_objects(self):
		objects = Ajiltan.objects.filter(baiguullaga = self.tze, status = True)
		for h in objects:
			self.ajiltans.add(h)
class UATailan_UsDamjuulah_tov(Create):
	tze = models.ForeignKey(TZE, verbose_name = 'Тусгай зөвшөөрөл эзэмшигч:')
	usDamjuulahBair = models.ManyToManyField(UsDamjuulahBair, verbose_name = 'Ус, дулаан дамжуулах төв:')
	tailan_date = models.DateField(verbose_name = 'Тайлангийн огноо:')
	def get_tailan_objects(self):
		objects = UsDamjuulahBair.objects.filter(tze = self.tze, status = True)
		for h in objects:
			self.usDamjuulahBair.add(h)

class UATailan(Create):
	tze = models.ForeignKey(TZE, verbose_name = u'Тусгай зөвшөөрөл эзэмшигч:')
	certificates = models.ManyToManyField(Certificate, verbose_name = u'Тусгай зөвшөөрлийн гэрчилгээнүүд:')
	tailan_date = models.DateTimeField(verbose_name=u'Тайлангийн огноо:')
	gunii_hudags = models.OneToOneField(UATailan_Gunii_Hudag, null=True)
	tsevershuuleh = models.OneToOneField(UATailan_Tsevershuuleh, null = True)
	tseverleh = models.OneToOneField(UATailan_Tseverleh, null = True)
	usansan = models.OneToOneField(UATailan_UsanSan, null = True)
	tsever_nasos_stants = models.OneToOneField(UATailan_Tsever_Nasos_stants, null = True)
	bohir_nasos_stants = models.OneToOneField(UATailan_Bohir_Nasos_stants, null = True)
	lab = models.OneToOneField(UATailan_Lab, null = True)
	tsever_usnii_shugam = models.OneToOneField(UATailan_tsever_usnii_shugam, null = True)
	bohir_usnii_shugam = models.OneToOneField(UATailan_bohir_usnii_shugam, null = True)
	abb = models.OneToOneField(UATailan_ABB, null = True)
	us_damjuulah_tov = models.OneToOneField(UATailan_UsDamjuulah_tov, null=True)
	us_tugeeh = models.OneToOneField(UATailan_UsTugeeh, null = True)
	water_car = models.OneToOneField(UATailan_WaterCar, null = True)
	bohir_car = models.OneToOneField(UATailan_BohirCar, null = True)
	ajiltans = models.OneToOneField(UATailan_ajiltan, null = True)
	def generate_tailans(self):
		tailan_names = self.tze.get_tailan_names()

		#print tailan_names
		for i in tailan_names:
			if i.material_number == 1:
				self.gunii_hudags = UATailan_Gunii_Hudag.objects.create(tze = self.tze, tailan_date = self.tailan_date)
				self.gunii_hudags.get_tailan_objects()
			if i.material_number == 2:
				self.tsevershuuleh = UATailan_Tsevershuuleh.objects.create(tze = self.tze, tailan_date = self.tailan_date)
				self.tsevershuuleh.get_tailan_objects()
			if i.material_number == 3:
				self.usansan  = UATailan_UsanSan.objects.create(tze = self.tze, tailan_date = self.tailan_date)
				self.usansan.get_tailan_objects()
			if i.material_number == 4:
				self.tsever_nasos_stants  = UATailan_Tsever_Nasos_stants.objects.create(tze = self.tze, tailan_date = self.tailan_date)
				self.tsever_nasos_stants.get_tailan_objects()
			if i.material_number == 5:
				self.lab  = UATailan_Lab.objects.create(tze = self.tze, tailan_date = self.tailan_date)
				self.lab.get_tailan_objects()
			if i.material_number == 6:
				self.tsever_usnii_shugam  = UATailan_tsever_usnii_shugam.objects.create(tze = self.tze, tailan_date = self.tailan_date)
				self.tsever_usnii_shugam.get_tailan_objects()
			if i.material_number == 7:
				self.abb  = UATailan_ABB.objects.create(tze = self.tze, tailan_date = self.tailan_date)
				self.abb.get_tailan_objects()
			if i.material_number == 8:
				self.us_damjuulah_tov  = UATailan_UsDamjuulah_tov.objects.create(tze = self.tze, tailan_date = self.tailan_date)
				self.us_damjuulah_tov.get_tailan_objects()
			if i.material_number == 9:
				self.bohir_usnii_shugam  = UATailan_bohir_usnii_shugam.objects.create(tze = self.tze, tailan_date = self.tailan_date)
				self.bohir_usnii_shugam.get_tailan_objects()
			if i.material_number == 10:
				self.tseverleh  = UATailan_Tseverleh.objects.create(tze = self.tze, tailan_date = self.tailan_date)
				self.tseverleh.get_tailan_objects()
			if i.material_number == 11:
				self.bohir_nasos_stants  = UATailan_Bohir_Nasos_stants.objects.create(tze = self.tze, tailan_date = self.tailan_date)
				self.bohir_nasos_stants.get_tailan_objects()
			if i.material_number == 12:
				self.us_tugeeh  = UATailan_UsTugeeh.objects.create(tze = self.tze, tailan_date = self.tailan_date)
				self.us_tugeeh.get_tailan_objects()
			if i.material_number == 13:
				self.water_car  = UATailan_WaterCar.objects.create(tze = self.tze, tailan_date = self.tailan_date)
				self.water_car.get_tailan_objects()
			if i.material_number == 14:
				self.bohir_car  = UATailan_BohirCar.objects.create(tze = self.tze, tailan_date = self.tailan_date)
				self.bohir_car.get_tailan_objects()
			if i.material_number == 15:
				self.ajiltans  = UATailan_ajiltan.objects.create(tze = self.tze, tailan_date = self.tailan_date)
				self.ajiltans.get_tailan_objects()

		# tailan_names - ees hamaarch tailanguudaa generate hiine
		#
		self.save()

		cert_querysets = self.tze.get_huchintei_certificates()
		for i in cert_querysets:
			self.certificates.add(i)

	def __unicode__(self):
		return "%s | %s" %(unicode(self.tze.org_name), self.tailan_date)


	@classmethod
	def export_to_excel(self, workbook, tailan_queryset):
		""" object-iin queryset-iig avna. Tuhain queryset-iin date_time uy deh data-g excel export hiine """
		# workbook argumentdaa avna
		if tailan_queryset:
			#[row_write, col_write] = self.excel_write_header_and_format(worksheet, row_start, col_start)
			
			worksheet = workbook.add_worksheet(u'Гүний худаг')
			queryset = Hudag.objects.none()
			row_write = 5
			col_write = 1
			[row_write, col_write] = Hudag.excel_write_header_and_format(worksheet = worksheet, row_start = row_write, col_start = col_write)
			for tailan in tailan_queryset:
				if tailan.gunii_hudags:
					queryset = tailan.gunii_hudags.hudags.all()
					[row_write, col_write] = Hudag.export_to_excel_without_header(worksheet = worksheet, row_start=row_write, col_start=col_write, queryset = queryset, date_time = tailan.tailan_date)


			worksheet = workbook.add_worksheet(u'Цэвэршүүлэх байгууламж')
			queryset = Ts_baiguulamj.objects.none()
			row_write = 5
			col_write = 1
			[row_write, col_write] = Ts_baiguulamj.excel_write_header_and_format(worksheet = worksheet, row_start = row_write, col_start = col_write)
			for tailan in tailan_queryset:
				if tailan.tsevershuuleh:
					queryset = tailan.tsevershuuleh.tsevershuuleh.all()
					[row_write, col_write] = Ts_baiguulamj.export_to_excel_without_header(worksheet = worksheet, row_start=row_write, col_start=col_write, queryset = queryset, date_time = tailan.tailan_date)
			

			worksheet = workbook.add_worksheet(u'Цэвэрлэх байгууламж')
			queryset = Ts_baiguulamj.objects.none()
			row_write = 5
			col_write = 1
			[row_write, col_write] = Ts_baiguulamj.excel_write_header_and_format(worksheet = worksheet, row_start = row_write, col_start = col_write)
			for tailan in tailan_queryset:
				if tailan.tseverleh:
					queryset = tailan.tseverleh.tseverleh.all()
					[row_write, col_write] = Ts_baiguulamj.export_to_excel_without_header(worksheet = worksheet, row_start=row_write, col_start=col_write, queryset = queryset, date_time = tailan.tailan_date)
			

			worksheet = workbook.add_worksheet(u'Усан сан')
			queryset = UsanSan.objects.none()
			row_write = 5
			col_write = 1
			[row_write, col_write] = UsanSan.excel_write_header_and_format(worksheet = worksheet, row_start = row_write, col_start = col_write)
			for tailan in tailan_queryset:
				if tailan.usansan:
					queryset = tailan.usansan.usan_sans.all()
					[row_write, col_write] = UsanSan.export_to_excel_without_header(worksheet = worksheet, row_start=row_write, col_start=col_write, queryset = queryset, date_time = tailan.tailan_date)
			

			worksheet = workbook.add_worksheet(u'Цэвэр усны насос станц')
			queryset = NasosStants.objects.none()
			row_write = 5
			col_write = 1
			[row_write, col_write] = NasosStants.excel_write_header_and_format(worksheet = worksheet, row_start = row_write, col_start = col_write)
			for tailan in tailan_queryset:
				if tailan.tsever_nasos_stants:
					queryset = tailan.tsever_nasos_stants.nasos_stantss.all()
					[row_write, col_write] = NasosStants.export_to_excel_without_header(worksheet = worksheet, row_start=row_write, col_start=col_write, queryset = queryset, date_time = tailan.tailan_date)
			

			worksheet = workbook.add_worksheet(u'Бохир усны насос станц')
			queryset = NasosStants.objects.none()
			row_write = 5
			col_write = 1
			[row_write, col_write] = NasosStants.excel_write_header_and_format(worksheet = worksheet, row_start = row_write, col_start = col_write)
			for tailan in tailan_queryset:
				if tailan.bohir_nasos_stants:
					queryset = tailan.bohir_nasos_stants.nasos_stantss.all()
					[row_write, col_write] = NasosStants.export_to_excel_without_header(worksheet = worksheet, row_start=row_write, col_start=col_write, queryset = queryset, date_time = tailan.tailan_date)

			worksheet = workbook.add_worksheet(u'Лаборатори')
			queryset = Lab.objects.none()
			row_write = 5
			col_write = 1
			[row_write, col_write] = Lab.excel_write_header_and_format(worksheet = worksheet, row_start = row_write, col_start = col_write)
			for tailan in tailan_queryset:
				if tailan.lab:
					queryset = tailan.lab.labs.all()
					[row_write, col_write] = Lab.export_to_excel_without_header(worksheet = worksheet, row_start=row_write, col_start=col_write, queryset = queryset, date_time = tailan.tailan_date)

			worksheet = workbook.add_worksheet(u'Цэвэр усны шугам')
			queryset = Sh_suljee.objects.none()
			row_write = 5
			col_write = 1
			[row_write, col_write] = Sh_suljee.excel_write_header_and_format(worksheet = worksheet, row_start = row_write, col_start = col_write)
			for tailan in tailan_queryset:
				if tailan.tsever_usnii_shugam:
					queryset = tailan.tsever_usnii_shugam.sh_suljees.all()
					[row_write, col_write] = Sh_suljee.export_to_excel_without_header(worksheet = worksheet, row_start=row_write, col_start=col_write, queryset = queryset, date_time = tailan.tailan_date)

			worksheet = workbook.add_worksheet(u'Бохир усны шугам')
			queryset = Sh_suljee.objects.none()
			row_write = 5
			col_write = 1
			[row_write, col_write] = Sh_suljee.excel_write_header_and_format(worksheet = worksheet, row_start = row_write, col_start = col_write)
			for tailan in tailan_queryset:
				if tailan.bohir_usnii_shugam:
					queryset = tailan.bohir_usnii_shugam.sh_suljees.all()
					[row_write, col_write] = Sh_suljee.export_to_excel_without_header(worksheet = worksheet, row_start=row_write, col_start=col_write, queryset = queryset, date_time = tailan.tailan_date)

			worksheet = workbook.add_worksheet(u'АХББ')
			queryset = ABB.objects.none()
			row_write = 5
			col_write = 1
			[row_write, col_write] = ABB.excel_write_header_and_format(worksheet = worksheet, row_start = row_write, col_start = col_write)
			for tailan in tailan_queryset:
				if tailan.abb:
					queryset = tailan.abb.abbs.all()
					[row_write, col_write] = ABB.export_to_excel_without_header(worksheet = worksheet, row_start=row_write, col_start=col_write, queryset = queryset, date_time = tailan.tailan_date)

			worksheet = workbook.add_worksheet(u'Ус, дулаан дамжуулах төв')
			queryset = UsDamjuulahBair.objects.none()
			row_write = 5
			col_write = 1
			[row_write, col_write] = UsDamjuulahBair.excel_write_header_and_format(worksheet = worksheet, row_start = row_write, col_start = col_write)
			for tailan in tailan_queryset:
				if tailan.us_damjuulah_tov:
					queryset = tailan.us_damjuulah_tov.usDamjuulahBair.all()
					[row_write, col_write] = UsDamjuulahBair.export_to_excel_without_header(worksheet = worksheet, row_start=row_write, col_start=col_write, queryset = queryset, date_time = tailan.tailan_date)

			worksheet = workbook.add_worksheet(u'Ус түгээх байр')
			queryset = UsTugeehBair.objects.none()
			row_write = 5
			col_write = 1
			[row_write, col_write] = UsTugeehBair.excel_write_header_and_format(worksheet = worksheet, row_start = row_write, col_start = col_write)
			for tailan in tailan_queryset:
				if tailan.us_tugeeh:
					queryset = tailan.us_tugeeh.us_tugeeh_bairs.all()
					[row_write, col_write] = UsTugeehBair.export_to_excel_without_header(worksheet = worksheet, row_start=row_write, col_start=col_write, queryset = queryset, date_time = tailan.tailan_date)

			worksheet = workbook.add_worksheet(u'Цэвэр усны машин')
			queryset = WaterCar.objects.none()
			row_write = 5
			col_write = 1
			[row_write, col_write] = WaterCar.excel_write_header_and_format(worksheet = worksheet, row_start = row_write, col_start = col_write)
			for tailan in tailan_queryset:
				if tailan.water_car:
					queryset = tailan.water_car.water_cars.all()
					[row_write, col_write] = WaterCar.export_to_excel_without_header(worksheet = worksheet, row_start=row_write, col_start=col_write, queryset = queryset, date_time = tailan.tailan_date)

			worksheet = workbook.add_worksheet(u'Бохир усны машин')
			queryset = BohirCar.objects.none()
			row_write = 5
			col_write = 1
			[row_write, col_write] = BohirCar.excel_write_header_and_format(worksheet = worksheet, row_start = row_write, col_start = col_write)
			for tailan in tailan_queryset:
				if tailan.bohir_car:
					queryset = tailan.bohir_car.bohir_cars.all()
					[row_write, col_write] = BohirCar.export_to_excel_without_header(worksheet = worksheet, row_start=row_write, col_start=col_write, queryset = queryset, date_time = tailan.tailan_date)

			worksheet = workbook.add_worksheet(u'Ажилчдын судалгаа')
			row_write = 5
			col_write = 1
			[row_write, col_write] = Ajiltan.excel_write_header_and_format(worksheet = worksheet, row_start = row_write, col_start = col_write)
			for tailan in tailan_queryset:
				if tailan.ajiltans:
					queryset = tailan.ajiltans.ajiltans.all()
					[row_write, col_write] = Ajiltan.export_to_excel_without_header(worksheet = worksheet, row_start=row_write, col_start=col_write, queryset = queryset, date_time = tailan.tailan_date)
				
		else:
			worksheet.write_string(row_start, col_start, u'Мэдээлэл байхгүй')




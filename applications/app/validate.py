#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from django import forms as f
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core import validators as v
from django.db.models import FileField
from django.template.defaultfilters import filesizeformat

def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.JPG', '.png', '.PNG', '.jpeg', '.JPEG', '.gif', '.GIF', '.xlsx', '.xls']
    if not ext in valid_extensions:
        raise ValidationError(u'Та pdf, doc, jpg, jpeg, png, gif, xls өргөтгөлтэй файл сонгоно уу.')

def validate_diplom_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    print ext
    valid_extensions = ['.pdf','.jpg', '.JPG', '.png', '.PNG', '.jpeg', '.JPEG']
    if not ext in valid_extensions:
        raise ValidationError(u'Та pdf, jpg, jpeg, png өргөтгөлтэй файл сонгоно уу.')
def validate_pdf_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    print ext
    valid_extensions = ['.pdf']
    if not ext in valid_extensions:
        raise ValidationError(u'Та .pdf өргөтгөлтэй файл сонгоно уу.')

def validate_picture_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = [ '.jpg', '.JPG', '.png', '.PNG', '.jpeg', '.JPEG', '.gif', '.GIF']
    if not ext in valid_extensions:
        raise ValidationError(u'Та  jpg, jpeg, png, gif өргөтгөлтэй зурган файл сонгоно уу.')

def validate_file_size(value):        
    file1 = value.file
    try:
        if file1._size > 5242880:
            raise ValidationError(_('Файлын хэмжээ %s -аас их байна. (%s)') % (filesizeformat(5242880), filesizeformat(file1._size)))
    except AttributeError:
        pass        

    return file1
def validate_phone(value):
	p = re.compile(ur'^[0-9]{8,11}$')
	if not re.match(p, value):
		raise f.ValidationError(u'"%s" Утасны дугаар буруу байна!' % value)

def validate_year(value):
    p = re.compile(ur'^(19|2[0-1])\d{2}$')
    if not re.match(p, value):
        raise f.ValidationError(u'он оруулна уу!')

def Validate(value):
	p = re.compile(ur'^[0-9]{7}$')
	if not re.match(p, value):
		raise ValidationError(u'7 оронтой тоо оруулна уу')
def validation_nine(value):
	p = re.compile(ur'^[0-9]{9}$')
	if not re.match(p, value):
		raise ValidationError(u'9 оронтой тоо оруулна уу')

def clean_reg(value):
	p = re.compile(ur'^[\u0410-\u044F\u0401\u0451\u04E8\u04E9\u04AE\u04AF]{2}[0-9]{2}(0[0-9]|1[012])(0[1-9]|1[0-9]|2[0-9]|3[01])[0-9]{2}$')
	if not p.match(value):
		raise ValidationError(u'Регистрийн дугаар буруу байна!')

def kirill(value):
	p = re.compile(ur'[\u0410-\u044F\u0401\u0451\u04E8\u04E9\u04AE\u04AF]')
	if not p.match(value):
		raise ValidationError(u'Та кирилл үсгийн фонтоор бичнэ үү!')

f.Field.default_error_messages = {
    'required': _(u"Энэ талбарыг бөглөнө үү."),
}

v.MaxLengthValidator.message = _('%(limit_value)d тоо оруулна (%(show_value)d байна).')

f.ModelChoiceField.default_error_messages = {
    'invalid_choice' : _(u'Буруу сонголт байна')
}
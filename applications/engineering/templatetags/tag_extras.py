from django.template.defaulttags import register
''' engineering extras '''
''' uilsee nemev start'''
@register.filter
def get_item(dictionary, key):	# templates dotor dictionary-giin value - d key -eer handahad ashiglaj baigaa
    return dictionary.get(key)

@register.filter
def get_item_tz_all(dictionary, key):
	return dictionary.get(key).tz.all()

@register.filter
def get_item_tz_some(dictionary, key):
	return dictionary.get(key).tz.all()[:3]

@register.filter
def get_item_material_all(dictionary, key):
	return dictionary.get(key).materialiud_list.tz_materialiud.all()
''' uilsee nemev end'''

@register.filter
def get_item_burdeliin_ajilchid(dictionary, key):
	return dictionary.get(key).ajiltans.all()

@register.filter
def get_item_burdeliin_zasag_tods(dictionary, key):
	return dictionary.get(key).zasag_dargiin_todorhoilolts.all()

@register.filter
def get_item_burdeliin_hangagch_baigs(dictionary, key):
	return dictionary.get(key).hangagch_baigs.all()

@register.filter
def get_item_burdeliin_tax_tods(dictionary, key):
	return dictionary.get(key).tax_tods.all()

@register.filter
def get_item_burdeliin_sanhuu_tailans(dictionary, key):
	return dictionary.get(key).sanhuu_tailans.all()

@register.filter
def get_item_burdeliin_audit_dugnelts(dictionary, key):
	return dictionary.get(key).audit_dugnelts.all()

@register.filter
def get_item_burdeliin_oron_toonii_schemas(dictionary, key):
	return dictionary.get(key).oron_toonii_schemas.all()

@register.filter
def get_item_burdeliin_norm_standarts(dictionary, key):
	return dictionary.get(key).norm_standarts.all()

@register.filter
def get_item_burdeliin_ulsiin_komis_akts(dictionary, key):
	return dictionary.get(key).ulsiin_komis_akts.all()

@register.filter
def get_item_burdeliin_us_ashiglah_zovshoorols(dictionary, key):
	return dictionary.get(key).us_ashiglah_zovshoorols.all()

@register.filter
def get_item_burdeliin_uildver_tech_schemas(dictionary, key):
	return dictionary.get(key).uildver_tech_schemas.all()

@register.filter
def get_item_burdeliin_mheg_dugnelts(dictionary, key):
	return dictionary.get(key).mheg_dugnelts.all()

@register.filter
def get_item_burdeliin_ajliin_bair_dugnelts(dictionary, key):
	return dictionary.get(key).ajliin_bair_dugnelts.all()

@register.filter
def get_item_burdeliin_mashin_tonog_tohooromjs(dictionary, key):
	return dictionary.get(key).mashin_tonog_tohooromjs.all()


from django.template.defaulttags import register

@register.simple_tag()
def huvaah_12(value):
	#return value
	return float("{0:.3f}".format(value / 12))
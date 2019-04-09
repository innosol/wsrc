# -*- coding: utf-8 -*-
import django_filters
from applications.app.models import TZ_Huselt, UAT_yavts

class TZ_tze_Huselt_filter(django_filters.FilterSet):
	class Meta:
		model = TZ_Huselt
		fields = ['yavts']

	def __init__(self, *args, **kwargs):
		super(TZ_tze_Huselt_filter, self).__init__(*args, **kwargs)
		self.filters['yavts'].extra.update({'empty_label': 'бүгд', 'help_text': '',})
		self.filters['yavts'].label = 'Хүсэлтийн явц'
		
class UAT_yavts_ognoo_filter(django_filters.FilterSet):
	on = django_filters.RangeFilter()
	class Meta:
		model = UAT_yavts
		fields = ['on']

	def __init__(self, *args, **kwargs):
		super(UAT_yavts_ognoo_filter, self).__init__(*args, **kwargs)
		self.filters['on'].label = 'Хугацааны интервал'
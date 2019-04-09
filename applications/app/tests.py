from django.test import TestCase
from .models import *
# Create your tests here.

class BaiguullagaTest(TestCase):

	def btest(self):
		b = Baiguullaga.objects.all()
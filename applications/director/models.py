# coding:utf-8
from django.db import models
from applications.app.models import Create, TZE

yvts_choice = (
	(u'Буцаасан',u'Буцаасан'),
	(u'Хадгалсан',u'Хадгалсан'),
	(u'Илгээсэн',u'Илгээсэн'),
	(u'Хийгдэж байна', u'Хийгдэж байна'),
	(u'Хүлээн авсан', u'Хүлээн авсан')
	)


ded_angilal = (
	('0',u'Дулааны хэсэг өөрийн'),
	('1',u'ААНБайгууллага'),
	('2',u'Спирт, архи, пиво, усны үйлдвэр, машин угаалга'),
	('3',u'Ноос ноолуур, арьс шир, өлөн гэдэс боловсруулах үйлдвэр'),
	('4',u'ААНБ-Зөөврөөр'),
	('5',u'Айл өрх/тоолууртай/'),
	('6',u'Айл өрх/тоолуургүй/'),
	('7',u'Ус түгээх байраар-УТБ'),
	('8', u'Ахуйн хэрэглэгч зөөврөөр'),
	('9',u'15'),
	('10',u'20'),
	('11',u'25'),
	('12',u'32'),
	('13',u'40'),
	('14',u'50'),
	('15',u'65'),
	('16',u'80'),
	('17',u'100'),
	('18',u'125'),
	('19',u'150'),
	('20',u'200'),
	('21',u'250'),
	('22',u'300'),
	('23',u'400-с дээш'),
	)

angilal_choice = (
	(u'0', u'Цэвэр'),
	(u'1', u'Бохир'),
	(u'2', u'Суурь'),
	(u'3', u'Дулаан'),
	(u'4', u'Цахилгаан'),
	)

tz_uil_ajillagaanii_angilal = (
	('0', u'Төвлөрсөн шугамын-Цэвэр ус'),
	('1', u'Төвлөрсөн шугамын-Бохир ус'),
	('2', u'Зөөвөр-УТБ'),
	('3', u'Бусад (Бохир өргөх насос, г,м)'),
	('4', u'Цахилгаан'),
	('5', u'Дулаан'),
	('6', u'Бусад'),
	)

class Tariff(models.Model):
	angilal = models.CharField(max_length = 250, choices = angilal_choice)
	name = models.CharField(max_length = 250, choices = ded_angilal)
	une = models.FloatField()

	def __unicode__(self):
		return u"%s | %s | %s" %(unicode(self.id), unicode(self.angilal), unicode(self.name))

class TariffAll(Create):
	songolt = (
		('0', u'Усны үйлчилгээний тариф'),
		('1', u'Голчийн тариф'),
		)
	tze = models.ForeignKey(TZE)
	name = models.CharField(choices = songolt, max_length=10)
	tariff = models.ManyToManyField(Tariff)
	suuri_une = models.FloatField(null = True)

	class Meta:
		ordering = ['id']

	def __unicode__(self):
		return unicode(self.name)

class Hereglegch(models.Model):
	angilal = models.CharField(max_length = 250, choices = angilal_choice)
	name = models.CharField(max_length = 250, choices = ded_angilal)
	htoo = models.IntegerField()

	def __unicode__(self):
		return "%s | %s" %(unicode(self.angilal), unicode(self.name))

class HereglegchAll(Create):
	tze = models.ForeignKey(TZE)
	hereglegch = models.ManyToManyField(Hereglegch)

	class Meta:
		ordering = ['id']

	def aanb_tsever_count(self):
		count = 0
		count = self.hereglegch.all()[0].htoo + self.hereglegch.all()[2].htoo + self.hereglegch.all()[4].htoo \
		+ self.hereglegch.all()[6].htoo + self.hereglegch.all()[8].htoo
		return count

	def aanb_bohir_count(self):
		count = 0
		count = self.hereglegch.all()[1].htoo + self.hereglegch.all()[3].htoo + self.hereglegch.all()[5].htoo \
		+ self.hereglegch.all()[7].htoo + self.hereglegch.all()[9].htoo
		return count

	def utb_zoovor_tsever_count(self):
		count = 0
		count = self.hereglegch.all()[14].htoo + self.hereglegch.all()[16].htoo
		return count

	def utb_zoovor_bohir_count(self):
		count = 0
		count = self.hereglegch.all()[15].htoo + self.hereglegch.all()[17].htoo
		return count

	def ahuin_tsever_count(self):
		count = 0
		count = self.hereglegch.all()[10].htoo + self.hereglegch.all()[12].htoo + self.utb_zoovor_tsever_count()
		return count

	def ahuin_bohir_count(self):
		count = 0
		count = self.hereglegch.all()[11].htoo + self.hereglegch.all()[13].htoo + self.utb_zoovor_bohir_count()
		return count

	def niit_tsever_count(self):
		count = 0
		count = self.aanb_tsever_count() + self.ahuin_tsever_count()
		return count
	
	def niit_bohir_count(self):
		count = 0
		count = self.aanb_bohir_count() + self.ahuin_bohir_count()
		return count


	def __unicode__(self):
		return unicode(self.tze)

class SanalGomdol(models.Model):
	songolt = (
		(0, u'Цэвэр усны тасалдалтай холбоотой'),
		(1, u'Ус хангамжийн чанартай холбоотой'),
		(2, u'Төлбөр тооцоотой холбоотой'),
		(3, u'Дуудлагын засвартай холбоотой'),
		(4, u'Борлуулалтын байцаагч нартай холбоотой'))
	torol = models.CharField(max_length = 50, choices = songolt)
	huleen_avsan = models.IntegerField(verbose_name=u'Хүлээн авсан')
 	shiidverlesen = models.IntegerField(verbose_name=u'Шийдвэрлэсэн')

class SanalGomdolMany(Create):
	tze = models.ForeignKey(TZE)
	sanal_gomdol = models.ManyToManyField(SanalGomdol)
	yvts = models.CharField(max_length = 100, choices = yvts_choice)
	sum0 = models.IntegerField(null = True, blank = True)
	sum1 = models.IntegerField(null = True, blank = True)

	def totals(self):
		count1 = 0
		count2 = 0
		for i in self.sanal_gomdol.all():
			count1 += i.huleen_avsan
			count2 += i.shiidverlesen
		setattr(self, 'sum0', count1)
		setattr(self, 'sum1', count2)
		self.save()

	def __unicode__(self):
		return unicode(self.yvts)

class TehnikNohtsol(models.Model):
	songolt = (
		(0, u'Техникийн нөхцөл хүсч өргөдөл гаргасан иргэд, ААНБ'),
		(1, u'Техникийн нөхцөл олгосон иргэд, ААНБ'),
		(2, u'Техникийн нөхцөл олгоогүй өргөдлийн тоо'))
	torol = models.CharField(max_length = 50, choices = songolt, verbose_name=u'Үзүүлэлт:')
	too = models.IntegerField()
	us= models.FloatField(verbose_name=u'Усны хэрэглээ -м3:')

class TehnikNohtsolMany(Create):
	tze = models.ForeignKey(TZE)
	tehnik_nohtsol = models.ManyToManyField(TehnikNohtsol)
	yvts = models.CharField(max_length = 100, choices = yvts_choice)
	sum0 = models.IntegerField(null = True, blank = True)
	sum1 = models.FloatField(null = True, blank = True)

	def totals(self):
		self.sum0 = self.tehnik_nohtsol.all()[0].too - self.tehnik_nohtsol.all()[1].too
		self.sum1 = self.tehnik_nohtsol.all()[0].us - self.tehnik_nohtsol.all()[1].us
		self.save()

	def __unicode__(self):
		return u"%s | %s" %(self.tze, self.id)

class Tasaldal(models.Model):
	songolt = (
		(0, u'Төлөвлөгөөт тасалдал'),
		(1, u'Хүний буруутай үйл ажиллагаанаас'),
		(2, u'Шугам, тоног төхөөрөмжийн гэмтлээс'),
		(3, u'Бусад тусгай зөвшөөрөл эзэмшигчдийн буруугаас'),
		(4, u'Гуравдагч этгээдийн буруугаас'),
		(5, u'Байгалийн гамшиг/аянга, хүчтэй салхи шуурга, үер/-аас'),
		(6, u'Бусад шалтгаанаар'))
	duration = models.IntegerField(verbose_name=u'Тасалдлын нийт хугацаа:')
	too= models.IntegerField(verbose_name=u'Тасалдалд хамрагдсан нийт хэрэглэгчдийн тоо:')
	torol = models.CharField(max_length = 50, choices = songolt, verbose_name=u'Шалтгаан:')

	def __unicode__(self):
		return unicode(self.torol)

class TasaldalMany(Create):
	tze = models.ForeignKey(TZE)
	tasaldal = models.ManyToManyField(Tasaldal)
	yvts = models.CharField(max_length = 100, choices = yvts_choice)
	sum0 = models.IntegerField(null = True, blank = True)
	sum1 = models.IntegerField(null = True, blank = True)

	def totals(self):
		count1 = 0
		count2 = 0
		for i in self.tasaldal.all():
			count1 += i.duration
			count2 += i.too
		self.sum0 = count1
		self.sum1 = count2
		self.save()

	def __unicode__(self):
		return unicode(self.yvts)

class Olborlolt(Create):
	tze = models.ForeignKey(TZE)
	torol1 = models.BooleanField(verbose_name = u'Өөрөө олборлогч:', default = False)
	torol2 = models.BooleanField(verbose_name = u'Худалдан авагч:', default = False)
	tsever = models.FloatField(null = True, blank = True)
	bohir = models.FloatField( null = True, blank = True)

	class Meta:
		ordering = ['id']

	def __unicode__(self):
		return u"%s | %s" %(self.torol1, self.torol2)

class Buteegdehuun(models.Model):
	name = models.CharField(max_length = 250, choices = ded_angilal)
	angilal = models.CharField(max_length = 250, choices = angilal_choice)
	too = models.FloatField()

	def __unicode__(self):
		return unicode(self.name)
	
class Orlogo(Create):
	olborloson_us = models.FloatField(null = True)
	buteegdehuun = models.ManyToManyField(Buteegdehuun)
	yvts = models.CharField(max_length = 20 ,choices = yvts_choice, verbose_name = 'Явц:', null = True, blank = True)

	def __unicode__(self):
		return unicode(self.yvts)

	def aanb_tsever_count(self):
		count = self.buteegdehuun.all()[2].too + self.buteegdehuun.all()[4].too + self.buteegdehuun.all()[6].too \
		+ self.buteegdehuun.all()[8].too
		return count

	def aanb_bohir_count(self):
		count = self.buteegdehuun.all()[3].too + self.buteegdehuun.all()[5].too + self.buteegdehuun.all()[7].too \
		+ self.buteegdehuun.all()[9].too
		return count

	def utbz_tsever_count(self):
		count = self.buteegdehuun.all()[14].too + self.buteegdehuun.all()[16].too
		return count

	def utbz_bohir_count(self):
		count = self.buteegdehuun.all()[15].too + self.buteegdehuun.all()[17].too
		return count

	def ahuin_tsever_count(self):
		count = self.buteegdehuun.all()[10].too + self.buteegdehuun.all()[12].too + self.utbz_tsever_count()
		return count

	def all_orh_count(self):
		count = self.buteegdehuun.all()[10].too + self.buteegdehuun.all()[12].too
		return count

	def ahuin_bohir_count(self):
		count = self.buteegdehuun.all()[11].too + self.buteegdehuun.all()[13].too + self.utbz_tsever_count()
		return count

	def all_tsever_count(self):
		count = self.aanb_tsever_count() + self.ahuin_tsever_count()
		return count

	def all_bohir_count(self):
		count = self.aanb_bohir_count() + self.ahuin_bohir_count()
		return count

	#def __unicode__(self):
	#	return u'%s | %s' %()

class GolchToo(models.Model):
	songolt = models.CharField(max_length = 10, choices = ded_angilal)
	too = models.IntegerField()

	def __unicode__(self):
		return unicode(self.songolt)

class Golch(Create):
	songolt = (
		('0', u'Цэвэр усны голчийн судалгаа'),
		('1', u'Хангагчаас авсан голчийн судалгаа'),
		)
	tze = models.ForeignKey(TZE)
	name = models.CharField(max_length=10, choices = songolt)
	buteegdehuun = models.ManyToManyField(GolchToo)
	total = models.IntegerField(null = True)

	class Meta:
		ordering = ['id']

	def totals(self):
		sums = 0
		for i in self.buteegdehuun.all():
			sums += i.too
		self.total = sums
		self.save()

	def __unicode__(self):
		return unicode(self.name)

class ZardalUndsen(models.Model):
	torol = models.CharField(max_length = 20, choices = tz_uil_ajillagaanii_angilal)

	class Meta:
		abstract = True

	@classmethod
	def catch(self):
		l = []
		for field in self._meta.fields:
			if isinstance(field, models.FloatField):
				l.append(field.name)
			if 'busad' in l:
				l.remove('busad')
				l.append('busad')
		return l

class ZardalBusad(ZardalUndsen):
	busad = models.FloatField(verbose_name = 'Бусад:')

	class Meta:
		abstract = True

class ZardalMany(Create):
	yvts = models.CharField(max_length = 20 ,choices = yvts_choice, verbose_name = 'Явц:')
	sum0 = models.FloatField(null = True, blank = True)
	sum1 = models.FloatField(null = True, blank = True)
	sum2 = models.FloatField(null = True, blank = True)
	sum3 = models.FloatField(null = True, blank = True)
	sum4 = models.FloatField(null = True, blank = True)
	sum5 = models.FloatField(null = True, blank = True)
	sum6 = models.FloatField(null = True, blank = True)

	class Meta:
		abstract = True

	def totals(self):
		attrs = self._meta.get_m2m_with_model()[0][0].rel.to.catch()
		cls = getattr(self, self._meta.get_m2m_with_model()[0][0].name)
		for too, i in enumerate(cls.all()):
			value = 0
			for a in attrs:
				value += getattr(i, a)
			setattr(self, 'sum%s' %too, value)

		niilber = 0
		for count, s in enumerate(attrs):
			setattr(self, 'nem%s' %count, cls.all()[:4].aggregate(models.Sum(s)).values()[0])
			niilber += getattr(self, 'nem%s' %count)
		self.nem = niilber
		
		total = 0
		for too, i in enumerate(attrs):
			setattr(self, 'total%s' %too, cls.all().aggregate(models.Sum(i)).values()[0])
			total += getattr(self, 'total%s' %too)
		self.total = total
		self.save()

	def niilber(self):
		for i in self.catch():
			print i



	def __unicode__(self):
		return unicode(self.yvts)

class ZardalUndsenMaterial(ZardalUndsen):
	undsen_tuuhii_ed_usnii = models.FloatField(verbose_name = 'Үндсэн түүхий эд усны зардал:')

	def __unicode__(self):
		return unicode(self.undsen_tuuhii_ed_usnii)

class ZardalUndsenMaterialMany(ZardalMany):
	undsen_material = models.ManyToManyField(ZardalUndsenMaterial)
	suuri_huraamj = models.FloatField(verbose_name = 'Суурь хураамжийн зардал:', null = True)
	
class ZardalTsalin(ZardalUndsen):
	undsen_ba_nemegdel_tsalin = models.FloatField(verbose_name = 'Үндсэн ба нэмэгдэл цалин:')
	ndsh_emdsh = models.FloatField(verbose_name = 'НДШ, ЭМДШ:', null = True)
	shagnal_uramshuulal = models.FloatField(verbose_name = 'Шагнал урамшуулал:')

class ZardalTsalinMany(ZardalMany):
	tsalin = models.ManyToManyField(ZardalTsalin)
	total0 = models.FloatField(null = True, blank = True)
	total1 = models.FloatField(null = True, blank = True)
	total2 = models.FloatField(null = True, blank = True)
	total = models.FloatField(null = True, blank = True)
	nem0 = models.FloatField(null = True, blank = True)
	nem1 = models.FloatField(null = True, blank = True)
	nem2 = models.FloatField(null = True, blank = True)
	nem = models.FloatField(null = True, blank = True)

'''
	def sum_sum0(self):
		return self.sum0 + self.ndsh_emdsh

	def sum_total(self):
		return self.total + self.ndsh_emdsh

	def nem0(self):
		nem = 0
		for i in range(4):
			nem += self.tsalin.all()[i].undsen_ba_nemegdel_tsalin
		return nem

	def nem1(self):
		nem = 0
		for i in range(4):
			nem += self.tsalin.all()[i].shagnal_uramshuulal
		return nem

	def nem(self):
		return self.nem0() + self.nem1() + self.ndsh_emdsh'''

class ZardalAshiglalt(ZardalUndsen):
	tsahilgaan = models.FloatField(verbose_name = 'Цахилгаан:')
	dulaan = models.FloatField(verbose_name = 'Дулаан:')
	us = models.FloatField(verbose_name = 'Ус:')
	tulee_nuurs = models.FloatField(verbose_name = 'Түлээ, нүүрс:')
	tulsh_shatahuun_shatah_toslol = models.FloatField(verbose_name = 'Түлш, шатахуун, шатах тослол:')
	teever = models.FloatField(verbose_name = 'Тээврийн зардал:')
	haruul_hamgaalalt = models.FloatField(verbose_name = 'Харуул хамгаалалт:')

class ZardalAshiglaltMany(ZardalMany):
	ashiglalt = models.ManyToManyField(ZardalAshiglalt)
	total0 = models.FloatField(null = True)
	total1 = models.FloatField(null = True)
	total2 = models.FloatField(null = True)
	total3 = models.FloatField(null = True)
	total4 = models.FloatField(null = True)
	total5 = models.FloatField(null = True)
	total6 = models.FloatField(null = True)
	total = models.FloatField(null = True)
	nem0 = models.FloatField(null = True)
	nem1 = models.FloatField(null = True)
	nem2 = models.FloatField(null = True)
	nem3 = models.FloatField(null = True)
	nem4 = models.FloatField(null = True)
	nem5 = models.FloatField(null = True)
	nem6 = models.FloatField(null = True)
	nem = models.FloatField(null = True)

class ZardalZasvarUilchilgee(ZardalBusad):
	barilga_baiguulamj = models.FloatField(verbose_name = 'Барилга байгууламжын засвар:')
	tonog_tohooromj = models.FloatField(verbose_name= 'Тоног төхөөрөмжийн засвар:')
	selbeg_heregsel = models.FloatField(verbose_name = 'Сэлбэг хэрэгсэл:')
	bagaj_heregsel = models.FloatField(verbose_name = 'Багаж хэрэгслийн зардал:')
	agaariin_nootsiin_hangalt = models.FloatField(verbose_name = 'Агаарын нөөцийн хангалт:')

class ZardalZasvarUilchilgeeMany(ZardalMany):
	zasvar_uilchilgee = models.ManyToManyField(ZardalZasvarUilchilgee)
	total0 = models.FloatField(null = True)
	total1 = models.FloatField(null = True)
	total2 = models.FloatField(null = True)
	total3 = models.FloatField(null = True)
	total4 = models.FloatField(null = True)
	total5 = models.FloatField(null = True)
	total = models.FloatField(null = True)
	nem0 = models.FloatField(null = True)
	nem1 = models.FloatField(null = True)
	nem2 = models.FloatField(null = True)
	nem3 = models.FloatField(null = True)
	nem4 = models.FloatField(null = True)
	nem5 = models.FloatField(null = True)
	nem = models.FloatField(null = True)

class ZardalAriutgal(ZardalBusad):
	chlor = models.FloatField(verbose_name = 'Хлорын зардал:')
	busad_ariutgal = models.FloatField(verbose_name = 'Бусад ариутгалын бодис:')
	lag = models.FloatField()

class ZardalAriutgalMany(ZardalMany):
	ariutgal = models.ManyToManyField(ZardalAriutgal)
	total0 = models.FloatField(null = True)
	total1 = models.FloatField(null = True)
	total2 = models.FloatField(null = True)
	total3 = models.FloatField(null = True)
	total = models.FloatField(null = True)
	nem0 = models.FloatField(null = True)
	nem1 = models.FloatField(null = True)
	nem2 = models.FloatField(null = True)
	nem3 = models.FloatField(null = True)
	nem = models.FloatField(null = True)

class ZardalKontor(ZardalBusad):
	bichig_hereg = models.FloatField(verbose_name = 'Бичиг хэрэг:')
	shuudan_holboo = models.FloatField(verbose_name = 'Шуудан холбоо:')
	tomilolt = models.FloatField(verbose_name = 'Томилолт:')
	surgaltiin_zardal = models.FloatField(verbose_name = 'Сургалтын зардал:')

class ZardalKontorMany(ZardalMany):
	kontor = models.ManyToManyField(ZardalKontor)
	total0 = models.FloatField(null = True)
	total1 = models.FloatField(null = True)
	total2 = models.FloatField(null = True)
	total3 = models.FloatField(null = True)
	total4 = models.FloatField(null = True)
	total = models.FloatField(null = True)
	nem0 = models.FloatField(null = True)
	nem1 = models.FloatField(null = True)
	nem2 = models.FloatField(null = True)
	nem3 = models.FloatField(null = True)
	nem4 = models.FloatField(null = True)
	nem = models.FloatField(null = True)

class ZardalHodolmorHamgaalal(ZardalBusad):
	ayulgui_ajillagaa = models.FloatField(verbose_name = 'Ажилгүй ажиллагаа:')
	eruul_ahui = models.FloatField(verbose_name = 'Эрүүл ахуй:')
	irgenii_hamgaalalt = models.FloatField(verbose_name = 'Иргэний хамгаалалт:')

class ZardalHodolmorHamgaalalMany(ZardalMany):
	hodolmor_hamgaalal = models.ManyToManyField(ZardalHodolmorHamgaalal)
	total0 = models.FloatField(null = True, blank = True)
	total1 = models.FloatField(null = True, blank = True)
	total2 = models.FloatField(null = True, blank = True)
	total3 = models.FloatField(null = True, blank = True)
	total = models.FloatField(null = True, blank = True)
	nem0 = models.FloatField(null = True, blank = True)
	nem1 = models.FloatField(null = True, blank = True)
	nem2 = models.FloatField(null = True, blank = True)
	nem3 = models.FloatField(null = True, blank = True)
	nem = models.FloatField(null = True, blank = True)

class ZardalMarketing(ZardalBusad):
	medeelel_surtalchilgaa = models.FloatField(verbose_name = 'Мэдээлэл сурталилгааны зардал:')
	surgalt = models.FloatField(verbose_name = 'Сургалтын зардал:')
	borluulalt_demjih_uramshuulal = models.FloatField(verbose_name = 'Борлуулалт дэмжих урамшуулал:')
	shalgalt_batalgaajuulalt = models.FloatField(verbose_name = 'Шалгалт баталгаажуулах:')

class ZardalMarketingMany(ZardalMany):
	marketing = models.ManyToManyField(ZardalMarketing)
	total0 = models.FloatField(null = True, blank = True)
	total1 = models.FloatField(null = True, blank = True)
	total2 = models.FloatField(null = True, blank = True)
	total3 = models.FloatField(null = True, blank = True)
	total4 = models.FloatField(null = True, blank = True)
	total = models.FloatField(null = True, blank = True)
	nem0 = models.FloatField(null = True, blank = True)
	nem1 = models.FloatField(null = True, blank = True)
	nem2 = models.FloatField(null = True, blank = True)
	nem3 = models.FloatField(null = True, blank = True)
	nem4 = models.FloatField(null = True, blank = True)
	nem = models.FloatField(null = True, blank = True)

class ZardalLaboratory(ZardalBusad):
	usnii_shinjilgee = models.FloatField(verbose_name = 'Усны шинжилгээ зардал:')
	reactive_bodis = models.FloatField(verbose_name = 'Реактив бодис:')
	shil_sav = models.FloatField(verbose_name = 'Шил сав:')
	batalgaajuulalt_hyanalt = models.FloatField(verbose_name = 'Баталгаажуулалт хяналт:')

class ZardalLaboratoryMany(ZardalMany):
	laboratory = models.ManyToManyField(ZardalLaboratory)
	total0 = models.FloatField(null = True, blank = True)
	total1 = models.FloatField(null = True, blank = True)
	total2 = models.FloatField(null = True, blank = True)
	total3 = models.FloatField(null = True, blank = True)
	total4 = models.FloatField(null = True, blank = True)
	total = models.FloatField(null = True, blank = True)
	nem0 = models.FloatField(null = True, blank = True)
	nem1 = models.FloatField(null = True, blank = True)
	nem2 = models.FloatField(null = True, blank = True)
	nem3 = models.FloatField(null = True, blank = True)
	nem4 = models.FloatField(null = True, blank = True)
	nem = models.FloatField(null = True, blank = True)

class ZardalGuitsetgehUdirdlaga(ZardalBusad):
	tsalin_ndsh = models.FloatField(verbose_name = 'Цалин+НДШ:')
	alban_tomilolt = models.FloatField(verbose_name = 'Албан томилолт:')
	shatahuun = models.FloatField(verbose_name = 'Шатахуун:')
	alban_heregtsee = models.FloatField(verbose_name = 'Албан хэрэгцээ:')

class ZardalGuitsetgehUdirdlagaMany(ZardalMany):
	guitsetgeh_udirdlaga = models.ManyToManyField(ZardalGuitsetgehUdirdlaga)
	total0 = models.FloatField(null = True, blank = True)
	total1 = models.FloatField(null = True, blank = True)
	total2 = models.FloatField(null = True, blank = True)
	total3 = models.FloatField(null = True, blank = True)
	total4 = models.FloatField(null = True, blank = True)
	total = models.FloatField(null = True, blank = True)
	nem0 = models.FloatField(null = True, blank = True)
	nem1 = models.FloatField(null = True, blank = True)
	nem2 = models.FloatField(null = True, blank = True)
	nem3 = models.FloatField(null = True, blank = True)
	nem4 = models.FloatField(null = True, blank = True)
	nem = models.FloatField(null = True, blank = True)

class ZardalTUZ(ZardalBusad):
	tsalin_ndsh_tuz = models.FloatField(verbose_name = 'Цалин НДШ:')
	alban_heregtsee_tuz = models.FloatField(verbose_name = 'Албан хэрэгцээ:')

class ZardalTUZMany(ZardalMany):
	tuz = models.ManyToManyField(ZardalTUZ)
	total0 = models.FloatField(null = True, blank = True)
	total1 = models.FloatField(null = True, blank = True)
	total2 = models.FloatField(null = True, blank = True)
	total = models.FloatField(null = True, blank = True)
	nem0 = models.FloatField(null = True, blank = True)
	nem1 = models.FloatField(null = True, blank = True)
	nem2 = models.FloatField(null = True, blank = True)
	nem = models.FloatField(null = True, blank = True)

class ZardalUndsenHorongiinElegdel(ZardalBusad):
	ul_hodloh_horongo = models.FloatField(verbose_name = 'Үл хөдлөх хөрөнгө:')
	tehnik_tonog_tohooromj = models.FloatField(verbose_name = 'Техник тоног төхөөрөмж:')
	tavilga_ed_hogshil = models.FloatField(verbose_name = 'Тавилга эд хогшил:')

class ZardalUndsenHorongiinElegdelMany(ZardalMany):
	undsen_horongiin_elegdel = models.ManyToManyField(ZardalUndsenHorongiinElegdel)
	total0 = models.FloatField(null = True, blank = True)
	total1 = models.FloatField(null = True, blank = True)
	total2 = models.FloatField(null = True, blank = True)
	total3 = models.FloatField(null = True, blank = True)
	total = models.FloatField(null = True, blank = True)
	nem0 = models.FloatField(null = True, blank = True)
	nem1 = models.FloatField(null = True, blank = True)
	nem2 = models.FloatField(null = True, blank = True)
	nem3 = models.FloatField(null = True, blank = True)
	nem = models.FloatField(null = True, blank = True)

class ZardalGadniiUilchilgee(ZardalBusad):
	zohitsuulah_uilchilgeenii_hols = models.FloatField(verbose_name = 'Зохицуулах үйлчилгээний хөлс:')
	turees = models.FloatField(verbose_name = 'Түрээсийн зардал:')
	audit = models.FloatField(verbose_name = 'Аудитын зардал:')
	program_hangamj = models.FloatField(verbose_name = 'Програм хангамж:')
	banknii_uilchilgee = models.FloatField(verbose_name = 'Банкны үйлчилгээ:')
	shuuhiin_uilchilgee = models.FloatField(verbose_name = 'Шүүхийн үйлчилгээ:')

class ZardalGadniiUilchilgeeMany(ZardalMany):
	gadnii_uilchilgee = models.ManyToManyField(ZardalGadniiUilchilgee)
	total0 = models.FloatField(null = True, blank = True)
	total1 = models.FloatField(null = True, blank = True)
	total2 = models.FloatField(null = True, blank = True)
	total3 = models.FloatField(null = True, blank = True)
	total4 = models.FloatField(null = True, blank = True)
	total5 = models.FloatField(null = True, blank = True)
	total6 = models.FloatField(null = True, blank = True)
	total = models.FloatField(null = True, blank = True)
	nem0 = models.FloatField(null = True, blank = True)
	nem1 = models.FloatField(null = True, blank = True)
	nem2 = models.FloatField(null = True, blank = True)
	nem3 = models.FloatField(null = True, blank = True)
	nem4 = models.FloatField(null = True, blank = True)
	nem5 = models.FloatField(null = True, blank = True)
	nem6 = models.FloatField(null = True, blank = True)
	nem = models.FloatField(null = True, blank = True)

class ZardalTatvar(ZardalBusad):
	gazriin_tatvar = models.FloatField()
	ul_hodloh_horongiin_tatvar = models.FloatField()
	teevriin_heregsliin_tatvar = models.FloatField()

class ZardalTatvarMany(ZardalMany):
	tatvar = models.ManyToManyField(ZardalTatvar)
	total0 = models.FloatField(null = True, blank = True)
	total1 = models.FloatField(null = True, blank = True)
	total2 = models.FloatField(null = True, blank = True)
	total3 = models.FloatField(null = True, blank = True)
	total = models.FloatField(null = True, blank = True)
	nem0 = models.FloatField(null = True, blank = True)
	nem1 = models.FloatField(null = True, blank = True)
	nem2 = models.FloatField(null = True, blank = True)
	nem3 = models.FloatField(null = True, blank = True)
	nem = models.FloatField(null = True, blank = True)

class ZardalDaatgal(ZardalBusad):
	teevriin_heregsliin_daatgal = models.FloatField(verbose_name = 'Тээврийн хэрэгслийн даатгал:')
	ul_hodloh_horongiin_daatgal = models.FloatField(verbose_name = 'Үл хөдлөх хөрөнгийн даатгал:')
	alijchdiin_hurimtlagdsan_daatgal = models.FloatField(verbose_name = 'Ажилчдын хуримтлагдман даатгал:')

class ZardalDaatgalMany(ZardalMany):
	daatgal = models.ManyToManyField(ZardalDaatgal)
	total0 = models.FloatField(null = True, blank = True)
	total1 = models.FloatField(null = True, blank = True)
	total2 = models.FloatField(null = True, blank = True)
	total3 = models.FloatField(null = True, blank = True)
	total = models.FloatField(null = True, blank = True)
	nem0 = models.FloatField(null = True, blank = True)
	nem1 = models.FloatField(null = True, blank = True)
	nem2 = models.FloatField(null = True, blank = True)
	nem3 = models.FloatField(null = True, blank = True)
	nem = models.FloatField(null = True, blank = True)

class ZardalBusadZardal(models.Model):
	torol = models.CharField(max_length = 20, choices = tz_uil_ajillagaanii_angilal)
	value = models.FloatField(verbose_name = 'Утга:')

class ZardalBusadMiddle(models.Model):
	name = models.CharField(max_length = 100, verbose_name = 'Нэр:')
	busad = models.ManyToManyField(ZardalBusadZardal)
	count = models.FloatField(null = True)
	nem = models.FloatField(null = True)

	def counts(self):
		count = 0
		for i in self.busad.all():
			count += i.value
		self.count = count

		nem = 0
		for s in self.busad.all()[:4]:
			nem += s.value
		self.nem = nem
		self.save()

	def __unicode__(self):
		return unicode(self.name)
	
class ZardalBusadZardalMany(ZardalMany):
	busad_zardal = models.ManyToManyField(ZardalBusadMiddle)
	count = models.FloatField(null = True)

	def counts(self):
		for i in range(4):
			count = 0
			for s in self.busad_zardal.all():
				count += s.busad.all()[i].value
			setattr(self, 'sum%s' %i, count)
		self.count = self.sum0 +  self.sum1 +  self.sum2 +  self.sum3
		self.save()

	#def nem(self):
	#	count = 0
	#	for i in self.busad_zardal.all():
	#		count += 

	def __unicode__(self):
		return unicode(self.yvts)

class ZardalAjilchidNiigmiin(ZardalBusad):
	hoolnii_hongololt = models.FloatField(verbose_name = 'Хоолны хөнгөлөлт:')
	unaanii_hongololt = models.FloatField(verbose_name = 'Унааны хөнгөлөлт:')
	tuleenii_hongololt = models.FloatField(verbose_name = 'Түлээний хөнгөлөлт:')
	tetgemj_tuslamj = models.FloatField(verbose_name = 'Тэтгэмж тусламж:')

class ZardalAjilchidNiigmiinMany(ZardalMany):
	ajilchid_niigmiin = models.ManyToManyField(ZardalAjilchidNiigmiin)
	total0 = models.FloatField(null = True, blank = True)
	total1 = models.FloatField(null = True, blank = True)
	total2 = models.FloatField(null = True, blank = True)
	total3 = models.FloatField(null = True, blank = True)
	total4 = models.FloatField(null = True, blank = True)
	total = models.FloatField(null = True, blank = True)
	nem0 = models.FloatField(null = True, blank = True)
	nem1 = models.FloatField(null = True, blank = True)
	nem2 = models.FloatField(null = True, blank = True)
	nem3 = models.FloatField(null = True, blank = True)
	nem4 = models.FloatField(null = True, blank = True)
	nem = models.FloatField(null = True, blank = True)

class ZardalHorongoOruulalt(ZardalBusad):
	urt_hugatsaat_zeel = models.FloatField(verbose_name = 'Урт хугацаат зээлийн хүү:')

	def __unicode__(self):
		return unicode(self.id)

class ZardalHorongoOruulaltMany(ZardalMany):
	horongo_oruulalt = models.ManyToManyField(ZardalHorongoOruulalt)
	total0 = models.FloatField(null = True, blank = True)
	total1 = models.FloatField(null = True, blank = True)
	total = models.FloatField(null = True, blank = True)
	nem0 = models.FloatField(null = True, blank = True)
	nem1 = models.FloatField(null = True, blank = True)
	nem = models.FloatField(null = True, blank = True)

class ZardalUndsenBusUilAjillagaa(models.Model):
	songolt = (
		(0, u'Ус'),
		(1, u'Цахилгаан'),
		(2, u'Дулаан'),
		(3, u'Бусад')
		)
	torol = models.CharField(max_length = 1 ,choices = songolt)
	shagnal_uramshuulal = models.FloatField()
	sport_soyliin_arga_hemjee = models.FloatField()
	busad = models.FloatField()

	@classmethod
	def catch(self):
		l = []
		for field in self._meta.fields:
			if isinstance(field, models.FloatField):
				l.append(field.name)
			if 'busad' in l:
				l.remove('busad')
				l.append('busad')
		return l

class ZardalUndsenBusUilAjillagaaMany(Create):
	yvts = models.CharField(max_length = 20 ,choices = yvts_choice, verbose_name = 'Явц:')
	undsen_bus_uil_ajillagaa = models.ManyToManyField(ZardalUndsenBusUilAjillagaa)
	total0 = models.FloatField(null = True, blank = True)
	total1 = models.FloatField(null = True, blank = True)
	total2 = models.FloatField(null = True, blank = True)
	total = models.FloatField(null = True, blank = True)
	sum0 = models.FloatField(null = True, blank = True)
	sum1 = models.FloatField(null = True, blank = True)
	sum2 = models.FloatField(null = True, blank = True)
	sum3 = models.FloatField(null = True, blank = True)

	def totals(self):
		attrs = self._meta.get_m2m_with_model()[0][0].rel.to.catch()
		cls = getattr(self, self._meta.get_m2m_with_model()[0][0].name)
		for too, i in enumerate(cls.all()):
			value = 0
			for a in attrs:
				value += getattr(i, a)
			setattr(self, 'sum%s' %too, value)
		
		total = 0
		for too, i in enumerate(attrs):
			print too
			setattr(self, 'total%s' %too, cls.all().aggregate(models.Sum(i)).values()[0])
			total += getattr(self, 'total%s' %too)
		self.total = total
		self.save()

	def __unicode__(self):
		return unicode(self.yvts)

class Zardal(Create):
	z1 = models.OneToOneField(ZardalUndsenMaterialMany, null = True, blank = True)
	z2 = models.OneToOneField(ZardalTsalinMany, null = True, blank = True)
	z3 = models.OneToOneField(ZardalAshiglaltMany, null = True)
	z4 = models.OneToOneField(ZardalZasvarUilchilgeeMany, null = True)
	z5 = models.OneToOneField(ZardalAriutgalMany, null = True)
	z6 = models.OneToOneField(ZardalKontorMany, null = True)
	z7 = models.OneToOneField(ZardalHodolmorHamgaalalMany, null = True)
	z8 = models.OneToOneField(ZardalMarketingMany, null = True)
	z9 = models.OneToOneField(ZardalLaboratoryMany, null = True)
	z10 = models.OneToOneField(ZardalGuitsetgehUdirdlagaMany, null = True)
	z11 = models.OneToOneField(ZardalTUZMany, null = True)
	z12 = models.OneToOneField(ZardalUndsenHorongiinElegdelMany, null = True)
	z13 = models.OneToOneField(ZardalGadniiUilchilgeeMany, null = True)
	z14 = models.OneToOneField(ZardalTatvarMany, null = True)
	z15 = models.OneToOneField(ZardalDaatgalMany, null = True)
	z16 = models.OneToOneField(ZardalBusadZardalMany, null = True)
	z17 = models.OneToOneField(ZardalAjilchidNiigmiinMany, null = True)
	z18 = models.OneToOneField(ZardalHorongoOruulaltMany, null = True)
	z19 = models.OneToOneField(ZardalUndsenBusUilAjillagaaMany, null = True)

	def __unicode__(self):
		return unicode(self.z2)

class BusadOrlogo(Create):
	yvts = models.CharField(max_length = 20 ,choices = yvts_choice, verbose_name = 'Явц:', null = True)
	unt = models.FloatField(verbose_name = u'Усны хэсгийн бусад орлого', null = True)
	unt0 = models.FloatField(verbose_name = 'Дулааны борлуулалтын орлого:', null = True)
	unt1 = models.FloatField(verbose_name = 'дулааны хэсгийн бусад орлого:', null = True)
	unt2 = models.FloatField(verbose_name = 'Цахилгааны борлуулалтын орлого:', null = True)
	unt3 = models.FloatField(verbose_name = 'цахилгааны хэсгийн бусад орлого:', null = True)
	unt4 = models.FloatField(verbose_name = 'Бусад орлого:', null = True)
	unt5 = models.FloatField(verbose_name = 'Үндсэн бус үйл ажиллагааны орлого:', null = True)

	def __unicode__(self):
		return unicode(self.yvts)

class Tsalin(models.Model):
	sss = (
		('0', u'Удирдлага'),
		('1', u'ИТА, албан хаагч'),
		('2', u'Ажилчид'),
		)
	songolt = models.CharField(choices = sss, max_length = 1)
	too = models.IntegerField(null = True)
	undsen_tsalin = models.FloatField(null = True)
	nemegdel = models.FloatField(null = True)
	sariin_ur_dun = models.FloatField(null = True)
	jiliin_ur_dun_shagnalt_tsalin = models.FloatField(null = True)

	'''def niit_salary(self):
		return self.undsen_tsalin + self.nemegdel + self.sariin_ur_dun + self.jiliin_ur_dun_shagnalt_tsalin

	def nemegdel_huvi(self):
		return int((self.nemegdel / self.niit_salary())*100)

	def sariin_huvi(self):
		return int((self.sariin_ur_dun / self.niit_salary())*100)

	def jiliin_huvi(self):
		return int((self.jiliin_ur_dun_shagnalt_tsalin / self.niit_salary())*100)

	def dundaj(self):
		#return self.niit_salary()
		return "{0:.2f}".format( ( self.niit_salary() / self.too) *1000 )'''

class TsalinMany(Create):
	tsalin = models.ManyToManyField(Tsalin)
	yvts = models.CharField(max_length = 20 ,choices = yvts_choice, verbose_name = 'Явц:', null = True)

	'''def niit_too(self):
		count = 0
		for i in self.tsalin.all():
			count += i.too
		return count
	def niit_undsen_tsalin(self):
		count = 0
		for i in self.tsalin.all():
			count += i.undsen_tsalin
		return count

	def niit_nemegdel(self):
		count = 0
		for i in self.tsalin.all():
			count += i.nemegdel
		return count

	def niit_sariin(self):
		count = 0
		for i in self.tsalin.all():
			count += i.sariin_ur_dun
		return count

	def niit_jiliin(self):
		count = 0
		for i in self.tsalin.all():
			count += i.jiliin_ur_dun_shagnalt_tsalin
		return count

	def niit(self):
		return self.niit_undsen_tsalin() + self.niit_sariin() + self.niit_nemegdel() + self.niit_jiliin()

	def nemegdel_huvi(self):
		return int((self.niit_nemegdel() / self.niit())*100)

	def sariin_huvi(self):
		return int((self.niit_sariin() / self.niit())*100)

	def jiliin_huvi(self):
		return int((self.niit_jiliin() / self.niit())*100)

	def dundaj(self):
		return "{0:.2f}".format( ( self.niit() / self.niit_too() ) * 1000 )

	def __unicode__(self):
		return unicode(self.yvts)'''

class Tailan(Create):
	tze = models.ForeignKey(TZE)
	year = models.IntegerField()
	zardal = models.OneToOneField(Zardal)
	orlogo = models.OneToOneField(Orlogo)
	busad_orlogo = models.OneToOneField(BusadOrlogo, null = True, blank = True)
	tariff_hereglegch = models.ManyToManyField(TariffAll, blank = True)
	golch = models.ManyToManyField(Golch, blank = True)
	sanal_gomdol = models.OneToOneField(SanalGomdolMany, null = True, blank = True)
	tehnik_nohtsol = models.OneToOneField(TehnikNohtsolMany, null = True, blank = True)
	tasaldal = models.OneToOneField(TasaldalMany, null = True, blank = True)
	yvts = models.CharField(max_length = 200, choices = yvts_choice)
	olborlolt = models.ForeignKey(Olborlolt, null = True, blank = True)
	hereglegch = models.ForeignKey(HereglegchAll, null = True, blank = True)
	tsalin = models.OneToOneField(TsalinMany, null = True)

	class Meta:
		abstract = True

	def __unicode__(self):
		return "%s | %s" %(unicode(self.tze), unicode(self.year))

	def example(self, k):
		return self.golch_return().buteegdehuun.all()[k].too * self.tariff_hereglegch_golch().tariff.all()[k].une / 1000
	
	def example_12(self, k):
		return self.example(k) * 12
	
	def tariff_hereglegch_us(self):
		return self.tariff_hereglegch.all().get(name = 0)

	def tariff_hereglegch_golch(self):
		return self.tariff_hereglegch.all().get(name = 1)

	def golch_return(self):
		return self.golch.all().get(name = 0)

	def golch_hangagch_return(self):
		return self.golch.all().get(name = 1)

	def suuri_une_count(self):
		return self.orlogo.all_orh_count() * self.tariff_hereglegch.all().get(name = 0).suuri_une / 1000

	def suuri_12_count(self):
		return self.suuri_une_count() * 12

	def boo_zardal_sum0(self):
		sum0 = 0
		#for i in range(3,16):
		#	print getattr(self.zardal, 'z%s' %i).sum0
		return sum0

	def orlogo_une(self):
		a = []
		for too, i in enumerate(self.tariff_hereglegch_us().tariff.all()):
			a.append(i.une * self.orlogo.buteegdehuun.all()[too+2].too)
		return a

	def zardal1_tsever(self):
		if self.zardal.z1:
			return self.zardal.z1.undsen_material.all()[0].undsen_tuuhii_ed_usnii * self.olborlolt.tsever
		else:
			return 0
	def zardal1_bohir(self):
		if self.zardal.z1:
			return self.zardal.z1.undsen_material.all()[1].undsen_tuuhii_ed_usnii * self.olborlolt.bohir
		else:
			return 0

	def zardal1_suuri_une(self):
		count = 0
		for i in range(15):
			count += self.golch_hangagch_return().buteegdehuun.all()[i].too * \
			self.tariff_hereglegch_golch().tariff.all()[i].une / 1000
		return count

	def zardal1_suuri_une_12(self):
		count = 0
		for i in range(15):
			count += self.golch_hangagch_return().buteegdehuun.all()[i].too * \
			self.tariff_hereglegch_golch().tariff.all()[i].une / 1000
		return count * 12

class SariinTailan(Tailan):
	month = models.IntegerField(null = True)
	tailan_status = models.BooleanField(default = False)

	def __unicode__(self):
		return u'%s | %s | %s' %(self.tze, self.year, self.month)

	class Meta:
		ordering = ['year', 'month']

class Sudalgaa(Tailan):
	pass

	

######################################### ТӨГСГӨЛ УУГАНАА ####################################################



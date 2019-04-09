# -*- coding:utf-8 -*- 

from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse
from django.db.models import Sum, F
from applications.app.views import LoginRequired
from applications.app.models import TZE, Ajiltan, Certificate
from applications.director.models import SariinTailan, HereglegchAll

class TailanView(LoginRequired, TemplateView):

	template_name = 'tailan.html'

	def get_context_data(self, **kwargs):
		context = super(TailanView, self).get_context_data(**kwargs)
		tailan = []
		for i in SariinTailan.objects.filter(tze = self.baiguullaga).values('year').distinct().order_by('-year'):
			tailan.append(i.values()[0])
		context['tailan'] = tailan
		return context

class YearTailanView(LoginRequired, TemplateView):

	template_name = 'year_tailan.html'


	def get_context_data(self, **kwargs):
		context = super(YearTailanView, self).get_context_data(**kwargs)
		context['name'] = self.kwargs['pk']
		return context

def export(request, bid = 0, year = 0, pk = 0):
	c = {}
	st = SariinTailan.objects.filter(tze__id = bid, year = year, month__gt = 0, tailan_status = False, yvts = u'Хүлээн авсан')
	try:
		c['tailan'] = st
	except:
		pass
	if pk == '1':
		c['org'] = TZE.objects.get(id = bid)
		#c['director'] = Ajiltan.objects.filter(baiguullaga__id = bid, alban_tushaal__position_name__name = u'Захирал')[0]
		c['cer'] = Certificate.objects.filter(tze__id = bid)
		#c['engiinering'] = Ajiltan.objects.filter(baiguullaga__id = bid, alban_tushaal__position_name__name = u'Ерөнхий инженер').first()
		#c['accountants'] = Ajiltan.objects.filter(baiguullaga__id = bid, alban_tushaal__position_name__name = u'Ерөнхий нягтлан').first()
		#c['us_eng'] = Ajiltan.objects.filter(baiguullaga__id = bid, alban_tushaal__position_name__name = u'Ус хангамжийн инженер').first()
		#c['ediin'] = Ajiltan.objects.filter(baiguullaga__id = bid, alban_tushaal__position_name__name = u'Эдийн засагч').first()
		#c['too_acc'] = Ajiltan.objects.filter(baiguullaga__id = bid, alban_tushaal__position_name__name = u'Тооцооны нягтлан').first()
		return render_to_response('husnegt/1.html', c)
	elif pk == '2':
		return render_to_response('husnegt/2.html')
	elif pk == '3':
		return render_to_response('husnegt/3.html')
	elif pk == '4':
		return render_to_response('husnegt/4.html')
	elif pk == '5':
		return render_to_response('husnegt/5.html')
	elif pk == '6':
		return render_to_response('husnegt/6.html')
	elif pk == '7':
		return render_to_response('husnegt/7.html')
	elif pk == '8':
		return render_to_response('husnegt/8.html', c)
	elif pk == '9':
		return render_to_response('husnegt/9.html', c)
	elif pk == '10':
		a = filtering(st)
		return render_to_response('husnegt/10.html', a)
	elif pk == '11':
		c['users'] = HereglegchAll.objects.first()
		for s in range(16):
			c['i%s' %s] = 0
		for i in st:
			for s in range(16):
				c['i%s' %s] += i.orlogo.buteegdehuun.all()[s].too		
		return render_to_response('husnegt/11.html', c)
	elif pk == '12':
		t = SariinTailan.objects.filter(tze__id = bid, year = year, month__gt = 0, tailan_status = False).last()
		for i in t.tariff_hereglegch.all():
			if i.name == '1':
				c['tariff'] = i
		for i in t.golch.all():
			if i.name == '0':
				c['golch'] = i
		return render_to_response('husnegt/12.html', c)
	elif pk == '13':
		raise Http404
		#return render_to_response('husnegt/13.html')
	elif pk == '14':
		a = 0
		c['users'] = HereglegchAll.objects.first().hereglegch.all().aggregate(Sum('htoo'))
		for m in st:
			if m.tasaldal:
				setattr(m, 'duration', m.tasaldal.tasaldal.all().aggregate(Sum('duration')))
				setattr(m, 'too', m.tasaldal.tasaldal.all().aggregate(Sum('too'))) 
		return render_to_response('husnegt/14.html', c)
	elif pk == '15':
		a = b = d = e = f = g = 0
		try:
			for t in st:
				m = t.tehnik_nohtsol.tehnik_nohtsol.all()[0].too - t.tehnik_nohtsol.tehnik_nohtsol.all()[1].too
				m1 = t.tehnik_nohtsol.tehnik_nohtsol.all()[0].us - t.tehnik_nohtsol.tehnik_nohtsol.all()[1].us
				setattr(t, 'm', m)
				setattr(t, 'm1', m1)
				a += t.tehnik_nohtsol.tehnik_nohtsol.all()[0].too
				b += t.tehnik_nohtsol.tehnik_nohtsol.all()[0].us
				d += t.tehnik_nohtsol.tehnik_nohtsol.all()[1].too
				e += t.tehnik_nohtsol.tehnik_nohtsol.all()[1].us
				f += t.m
				g += t.m1
			c['a'] = a
			c['b'] = b
			c['d'] = d
			c['e'] = e
			c['f'] = f
			c['g'] = g
		except:
			pass
		return render_to_response('husnegt/15.html', c)
	elif pk == '16':
		a=a1=b=b1=d=d1=e=e1=f=f1=0
		try:
			for m in st:
				if m.sanal_gomdol:
					a += m.sanal_gomdol.sanal_gomdol.all()[0].huleen_avsan_ognoo
					a1 += m.sanal_gomdol.sanal_gomdol.all()[0].shiidverlesen_ognoo
					b += m.sanal_gomdol.sanal_gomdol.all()[1].huleen_avsan_ognoo
					b1 += m.sanal_gomdol.sanal_gomdol.all()[1].shiidverlesen_ognoo
					d += m.sanal_gomdol.sanal_gomdol.all()[2].huleen_avsan_ognoo
					d1 += m.sanal_gomdol.sanal_gomdol.all()[2].shiidverlesen_ognoo
					e += m.sanal_gomdol.sanal_gomdol.all()[3].huleen_avsan_ognoo
					e1 += m.sanal_gomdol.sanal_gomdol.all()[3].shiidverlesen_ognoo
					f += m.sanal_gomdol.sanal_gomdol.all()[4].huleen_avsan_ognoo
					f1 += m.sanal_gomdol.sanal_gomdol.all()[4].shiidverlesen_ognoo
					setattr(m, 'huleen', m.sanal_gomdol.sanal_gomdol.all().aggregate(Sum('huleen_avsan_ognoo')))
					setattr(m, 'shiid', m.sanal_gomdol.sanal_gomdol.all().aggregate(Sum('shiidverlesen_ognoo')))
			c['a'] = a
			c['a1'] = a1
			c['b'] = b
			c['b1'] = b1
			c['d'] = d
			c['d1'] = d1
			c['e'] = e
			c['e1'] = e1
			c['f'] = f
			c['f1'] = f1
			c['niit'] = a+b+d+e+f
			c['niit1'] = a1+b1+d1+e1+f1
		except:
			pass
		return render_to_response('husnegt/16.html', c)
	else:
		raise Http404


def filtering(st):
	try:
		c = {}

		c['i'] = st.filter(zardal__z1__undsen_material__torol = 0).aggregate(i = Sum('zardal__z1__undsen_material__undsen_tuuhii_ed_usnii'))
		c['i'].update(st.filter(zardal__z1__undsen_material__torol = 1).aggregate(i1 = Sum('zardal__z1__undsen_material__undsen_tuuhii_ed_usnii')))

		#c['i'].update(st.filter(zardal__z2__tsalin__torol = 0).aggregate(aa1 = Sum('zardal__z2__tsalin__undsen_ba_nemegdel_tsalin')))
		#c['i'].update(st.filter(zardal__z2__tsalin__torol = 1).aggregate(aa2 = Sum('zardal__z2__tsalin__undsen_ba_nemegdel_tsalin')))
		#c['i'].update(st.filter(zardal__z2__tsalin__torol = 2).aggregate(aa3 = Sum('zardal__z2__tsalin__undsen_ba_nemegdel_tsalin')))
		#c['i'].update(st.filter(zardal__z2__tsalin__torol__in = [3,4,5]).aggregate(aa4 = Sum('zardal__z2__tsalin__undsen_ba_nemegdel_tsalin')))
		#c['i'].update(st.aggregate(aa5 = Sum('zardal__z2__tsalin__undsen_ba_nemegdel_tsalin')))
		
		#c['i'].update(st.filter(zardal__z2__tsalin__torol = 0).aggregate(ab1 = Sum('zardal__z2__tsalin__ndsh_emdsh')))
		#c['i'].update(st.filter(zardal__z2__tsalin__torol = 1).aggregate(ab2 = Sum('zardal__z2__tsalin__ndsh_emdsh')))
		#c['i'].update(st.filter(zardal__z2__tsalin__torol = 2).aggregate(ab3 = Sum('zardal__z2__tsalin__ndsh_emdsh')))
		#c['i'].update(st.filter(zardal__z2__tsalin__torol__in = [3,4,5]).aggregate(ab4 = Sum('zardal__z2__tsalin__ndsh_emdsh')))
		#c['i'].update(st.aggregate(ab5 = Sum('zardal__z2__tsalin__ndsh_emdsh')))
		
		#c['i'].update(st.filter(zardal__z2__tsalin__torol = 0).aggregate(ac1 = Sum('zardal__z2__tsalin__shagnal_uramshuulal')))
		#c['i'].update(st.filter(zardal__z2__tsalin__torol = 1).aggregate(ac2 = Sum('zardal__z2__tsalin__shagnal_uramshuulal')))
		#c['i'].update(st.filter(zardal__z2__tsalin__torol = 2).aggregate(ac3 = Sum('zardal__z2__tsalin__shagnal_uramshuulal')))
		#c['i'].update(st.filter(zardal__z2__tsalin__torol__in = [3,4,5]).aggregate(ac4 = Sum('zardal__z2__tsalin__shagnal_uramshuulal')))
		#c['i'].update(st.aggregate(ac5 = Sum('zardal__z2__tsalin__shagnal_uramshuulal')))
		
		#c['i']['ad1'] = c['i']['aa1'] + c['i']['ab1'] + c['i']['ac1']
		#c['i']['ad2'] = c['i']['aa2'] + c['i']['ab2'] + c['i']['ac2']
		#c['i']['ad3'] = c['i']['aa3'] + c['i']['ab3'] + c['i']['ac3']
		#c['i']['ad4'] = c['i']['aa4'] + c['i']['ab4'] + c['i']['ac4']
		#c['i']['ad5'] = c['i']['aa5'] + c['i']['ab5'] + c['i']['ac5']
		
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol = 0).aggregate(ba1 = Sum('zardal__z3__ashiglalt__tsahilgaan')))
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol = 1).aggregate(ba2 = Sum('zardal__z3__ashiglalt__tsahilgaan')))
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol = 2).aggregate(ba3 = Sum('zardal__z3__ashiglalt__tsahilgaan')))
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol__in = [3,4,5]).aggregate(ba4 = Sum('zardal__z3__ashiglalt__tsahilgaan')))
		c['i'].update(st.aggregate(ba5 = Sum('zardal__z3__ashiglalt__tsahilgaan')))
		
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol = 0).aggregate(bb1 = Sum('zardal__z3__ashiglalt__dulaan')))
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol = 1).aggregate(bb2 = Sum('zardal__z3__ashiglalt__dulaan')))
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol = 2).aggregate(bb3 = Sum('zardal__z3__ashiglalt__dulaan')))
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol__in = [3,4,5]).aggregate(bb4 = Sum('zardal__z3__ashiglalt__dulaan')))
		c['i'].update(st.aggregate(bb5 = Sum('zardal__z3__ashiglalt__dulaan')))

		c['i'].update(st.filter(zardal__z3__ashiglalt__torol = 0).aggregate(bc1 = Sum('zardal__z3__ashiglalt__us')))
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol = 1).aggregate(bc2 = Sum('zardal__z3__ashiglalt__us')))
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol = 2).aggregate(bc3 = Sum('zardal__z3__ashiglalt__us')))
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol__in = [3,4,5]).aggregate(bc4 = Sum('zardal__z3__ashiglalt__us')))
		c['i'].update(st.aggregate(bc5 = Sum('zardal__z3__ashiglalt__us')))
		
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol = 0).aggregate(bd1 = Sum('zardal__z3__ashiglalt__tulee_nuurs')))
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol = 1).aggregate(bd2 = Sum('zardal__z3__ashiglalt__tulee_nuurs')))
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol = 2).aggregate(bd3 = Sum('zardal__z3__ashiglalt__tulee_nuurs')))
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol__in = [3,4,5]).aggregate(bd4 = Sum('zardal__z3__ashiglalt__tulee_nuurs')))
		c['i'].update(st.aggregate(bd5 = Sum('zardal__z3__ashiglalt__tulee_nuurs')))

		c['i'].update(st.filter(zardal__z3__ashiglalt__torol = 0).aggregate(be1 = Sum('zardal__z3__ashiglalt__tulsh_shatahuun_shatah_toslol')))
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol = 1).aggregate(be2 = Sum('zardal__z3__ashiglalt__tulsh_shatahuun_shatah_toslol')))
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol = 2).aggregate(be3 = Sum('zardal__z3__ashiglalt__tulsh_shatahuun_shatah_toslol')))
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol__in = [3,4,5]).aggregate(be4 = Sum('zardal__z3__ashiglalt__tulsh_shatahuun_shatah_toslol')))
		c['i'].update(st.aggregate(be5 = Sum('zardal__z3__ashiglalt__tulsh_shatahuun_shatah_toslol')))
		
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol = 0).aggregate(bf1 = Sum('zardal__z3__ashiglalt__teever')))
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol = 1).aggregate(bf2 = Sum('zardal__z3__ashiglalt__teever')))
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol = 2).aggregate(bf3 = Sum('zardal__z3__ashiglalt__teever')))
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol__in = [3,4,5]).aggregate(bf4 = Sum('zardal__z3__ashiglalt__teever')))
		c['i'].update(st.aggregate(bf5 = Sum('zardal__z3__ashiglalt__teever')))
		
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol = 0).aggregate(bg1 = Sum('zardal__z3__ashiglalt__haruul_hamgaalalt')))
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol = 1).aggregate(bg2 = Sum('zardal__z3__ashiglalt__haruul_hamgaalalt')))
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol = 2).aggregate(bg3 = Sum('zardal__z3__ashiglalt__haruul_hamgaalalt')))
		c['i'].update(st.filter(zardal__z3__ashiglalt__torol__in = [3,4,5]).aggregate(bg4 = Sum('zardal__z3__ashiglalt__haruul_hamgaalalt')))
		c['i'].update(st.aggregate(bg5 = Sum('zardal__z3__ashiglalt__haruul_hamgaalalt')))
		
		c['i']['bh1'] = c['i']['ba1'] + c['i']['bb1'] + c['i']['bc1'] + c['i']['bd1'] + c['i']['be1'] + c['i']['bf1'] + c['i']['bg1']
		c['i']['bh2'] = c['i']['ba2'] + c['i']['bb2'] + c['i']['bc2'] + c['i']['bd2'] + c['i']['be2'] + c['i']['bf2'] + c['i']['bg2']
		c['i']['bh3'] = c['i']['ba3'] + c['i']['bb3'] + c['i']['bc3'] + c['i']['bd3'] + c['i']['be3'] + c['i']['bf3'] + c['i']['bg3']
		c['i']['bh4'] = c['i']['ba4'] + c['i']['bb4'] + c['i']['bc4'] + c['i']['bd4'] + c['i']['be4'] + c['i']['bf4'] + c['i']['bg4']
		c['i']['bh5'] = c['i']['ba5'] + c['i']['bb5'] + c['i']['bc5'] + c['i']['bd5'] + c['i']['be5'] + c['i']['bf5'] + c['i']['bg5']
		
		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol = 0).aggregate(ca1 = Sum('zardal__z4__zasvar_uilchilgee__barilga_baiguulamj')))
		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol = 1).aggregate(ca2 = Sum('zardal__z4__zasvar_uilchilgee__barilga_baiguulamj')))
		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol = 2).aggregate(ca3 = Sum('zardal__z4__zasvar_uilchilgee__barilga_baiguulamj')))
		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol__in = [3,4,5]).aggregate(ca4 = Sum('zardal__z4__zasvar_uilchilgee__barilga_baiguulamj')))
		c['i'].update(st.aggregate(ca5 = Sum('zardal__z4__zasvar_uilchilgee__barilga_baiguulamj')))
		
		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol = 0).aggregate(cb1 = Sum('zardal__z4__zasvar_uilchilgee__tonog_tohooromj')))
		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol = 1).aggregate(cb2 = Sum('zardal__z4__zasvar_uilchilgee__tonog_tohooromj')))
		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol = 2).aggregate(cb3 = Sum('zardal__z4__zasvar_uilchilgee__tonog_tohooromj')))
		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol__in = [3,4,5]).aggregate(cb4 = Sum('zardal__z4__zasvar_uilchilgee__tonog_tohooromj')))
		c['i'].update(st.aggregate(cb5 = Sum('zardal__z4__zasvar_uilchilgee__tonog_tohooromj')))

		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol = 0).aggregate(cc1 = Sum('zardal__z4__zasvar_uilchilgee__selbeg_heregsel')))
		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol = 1).aggregate(cc2 = Sum('zardal__z4__zasvar_uilchilgee__selbeg_heregsel')))
		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol = 2).aggregate(cc3 = Sum('zardal__z4__zasvar_uilchilgee__selbeg_heregsel')))
		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol__in = [3,4,5]).aggregate(cc4 = Sum('zardal__z4__zasvar_uilchilgee__selbeg_heregsel')))
		c['i'].update(st.aggregate(cc5 = Sum('zardal__z4__zasvar_uilchilgee__selbeg_heregsel')))
		
		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol = 0).aggregate(cd1 = Sum('zardal__z4__zasvar_uilchilgee__bagaj_heregsel')))
		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol = 1).aggregate(cd2 = Sum('zardal__z4__zasvar_uilchilgee__bagaj_heregsel')))
		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol = 2).aggregate(cd3 = Sum('zardal__z4__zasvar_uilchilgee__bagaj_heregsel')))
		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol__in = [3,4,5]).aggregate(cd4 = Sum('zardal__z4__zasvar_uilchilgee__bagaj_heregsel')))
		c['i'].update(st.aggregate(cd5 = Sum('zardal__z4__zasvar_uilchilgee__bagaj_heregsel')))

		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol = 0).aggregate(ce1 = Sum('zardal__z4__zasvar_uilchilgee__agaariin_nootsiin_hangalt')))
		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol = 1).aggregate(ce2 = Sum('zardal__z4__zasvar_uilchilgee__agaariin_nootsiin_hangalt')))
		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol = 2).aggregate(ce3 = Sum('zardal__z4__zasvar_uilchilgee__agaariin_nootsiin_hangalt')))
		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol__in = [3,4,5]).aggregate(ce4 = Sum('zardal__z4__zasvar_uilchilgee__agaariin_nootsiin_hangalt')))
		c['i'].update(st.aggregate(ce5 = Sum('zardal__z4__zasvar_uilchilgee__agaariin_nootsiin_hangalt')))
		
		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol = 0).aggregate(cf1 = Sum('zardal__z4__zasvar_uilchilgee__busad')))
		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol = 1).aggregate(cf2 = Sum('zardal__z4__zasvar_uilchilgee__busad')))
		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol = 2).aggregate(cf3 = Sum('zardal__z4__zasvar_uilchilgee__busad')))
		c['i'].update(st.filter(zardal__z4__zasvar_uilchilgee__torol__in = [3,4,5]).aggregate(cf4 = Sum('zardal__z4__zasvar_uilchilgee__busad')))
		c['i'].update(st.aggregate(cf5 = Sum('zardal__z4__zasvar_uilchilgee__busad')))
		
		c['i']['cg1'] = c['i']['ca1'] + c['i']['cb1'] + c['i']['cc1'] + c['i']['cd1'] + c['i']['ce1'] + c['i']['cf1']
		c['i']['cg2'] = c['i']['ca2'] + c['i']['cb2'] + c['i']['cc2'] + c['i']['cd2'] + c['i']['ce2'] + c['i']['cf2']
		c['i']['cg3'] = c['i']['ca3'] + c['i']['cb3'] + c['i']['cc3'] + c['i']['cd3'] + c['i']['ce3'] + c['i']['cf3']
		c['i']['cg4'] = c['i']['ca4'] + c['i']['cb4'] + c['i']['cc4'] + c['i']['cd4'] + c['i']['ce4'] + c['i']['cf4']
		c['i']['cg5'] = c['i']['ca5'] + c['i']['cb5'] + c['i']['cc5'] + c['i']['cd5'] + c['i']['ce5'] + c['i']['cf5']

		c['i'].update(st.filter(zardal__z5__ariutgal__torol = 0).aggregate(da1 = Sum('zardal__z5__ariutgal__chlor')))
		c['i'].update(st.filter(zardal__z5__ariutgal__torol = 1).aggregate(da2 = Sum('zardal__z5__ariutgal__chlor')))
		c['i'].update(st.filter(zardal__z5__ariutgal__torol = 2).aggregate(da3 = Sum('zardal__z5__ariutgal__chlor')))
		c['i'].update(st.filter(zardal__z5__ariutgal__torol__in = [3,4,5]).aggregate(da4 = Sum('zardal__z5__ariutgal__chlor')))
		c['i'].update(st.aggregate(da5 = Sum('zardal__z5__ariutgal__chlor')))
		
		c['i'].update(st.filter(zardal__z5__ariutgal__torol = 0).aggregate(db1 = Sum('zardal__z5__ariutgal__busad_ariutgal')))
		c['i'].update(st.filter(zardal__z5__ariutgal__torol = 1).aggregate(db2 = Sum('zardal__z5__ariutgal__busad_ariutgal')))
		c['i'].update(st.filter(zardal__z5__ariutgal__torol = 2).aggregate(db3 = Sum('zardal__z5__ariutgal__busad_ariutgal')))
		c['i'].update(st.filter(zardal__z5__ariutgal__torol__in = [3,4,5]).aggregate(db4 = Sum('zardal__z5__ariutgal__busad_ariutgal')))
		c['i'].update(st.aggregate(db5 = Sum('zardal__z5__ariutgal__busad_ariutgal')))

		c['i'].update(st.filter(zardal__z5__ariutgal__torol = 0).aggregate(dc1 = Sum('zardal__z5__ariutgal__lag')))
		c['i'].update(st.filter(zardal__z5__ariutgal__torol = 1).aggregate(dc2 = Sum('zardal__z5__ariutgal__lag')))
		c['i'].update(st.filter(zardal__z5__ariutgal__torol = 2).aggregate(dc3 = Sum('zardal__z5__ariutgal__lag')))
		c['i'].update(st.filter(zardal__z5__ariutgal__torol__in = [3,4,5]).aggregate(dc4 = Sum('zardal__z5__ariutgal__lag')))
		c['i'].update(st.aggregate(dc5 = Sum('zardal__z5__ariutgal__lag')))
		
		c['i'].update(st.filter(zardal__z5__ariutgal__torol = 0).aggregate(dd1 = Sum('zardal__z5__ariutgal__busad')))
		c['i'].update(st.filter(zardal__z5__ariutgal__torol = 1).aggregate(dd2 = Sum('zardal__z5__ariutgal__busad')))
		c['i'].update(st.filter(zardal__z5__ariutgal__torol = 2).aggregate(dd3 = Sum('zardal__z5__ariutgal__busad')))
		c['i'].update(st.filter(zardal__z5__ariutgal__torol__in = [3,4,5]).aggregate(dd4 = Sum('zardal__z5__ariutgal__busad')))
		c['i'].update(st.aggregate(dd5 = Sum('zardal__z5__ariutgal__busad')))
		
		c['i']['de1'] = c['i']['da1'] + c['i']['db1'] + c['i']['dc1'] + c['i']['dd1']
		c['i']['de2'] = c['i']['da2'] + c['i']['db2'] + c['i']['dc2'] + c['i']['dd2']
		c['i']['de3'] = c['i']['da3'] + c['i']['db3'] + c['i']['dc3'] + c['i']['dd3']
		c['i']['de4'] = c['i']['da4'] + c['i']['db4'] + c['i']['dc4'] + c['i']['dd4']
		c['i']['de5'] = c['i']['da5'] + c['i']['db5'] + c['i']['dc5'] + c['i']['dd5']


		c['i'].update(st.filter(zardal__z6__kontor__torol = 0).aggregate(ea1 = Sum('zardal__z6__kontor__bichig_hereg')))
		c['i'].update(st.filter(zardal__z6__kontor__torol = 1).aggregate(ea2 = Sum('zardal__z6__kontor__bichig_hereg')))
		c['i'].update(st.filter(zardal__z6__kontor__torol = 2).aggregate(ea3 = Sum('zardal__z6__kontor__bichig_hereg')))
		c['i'].update(st.filter(zardal__z6__kontor__torol__in = [3,4,5]).aggregate(ea4 = Sum('zardal__z6__kontor__bichig_hereg')))
		c['i'].update(st.aggregate(ea5 = Sum('zardal__z6__kontor__bichig_hereg')))
		
		c['i'].update(st.filter(zardal__z6__kontor__torol = 0).aggregate(eb1 = Sum('zardal__z6__kontor__shuudan_holboo')))
		c['i'].update(st.filter(zardal__z6__kontor__torol = 1).aggregate(eb2 = Sum('zardal__z6__kontor__shuudan_holboo')))
		c['i'].update(st.filter(zardal__z6__kontor__torol = 2).aggregate(eb3 = Sum('zardal__z6__kontor__shuudan_holboo')))
		c['i'].update(st.filter(zardal__z6__kontor__torol__in = [3,4,5]).aggregate(eb4 = Sum('zardal__z6__kontor__shuudan_holboo')))
		c['i'].update(st.aggregate(eb5 = Sum('zardal__z6__kontor__shuudan_holboo')))

		c['i'].update(st.filter(zardal__z6__kontor__torol = 0).aggregate(ec1 = Sum('zardal__z6__kontor__tomilolt')))
		c['i'].update(st.filter(zardal__z6__kontor__torol = 1).aggregate(ec2 = Sum('zardal__z6__kontor__tomilolt')))
		c['i'].update(st.filter(zardal__z6__kontor__torol = 2).aggregate(ec3 = Sum('zardal__z6__kontor__tomilolt')))
		c['i'].update(st.filter(zardal__z6__kontor__torol__in = [3,4,5]).aggregate(ec4 = Sum('zardal__z6__kontor__tomilolt')))
		c['i'].update(st.aggregate(ec5 = Sum('zardal__z6__kontor__tomilolt')))

		c['i'].update(st.filter(zardal__z6__kontor__torol = 0).aggregate(ed1 = Sum('zardal__z6__kontor__surgaltiin_zardal')))
		c['i'].update(st.filter(zardal__z6__kontor__torol = 1).aggregate(ed2 = Sum('zardal__z6__kontor__surgaltiin_zardal')))
		c['i'].update(st.filter(zardal__z6__kontor__torol = 2).aggregate(ed3 = Sum('zardal__z6__kontor__surgaltiin_zardal')))
		c['i'].update(st.filter(zardal__z6__kontor__torol__in = [3,4,5]).aggregate(ed4 = Sum('zardal__z6__kontor__surgaltiin_zardal')))
		c['i'].update(st.aggregate(ed5 = Sum('zardal__z6__kontor__surgaltiin_zardal')))
		
		c['i'].update(st.filter(zardal__z6__kontor__torol = 0).aggregate(ee1 = Sum('zardal__z6__kontor__busad')))
		c['i'].update(st.filter(zardal__z6__kontor__torol = 1).aggregate(ee2 = Sum('zardal__z6__kontor__busad')))
		c['i'].update(st.filter(zardal__z6__kontor__torol = 2).aggregate(ee3 = Sum('zardal__z6__kontor__busad')))
		c['i'].update(st.filter(zardal__z6__kontor__torol__in = [3,4,5]).aggregate(ee4 = Sum('zardal__z6__kontor__busad')))
		c['i'].update(st.aggregate(ee5 = Sum('zardal__z6__kontor__busad')))
		
		c['i']['ef1'] = c['i']['ea1'] + c['i']['eb1'] + c['i']['ec1'] + c['i']['ed1'] + c['i']['ee1']
		c['i']['ef2'] = c['i']['ea2'] + c['i']['eb2'] + c['i']['ec2'] + c['i']['ed2'] + c['i']['ee2']
		c['i']['ef3'] = c['i']['ea3'] + c['i']['eb3'] + c['i']['ec3'] + c['i']['ed3'] + c['i']['ee3']
		c['i']['ef4'] = c['i']['ea4'] + c['i']['eb4'] + c['i']['ec4'] + c['i']['ed4'] + c['i']['ee4']
		c['i']['ef5'] = c['i']['ea5'] + c['i']['eb5'] + c['i']['ec5'] + c['i']['ed5'] + c['i']['ee5']
		

		c['i'].update(st.filter(zardal__z7__hodolmor_hamgaalal__torol = 0).aggregate(fa1 = Sum('zardal__z7__hodolmor_hamgaalal__ayulgui_ajillagaa')))
		c['i'].update(st.filter(zardal__z7__hodolmor_hamgaalal__torol = 1).aggregate(fa2 = Sum('zardal__z7__hodolmor_hamgaalal__ayulgui_ajillagaa')))
		c['i'].update(st.filter(zardal__z7__hodolmor_hamgaalal__torol = 2).aggregate(fa3 = Sum('zardal__z7__hodolmor_hamgaalal__ayulgui_ajillagaa')))
		c['i'].update(st.filter(zardal__z7__hodolmor_hamgaalal__torol__in = [3,4,5]).aggregate(fa4 = Sum('zardal__z7__hodolmor_hamgaalal__ayulgui_ajillagaa')))
		c['i'].update(st.aggregate(fa5 = Sum('zardal__z7__hodolmor_hamgaalal__ayulgui_ajillagaa')))
		
		c['i'].update(st.filter(zardal__z7__hodolmor_hamgaalal__torol = 0).aggregate(fb1 = Sum('zardal__z7__hodolmor_hamgaalal__eruul_ahui')))
		c['i'].update(st.filter(zardal__z7__hodolmor_hamgaalal__torol = 1).aggregate(fb2 = Sum('zardal__z7__hodolmor_hamgaalal__eruul_ahui')))
		c['i'].update(st.filter(zardal__z7__hodolmor_hamgaalal__torol = 2).aggregate(fb3 = Sum('zardal__z7__hodolmor_hamgaalal__eruul_ahui')))
		c['i'].update(st.filter(zardal__z7__hodolmor_hamgaalal__torol__in = [3,4,5]).aggregate(fb4 = Sum('zardal__z7__hodolmor_hamgaalal__eruul_ahui')))
		c['i'].update(st.aggregate(fb5 = Sum('zardal__z7__hodolmor_hamgaalal__eruul_ahui')))

		c['i'].update(st.filter(zardal__z7__hodolmor_hamgaalal__torol = 0).aggregate(fc1 = Sum('zardal__z7__hodolmor_hamgaalal__irgenii_hamgaalalt')))
		c['i'].update(st.filter(zardal__z7__hodolmor_hamgaalal__torol = 1).aggregate(fc2 = Sum('zardal__z7__hodolmor_hamgaalal__irgenii_hamgaalalt')))
		c['i'].update(st.filter(zardal__z7__hodolmor_hamgaalal__torol = 2).aggregate(fc3 = Sum('zardal__z7__hodolmor_hamgaalal__irgenii_hamgaalalt')))
		c['i'].update(st.filter(zardal__z7__hodolmor_hamgaalal__torol__in = [3,4,5]).aggregate(fc4 = Sum('zardal__z7__hodolmor_hamgaalal__irgenii_hamgaalalt')))
		c['i'].update(st.aggregate(fc5 = Sum('zardal__z7__hodolmor_hamgaalal__irgenii_hamgaalalt')))

		c['i'].update(st.filter(zardal__z7__hodolmor_hamgaalal__torol = 0).aggregate(fd1 = Sum('zardal__z7__hodolmor_hamgaalal__busad')))
		c['i'].update(st.filter(zardal__z7__hodolmor_hamgaalal__torol = 1).aggregate(fd2 = Sum('zardal__z7__hodolmor_hamgaalal__busad')))
		c['i'].update(st.filter(zardal__z7__hodolmor_hamgaalal__torol = 2).aggregate(fd3 = Sum('zardal__z7__hodolmor_hamgaalal__busad')))
		c['i'].update(st.filter(zardal__z7__hodolmor_hamgaalal__torol__in = [3,4,5]).aggregate(fd4 = Sum('zardal__z7__hodolmor_hamgaalal__busad')))
		c['i'].update(st.aggregate(fd5 = Sum('zardal__z7__hodolmor_hamgaalal__busad')))
		
		c['i']['fe1'] = c['i']['fa1'] + c['i']['fb1'] + c['i']['fc1'] + c['i']['fd1']
		c['i']['fe2'] = c['i']['fa2'] + c['i']['fb2'] + c['i']['fc2'] + c['i']['fd2']
		c['i']['fe3'] = c['i']['fa3'] + c['i']['fb3'] + c['i']['fc3'] + c['i']['fd3']
		c['i']['fe4'] = c['i']['fa4'] + c['i']['fb4'] + c['i']['fc4'] + c['i']['fd4']
		c['i']['fe5'] = c['i']['fa5'] + c['i']['fb5'] + c['i']['fc5'] + c['i']['fd5']


		c['i'].update(st.filter(zardal__z8__marketing__torol = 0).aggregate(ga1 = Sum('zardal__z8__marketing__medeelel_surtalchilgaa')))
		c['i'].update(st.filter(zardal__z8__marketing__torol = 1).aggregate(ga2 = Sum('zardal__z8__marketing__medeelel_surtalchilgaa')))
		c['i'].update(st.filter(zardal__z8__marketing__torol = 2).aggregate(ga3 = Sum('zardal__z8__marketing__medeelel_surtalchilgaa')))
		c['i'].update(st.filter(zardal__z8__marketing__torol__in = [3,4,5]).aggregate(ga4 = Sum('zardal__z8__marketing__medeelel_surtalchilgaa')))
		c['i'].update(st.aggregate(ga5 = Sum('zardal__z8__marketing__medeelel_surtalchilgaa')))
		
		c['i'].update(st.filter(zardal__z8__marketing__torol = 0).aggregate(gb1 = Sum('zardal__z8__marketing__surgalt')))
		c['i'].update(st.filter(zardal__z8__marketing__torol = 1).aggregate(gb2 = Sum('zardal__z8__marketing__surgalt')))
		c['i'].update(st.filter(zardal__z8__marketing__torol = 2).aggregate(gb3 = Sum('zardal__z8__marketing__surgalt')))
		c['i'].update(st.filter(zardal__z8__marketing__torol__in = [3,4,5]).aggregate(gb4 = Sum('zardal__z8__marketing__surgalt')))
		c['i'].update(st.aggregate(gb5 = Sum('zardal__z8__marketing__surgalt')))

		c['i'].update(st.filter(zardal__z8__marketing__torol = 0).aggregate(gc1 = Sum('zardal__z8__marketing__borluulalt_demjih_uramshuulal')))
		c['i'].update(st.filter(zardal__z8__marketing__torol = 1).aggregate(gc2 = Sum('zardal__z8__marketing__borluulalt_demjih_uramshuulal')))
		c['i'].update(st.filter(zardal__z8__marketing__torol = 2).aggregate(gc3 = Sum('zardal__z8__marketing__borluulalt_demjih_uramshuulal')))
		c['i'].update(st.filter(zardal__z8__marketing__torol__in = [3,4,5]).aggregate(gc4 = Sum('zardal__z8__marketing__borluulalt_demjih_uramshuulal')))
		c['i'].update(st.aggregate(gc5 = Sum('zardal__z8__marketing__borluulalt_demjih_uramshuulal')))

		c['i'].update(st.filter(zardal__z8__marketing__torol = 0).aggregate(gd1 = Sum('zardal__z8__marketing__shalgalt_batalgaajuulalt')))
		c['i'].update(st.filter(zardal__z8__marketing__torol = 1).aggregate(gd2 = Sum('zardal__z8__marketing__shalgalt_batalgaajuulalt')))
		c['i'].update(st.filter(zardal__z8__marketing__torol = 2).aggregate(gd3 = Sum('zardal__z8__marketing__shalgalt_batalgaajuulalt')))
		c['i'].update(st.filter(zardal__z8__marketing__torol__in = [3,4,5]).aggregate(gd4 = Sum('zardal__z8__marketing__shalgalt_batalgaajuulalt')))
		c['i'].update(st.aggregate(gd5 = Sum('zardal__z8__marketing__shalgalt_batalgaajuulalt')))

		c['i'].update(st.filter(zardal__z8__marketing__torol = 0).aggregate(ge1 = Sum('zardal__z8__marketing__busad')))
		c['i'].update(st.filter(zardal__z8__marketing__torol = 1).aggregate(ge2 = Sum('zardal__z8__marketing__busad')))
		c['i'].update(st.filter(zardal__z8__marketing__torol = 2).aggregate(ge3 = Sum('zardal__z8__marketing__busad')))
		c['i'].update(st.filter(zardal__z8__marketing__torol__in = [3,4,5]).aggregate(ge4 = Sum('zardal__z8__marketing__busad')))
		c['i'].update(st.aggregate(ge5 = Sum('zardal__z8__marketing__busad')))
		
		c['i']['gf1'] = c['i']['ga1'] + c['i']['gb1'] + c['i']['gc1'] + c['i']['gd1'] + c['i']['ge1']
		c['i']['gf2'] = c['i']['ga2'] + c['i']['gb2'] + c['i']['gc2'] + c['i']['gd2'] + c['i']['ge2']
		c['i']['gf3'] = c['i']['ga3'] + c['i']['gb3'] + c['i']['gc3'] + c['i']['gd3'] + c['i']['ge3']
		c['i']['gf4'] = c['i']['ga4'] + c['i']['gb4'] + c['i']['gc4'] + c['i']['gd4'] + c['i']['ge4']
		c['i']['gf5'] = c['i']['ga5'] + c['i']['gb5'] + c['i']['gc5'] + c['i']['gd5'] + c['i']['ge5']


		c['i'].update(st.filter(zardal__z9__laboratory__torol = 0).aggregate(ha1 = Sum('zardal__z9__laboratory__usnii_shinjilgee')))
		c['i'].update(st.filter(zardal__z9__laboratory__torol = 1).aggregate(ha2 = Sum('zardal__z9__laboratory__usnii_shinjilgee')))
		c['i'].update(st.filter(zardal__z9__laboratory__torol = 2).aggregate(ha3 = Sum('zardal__z9__laboratory__usnii_shinjilgee')))
		c['i'].update(st.filter(zardal__z9__laboratory__torol__in = [3,4,5]).aggregate(ha4 = Sum('zardal__z9__laboratory__usnii_shinjilgee')))
		c['i'].update(st.aggregate(ha5 = Sum('zardal__z9__laboratory__usnii_shinjilgee')))
		
		c['i'].update(st.filter(zardal__z9__laboratory__torol = 0).aggregate(hb1 = Sum('zardal__z9__laboratory__reactive_bodis')))
		c['i'].update(st.filter(zardal__z9__laboratory__torol = 1).aggregate(hb2 = Sum('zardal__z9__laboratory__reactive_bodis')))
		c['i'].update(st.filter(zardal__z9__laboratory__torol = 2).aggregate(hb3 = Sum('zardal__z9__laboratory__reactive_bodis')))
		c['i'].update(st.filter(zardal__z9__laboratory__torol__in = [3,4,5]).aggregate(hb4 = Sum('zardal__z9__laboratory__reactive_bodis')))
		c['i'].update(st.aggregate(hb5 = Sum('zardal__z9__laboratory__reactive_bodis')))

		c['i'].update(st.filter(zardal__z9__laboratory__torol = 0).aggregate(hc1 = Sum('zardal__z9__laboratory__shil_sav')))
		c['i'].update(st.filter(zardal__z9__laboratory__torol = 1).aggregate(hc2 = Sum('zardal__z9__laboratory__shil_sav')))
		c['i'].update(st.filter(zardal__z9__laboratory__torol = 2).aggregate(hc3 = Sum('zardal__z9__laboratory__shil_sav')))
		c['i'].update(st.filter(zardal__z9__laboratory__torol__in = [3,4,5]).aggregate(hc4 = Sum('zardal__z9__laboratory__shil_sav')))
		c['i'].update(st.aggregate(hc5 = Sum('zardal__z9__laboratory__shil_sav')))

		c['i'].update(st.filter(zardal__z9__laboratory__torol = 0).aggregate(hd1 = Sum('zardal__z9__laboratory__batalgaajuulalt_hyanalt')))
		c['i'].update(st.filter(zardal__z9__laboratory__torol = 1).aggregate(hd2 = Sum('zardal__z9__laboratory__batalgaajuulalt_hyanalt')))
		c['i'].update(st.filter(zardal__z9__laboratory__torol = 2).aggregate(hd3 = Sum('zardal__z9__laboratory__batalgaajuulalt_hyanalt')))
		c['i'].update(st.filter(zardal__z9__laboratory__torol__in = [3,4,5]).aggregate(hd4 = Sum('zardal__z9__laboratory__batalgaajuulalt_hyanalt')))
		c['i'].update(st.aggregate(hd5 = Sum('zardal__z9__laboratory__batalgaajuulalt_hyanalt')))

		c['i'].update(st.filter(zardal__z9__laboratory__torol = 0).aggregate(he1 = Sum('zardal__z9__laboratory__busad')))
		c['i'].update(st.filter(zardal__z9__laboratory__torol = 1).aggregate(he2 = Sum('zardal__z9__laboratory__busad')))
		c['i'].update(st.filter(zardal__z9__laboratory__torol = 2).aggregate(he3 = Sum('zardal__z9__laboratory__busad')))
		c['i'].update(st.filter(zardal__z9__laboratory__torol__in = [3,4,5]).aggregate(he4 = Sum('zardal__z9__laboratory__busad')))
		c['i'].update(st.aggregate(he5 = Sum('zardal__z9__laboratory__busad')))
		
		
		c['i']['hf1'] = c['i']['ha1'] + c['i']['hb1'] + c['i']['hc1'] + c['i']['hd1'] + c['i']['he1']
		c['i']['hf2'] = c['i']['ha2'] + c['i']['hb2'] + c['i']['hc2'] + c['i']['hd2'] + c['i']['he2']
		c['i']['hf3'] = c['i']['ha3'] + c['i']['hb3'] + c['i']['hc3'] + c['i']['hd3'] + c['i']['he3']
		c['i']['hf4'] = c['i']['ha4'] + c['i']['hb4'] + c['i']['hc4'] + c['i']['hd4'] + c['i']['he4']
		c['i']['hf5'] = c['i']['ha5'] + c['i']['hb5'] + c['i']['hc5'] + c['i']['hd5'] + c['i']['he5']


		c['i'].update(st.filter(zardal__z10__guitsetgeh_udirdlaga__torol = 0).aggregate(ia1 = Sum('zardal__z10__guitsetgeh_udirdlaga__tsalin_ndsh')))
		c['i'].update(st.filter(zardal__z10__guitsetgeh_udirdlaga__torol = 1).aggregate(ia2 = Sum('zardal__z10__guitsetgeh_udirdlaga__tsalin_ndsh')))
		c['i'].update(st.filter(zardal__z10__guitsetgeh_udirdlaga__torol = 2).aggregate(ia3 = Sum('zardal__z10__guitsetgeh_udirdlaga__tsalin_ndsh')))
		c['i'].update(st.filter(zardal__z10__guitsetgeh_udirdlaga__torol__in = [3,4,5]).aggregate(ia4 = Sum('zardal__z10__guitsetgeh_udirdlaga__tsalin_ndsh')))
		c['i'].update(st.aggregate(ia5 = Sum('zardal__z10__guitsetgeh_udirdlaga__tsalin_ndsh')))
		
		c['i'].update(st.filter(zardal__z10__guitsetgeh_udirdlaga__torol = 0).aggregate(ib1 = Sum('zardal__z10__guitsetgeh_udirdlaga__alban_tomilolt')))
		c['i'].update(st.filter(zardal__z10__guitsetgeh_udirdlaga__torol = 1).aggregate(ib2 = Sum('zardal__z10__guitsetgeh_udirdlaga__alban_tomilolt')))
		c['i'].update(st.filter(zardal__z10__guitsetgeh_udirdlaga__torol = 2).aggregate(ib3 = Sum('zardal__z10__guitsetgeh_udirdlaga__alban_tomilolt')))
		c['i'].update(st.filter(zardal__z10__guitsetgeh_udirdlaga__torol__in = [3,4,5]).aggregate(ib4 = Sum('zardal__z10__guitsetgeh_udirdlaga__alban_tomilolt')))
		c['i'].update(st.aggregate(ib5 = Sum('zardal__z10__guitsetgeh_udirdlaga__alban_tomilolt')))

		c['i'].update(st.filter(zardal__z10__guitsetgeh_udirdlaga__torol = 0).aggregate(ic1 = Sum('zardal__z10__guitsetgeh_udirdlaga__shatahuun')))
		c['i'].update(st.filter(zardal__z10__guitsetgeh_udirdlaga__torol = 1).aggregate(ic2 = Sum('zardal__z10__guitsetgeh_udirdlaga__shatahuun')))
		c['i'].update(st.filter(zardal__z10__guitsetgeh_udirdlaga__torol = 2).aggregate(ic3 = Sum('zardal__z10__guitsetgeh_udirdlaga__shatahuun')))
		c['i'].update(st.filter(zardal__z10__guitsetgeh_udirdlaga__torol__in = [3,4,5]).aggregate(ic4 = Sum('zardal__z10__guitsetgeh_udirdlaga__shatahuun')))
		c['i'].update(st.aggregate(ic5 = Sum('zardal__z10__guitsetgeh_udirdlaga__shatahuun')))

		c['i'].update(st.filter(zardal__z10__guitsetgeh_udirdlaga__torol = 0).aggregate(id1 = Sum('zardal__z10__guitsetgeh_udirdlaga__alban_heregtsee')))
		c['i'].update(st.filter(zardal__z10__guitsetgeh_udirdlaga__torol = 1).aggregate(id2 = Sum('zardal__z10__guitsetgeh_udirdlaga__alban_heregtsee')))
		c['i'].update(st.filter(zardal__z10__guitsetgeh_udirdlaga__torol = 2).aggregate(id3 = Sum('zardal__z10__guitsetgeh_udirdlaga__alban_heregtsee')))
		c['i'].update(st.filter(zardal__z10__guitsetgeh_udirdlaga__torol__in = [3,4,5]).aggregate(id4 = Sum('zardal__z10__guitsetgeh_udirdlaga__alban_heregtsee')))
		c['i'].update(st.aggregate(id5 = Sum('zardal__z10__guitsetgeh_udirdlaga__alban_heregtsee')))

		c['i'].update(st.filter(zardal__z10__guitsetgeh_udirdlaga__torol = 0).aggregate(ie1 = Sum('zardal__z10__guitsetgeh_udirdlaga__busad')))
		c['i'].update(st.filter(zardal__z10__guitsetgeh_udirdlaga__torol = 1).aggregate(ie2 = Sum('zardal__z10__guitsetgeh_udirdlaga__busad')))
		c['i'].update(st.filter(zardal__z10__guitsetgeh_udirdlaga__torol = 2).aggregate(ie3 = Sum('zardal__z10__guitsetgeh_udirdlaga__busad')))
		c['i'].update(st.filter(zardal__z10__guitsetgeh_udirdlaga__torol__in = [3,4,5]).aggregate(ie4 = Sum('zardal__z10__guitsetgeh_udirdlaga__busad')))
		c['i'].update(st.aggregate(ie5 = Sum('zardal__z10__guitsetgeh_udirdlaga__busad')))
		
		
		c['i']['if1'] = c['i']['ia1'] + c['i']['ib1'] + c['i']['ic1'] + c['i']['id1'] + c['i']['ie1']
		c['i']['if2'] = c['i']['ia2'] + c['i']['ib2'] + c['i']['ic2'] + c['i']['id2'] + c['i']['ie2']
		c['i']['if3'] = c['i']['ia3'] + c['i']['ib3'] + c['i']['ic3'] + c['i']['id3'] + c['i']['ie3']
		c['i']['if4'] = c['i']['ia4'] + c['i']['ib4'] + c['i']['ic4'] + c['i']['id4'] + c['i']['ie4']
		c['i']['if5'] = c['i']['ia5'] + c['i']['ib5'] + c['i']['ic5'] + c['i']['id5'] + c['i']['ie5']


		c['i'].update(st.filter(zardal__z11__tuz__torol = 0).aggregate(ja1 = Sum('zardal__z11__tuz__tsalin_ndsh_tuz')))
		c['i'].update(st.filter(zardal__z11__tuz__torol = 1).aggregate(ja2 = Sum('zardal__z11__tuz__tsalin_ndsh_tuz')))
		c['i'].update(st.filter(zardal__z11__tuz__torol = 2).aggregate(ja3 = Sum('zardal__z11__tuz__tsalin_ndsh_tuz')))
		c['i'].update(st.filter(zardal__z11__tuz__torol__in = [3,4,5]).aggregate(ja4 = Sum('zardal__z11__tuz__tsalin_ndsh_tuz')))
		c['i'].update(st.aggregate(ja5 = Sum('zardal__z11__tuz__tsalin_ndsh_tuz')))

		c['i'].update(st.filter(zardal__z11__tuz__torol = 0).aggregate(jb1 = Sum('zardal__z11__tuz__alban_heregtsee_tuz')))
		c['i'].update(st.filter(zardal__z11__tuz__torol = 1).aggregate(jb2 = Sum('zardal__z11__tuz__alban_heregtsee_tuz')))
		c['i'].update(st.filter(zardal__z11__tuz__torol = 2).aggregate(jb3 = Sum('zardal__z11__tuz__alban_heregtsee_tuz')))
		c['i'].update(st.filter(zardal__z11__tuz__torol__in = [3,4,5]).aggregate(jb4 = Sum('zardal__z11__tuz__alban_heregtsee_tuz')))
		c['i'].update(st.aggregate(jb5 = Sum('zardal__z11__tuz__alban_heregtsee_tuz')))

		c['i'].update(st.filter(zardal__z11__tuz__torol = 0).aggregate(jc1 = Sum('zardal__z11__tuz__busad')))
		c['i'].update(st.filter(zardal__z11__tuz__torol = 1).aggregate(jc2 = Sum('zardal__z11__tuz__busad')))
		c['i'].update(st.filter(zardal__z11__tuz__torol = 2).aggregate(jc3 = Sum('zardal__z11__tuz__busad')))
		c['i'].update(st.filter(zardal__z11__tuz__torol__in = [3,4,5]).aggregate(jc4 = Sum('zardal__z11__tuz__busad')))
		c['i'].update(st.aggregate(jc5 = Sum('zardal__z11__tuz__busad')))
		
		
		c['i']['jd1'] = c['i']['ja1'] + c['i']['jb1'] + c['i']['jc1']
		c['i']['jd2'] = c['i']['ja2'] + c['i']['jb2'] + c['i']['jc2']
		c['i']['jd3'] = c['i']['ja3'] + c['i']['jb3'] + c['i']['jc3']
		c['i']['jd4'] = c['i']['ja4'] + c['i']['jb4'] + c['i']['jc4']
		c['i']['jd5'] = c['i']['ja5'] + c['i']['jb5'] + c['i']['jc5']


		c['i'].update(st.filter(zardal__z12__undsen_horongiin_elegdel__torol = 0).aggregate(ka1 = Sum('zardal__z12__undsen_horongiin_elegdel__ul_hodloh_horongo')))
		c['i'].update(st.filter(zardal__z12__undsen_horongiin_elegdel__torol = 1).aggregate(ka2 = Sum('zardal__z12__undsen_horongiin_elegdel__ul_hodloh_horongo')))
		c['i'].update(st.filter(zardal__z12__undsen_horongiin_elegdel__torol = 2).aggregate(ka3 = Sum('zardal__z12__undsen_horongiin_elegdel__ul_hodloh_horongo')))
		c['i'].update(st.filter(zardal__z12__undsen_horongiin_elegdel__torol__in = [3,4,5]).aggregate(ka4 = Sum('zardal__z12__undsen_horongiin_elegdel__ul_hodloh_horongo')))
		c['i'].update(st.aggregate(ka5 = Sum('zardal__z12__undsen_horongiin_elegdel__ul_hodloh_horongo')))

		c['i'].update(st.filter(zardal__z12__undsen_horongiin_elegdel__torol = 0).aggregate(kb1 = Sum('zardal__z12__undsen_horongiin_elegdel__tehnik_tonog_tohooromj')))
		c['i'].update(st.filter(zardal__z12__undsen_horongiin_elegdel__torol = 1).aggregate(kb2 = Sum('zardal__z12__undsen_horongiin_elegdel__tehnik_tonog_tohooromj')))
		c['i'].update(st.filter(zardal__z12__undsen_horongiin_elegdel__torol = 2).aggregate(kb3 = Sum('zardal__z12__undsen_horongiin_elegdel__tehnik_tonog_tohooromj')))
		c['i'].update(st.filter(zardal__z12__undsen_horongiin_elegdel__torol__in = [3,4,5]).aggregate(kb4 = Sum('zardal__z12__undsen_horongiin_elegdel__tehnik_tonog_tohooromj')))
		c['i'].update(st.aggregate(kb5 = Sum('zardal__z12__undsen_horongiin_elegdel__tehnik_tonog_tohooromj')))

		c['i'].update(st.filter(zardal__z12__undsen_horongiin_elegdel__torol = 0).aggregate(kc1 = Sum('zardal__z12__undsen_horongiin_elegdel__tavilga_ed_hogshil')))
		c['i'].update(st.filter(zardal__z12__undsen_horongiin_elegdel__torol = 1).aggregate(kc2 = Sum('zardal__z12__undsen_horongiin_elegdel__tavilga_ed_hogshil')))
		c['i'].update(st.filter(zardal__z12__undsen_horongiin_elegdel__torol = 2).aggregate(kc3 = Sum('zardal__z12__undsen_horongiin_elegdel__tavilga_ed_hogshil')))
		c['i'].update(st.filter(zardal__z12__undsen_horongiin_elegdel__torol__in = [3,4,5]).aggregate(kc4 = Sum('zardal__z12__undsen_horongiin_elegdel__tavilga_ed_hogshil')))
		c['i'].update(st.aggregate(kc5 = Sum('zardal__z12__undsen_horongiin_elegdel__tavilga_ed_hogshil')))
		
		c['i'].update(st.filter(zardal__z12__undsen_horongiin_elegdel__torol = 0).aggregate(kd1 = Sum('zardal__z12__undsen_horongiin_elegdel__busad')))
		c['i'].update(st.filter(zardal__z12__undsen_horongiin_elegdel__torol = 1).aggregate(kd2 = Sum('zardal__z12__undsen_horongiin_elegdel__busad')))
		c['i'].update(st.filter(zardal__z12__undsen_horongiin_elegdel__torol = 2).aggregate(kd3 = Sum('zardal__z12__undsen_horongiin_elegdel__busad')))
		c['i'].update(st.filter(zardal__z12__undsen_horongiin_elegdel__torol__in = [3,4,5]).aggregate(kd4 = Sum('zardal__z12__undsen_horongiin_elegdel__busad')))
		c['i'].update(st.aggregate(kd5 = Sum('zardal__z12__undsen_horongiin_elegdel__busad')))
		
		
		c['i']['ke1'] = c['i']['ka1'] + c['i']['kb1'] + c['i']['kc1'] + c['i']['kd1']
		c['i']['ke2'] = c['i']['ka2'] + c['i']['kb2'] + c['i']['kc2'] + c['i']['kd2']
		c['i']['ke3'] = c['i']['ka3'] + c['i']['kb3'] + c['i']['kc3'] + c['i']['kd3']
		c['i']['ke4'] = c['i']['ka4'] + c['i']['kb4'] + c['i']['kc4'] + c['i']['kd4']
		c['i']['ke5'] = c['i']['ka5'] + c['i']['kb5'] + c['i']['kc5'] + c['i']['kd5']


		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol = 0).aggregate(la1 = Sum('zardal__z13__gadnii_uilchilgee__zohitsuulah_uilchilgeenii_hols')))
		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol = 1).aggregate(la2 = Sum('zardal__z13__gadnii_uilchilgee__zohitsuulah_uilchilgeenii_hols')))
		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol = 2).aggregate(la3 = Sum('zardal__z13__gadnii_uilchilgee__zohitsuulah_uilchilgeenii_hols')))
		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol__in = [3,4,5]).aggregate(la4 = Sum('zardal__z13__gadnii_uilchilgee__zohitsuulah_uilchilgeenii_hols')))
		c['i'].update(st.aggregate(la5 = Sum('zardal__z13__gadnii_uilchilgee__zohitsuulah_uilchilgeenii_hols')))

		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol = 0).aggregate(lb1 = Sum('zardal__z13__gadnii_uilchilgee__turees')))
		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol = 1).aggregate(lb2 = Sum('zardal__z13__gadnii_uilchilgee__turees')))
		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol = 2).aggregate(lb3 = Sum('zardal__z13__gadnii_uilchilgee__turees')))
		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol__in = [3,4,5]).aggregate(lb4 = Sum('zardal__z13__gadnii_uilchilgee__turees')))
		c['i'].update(st.aggregate(lb5 = Sum('zardal__z13__gadnii_uilchilgee__turees')))

		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol = 0).aggregate(lc1 = Sum('zardal__z13__gadnii_uilchilgee__audit')))
		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol = 1).aggregate(lc2 = Sum('zardal__z13__gadnii_uilchilgee__audit')))
		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol = 2).aggregate(lc3 = Sum('zardal__z13__gadnii_uilchilgee__audit')))
		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol__in = [3,4,5]).aggregate(lc4 = Sum('zardal__z13__gadnii_uilchilgee__audit')))
		c['i'].update(st.aggregate(lc5 = Sum('zardal__z13__gadnii_uilchilgee__audit')))
		
		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol = 0).aggregate(ld1 = Sum('zardal__z13__gadnii_uilchilgee__program_hangamj')))
		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol = 1).aggregate(ld2 = Sum('zardal__z13__gadnii_uilchilgee__program_hangamj')))
		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol = 2).aggregate(ld3 = Sum('zardal__z13__gadnii_uilchilgee__program_hangamj')))
		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol__in = [3,4,5]).aggregate(ld4 = Sum('zardal__z13__gadnii_uilchilgee__program_hangamj')))
		c['i'].update(st.aggregate(ld5 = Sum('zardal__z13__gadnii_uilchilgee__program_hangamj')))

		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol = 0).aggregate(le1 = Sum('zardal__z13__gadnii_uilchilgee__banknii_uilchilgee')))
		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol = 1).aggregate(le2 = Sum('zardal__z13__gadnii_uilchilgee__banknii_uilchilgee')))
		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol = 2).aggregate(le3 = Sum('zardal__z13__gadnii_uilchilgee__banknii_uilchilgee')))
		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol__in = [3,4,5]).aggregate(le4 = Sum('zardal__z13__gadnii_uilchilgee__banknii_uilchilgee')))
		c['i'].update(st.aggregate(le5 = Sum('zardal__z13__gadnii_uilchilgee__banknii_uilchilgee')))

		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol = 0).aggregate(lf1 = Sum('zardal__z13__gadnii_uilchilgee__shuuhiin_uilchilgee')))
		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol = 1).aggregate(lf2 = Sum('zardal__z13__gadnii_uilchilgee__shuuhiin_uilchilgee')))
		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol = 2).aggregate(lf3 = Sum('zardal__z13__gadnii_uilchilgee__shuuhiin_uilchilgee')))
		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol__in = [3,4,5]).aggregate(lf4 = Sum('zardal__z13__gadnii_uilchilgee__shuuhiin_uilchilgee')))
		c['i'].update(st.aggregate(lf5 = Sum('zardal__z13__gadnii_uilchilgee__shuuhiin_uilchilgee')))

		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol = 0).aggregate(lg1 = Sum('zardal__z13__gadnii_uilchilgee__busad')))
		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol = 1).aggregate(lg2 = Sum('zardal__z13__gadnii_uilchilgee__busad')))
		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol = 2).aggregate(lg3 = Sum('zardal__z13__gadnii_uilchilgee__busad')))
		c['i'].update(st.filter(zardal__z13__gadnii_uilchilgee__torol__in = [3,4,5]).aggregate(lg4 = Sum('zardal__z13__gadnii_uilchilgee__busad')))
		c['i'].update(st.aggregate(lg5 = Sum('zardal__z13__gadnii_uilchilgee__busad')))
		
		
		c['i']['lh1'] = c['i']['la1'] + c['i']['lb1'] + c['i']['lc1'] + c['i']['ld1'] + c['i']['le1'] + c['i']['lf1'] + c['i']['lg1']
		c['i']['lh2'] = c['i']['la2'] + c['i']['lb2'] + c['i']['lc2'] + c['i']['ld2'] + c['i']['le2'] + c['i']['lf2'] + c['i']['lg2']
		c['i']['lh3'] = c['i']['la3'] + c['i']['lb3'] + c['i']['lc3'] + c['i']['ld3'] + c['i']['le3'] + c['i']['lf3'] + c['i']['lg3']
		c['i']['lh4'] = c['i']['la4'] + c['i']['lb4'] + c['i']['lc4'] + c['i']['ld4'] + c['i']['le4'] + c['i']['lf4'] + c['i']['lg4']
		c['i']['lh5'] = c['i']['la5'] + c['i']['lb5'] + c['i']['lc5'] + c['i']['ld5'] + c['i']['le5'] + c['i']['lf5'] + c['i']['lg5']


		c['i'].update(st.filter(zardal__z14__tatvar__torol = 0).aggregate(ma1 = Sum('zardal__z14__tatvar__gazriin_tatvar')))
		c['i'].update(st.filter(zardal__z14__tatvar__torol = 1).aggregate(ma2 = Sum('zardal__z14__tatvar__gazriin_tatvar')))
		c['i'].update(st.filter(zardal__z14__tatvar__torol = 2).aggregate(ma3 = Sum('zardal__z14__tatvar__gazriin_tatvar')))
		c['i'].update(st.filter(zardal__z14__tatvar__torol__in = [3,4,5]).aggregate(ma4 = Sum('zardal__z14__tatvar__gazriin_tatvar')))
		c['i'].update(st.aggregate(ma5 = Sum('zardal__z14__tatvar__gazriin_tatvar')))

		c['i'].update(st.filter(zardal__z14__tatvar__torol = 0).aggregate(mb1 = Sum('zardal__z14__tatvar__ul_hodloh_horongiin_tatvar')))
		c['i'].update(st.filter(zardal__z14__tatvar__torol = 1).aggregate(mb2 = Sum('zardal__z14__tatvar__ul_hodloh_horongiin_tatvar')))
		c['i'].update(st.filter(zardal__z14__tatvar__torol = 2).aggregate(mb3 = Sum('zardal__z14__tatvar__ul_hodloh_horongiin_tatvar')))
		c['i'].update(st.filter(zardal__z14__tatvar__torol__in = [3,4,5]).aggregate(mb4 = Sum('zardal__z14__tatvar__ul_hodloh_horongiin_tatvar')))
		c['i'].update(st.aggregate(mb5 = Sum('zardal__z14__tatvar__ul_hodloh_horongiin_tatvar')))

		c['i'].update(st.filter(zardal__z14__tatvar__torol = 0).aggregate(mc1 = Sum('zardal__z14__tatvar__teevriin_heregsliin_tatvar')))
		c['i'].update(st.filter(zardal__z14__tatvar__torol = 1).aggregate(mc2 = Sum('zardal__z14__tatvar__teevriin_heregsliin_tatvar')))
		c['i'].update(st.filter(zardal__z14__tatvar__torol = 2).aggregate(mc3 = Sum('zardal__z14__tatvar__teevriin_heregsliin_tatvar')))
		c['i'].update(st.filter(zardal__z14__tatvar__torol__in = [3,4,5]).aggregate(mc4 = Sum('zardal__z14__tatvar__teevriin_heregsliin_tatvar')))
		c['i'].update(st.aggregate(mc5 = Sum('zardal__z14__tatvar__teevriin_heregsliin_tatvar')))
		
		c['i'].update(st.filter(zardal__z14__tatvar__torol = 0).aggregate(md1 = Sum('zardal__z14__tatvar__busad')))
		c['i'].update(st.filter(zardal__z14__tatvar__torol = 1).aggregate(md2 = Sum('zardal__z14__tatvar__busad')))
		c['i'].update(st.filter(zardal__z14__tatvar__torol = 2).aggregate(md3 = Sum('zardal__z14__tatvar__busad')))
		c['i'].update(st.filter(zardal__z14__tatvar__torol__in = [3,4,5]).aggregate(md4 = Sum('zardal__z14__tatvar__busad')))
		c['i'].update(st.aggregate(md5 = Sum('zardal__z14__tatvar__busad')))
		
		
		c['i']['me1'] = c['i']['ma1'] + c['i']['mb1'] + c['i']['mc1'] + c['i']['md1']
		c['i']['me2'] = c['i']['ma2'] + c['i']['mb2'] + c['i']['mc2'] + c['i']['md2']
		c['i']['me3'] = c['i']['ma3'] + c['i']['mb3'] + c['i']['mc3'] + c['i']['md3']
		c['i']['me4'] = c['i']['ma4'] + c['i']['mb4'] + c['i']['mc4'] + c['i']['md4']
		c['i']['me5'] = c['i']['ma5'] + c['i']['mb5'] + c['i']['mc5'] + c['i']['md5']

		c['i'].update(st.filter(zardal__z15__daatgal__torol = 0).aggregate(na1 = Sum('zardal__z15__daatgal__teevriin_heregsliin_daatgal')))
		c['i'].update(st.filter(zardal__z15__daatgal__torol = 1).aggregate(na2 = Sum('zardal__z15__daatgal__teevriin_heregsliin_daatgal')))
		c['i'].update(st.filter(zardal__z15__daatgal__torol = 2).aggregate(na3 = Sum('zardal__z15__daatgal__teevriin_heregsliin_daatgal')))
		c['i'].update(st.filter(zardal__z15__daatgal__torol__in = [3,4,5]).aggregate(na4 = Sum('zardal__z15__daatgal__teevriin_heregsliin_daatgal')))
		c['i'].update(st.aggregate(na5 = Sum('zardal__z15__daatgal__teevriin_heregsliin_daatgal')))

		c['i'].update(st.filter(zardal__z15__daatgal__torol = 0).aggregate(nb1 = Sum('zardal__z15__daatgal__ul_hodloh_horongiin_daatgal')))
		c['i'].update(st.filter(zardal__z15__daatgal__torol = 1).aggregate(nb2 = Sum('zardal__z15__daatgal__ul_hodloh_horongiin_daatgal')))
		c['i'].update(st.filter(zardal__z15__daatgal__torol = 2).aggregate(nb3 = Sum('zardal__z15__daatgal__ul_hodloh_horongiin_daatgal')))
		c['i'].update(st.filter(zardal__z15__daatgal__torol__in = [3,4,5]).aggregate(nb4 = Sum('zardal__z15__daatgal__ul_hodloh_horongiin_daatgal')))
		c['i'].update(st.aggregate(nb5 = Sum('zardal__z15__daatgal__ul_hodloh_horongiin_daatgal')))

		c['i'].update(st.filter(zardal__z15__daatgal__torol = 0).aggregate(nc1 = Sum('zardal__z15__daatgal__alijchdiin_hurimtlagdsan_daatgal')))
		c['i'].update(st.filter(zardal__z15__daatgal__torol = 1).aggregate(nc2 = Sum('zardal__z15__daatgal__alijchdiin_hurimtlagdsan_daatgal')))
		c['i'].update(st.filter(zardal__z15__daatgal__torol = 2).aggregate(nc3 = Sum('zardal__z15__daatgal__alijchdiin_hurimtlagdsan_daatgal')))
		c['i'].update(st.filter(zardal__z15__daatgal__torol__in = [3,4,5]).aggregate(nc4 = Sum('zardal__z15__daatgal__alijchdiin_hurimtlagdsan_daatgal')))
		c['i'].update(st.aggregate(nc5 = Sum('zardal__z15__daatgal__alijchdiin_hurimtlagdsan_daatgal')))
		
		c['i'].update(st.filter(zardal__z15__daatgal__torol = 0).aggregate(nd1 = Sum('zardal__z15__daatgal__busad')))
		c['i'].update(st.filter(zardal__z15__daatgal__torol = 1).aggregate(nd2 = Sum('zardal__z15__daatgal__busad')))
		c['i'].update(st.filter(zardal__z15__daatgal__torol = 2).aggregate(nd3 = Sum('zardal__z15__daatgal__busad')))
		c['i'].update(st.filter(zardal__z15__daatgal__torol__in = [3,4,5]).aggregate(nd4 = Sum('zardal__z15__daatgal__busad')))
		c['i'].update(st.aggregate(nd5 = Sum('zardal__z15__daatgal__busad')))
		
		
		c['i']['ne1'] = c['i']['na1'] + c['i']['nb1'] + c['i']['nc1'] + c['i']['nd1']
		c['i']['ne2'] = c['i']['na2'] + c['i']['nb2'] + c['i']['nc2'] + c['i']['nd2']
		c['i']['ne3'] = c['i']['na3'] + c['i']['nb3'] + c['i']['nc3'] + c['i']['nd3']
		c['i']['ne4'] = c['i']['na4'] + c['i']['nb4'] + c['i']['nc4'] + c['i']['nd4']
		c['i']['ne5'] = c['i']['na5'] + c['i']['nb5'] + c['i']['nc5'] + c['i']['nd5']

		
		c['i'].update(st.filter(zardal__z17__ajilchid_niigmiin__torol = 0).aggregate(pa1 = Sum('zardal__z17__ajilchid_niigmiin__hoolnii_hongololt')))
		c['i'].update(st.filter(zardal__z17__ajilchid_niigmiin__torol = 1).aggregate(pa2 = Sum('zardal__z17__ajilchid_niigmiin__hoolnii_hongololt')))
		c['i'].update(st.filter(zardal__z17__ajilchid_niigmiin__torol = 2).aggregate(pa3 = Sum('zardal__z17__ajilchid_niigmiin__hoolnii_hongololt')))
		c['i'].update(st.filter(zardal__z17__ajilchid_niigmiin__torol__in = [3,4,5]).aggregate(pa4 = Sum('zardal__z17__ajilchid_niigmiin__hoolnii_hongololt')))
		c['i'].update(st.aggregate(pa5 = Sum('zardal__z17__ajilchid_niigmiin__hoolnii_hongololt')))

		c['i'].update(st.filter(zardal__z17__ajilchid_niigmiin__torol = 0).aggregate(pb1 = Sum('zardal__z17__ajilchid_niigmiin__unaanii_hongololt')))
		c['i'].update(st.filter(zardal__z17__ajilchid_niigmiin__torol = 1).aggregate(pb2 = Sum('zardal__z17__ajilchid_niigmiin__unaanii_hongololt')))
		c['i'].update(st.filter(zardal__z17__ajilchid_niigmiin__torol = 2).aggregate(pb3 = Sum('zardal__z17__ajilchid_niigmiin__unaanii_hongololt')))
		c['i'].update(st.filter(zardal__z17__ajilchid_niigmiin__torol__in = [3,4,5]).aggregate(pb4 = Sum('zardal__z17__ajilchid_niigmiin__unaanii_hongololt')))
		c['i'].update(st.aggregate(pb5 = Sum('zardal__z17__ajilchid_niigmiin__unaanii_hongololt')))

		c['i'].update(st.filter(zardal__z17__ajilchid_niigmiin__torol = 0).aggregate(pc1 = Sum('zardal__z17__ajilchid_niigmiin__tuleenii_hongololt')))
		c['i'].update(st.filter(zardal__z17__ajilchid_niigmiin__torol = 1).aggregate(pc2 = Sum('zardal__z17__ajilchid_niigmiin__tuleenii_hongololt')))
		c['i'].update(st.filter(zardal__z17__ajilchid_niigmiin__torol = 2).aggregate(pc3 = Sum('zardal__z17__ajilchid_niigmiin__tuleenii_hongololt')))
		c['i'].update(st.filter(zardal__z17__ajilchid_niigmiin__torol__in = [3,4,5]).aggregate(pc4 = Sum('zardal__z17__ajilchid_niigmiin__tuleenii_hongololt')))
		c['i'].update(st.aggregate(pc5 = Sum('zardal__z17__ajilchid_niigmiin__tuleenii_hongololt')))
		
		c['i'].update(st.filter(zardal__z17__ajilchid_niigmiin__torol = 0).aggregate(pd1 = Sum('zardal__z17__ajilchid_niigmiin__tetgemj_tuslamj')))
		c['i'].update(st.filter(zardal__z17__ajilchid_niigmiin__torol = 1).aggregate(pd2 = Sum('zardal__z17__ajilchid_niigmiin__tetgemj_tuslamj')))
		c['i'].update(st.filter(zardal__z17__ajilchid_niigmiin__torol = 2).aggregate(pd3 = Sum('zardal__z17__ajilchid_niigmiin__tetgemj_tuslamj')))
		c['i'].update(st.filter(zardal__z17__ajilchid_niigmiin__torol__in = [3,4,5]).aggregate(pd4 = Sum('zardal__z17__ajilchid_niigmiin__tetgemj_tuslamj')))
		c['i'].update(st.aggregate(pd5 = Sum('zardal__z17__ajilchid_niigmiin__tetgemj_tuslamj')))
		
		c['i'].update(st.filter(zardal__z17__ajilchid_niigmiin__torol = 0).aggregate(pe1 = Sum('zardal__z17__ajilchid_niigmiin__busad')))
		c['i'].update(st.filter(zardal__z17__ajilchid_niigmiin__torol = 1).aggregate(pe2 = Sum('zardal__z17__ajilchid_niigmiin__busad')))
		c['i'].update(st.filter(zardal__z17__ajilchid_niigmiin__torol = 2).aggregate(pe3 = Sum('zardal__z17__ajilchid_niigmiin__busad')))
		c['i'].update(st.filter(zardal__z17__ajilchid_niigmiin__torol__in = [3,4,5]).aggregate(pe4 = Sum('zardal__z17__ajilchid_niigmiin__busad')))
		c['i'].update(st.aggregate(pe5 = Sum('zardal__z17__ajilchid_niigmiin__busad')))
		
		
		c['i']['pf1'] = c['i']['pa1'] + c['i']['pb1'] + c['i']['pc1'] + c['i']['pd1'] + c['i']['pe1']
		c['i']['pf2'] = c['i']['pa2'] + c['i']['pb2'] + c['i']['pc2'] + c['i']['pd2'] + c['i']['pe2']
		c['i']['pf3'] = c['i']['pa3'] + c['i']['pb3'] + c['i']['pc3'] + c['i']['pd3'] + c['i']['pe3']
		c['i']['pf4'] = c['i']['pa4'] + c['i']['pb4'] + c['i']['pc4'] + c['i']['pd4'] + c['i']['pe4']
		c['i']['pf5'] = c['i']['pa5'] + c['i']['pb5'] + c['i']['pc5'] + c['i']['pd5'] + c['i']['pe5']

		c['i'].update(st.filter(zardal__z18__horongo_oruulalt__torol = 0).aggregate(qa1 = Sum('zardal__z18__horongo_oruulalt__urt_hugatsaat_zeel')))
		c['i'].update(st.filter(zardal__z18__horongo_oruulalt__torol = 1).aggregate(qa2 = Sum('zardal__z18__horongo_oruulalt__urt_hugatsaat_zeel')))
		c['i'].update(st.filter(zardal__z18__horongo_oruulalt__torol = 2).aggregate(qa3 = Sum('zardal__z18__horongo_oruulalt__urt_hugatsaat_zeel')))
		c['i'].update(st.filter(zardal__z18__horongo_oruulalt__torol__in = [3,4,5]).aggregate(qa4 = Sum('zardal__z18__horongo_oruulalt__urt_hugatsaat_zeel')))
		c['i'].update(st.aggregate(qa5 = Sum('zardal__z18__horongo_oruulalt__urt_hugatsaat_zeel')))

		c['i'].update(st.filter(zardal__z18__horongo_oruulalt__torol = 0).aggregate(qb1 = Sum('zardal__z18__horongo_oruulalt__busad')))
		c['i'].update(st.filter(zardal__z18__horongo_oruulalt__torol = 1).aggregate(qb2 = Sum('zardal__z18__horongo_oruulalt__busad')))
		c['i'].update(st.filter(zardal__z18__horongo_oruulalt__torol = 2).aggregate(qb3 = Sum('zardal__z18__horongo_oruulalt__busad')))
		c['i'].update(st.filter(zardal__z18__horongo_oruulalt__torol__in = [3,4,5]).aggregate(qb4 = Sum('zardal__z18__horongo_oruulalt__busad')))
		c['i'].update(st.aggregate(qb5 = Sum('zardal__z18__horongo_oruulalt__busad')))
		
		c['i']['qc1'] = c['i']['qa1'] + c['i']['qb1']
		c['i']['qc2'] = c['i']['qa2'] + c['i']['qb2']
		c['i']['qc3'] = c['i']['qa3'] + c['i']['qb3']
		c['i']['qc4'] = c['i']['qa4'] + c['i']['qb4']
		c['i']['qc5'] = c['i']['qa5'] + c['i']['qb5']

		return c
	except:
		return None
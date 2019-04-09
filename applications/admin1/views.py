#!/usr/bin/env python
# -*- coding:utf-8 -*-
import jsonpickle
from django.views.generic import FormView, TemplateView, UpdateView
from applications.app.views import LoginRequired
from applications.app.models import Ajiltan
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy

class Admin(LoginRequired, TemplateView):
	permission = 500
	super_permission = 501
	template_name = 'adminuser.html'

	def get_context_data(self, *args, **kwargs):
		context = super(Admin, self).get_context_data(*args, **kwargs)
		paginator = Paginator(Ajiltan.objects.filter(baiguullaga = context['baiguullaga'], status = True).order_by('-id'), 10)
		page = self.request.GET.get('page')
		
		try:
			context['ajiltan'] = paginator.page(page)
		except PageNotAnInteger:
			context['ajiltan'] = paginator.page(1)
		except EmptyPage:
			context['ajiltan'] = paginator.page(paginator.num_pages)
		return context

class EmployeeCreate(LoginRequired, FormView):
	permission = 500
	super_permission = 501
	form_class = ZZAForm
	template_name = 'create.html'
	success_url = reverse_lazy('admin')

	def dispatch(self, request, *args, **kwargs):
		self.user = jsonpickle.decode(request.session['user'])
		return super(EmployeeCreate, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(EmployeeCreate, self).get_form_kwargs()
		kwargs.update({'baiguullaga': self.user.user_id.baiguullaga})
		return kwargs

	def form_valid(self, form):
		employee = form.save(commit = False)
		employee.baiguullaga = self.user.user_id.baiguullaga
		employee.save()
		return super(EmployeeCreate, self).form_valid(form)

class EmployeeUpdate(LoginRequired, UpdateView):
	permission = 500
	super_permission = 501
	model = Ajiltan
	form_class = ZZAForm
	template_name = 'create.html'
	success_url = reverse_lazy('admin')

	def dispatch(self, request, *args, **kwargs):
		self.user = jsonpickle.decode(request.session['user'])
		return super(EmployeeUpdate, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(EmployeeUpdate, self).get_form_kwargs()
		kwargs.update({'baiguullaga': self.user.user_id.baiguullaga})
		return kwargs

	def form_valid(self, form):
		employee = form.save(commit = False)
		employee.baiguullaga = self.user.user_id.baiguullaga
		employee.save()
		return super(EmployeeUpdate, self).form_valid(form)

class TasagCreate(LoginRequired, FormView):
	permission = 500
	super_permission = 501
	template_name = 'tasag.html'
	form_class = BaiguullagaTasagForm
	success_url = reverse_lazy('admin')

	def dispatch(self, request, *args, **kwargs):
		self.user = jsonpickle.decode(request.session['user'])
		return super(TasagCreate, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		tasaglist = form.cleaned_data['dep_name']
		if TasagList.objects.filter(name = tasaglist):
			tasag = TasagList.objects.get(name = tasaglist)
		else:
			tasag = TasagList.objects.create(name = tasaglist)
		employee = form.save(commit = False)
		employee.baiguullaga = self.user.user_id.baiguullaga
		employee.dep_name = tasag
		employee.status = True
		employee.save()
		return super(TasagCreate, self).form_valid(form)

class TushaalCreate(LoginRequired, FormView):
	permission = 500
	super_permission = 501
	template_name = 'tasag.html'
	form_class = TushaalForm
	success_url = reverse_lazy('admin')

	def dispatch(self, request, *args, **kwargs):
		self.user = jsonpickle.decode(request.session['user'])
		return super(TushaalCreate, self).dispatch(request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(TushaalCreate, self).get_form_kwargs()
		kwargs.update({'baiguullaga': self.user.user_id.baiguullaga})
		return kwargs

	def form_valid(self, form):
		tushaallist = form.cleaned_data['position_name']
		if AlbanTushaalList.objects.filter(name = tushaallist):
			tushaal = AlbanTushaalList.objects.get(name = tushaallist)
		else:
			tushaal = AlbanTushaalList.objects.create(name = tushaallist)
		employee = form.save(commit = False)
		employee.baiguullaga = self.user.user_id.baiguullaga
		employee.position_name = tushaal
		employee.status = True
		employee.save()
		return super(TushaalCreate, self).form_valid(form)
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import jsonpickle
from django.core.context_processors import csrf
from django.views.generic import FormView, TemplateView, ListView
from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseForbidden
from applications.app.forms import *
from applications.app.models import *
from django.shortcuts import render_to_response
from django.utils import timezone
from django.template import RequestContext
from django.forms.utils import ErrorList
from django.core.exceptions import PermissionDenied
from applications.director.models import *
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_messages.models import Message
from datetime import timedelta



class LoginRequired(object):
	perm_code_names = []
	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			self.user = User.objects.get(id = request.user.id)
			if ZZ.objects.filter(id = self.user.user_id.baiguullaga.id):
				self.baiguullaga = ZZ.objects.filter(id = self.user.user_id.baiguullaga.id)
			else:
				self.baiguullaga = TZE.objects.get(id = self.user.user_id.baiguullaga.id)
		return super(LoginRequired, self).dispatch(request, *args, **kwargs)
			#has_permission = False
			#perms_list = self.get_permissions()
			#for user_p in self.user.user_permissions.all():
			#	if user_p in perms_list:
			#		has_permission = True
			#for group in self.user.groups.all():
			#	for p in group.permissions.all():
			#		if p in perms_list:
			#			has_permission = True
			#if has_permission:
			#	return super(LoginRequired, self).dispatch(request, *args, **kwargs)
			#else:
			#	raise PermissionDenied
	def get_permissions(self):
		perm_list = []
		for p in self.perm_code_names:
			perm = Permission.objects.get(codename = p)
			perm_list.append(perm)
		return perm_list


	def get_context_data(self, **kwargs):
		context = super(LoginRequired, self).get_context_data(**kwargs)
		context['user'] = self.user
		context['baiguullaga'] = self.baiguullaga
		context['unread_message'] = Message.objects.filter(recipient = self.user, read_at = None)
		if self.user.notifications.unread().count()<10:
			read_nots =  self.user.notifications.read().filter(timestamp__gte = timezone.now() - timedelta(days=3))
			context['notifications'] = self.user.notifications.unread() | read_nots
		else:
			context['notifications'] = self.user.notifications.unread()
		return context

class Notifications_list(LoginRequired, ListView):
	perm_code_names = ['tze_baiguullaga_menu_view']
	template_name = 'tze_notifications.html'

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			self.user = User.objects.get(id = request.user.id)
			if ZZ.objects.filter(id = self.user.user_id.baiguullaga.id):
				self.baiguullaga = ZZ.objects.get(id = self.user.user_id.baiguullaga.id)
				if self.user.user_id.tasag.dep_name == u'Үнэ тарифын алба':
					self.template_name = 'uta/uta_notifications.html'
				elif  self.user.user_id.tasag.dep_name == u'Тусгай зөвшөөрлийн алба':
					self.template_name = 'tza/tza_notifications.html'
				elif  self.user.user_id.tasag.dep_name == u'Эрх зүй, мэдээлэл, захиргааны алба':
					self.template_name = 'hzm/hzm_notifications.html'
		return super(Notifications_list, self).dispatch(request, *args, **kwargs)

	def get_queryset(self):
		queryset = self.user.notifications.all()
		return queryset

class Login(FormView):
	form_class = LoginForm
	template_name = "login.html"
	success_url = '/home/'

	def get(self, *args):
		if self.request.user.is_authenticated():
			return HttpResponseRedirect('/home/')
		return super(Login, self).get(*args)

	def form_valid(self, form):
		user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
		if user:
			login(self.request, user)
		return super(Login, self).form_valid(form)

	
def Logout(request):
	if request.user.is_authenticated():
		logout(request)
	return HttpResponseRedirect('/')

class HomeView(TemplateView):
	
	template_name = 'home.html'

	def dispatch(self, request):
		if self.request.user:
			if User.objects.filter(id = self.request.user.id):
				self.user = User.objects.get(id = self.request.user.id)
				if ZZ.objects.filter(id = self.user.user_id.baiguullaga.id):
					self.baiguullaga = ZZ.objects.get(id = self.user.user_id.baiguullaga.id)
					if self.user.user_id.tasag.dep_name == u'Үнэ тарифын алба':
						return HttpResponseRedirect('/uta/sez/')
					elif  self.user.user_id.tasag.dep_name == u'Тусгай зөвшөөрлийн алба':
						return HttpResponseRedirect('/tza/huseltuud/')
					elif self.user.user_id.tasag.dep_name == u'Эрх зүй, мэдээлэл, захиргааны алба':
						return HttpResponseRedirect('/hzm/')
				else:
					self.baiguullaga = TZE.objects.get(id = self.user.user_id.baiguullaga.id)
					return HttpResponseRedirect('/engineering/baiguullaga/')
			else:
				return HttpResponseRedirect('/')
		else:
			return HttpResponseRedirect('/')

class HandahErh(FormView):
	form_class = TZE_handah_huselt_form
	template_name = 'handaherh.html'
	
	def form_valid(self, form):
		a = form.save()
		create_tailan(a['baiguullaga'])
		return render_to_response('batalgaajuulalt.html', {'bai':a['baiguullaga'], 'director':a['z']})


def create_tailan(tze):
	for i in range(3):
		z = Zardal.objects.create(status = True)
		o = Orlogo.objects.create(status = True)
		s = Sudalgaa.objects.create(tze = tze, orlogo = o, zardal = z, status = True, yvts = u'Хийгдэж байна', year = int(timezone.now().year) - int(i+1))


def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

def handler500(request):
	response = render_to_response('500.html', {}, context_instance=RequestContext(request))
	response.status_code = 500
	return response

def get_object_or_none(model):
	try:
		return model
	except model.DoesNotExist:
		return None

def get_true_or_false(args):
	try:
		if args:
			return True
	except:
		return False

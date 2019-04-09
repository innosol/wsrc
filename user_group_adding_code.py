# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group
from applications.app.models import User, Ajiltan

group_tze = Group.objects.filter(name__icontains="тзэ")
users = User.objects.all()
ajiltan = Ajiltan.objects.all()

for a in ajiltan:
	a.save()

for u in users:
	u.groups = group_tze

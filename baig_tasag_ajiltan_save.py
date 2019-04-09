from applications.app.models import TZE, Ajiltan, Tasag, AlbanTushaal

tzes = TZE.objects.all()
for i in tzes:
	i.save()

objects = Ajiltan.objects.all()
for i in objects:
	i.save()

objects = Tasag.objects.all()
for i in objects:
	i.save()

objects = AlbanTushaal.objects.all()
for i in objects:
	i.save()
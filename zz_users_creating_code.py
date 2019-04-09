from applications.app.models import ZZ, Ajiltan, User

zz = ZZ.objects.all().first()

ajilchid = Ajiltan.objects.filter(baiguullaga = zz)

for a in ajilchid:
	u = User(username = a.e_mail, is_active = True, user_id = a)
	u.set_password('12345')
	u.save()
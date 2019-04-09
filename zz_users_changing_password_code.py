from applications.app.models import ZZ, Ajiltan, User

zz = ZZ.objects.all().first()

ajilchid = Ajiltan.objects.filter(baiguullaga = zz)

for a in ajilchid:
	user = User.objects.get(user_id=a)
	print a.emp_name
	password = input("Enter password: ")
	user.set_password(password)
	user.save()
	print "saved"

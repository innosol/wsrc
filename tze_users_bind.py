

from applications.app.models import TZE, Ajiltan, User, TZE_Users_bind

tze_qs = TZE.objects.exclude(reg_num = '2076675')
for tze in tze_qs:
	tze_ajiltan = Ajiltan.objects.filter(baiguullaga = tze)[0]
	tze_ajiltan.save()
	user = tze_ajiltan.user
	b = TZE_Users_bind(tze = tze, user_zahiral = user)
	b.status=True
	b.save()
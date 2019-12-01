from django.contrib.auth.models import User
from ..models import Group

# publicなUserとGroupを取得する。
def get_public():
	public_user = User.objects.filter(username='public').first()
	public_group = Group.objects.filter(owner=public_user).first()
	return (public_user, public_group)
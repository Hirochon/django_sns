from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import message

from django.contrib.auth.decorators import login_required

@login_required(login_url='/admin/login/')
def index1(request):
	# publicのuserを取得
	(public_user, public_group) = get_public()

	# POST送信時の処理

# publicなUserとGroupを取得する。
def get_public():
	public_user = User.objects.filter(username='public').first()
	public_group = Group.objects.filter(owner=public_user).first()
	return (public_user, public_group)

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth.decorators import login_required

@loogin_required(login_url='/admin/login/')
def add1(request):
	# 追加するUserを取得
	add_name = request.GET['name']
	add_user = User.objects.filter(username=add_name).first()
	# Userが本人だった場合の処理
	if add_user == request.user:
		messages.info(request, "自分自身をFriendに追加することはできません。")
		return redirect(to='/sns')
	#publicの取得
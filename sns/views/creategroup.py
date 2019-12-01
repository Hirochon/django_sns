from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages

from ..models import Group

from django.contrib.auth.decorators import login_required

@login_required(login_url='/admin/login/')
def creategroup1(request):
	# Groupを作り、Userとtitleを設定して保存する。
	if request.method == 'POST':
		gp = Group()
		gp.owner = request.user
		gp.title = request.POST['group_name']
		gp.save()
		message.info(request, '新しいグループを作成しました。')
		return redirect(to='/sns/groups')
		
	# POSTありきのプログラムを回避
	else:
		return redirect(to='/sns/groups')
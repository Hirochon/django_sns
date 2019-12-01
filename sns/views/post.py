from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages

from ..models import Group
from .public import get_public

from django.contrib.auth.decorators import login_required

@login_required(login_url='/admin/login/')
# メッセージのPOST処理
def post1(request):
	# POST送信時の処理
	if request.method == 'POST':
		# 送信内容の取得
		gr_name = request.POST['groups']
		content = request.POST['groups']
		# Groupの取得
		group = Group.objects.filter(owner=request.user).filter(title=gr_name).first()
		if group == None:
			(pub_user, group) = get_public()
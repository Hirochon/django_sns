from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages

from ..models import Group, Friend, Message
from ..forms import SearchForm, GroupCheckForm
from .public import get_public
from .gp_message import get_your_group_message

from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required(login_url='/admin/login/')
def index1(request):
	# publicのuserを取得
	(public_user, public_group) = get_public()

	# POST送信時の処理
	if request.method == 'POST':
		# Groupのチェックを更新したときの処理
		if request.method['mode'] == '__check_form__':
			# フォームの用意
			searchform = SearchForm()
			checkform = GroupCheckForm(request.user, request.POST)
			#チェックされたGroup名をリストにまとめる
			glist = []
			for item in request.POST.getlist('groups'):
				glist.append(item)
			# Messageの取得
			message = get_your_group_message(request.user, glist, None)

		# Groupメニューを変更したときの処理
		if request.method['mode'] == '__search_form__':
			# フォームの用意
			searchform = SearchForm(request.POST)
			checkform = GroupCheckForm(request.user)
			# Groupリストを取得
			gps = Group.objects.filter(owner=request.user)
			glist = [public_group]
			for item in gps:
				glist.append(item)
			# Messageの取得
			messages = get_your_group_message(request.user, glist, request.POST['search'])

	# GETアクセス時の処理
	else:
		#フォームの用意
		searchform = SearchForm()
		checkform = GroupCheckForm(request.user)
		# Groupのリストを取得
		gps = Group.objects.filter(owner=request.user)
		glist = [public_group]
		for item in gps:
			glist.append(item)
		# メッセージの取得
		messages = get_your_group_message(request.user, glist, None)
		
	# 共通処理
	params = {
		'login_user' : request.user,
		'contents' : messages,
		'check_form' : checkform,
		'search_form' : searchform,
	}
	return render(request, 'sns/index.html', params)

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages

from ..models import Group, Friend, Message
from ..forms import SearchForm, GroupCheckForm
from .public import get_public

from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required(login_url='/admin/login/')
def index1(request):
	# publicのuserを取得
	(public_user, public_group) = get_public()

	# POST送信時の処理
	if request.method == 'POST':
		# Groupのチェックを更新したときの処理
		if request.POST['mode'] == "__check_form__":
			# フォームの用意
			searchform = SearchForm()
			checkform = GroupCheckForm(request.user, request.POST)
			#チェックされたGroup名をリストにまとめる
			glist = []
			for item in request.POST.getlist('groups'):
				glist.append(item)
			# Messageの取得
			messages = get_your_group_message(request.user, glist, None)

		# Groupメニューを変更したときの処理
		if request.POST['mode'] == '__search_form__':
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


# 指定されたグループ及び検索文字によるMessageの取得
def get_your_group_message(owner, glist, find):
	# publicの取得
	(public_user, public_group) = get_public()
	# チェックされたGroupの取得
	groups = Group.objects.filter(Q(owner = owner) | Q(owner = public_user)).filter(title__in=glist)
	# Groupに含まれるFriendを取得
	me_friends = Friend.objects.filter(group__in=groups)
	# FriendのUserをリストにまとめる
	me_users = []
	for f in me_friends:
		me_users.append(f.user)
	#UserリストのUserが作ったGroupの取得
	his_groups = Group.objects.filter(owner__in=me_users)
	his_friends = Friend.objects.filter(user=owner).filter(group__in=his_groups)
	me_groups = []
	for hf in his_friends:
		me_groups.append(hf.group)
	# groupがgroupsに含まれているか、me_groupsに含まれるMessageの取得
	if find == None:
		messages = Message.objects.filter(Q(group__in=groups) | Q(group__in=me_groups))[:100]
	else:
		messages = Message.objects.filter(Q(group__in=groups) | Q(group__in=me_groups)).filter(content__contains=find)[:100]
	return messages
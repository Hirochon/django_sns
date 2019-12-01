from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages

from ..models import Friend, Group
from ..forms import GroupSelectForm, FriendsForm, CreateGroupForm

from django.contrib.auth.decorators import login_required

@login_required(login_url='/admin/login/')
def groups1(request):
	# 自分が登録したFriendを取得
	friends = Friend.objects.filter(owner=request.user)

	#POST送信時の処理
	if request.method == 'POST':

		# Groupsメニュー選択肢の処理
		if request.POST['mode'] == '__groups_form__':
			# 選択したGroup名を取得
			sel_group = request.POST['groups']
			# Groupを取得
			gp = Group.objects.filter(owner=request.user).filter(title=sel_group).first()
			# Groupに含まれるFriendを取得
			fds = Friend.objects.filter(owner=request.user).filter(group=gp)
			# Friendのuserリストをまとめる
			vlist = []
			for item in fds:
				vlist.append(item.user.username)
			# フォームの用意
			groupsform = GroupSelectForm(request.user, request.POST)
			friendsform = FriendsForm(request.user, friends=friends, vals=vlist)
		
		# Friendsのチェック更新時の処理
		if request.POST['mode'] == '__friends_form__':
			# 選択したGrouoの取得
			sel_group = request.POST['group']
			group_pbj = Group.objects.filter(title=sel_group).first()
			# チェックしたFriendsを取得
			sel_fds = request.POST.getlist('friends')
			# FriendsのUserを取得
			sel_users = User.objects.filter(owner=request.user).filter(user__in=sel_users)
			# 全てのFriendにGroupを設定し、保存する
			vlist = []
			for item in fds:
				item.group = group_obj
				item.save()
				vlist.append(item.user.username)
			# メッセージを設定
			messages.success(request, 'チェックされたFriendを' + sel_group + 'に登録しました。')
			# フォームの用意
			groupsform = GroupSelectForm(request.user, {'groups':sel_group})
			friendsform = FriendsForm(request.user, friends=friends, vals=vlist)

	# Getアクセス時の処理
	else:
		# フォームの用意
		groupsform = GroupSelectForm(request.user)
		friendsform =FriendsForm(request.user, friends=friends, vals=[])
		sel_group = '-'

	# 共通処理
	createform = CreateGroupForm()
	params = {
		'login_user':request.user,
		'groups_form':groupsform,
		'friends_form':friendsform,
		'create_form':createform,
		'group':sel_group,
	}
	return render(request, 'sns/groups.html', params)
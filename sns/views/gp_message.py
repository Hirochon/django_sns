from django.db.models import Q
from django.contrib import messages

from ..models import Group, Friend, Message
from .public import get_public

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
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages

from ..forms import PostForm
from ..models import Group, Message
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
		# Messageを作成し設定して保存
		msg = Message()
		msg.owner = request.user
		msg.group = group
		msg.content = content
		msg.save()
		# メッセージを設定
		messages.success(request, '新しいメッセージを投稿しました！')
		return redirect(to='/sns')
	
	# GETアクセス時の処理
	else:

		form = PostForm(request.user)

	# 共通処理
	params = {
		'login_user':request.user,
		'form':form,
	}
	return render(request, 'sns/post.html', params)
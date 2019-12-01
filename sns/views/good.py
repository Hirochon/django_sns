from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages

from ..models import Message, Good

from django.contrib.auth.decorators import login_required

# goodボタンの処理
@login_required(login_url='/admin/login/')
def good1(request):
	# goodするMessageの取得
	good_msg = Message.objects.get(id=good_id)
	# 自分がメッセージにGoodした数を調べる
	is_good = Good.objects.filter(owner=request.user).filter(message=good_msg).count()
	# ゼロより大きければ既にgood済み
	if is_good > 0:
		messages.success(request, '既にメッセージにはGoodしています。')
		return redrect(to='/sns')
	
	# Messageのgood_countを1増やす
	good_msg.good_count += 1
	good_msg.save()
	#Goodを作成し、設定して保存
	good = Good()
	good.owner = request.user
	good.message = good_msg
	good.save()
	#メッセージを設定
	messages.success(request, 'メッセージにGoodしました！')
	return redirect(to='/sns')
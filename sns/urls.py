from django.urls import path
from .views import index,groups,add,creategroup,post,share,good

urlpatterns = [
	path('', index.index1, name='index'),
	path('groups/', groups.groups1, name='groups'),
	path('add/', add.add1, name='add'),
	path('creategroup/', creategroup.creategroup1, name='creategroup'),
	path('post/', post.post1, name='post'),
	path('share/<int:share_id>', share.share1, name='share'),
	path('good/<int:good_id>', good.good1, name='good'),
]
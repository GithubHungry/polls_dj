from django.urls import path

from blog import views

app_name = 'blog'
urlpatterns = [
	path('', views.PostListView.as_view(), name='post_list'),
	path('<slug:slug>/share', views.post_share, name='post_share'),
	path('<slug:slug>/<int:year>/<int:month>/<int:day>/', views.post_detail, name='post_detail'),
]

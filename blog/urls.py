from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    # path('', views.PostListView.as_view(), name ='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name="post_share"),
    path('create/', views.create_post, name='create_post'),
    path('<int:post_id>/update', views.UpdatePostView, name='update_post'),
    path('<int:post_id>/delete', views.DeletePostView, name='delete_post'),
    path('like/<int:post_id>', views.LikeView, name='like_post'),
    path('search/', views.search, name = 'search'),

]


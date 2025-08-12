from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('create-post', views.create_post, name='create_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('logout/', views.logout_view, name='logout'),
        path('my-comments/', views.superuser_comments, name='superuser_comments'),
        path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('like-post', views.like_post, name = 'like-post'),
    path('delete-post', views.delete_post, name = 'delete-post'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name = 'logout'),
    path('signup', views.signup, name='signup'),
    path('create-outfit/', views.create_outfit, name='create-outfit'),
    path('outfits/', views.outfit_list, name='outfit_list')
]
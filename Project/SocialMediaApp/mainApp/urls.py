from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('signup',views.signUpPage,name='signUpPage'),
    path('signin',views.signIn,name='signIn'),
    path('home',views.home,name='home'),
    path('settings',views.settingsPage,name='settingsPage'),
    path('Logout',views.logout,name='logout'),
    path('upload',views.upload,name='upload'),
    path('like_post',views.like_post,name='like_post'),
    path('getProfile/<str:pk>',views.getProfile,name='getProfile'),
    path('follow',views.FollowUser,name='FollowUser'),
    path('search',views.search,name='search'),
    path('myProfile',views.myProfile,name='myProfile'),
    path('delete',views.deletePost,name='deletePost'),
]

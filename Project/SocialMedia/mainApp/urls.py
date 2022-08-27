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
]
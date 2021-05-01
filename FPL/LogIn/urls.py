from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name ='index'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name = 'signup'),
    path('loginasadmin',views.loginasadmin,name = 'loginasadmin'),
    path('signout',views.signout,name='signout'),
    path('help',views.help,name='help',)
]

from django.urls import path
from . import views
urlpatterns = [
    path('loginasadminpage',views.loginasadminpage,name='loginasadminpage'),
    path('userlogin',views.userlogin,name='userlogin'),
    path('insertplayer',views.insertplayer,name='insertplayer'),
    path('insertschedule',views.insertschedule,name='insertschedule'),
    path('updateresult',views.updateresult,name='updateresult'),
    path('admininsert',views.admininsert,name='admininsert'),
    path('updateteamresult',views.updateteamresult,name='updateteamresult'),
    path('updateplayerstat',views.updateplayerstat,name='updateplayerstat'),
    path('addadmin',views.addadmin,name='addadmin'),
    path('adminadd',views.adminadd,name='adminadd'),
    path('pick_gweekshow',views.pick_gweekshow,name='pick_gweekshow'),
    path('showfix',views.showfix,name='showfix'),
]

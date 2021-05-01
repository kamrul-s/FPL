from django.urls import path
from . import views

urlpatterns = [
    path('pick_team',views.pick_team,name ='pick_team'),
    path('captain',views.captain,name = 'captain'),
    path('pick_team2',views.pick_team2,name ='pick_team2'),
    path('home',views.home,name='home'),
    path('myteam',views.myteam,name='myteam'),
    path('points',views.points,name='points'),
    path('showpoints',views.showpoints,name='showpoints'),
]
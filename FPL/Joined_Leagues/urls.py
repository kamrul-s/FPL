from django.urls import path
from . import views

urlpatterns = [
    path('leagues',views.leagues,name='leagues'),
    path('manage_leagues',views.manage_leagues,name ='manage_leagues'),
]
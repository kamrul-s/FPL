from django.urls import path
from . import views

urlpatterns = [
    path('details',views.details,name ='details'),
    path('squad_selection',views.squad_selection,name = 'squad_selection'),
]
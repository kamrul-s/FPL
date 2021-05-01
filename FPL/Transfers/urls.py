from django.urls import path
from . import views

urlpatterns = [
    path('transfers',views.transfers,name ='transfers'),
    path('make_transfers',views.make_transfers,name = 'make_transfers'),
    path('viewhistory',views.viewhistory,name='viewhistory'),
]
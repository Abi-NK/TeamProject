from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('data', views.data, name='data'),
    path('getsummary', views.get_summary, name='getsummary'),
    path('getorders', views.get_orders, name='getorders'),
    path('gettables', views.get_tables, name='gettables'),
    path('managermenu', views.show_menu, name='managermenu'),
]

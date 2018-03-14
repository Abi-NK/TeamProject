from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('data', views.data, name='data'),
    path('employee', views.employee, name='employee'),
    path('getsummary', views.get_summary, name='getsummary'),
    path('getorders', views.get_orders, name='getorders'),
    path('gettables', views.get_tables, name='gettables'),
    path('getstock', views.get_stock, name='getstock'),
    path('getassignments', views.get_assignments, name='getassignments'),
    path('managermenu', views.adjust_menu, name='managermenu'),
    path('waiterassignments', views.waiter_assignments, name='waiterassignments'),
]

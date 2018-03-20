from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('getordersconfirm', views.get_orders_confirm, name='getordersconfirm'),
    path('getorderscancel', views.get_orders_cancel, name='getorderscancel'),
    path('getordersdelivery', views.get_orders_delivery, name='getordersdelivery'),
    path('getordersunpaid', views.get_orders_unpaid, name='getordersunpaid'),
    path('getoccupiedseating', views.get_occupied_seating, name='getoccupiedseating'),
    path('getalerts', views.get_alerts, name="getalerts"),
    path('gettables', views.get_tables, name="gettables"),
    path('getseating', views.get_seating, name="getseating"),
    path('getorderspaid', views.get_orders_paid, name='getorderspaid'),
]

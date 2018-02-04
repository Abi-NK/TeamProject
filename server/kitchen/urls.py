from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('readyorders', views.ready_orders, name='readyorders'),
    path('orders', views.orders, name='orders'),
    path('getorders', views.get_orders, name='getorders'),
    path('confirmorder', views.confirm_order, name='confirmorder'),
]

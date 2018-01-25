from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('makeorder', views.make_order, name='makeorder'),
    path('orderstatus', views.order_status, name='orderstatus'),
    path('readyorders', views.ready_orders, name='readyorders'),
    path('orders', views.orders, name='orders'),
]
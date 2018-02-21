from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('makeorder', views.make_order, name='makeorder'),
    path('readyorders', views.ready_orders, name='readyorders'),
    path('orders', views.orders, name='orders'),
    path('getorders', views.get_orders, name='getorders'),
    path('getordershtml', views.get_orders_html, name='getordershtml'),
    path('confirmorder', views.confirm_order, name='confirmorder'),
    path('requesthelp', views.request_help, name='requesthelp'),
    path('deliveries', views.deliveries, name='deliveries'),
]

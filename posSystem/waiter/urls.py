from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('makeorder', views.make_order, name='makeorder'),
    path('readyorders', views.ready_orders, name='readyorders'),
    path('getorders', views.get_orders, name='getorders'),
    path('confirmorder', views.confirm_order, name='confirmorder'),
    path('requesthelp', views.request_help, name='requesthelp'),
    path('cancelhelp', views.cancel_help, name='cancelhelp'),
    path('deliveries', views.deliveries, name='deliveries'),
]

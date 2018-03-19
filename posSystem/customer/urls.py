from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('getorderextra', views.get_order_extra, name='getorderextra'),
    path('cancelorderextraitem', views.cancel_order_extra_item, name='cancelorderextraitem'),
    path('takeseat', views.take_seat, name='takeseat'),
    path('payment', views.payment, name='payment'),
    path('takeseat', views.take_seat, name='takeseat'),
    path('statuses', views.statuses, name='statuses'),
    path('getOrderInfo', views.getOrderInfo, name='getOrderInfo')
]

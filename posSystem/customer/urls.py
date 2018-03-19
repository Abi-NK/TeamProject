from django.urls import path
from . import views
import core.views as core_views

urlpatterns = [
    path('', views.index, name='index'),
    path('getorderextra', core_views.get_order_extra, name='getorderextra'),
    path('cancelorderextraitem', core_views.cancel_order_extra_item, name='cancelorderextraitem'),
    path('takeseat', core_views.take_seat, name='takeseat'),
    path('payment', views.payment, name='payment'),
    path('statuses', core_views.statuses, name='statuses'),
    path('getOrderInfo', views.getOrderInfo, name='getOrderInfo')
]

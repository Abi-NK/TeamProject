from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('makeorder', views.make_order, name='makeorder'),
    path('placeorderextra', views.place_order_extra, name='placeorderextra'),
    path('getordersconfirm', views.get_orders_confirm, name='getordersconfirm'),
    path('getorderscancel', views.get_orders_cancel, name='getorderscancel'),
    path('getordersdelivery', views.get_orders_delivery, name='getordersdelivery'),
    path('getordersunpaid', views.get_orders_unpaid, name='getordersunpaid'),
    path('getoccupiedseating', views.get_occupied_seating, name='getoccupiedseating'),
    path('getalerts', views.get_alerts, name="getalerts"),
    path('gettables', views.get_tables, name="gettables"),
    path('getwaiteronduty', views.get_waiter_on_duty, name='getwaiteronduty'),
    path('getwaiteroffduty', views.get_waiter_off_duty, name='getwaiteroffduty'),
    path('waiteronduty', views.waiter_on_duty, name='waiteronduty'),
    path('waiteroffduty', views.waiter_off_duty, name='waiteroffduty'),
    path('confirmorder', views.confirm_order, name='confirmorder'),
    path('cancelorder', views.cancel_order, name='cancelorder'),
    path('requesthelp', views.request_help, name='requesthelp'),
    path('cancelhelp', views.cancel_help, name='cancelhelp'),
    path('confirmPayment', views.confirm_payment, name='confirmPayment'),
    path('getorderspaid', views.get_orders_paid, name='getorderspaid'),
]

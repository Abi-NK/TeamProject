from django.urls import path

from . import views
import core.views as core_views

urlpatterns = [
    path('', views.index, name='index'),
    path('makeorder', core_views.make_order, name='makeorder'),
    path('placeorderextra', core_views.place_order_extra, name='placeorderextra'),
    path('getordersconfirm', views.get_orders_confirm, name='getordersconfirm'),
    path('getorderscancel', views.get_orders_cancel, name='getorderscancel'),
    path('getordersdelivery', views.get_orders_delivery, name='getordersdelivery'),
    path('getordersunpaid', views.get_orders_unpaid, name='getordersunpaid'),
    path('getoccupiedseating', views.get_occupied_seating, name='getoccupiedseating'),
    path('getalerts', views.get_alerts, name="getalerts"),
    path('gettables', views.get_tables, name="gettables"),
    path('getseating', views.get_seating, name="getseating"),
    path('assigntoseating', core_views.assign_to_seating, name='assigntoseating'),
    path('unassignfromseating', core_views.unassign_from_seating, name='unassignfromseating'),
    path('waiteronduty', core_views.waiter_on_duty, name='waiteronduty'),
    path('waiteroffduty', core_views.waiter_off_duty, name='waiteroffduty'),
    path('autoassign', core_views.auto_assign, name='autoassign'),
    path('confirmorder', core_views.confirm_order, name='confirmorder'),
    path('cancelorder', core_views.cancel_order, name='cancelorder'),
    path('removemenuitem', core_views.remove_menu_item, name='removemenuitem'),
    path('requesthelp', core_views.request_help, name='requesthelp'),
    path('cancelhelp', core_views.cancel_help, name='cancelhelp'),
    path('delayorder', core_views.delay_order, name='delayorder'),
    path('confirmPayment', core_views.confirm_payment, name='confirmPayment'),
    path('getorderspaid', views.get_orders_paid, name='getorderspaid'),
]

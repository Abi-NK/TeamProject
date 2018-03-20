from django.urls import include, path
from . import views

menu_model_urls = [
    path('managermenu', views.adjust_menu, name='managermenu'),
    path('removemenuitem', views.remove_menu_item, name='removemenuitem'),
]

order_model_html_urls = [
    path('kitchen_cards', views.html_kitchen_cards, name='kitchen_cards'),
]

order_model_urls = [
    path('html/', include(order_model_html_urls)),
    path('makeorder', views.make_order, name='makeorder'),
    path('confirmorder', views.confirm_order, name='confirmorder'),
    path('cancelorder', views.cancel_order, name='cancelorder'),
    path('readyDelivery', views.readyDelivery, name='readyDelivery'),
    path('delayorder', views.delay_order, name='delayorder'),
]

orderextra_model_urls = [
    path('placeorderextra', views.place_order_extra, name='placeorderextra'),
    path('getorderextra', views.get_order_extra, name='getorderextra'),
    path('cancelorderextraitem', views.cancel_order_extra_item, name='cancelorderextraitem'),
]

orderitem_model_urls = [

]

payment_model_urls = [
    path('confirmPayment', views.confirm_payment, name='confirmPayment'),
]

seating_model_urls = [
    path('takeseat', views.take_seat, name='takeseat'),
    path('assigntoseating', views.assign_to_seating, name='assigntoseating'),
    path('unassignfromseating', views.unassign_from_seating, name='unassignfromseating'),
    path('requesthelp', views.request_help, name='requesthelp'),
    path('cancelhelp', views.cancel_help, name='cancelhelp'),
]

waiter_model_urls = [
    path('waiteronduty', views.waiter_on_duty, name='waiteronduty'),
    path('waiteroffduty', views.waiter_off_duty, name='waiteroffduty'),
    path('getassignments', views.get_assignments, name='getassignments'),
    path('getwaiters', views.get_waiters, name='getwaiters'),
    path('autoassign', views.auto_assign, name='autoassign'),
]

urlpatterns = [
    path('menu/', include(menu_model_urls)),
    path('order/', include(order_model_urls)),
    path('orderextra/', include(orderextra_model_urls)),
    path('orderitem/', include(orderitem_model_urls)),
    path('payment/', include(payment_model_urls)),
    path('seating/', include(seating_model_urls)),
    path('waiter/', include(waiter_model_urls)),
]

from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # This is a regular expression. r'' means that it's a regular expression.
    # ^ represents the beginning and $ represents the end of a regular expression.
    # (?P<menu_id>) represents the the number that is assigned to each menu item. This
    # is used for making links to each item inside the menu. [0-9]+ is used to show
    # the amount of in

    path('takeseat', views.take_seat, name='takeseat'),
    path('payment', views.payment, name='payment'),
    path('takeseat', views.take_seat, name='takeseat'),
    path('statuses', views.statuses, name='statuses')
]

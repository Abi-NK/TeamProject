from django.urls import path

from . import views
import core.views as core_views

urlpatterns = [
    path('', views.index, name='index'),
    path('getorders', views.get_orders, name='getorders'),
    path('readyDelivery', core_views.readyDelivery, name='readyDelivery'),
]

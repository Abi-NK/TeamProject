from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('getorders', views.get_orders, name='getorders'),
]

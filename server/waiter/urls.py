from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('makeorder', views.makeorder, name='makeorder'),
    path('orderstatus', views.orderstatus, name='orderstatus'),
    path('readyorders', views.readyorders, name='readyorders'),
]
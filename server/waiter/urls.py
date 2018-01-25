from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/makeorder', views.index, name='makeorder'),
    path('/orderstatus', views.index, name='orderstatus'),
    path('/readyorders', views.index, name='readyorders'),
]
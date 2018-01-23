from django.urls import path
from django.conf.urls import url
from . import views # from current directory

urlpatterns = [
    # /music/
    path('', views.index, name='index'),
    # /music/123/
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
]

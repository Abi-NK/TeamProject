try:
    from django.urls import path
    from . import views
except ImportError:
    print("failed import")

urlpatterns = [
    path('', views.index, name='index'),
    path('payment', views.payment, name='payment'),
    path('statuses', views.statuses, name='statuses'),
]

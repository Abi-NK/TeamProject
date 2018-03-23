try:
    from django.urls import path
    from . import views
except ImportError:
    print("failed import")

urlpatterns = [
    path('', views.index, name='index'),
    path('data', views.data, name='data'),
    path('employee', views.employee, name='employee'),
    path('waiterassignments', views.waiter_assignments, name='waiterassignments'),
]

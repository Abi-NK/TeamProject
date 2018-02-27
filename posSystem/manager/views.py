from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test


def group_check(user):
    return user.username.startswith('manager')


@user_passes_test(group_check)
def index(request):
    """Return the manager page."""
    return render(request, 'manager/index.html')


@user_passes_test(group_check)
def data(request):
    """Return the live updating data page."""
    return render(request, 'manager/data.html')


@user_passes_test(group_check)
def get_summary(request):
    """Returns a summary of restaurant data in formatted HTML."""
    return render(request, 'manager/get/summary.html')

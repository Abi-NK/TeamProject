from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test


def group_check(user):
    return user.username.startswith('manager')


@user_passes_test(group_check)
def index(request):
    """Return the manager page."""
    return render(request, 'manager/index.html')

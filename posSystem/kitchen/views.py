from core.models import Order
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import user_passes_test


def group_check(user):
    return user.username.startswith('kitchen')


@ensure_csrf_cookie
@user_passes_test(group_check)
def index(request):
    """Return the kitchen page."""
    return render(request, 'kitchen/status.html', {'all_menu': Order.get_all_orders(all)})

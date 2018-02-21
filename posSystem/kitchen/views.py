from django.http import HttpResponse, JsonResponse
from waiter.models import Order
import json
from django.utils import timezone
from django.shortcuts import render
from django.core.serializers import serialize
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required, user_passes_test


def group_check(user):
    return user.username.startswith('kitchen')


@ensure_csrf_cookie
@user_passes_test(group_check)
def index(request):
    """Return the kitchen page."""
    return render(request, 'kitchen/status.html', {'all_menu': Order.get_all_orders(all)})


@require_http_methods(["GET"])
@login_required
def get_orders(request):
    """Return all orders as formatted HTML."""
    orders = Order.get_kitchen_orders(all)
    return render(request, "kitchen/ordercards.html", {'orders': orders})


@require_http_methods(["POST"])
@login_required
def readyDelivery(request):
    """sets the ready_delivery in the database to true."""
    order_id = json.loads(request.body.decode('utf-8'))["id"]
    Order.objects.get(pk=order_id).set_ready_delivery()
    return HttpResponse("Order ready, calling waiter")

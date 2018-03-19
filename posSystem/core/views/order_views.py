from django.http import HttpResponse
from django.shortcuts import render
from core.models import Order
import json
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required


def statuses(request):
    """..."""
    orders = Order.objects.all()
    return render(request, 'customer/statuses.html', {'orders': orders})


@require_http_methods(["POST"])
@login_required
def readyDelivery(request):
    """sets the ready_delivery in the database to true."""
    order_id = json.loads(request.body.decode('utf-8'))["id"]
    Order.objects.get(pk=order_id).set_ready_delivery()
    return HttpResponse("Order ready, calling waiter")

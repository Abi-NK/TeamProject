from django.http import HttpResponse
from django.shortcuts import render
from core.models import OrderExtra, OrderItem, Seating
from django.views.decorators.http import require_http_methods
import json


@require_http_methods(["GET"])
def get_order_extra(request):
    """Return the suggested order items as formatted HTML."""
    try:
        order_extra = OrderExtra.active_objects.get(seating=Seating.occupied_objects.get(pk=request.session['seating_id']))
        return render(request, "customer/get/orderextra.html", {'order_extra': order_extra})
    except:
        return render(request, "customer/get/orderextra.html")


@require_http_methods(["POST"])
def cancel_order_extra_item(request):
    """Remove an OrderItem from an OrderExtra."""
    received_json = json.loads(request.body.decode('utf-8'))
    order_extra = OrderExtra.active_objects.get(pk=received_json["order_extra_id"])
    order_item = OrderItem.objects.get(pk=received_json["order_item_id"])
    order_extra.items.remove(order_item)
    if order_extra.items.count() == 0:
        order_extra.delete()
    return HttpResponse("received")

from django.http import HttpResponse
from django.shortcuts import render
from .models import Menu, Seating
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from waiter.models import Order, OrderItem, OrderExtra
import json


@ensure_csrf_cookie
def index(request):
    """Return the menu page."""
    context = {
        'all_menu': Menu.objects.all(),
    }
    if 'seating_label' in request.session:
        context['seating_label'] = request.session['seating_label']
    else:
        context['seating'] = Seating.available_objects.all()
    return render(request, 'customer/menu.html', context)


@require_http_methods(["GET"])
def get_order_extra(request):
    """Return the suggested order items as formatted HTML."""
    try:
        order_extra = OrderExtra.active_objects.get(seating=Seating.occupied_objects.get(pk=request.session['seating_id']))
        return render(request, "customer/get/orderextra.html", {'order_extra': order_extra})
    except:
        return render(request, "customer/get/orderextra.html")


@require_http_methods(["POST"])
def take_seat(request):
    """Marks the provided seating as unavailable in the database."""
    table_id = json.loads(request.body.decode('utf-8'))["tableID"]
    Seating.objects.get(pk=table_id).set_unavailable()
    request.session['seating_id'] = table_id
    request.session['seating_label'] = Seating.objects.get(pk=table_id).label
    return HttpResponse("received")


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


def statuses(request):
    """..."""
    orders = Order.objects.all()
    return render(request, 'customer/statuses.html', {'orders': orders})

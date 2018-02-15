from django.http import HttpResponse, JsonResponse
from .models import Order
from customer.models import Menu, Seating
import json
from django.utils import timezone
from django.shortcuts import render
from django.core.serializers import serialize
from django.views.decorators.http import require_http_methods


# list of orders that are ready is updated every time the page is accessed (refreshed)
def index(request):
    """Return the waiter index page."""
    unconfirmed_orders = Order.objects.filter(confirmed=False)
    undelivered_orders = Order.objects.filter(delivered=False, confirmed=True, ready_delivery=True)
    return render(request, "waiter/index.html", {'undelivered': Order.objects.filter(delivered=False),
                                                 'unconfirmed_orders': unconfirmed_orders,
                                                 'undelivered_orders': undelivered_orders})


def deliveries(request):
    """Return the waiter delivery page and confirm deliveries using django forms"""
    """Changes the order table when the delivered button has been pressed"""
    delivery = Order.objects.filter(confirmed=True, ready_delivery=True, delivered=False)
    if request.method == "POST":
        order_update = Order.objects.get(pk=request.POST['delivery_id'])
        order_update.delivered = True
        order_update.save()

    return render(request, "waiter/deliveries.html", {'delivery': delivery})


def orders(request):
    """Return the page for viewing all orders."""
    return render(request, "waiter/orders.html")


@require_http_methods(["GET"])
def get_orders(request):
    """Return all orders as JSON."""
    json = serialize('json', Order.get_not_confirmed_orders(all))
    return JsonResponse(json, safe=False)


@require_http_methods(["GET"])
def ready_orders(request):
    """Return all ready orders as JSON."""
    json = serialize('json', Order.objects.filter(confirmed=True))
    return JsonResponse(json, safe=False)


@require_http_methods(["POST"])
def make_order(request):
    """Create an order from the provided JSON."""
    Order.make_order(request)
    return HttpResponse("recieved")


@require_http_methods(["POST"])
def confirm_order(request):
    """Confirm the provided order in the database."""
    order_id = json.loads(request.body.decode('utf-8'))["id"]
    print("Recieved ID: " + str(order_id))
    order = Order.objects.get(pk=order_id)
    order.confirmed = True
    order.save()
    return HttpResponse("recieved")


@require_http_methods(["POST"])
def request_help(request):
    seating_id = json.loads(request.body.decode('utf-8'))["tableNumber"]
    Seating.objects.get(pk=seating_id).set_assistance_true()
    return HttpResponse("recieved")

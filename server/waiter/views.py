from django.http import HttpResponse, JsonResponse
from .models import Order
from customer.models import Menu
import json
from django.utils import timezone
from django.shortcuts import render
from django.core.serializers import serialize
from django.views.decorators.http import require_http_methods
from customer.views import seating

help_requested = []


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
    json = serialize('json', Order.objects.filter(confirmed=False))
    return JsonResponse(json, safe=False)


@require_http_methods(["GET"])
def ready_orders(request):
    """Return all ready orders as JSON."""
    json = serialize('json', Order.objects.filter(confirmed=True))
    return JsonResponse(json, safe=False)


@require_http_methods(["POST"])
def make_order(request):
    """Create an order from the provided JSON."""
    order_json = json.loads(request.body.decode('utf-8'))
    print("Recieved order: ", order_json)
    order_contents = [Menu.objects.get(pk=key) for key in order_json]
    total_price = sum([item.price * order_json[str(item.id)] for item in order_contents])
    Order(
        table="0",
        confirmed=False,
        time=timezone.now(),
        items="<br />\n".join(["%s %s" % (order_json[str(item.id)], str(item)) for item in order_contents]),
        cooking_instructions='none',
        purchase_method='none',
        total_price=total_price,
        delivered=False,
        table_assistance=False
    ).save(force_insert=True)
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
    table_id = json.loads(request.body.decode('utf-8'))["tableNumber"]
    table_label = [seat["label"] for seat in seating if seat["id"] == table_id][0]
    print("Table %s requested help" % table_label)
    if table_label not in help_requested:
        help_requested.append(table_label)
        print("Tables requesting help: %s" % help_requested)
    return HttpResponse("recieved")

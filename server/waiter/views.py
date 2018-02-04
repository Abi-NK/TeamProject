from django.http import HttpResponse, JsonResponse
from .models import Order
from customer.models import Menu
import json
from django.utils import timezone
from django.shortcuts import render
from django.core.serializers import serialize
from django.views.decorators.http import require_http_methods

help_requested = []


# list of orders that are ready is updated every time the page is accessed (refreshed)
def index(request):
    """Return the waiter index page."""
    return HttpResponse("Waiter index page, to be implemented.")


def orders(request):
    """Return the page for viewing all orders."""
    return render(request, "waiter/orders.html")


@require_http_methods(["GET"])
def get_orders(request):
    """Return all orders as JSON."""
    json = serialize('json', Order.objects.all())
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
def request_help():
    pass

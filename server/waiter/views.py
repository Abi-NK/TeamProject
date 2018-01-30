from django.http import HttpResponse, JsonResponse
from .models import Order
from customer.models import Menu
import json
from django.utils import timezone
from django.shortcuts import render
from django.core.serializers import serialize
from django.views.decorators.http import require_http_methods


def index(request):
    return HttpResponse("This page has the potential to be the best page ever... it's just not there yet")


@require_http_methods(["POST"])
def make_order(request):
    all_orders = json.loads(request.body.decode('utf-8'))
    print("Recieved order from front-end: ", all_orders)

    order_contents = [Menu.objects.get(pk=key) for key in all_orders]
    total_price = sum([item.price * all_orders[str(item.id)] for item in order_contents])
    new_order = Order(
        customer_name="none",
        order_complete=False,
        time_taken=timezone.now(),
        order_contents=", ".join([str(item) for item in order_contents]),
        cooking_instructions='none',
        purchase_method='none',
        total_price=total_price)
    new_order.save(force_insert=True)

    return HttpResponse("recieved")


# used to confirm an order
@require_http_methods(["POST"])
def confirm_order(request):
    order_id = json.loads(request.body.decode('utf-8'))["id"]
    print("Recieved ID: " + str(order_id))
    order = Order.objects.get(pk=order_id)
    order.order_complete = True
    order.save()
    return HttpResponse("recieved")


def ready_orders(request):
    orders_json = serialize('json', Order.objects.filter(order_complete=True))
    return JsonResponse(orders_json, safe=False)


# page for displaying all orders
def orders(request):
    return render(request, "waiter/orders.html")


# returns JSON of all orders from orders table
def get_orders(request):
    orders_json = serialize('json', Order.objects.all())
    return JsonResponse(orders_json, safe=False)

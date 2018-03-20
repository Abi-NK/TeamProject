from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from core.models import Order
import json
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required


@require_http_methods(["POST"])
def make_order(request):
    """Create an order from the provided JSON."""
    if "seating_id" not in request.session:
        print("A session without a seating ID tried to place an order.")
        return HttpResponseNotFound("no seating_id in session")

    order_json = json.loads(request.body.decode('utf-8'))["order"]
    order = Order.make_order(order_json, request.session["seating_id"])
    order.reduce_stock()
    return HttpResponse("recieved")


@require_http_methods(["POST"])
@login_required
def confirm_order(request):
    """Confirm the provided order in the database."""
    order_id = json.loads(request.body.decode('utf-8'))["id"]
    print("Recieved ID: " + str(order_id))
    order = Order.objects.get(pk=order_id)
    order.confirmed = True
    order.save()
    return HttpResponse("recieved")


# cancel orders post request
@require_http_methods(["POST"])
@login_required
def cancel_order(request):
    """Cancel the order, walkout data left in database."""
    order_id = json.loads(request.body.decode('utf-8'))["id"]
    print("Recieved ID: " + str(order_id))
    order = Order.objects.get(pk=order_id)
    order.confirmed = False
    order.cancelled = True
    order.refund_stock()
    order.save()
    return HttpResponse("recieved")


@require_http_methods(["POST"])
@login_required
def readyDelivery(request):
    """sets the ready_delivery in the database to true."""
    order_id = json.loads(request.body.decode('utf-8'))["id"]
    Order.objects.get(pk=order_id).set_ready_delivery()
    return HttpResponse("Order ready, calling waiter")


@require_http_methods(["POST"])
def delay_order(request):
    """Delay the order."""
    order_id = json.loads(request.body.decode('utf-8'))["id"]
    print("Recieved ID: " + str(order_id))
    order = Order.objects.get(pk=order_id)
    order.delayed = True
    order.save()
    return HttpResponse("recieved")


@require_http_methods(["GET"])
@login_required
def html_kitchen_cards(request):
    """Return all orders for the kitchen as formatted HTML."""
    orders = Order.get_kitchen_orders(all)
    return render(request, "core/order/kitchen_cards.html", {'orders': orders})

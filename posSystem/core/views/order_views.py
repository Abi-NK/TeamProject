from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from core.models import Order
import json
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Q


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


# HTML rendering views are listed below


@require_http_methods(["GET"])
@login_required
def html_kitchen_cards(request):
    """Return all orders for the kitchen as formatted HTML."""
    orders = Order.get_kitchen_orders(all)
    return render(request, "core/order/kitchen_cards.html", {'orders': orders})


@require_http_methods(["GET"])
@login_required
def html_confirm_cards(request):
    """Return all orders which need confirmation as formatted HTML."""
    orders = Order.objects.filter(confirmed=False, cancelled=False)
    return render(request, "core/order/order_cards.html", {'orders': orders, 'confirm': True})


@require_http_methods(["GET"])
@login_required
def html_delivery_cards(request):
    """Return all orders which are ready to be delivered as formatted HTML."""
    orders = Order.objects.filter(confirmed=True, ready_delivery=True, delivered=False)
    return render(request, "core/order/order_cards.html", {'orders': orders, 'delivery': True})


@require_http_methods(["GET"])
@login_required
def html_unpaid_cards(request):  # what the user does not see, will not hurt them...
    """Return all orders which have been delivered but not paid for as formatted HTML."""
    # the order quiey bellow checks both the order model and the payment fk model
    orders = Order.objects.filter(Q(delivered=True, paid=False) | Q(payment__payment_accepted=False)).order_by('time')
    newORder = []  # list to store orders to send but only once instnace of that order
    listOfTables = []  # track tabkes that are already populated in waiter page
    for order in orders:
        if order.table in listOfTables:
            print("hide payment")
        else:
            # if the order is not in the table then add it the new order field and table
            newORder.append(order)
            listOfTables.append(order.table)
    return render(request, "core/order/order_cards.html", {'orders': newORder, 'unpaid': True})

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from core.models import Order, Seating
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
    orders = Order.unpaid_objects.filter(delivered=True).order_by('time')
    return render(request, "core/order/order_cards.html", {'orders': orders, 'unpaid': True})


@login_required
def html_summary_list(request):
    """Return a summary of restaurant data in formatted HTML."""
    context = {
        "seating_data": {
            "occupied_count": len(Seating.occupied_objects.all()),
            "available_count": len(Seating.available_objects.all()),
        },
        "order_data": {
            "active_count": len(Order.active_objects.all()),
            "unconfirmed_count": len(Order.unconfirmed_objects.all()),
            "confirmed_count": len(Order.confirmed_objects.all()),
            "ready_count": len(Order.ready_objects.all()),
            "delivered_today": len(Order.delivered_today_objects.all()),
            "delivered_week": len(Order.delivered_week_objects.all()),
            "cancelled_today": len(Order.cancelled_today_objects.all()),
            "cancelled_week": len(Order.cancelled_week_objects.all()),
        },
    }
    return render(request, 'core/order/summary_list.html', context)


@login_required
def html_active_list(request):
    """Return all active orders in formatted HTML."""
    context = {
        "orders": Order.active_objects.all(),
    }
    return render(request, 'core/order/active_list.html', context)


def html_customer_cards(request):
    unpaid_orders = Order.unpaid_objects.filter(table=request.session['seating_id'])
    active_orders = Order.active_objects.filter(table=request.session['seating_id'])
    orders = []
    for order in active_orders:
        orders.insert(0, order)
    for order in unpaid_orders:
        if order not in orders:
            orders.insert(0, order)
    seating_label = request.session['seating_label']
    return render(request, 'customer/statuses.html', {
        'orders': orders,
        'seating_label': seating_label,
    })

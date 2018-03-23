try:
    from django.http import HttpResponse
    from django.shortcuts import render
    from core.models import OrderExtra, OrderItem, Seating
    from django.contrib.auth.models import User
    from django.views.decorators.http import require_http_methods
    from django.contrib.auth.decorators import login_required
except ImportError:
    print("failed import")
import json


def place_order_extra(request):
    """Create an OrderExtra from the provided JSON, or update an existing one."""
    received_json = json.loads(request.body.decode('utf-8'))
    seating_id = received_json["seating_id"]
    menu_item_id = received_json["menu_item_id"]
    quantity = received_json["quantity"]

    order_extra = None
    try:
        order_extra = OrderExtra.active_objects.get(seating=Seating.occupied_objects.get(pk=seating_id))
    except:
        order_extra = OrderExtra.objects.create(
            seating=Seating.occupied_objects.get(pk=seating_id),
            waiter=User.objects.get(username=request.user.username),
        )
    order_extra.add_item(menu_item_id, quantity)
    print(order_extra)
    return HttpResponse("recieved")


def get_order_extra(request):
    """Return the suggested order items as formatted HTML."""
    try:
        order_extra = OrderExtra.active_objects.get(seating=Seating.occupied_objects.get(pk=request.session['seating_id']))
        return render(request, "core/orderextra/orderextra_list.html", {'order_extra': order_extra})
    except:
        return render(request, "core/orderextra/orderextra_list.html")


def cancel_order_extra_item(request):
    """Remove an OrderItem from an OrderExtra."""
    received_json = json.loads(request.body.decode('utf-8'))
    order_extra = OrderExtra.active_objects.get(pk=received_json["order_extra_id"])
    order_item = OrderItem.objects.get(pk=received_json["order_item_id"])
    order_extra.items.remove(order_item)
    if order_extra.items.count() == 0:
        order_extra.delete()
    return HttpResponse("received")

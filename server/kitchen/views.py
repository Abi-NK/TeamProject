from django.http import HttpResponse, JsonResponse
from waiter.models import Order
import json
from django.utils import timezone
from django.shortcuts import render
from django.core.serializers import serialize
from django.views.decorators.http import require_http_methods


def index(request):
    """Return the waiter index page."""
    return render(request, "kitchen/status.html")


def orders(request):
    """Return the page for viewing all orders."""
    return render(request, "kitchen/status.html")


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
def confirm_order(request):
    """Confirm the provided order in the database."""
    order_id = json.loads(request.body.decode('utf-8'))["id"]
    print("Recieved ID: " + str(order_id))
    order = Order.objects.get(pk=order_id)
    order.confirmed = True
    order.save()
    return HttpResponse("ready, calling waiter")

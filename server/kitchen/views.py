from django.http import HttpResponse, JsonResponse
from waiter.models import Order
import json
from django.utils import timezone
from django.shortcuts import render
from django.core.serializers import serialize
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def index(request):
    """Return the kitchen page."""
    return render(request, 'kitchen/status.html', {'all_menu': Order.objects.all})


@require_http_methods(["GET"])
def get_orders(request):
    """Return all orders as JSON."""
    json = serialize('json', Order.objects.filter(ready_delivery=False, confirmed=True).order_by('time'))
    return JsonResponse(json, safe=False)


@require_http_methods(["POST"])
def readyDelivery(request):
    """sets the ready_delivery in the database to true."""
    order_id = json.loads(request.body.decode('utf-8'))["id"]
    print("Recieved ID: " + str(order_id))
    order = Order.objects.get(pk=order_id)
    order.ready_delivery = True
    order.save()
    return HttpResponse("Order ready, calling waiter")

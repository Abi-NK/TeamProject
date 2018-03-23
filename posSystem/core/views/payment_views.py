try:
    from django.http import HttpResponse
    from core.models import Order
    from django.views.decorators.http import require_http_methods
    from django.contrib.auth.decorators import login_required
except ImportError:
    print("failed import")
import json

def confirm_payment(request):
    """
    Confirm the payment status of an order in the database.

    :param request: HTTPrequest
    :return: HTTP Response
                "received" message
    """
    order_id = json.loads(request.body.decode('utf-8'))["id"]
    order = Order.objects.get(pk=order_id)
    order.paid = True
    order.save()
    return HttpResponse("recieved")

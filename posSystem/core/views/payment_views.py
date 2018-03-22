from django.http import HttpResponse
from core.models import Order
import json
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required


@require_http_methods(["POST"])
@login_required
def confirm_payment(request):
    """Confirm the payment status of an order in the database."""
    order_id = json.loads(request.body.decode('utf-8'))["id"]
    order = Order.objects.get(pk=order_id)
    order.paid = True
    order.save()
    return HttpResponse("recieved")

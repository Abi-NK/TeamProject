from django.http import HttpResponse
from core.models import Order
import json
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required


@require_http_methods(["POST"])
@login_required
def confirm_payment(request):
    """Confirm the provided payment in the database."""
    # This method now takes a table refrance and sets the paid field in all the orders of that table to true.
    payment_id = json.loads(request.body.decode('utf-8'))["id"]
    print("Recieved ID: " + str(payment_id))
    payment = Order.objects.get(pk=payment_id).payment
    payment.payment_accepted = True
    payment.save()
    # sets order model paid field
    allOrders = Order.objects.get(pk=payment_id).table
    orders = Order.objects.filter(table=allOrders)
    for order in orders:
        order.paid = True
        order.save()
    return HttpResponse("recieved")

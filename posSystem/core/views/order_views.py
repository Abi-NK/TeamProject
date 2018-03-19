from core.models import Order
from django.shortcuts import render


def statuses(request):
    """..."""
    orders = Order.objects.all()
    return render(request, 'customer/statuses.html', {'orders': orders})

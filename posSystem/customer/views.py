from django.http import HttpResponse
from django.shortcuts import render
from .models import Menu, Seating
from waiter.models import Payment, Order
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from waiter.models import Order
import json


@ensure_csrf_cookie
def index(request):
    """Return the menu page."""
    context = {
        'all_menu': Menu.objects.all(),
    }
    if 'seating_label' in request.session:
        context['seating_label'] = request.session['seating_label']
    else:
        context['seating'] = Seating.available_objects.all()
    return render(request, 'customer/menu.html', context)


@require_http_methods(["POST"])
def take_seat(request):
    """Marks the provided seating as unavailable in the database."""
    table_id = json.loads(request.body.decode('utf-8'))["tableID"]
    Seating.objects.get(pk=table_id).set_unavailable()
    request.session['seating_id'] = table_id
    request.session['seating_label'] = Seating.objects.get(pk=table_id).label
    return HttpResponse("received")

        # order': Order.objects.get(table=request.session['seating_id']),
        # 'payment': ,

def payment(request):

        context = {
            'payment': Payment.objects.filter(order=request.session['seating_id']),
            'order': Order.objects.get(table=request.session['seating_id']),
            # 'orderItems': Order.objects.get(table=request.session['seating_id']).items.all(),
        }
        if request.method == "POST":
            Payment(    # note- table is shown in payment page but not used in model
                order=Order.objects.get(table=request.session['seating_id']),
                # order=request.POST.get('order'),
                card_holder=request.POST.get('name'),
                card_number=request.POST.get('card-number'),
                cvc=request.POST.get('cvc'),
                expiry=request.POST.get('expiry'),
                terms_conditions=checkbox_check(request.POST.get('cbx')),
                payment_received=True
            ).save(force_insert=True)
        return render(request, "customer/e_payment.html", context)


def checkbox_check(val):
    if val == 'on':
        return "True"
    return "False"


def t_and_c(request):
    if request.method == "POST":
        payment_update = Payment.objects.get(terms_conditions=request.POST['t-c'])
        payment_update.delivered = True
        payment_update.save()



def statuses(request):
    """..."""
    orders = Order.objects.all()
    return render(request, 'customer/statuses.html', {'orders': orders})
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Menu, Seating
from waiter.models import Payment, Order
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from waiter.models import Order, OrderItem, OrderExtra
import json


@ensure_csrf_cookie
def index(request):
    """Return the menu page."""

    if 'seating_label' in request.session:

        context = {
            'all_menu': Menu.objects.all(),
            'order': Order.objects.filter(table=request.session['seating_id']).first(),
        }
        if 'seating_label' in request.session:
            context['seating_label'] = request.session['seating_label']
        else:
            context['seating'] = Seating.available_objects.all()
    else:
        context = {
            'all_menu': Menu.objects.all(),
        }
        if 'seating_label' in request.session:
            context['seating_label'] = request.session['seating_label']
        else:
            context['seating'] = Seating.available_objects.all()
    return render(request, 'customer/menu.html', context)


@require_http_methods(["GET"])
def getOrderInfo(request):
    context = {
        'all_menu': Menu.objects.all(),
        'order': Order.objects.filter(table=request.session['seating_id']).first()
    }
    return render(request, 'customer/menu.html', context)


@require_http_methods(["GET"])
def get_order_extra(request):
    """Return the suggested order items as formatted HTML."""
    try:
        order_extra = OrderExtra.active_objects.get(seating=Seating.occupied_objects.get(pk=request.session['seating_id']))
        return render(request, "customer/get/orderextra.html", {'order_extra': order_extra})
    except:
        return render(request, "customer/get/orderextra.html")


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
            'order': Order.objects.filter(table=request.session['seating_id']),
            # 'orderItems': Order.objects.get(table=request.session['seating_id']).items.all(),
        }
        if request.method == "POST":
            Payment(
                card_holder=request.POST.get('name'),
                card_number=request.POST.get('card-number'),
                cvc=request.POST.get('cvc'),
                expiry=request.POST.get('expiry'),
                terms_conditions=checkbox_check(request.POST.get('cbx')),
                payment_received=True
            ).save(force_insert=True)
            # assign this paymet to its order

            order = Order.objects.filter(table=request.session['seating_id'])
            order.payment = Payment.objects.filter(card_number=request.POST.get('card-number'))
            order.save()
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



@require_http_methods(["POST"])
def cancel_order_extra_item(request):
    """Remove an OrderItem from an OrderExtra."""
    received_json = json.loads(request.body.decode('utf-8'))
    order_extra = OrderExtra.active_objects.get(pk=received_json["order_extra_id"])
    order_item = OrderItem.objects.get(pk=received_json["order_item_id"])
    order_extra.items.remove(order_item)
    if order_extra.items.count() == 0:
        order_extra.delete()
    return HttpResponse("received")


def statuses(request):
    """..."""
    orders = Order.objects.all()
    return render(request, 'customer/statuses.html', {'orders': orders})

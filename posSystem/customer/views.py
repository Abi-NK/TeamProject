from django.shortcuts import render, redirect
from core.models import Menu, Order, Payment, Seating
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods


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


def payment(request):
    """Either sends out a list of payment and order objects or takes in a payment using POST."""
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

        c = len(order)

        for i in range(c):
            # for every item in the order list add it to the same payment as it came from the same table
            nOrder = Order.objects.get(id=order[i].id)
            nOrder.payment = Payment.objects.filter(card_number=request.POST.get('card-number')).last()
            nOrder.save()

        return redirect('/customer')
    return render(request, "customer/e_payment.html", context)


def checkbox_check(val):
    """Converts html checkbox to django model format"""
    if val == 'on':
        return "True"
    return "False"


def t_and_c(request):
    """Sets t and c field in DB from POST (not in html form)"""
    if request.method == "POST":
        payment_update = Payment.objects.get(terms_conditions=request.POST['t-c'])
        payment_update.delivered = True
        payment_update.save()
        

def statuses(request):
    """..."""
    orders = Order.objects.all()
    return render(request, 'customer/statuses.html', {'orders': orders})

from django.shortcuts import render, redirect
from core.models import Menu, Order, Payment, Seating
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def index(request):
    """Return the menu page."""

    if 'seating_label' in request.session:

        context = {
            'all_menu': Menu.objects.all(),
            'order': Order.unpaid_objects.filter(table=request.session['seating_id']).order_by('time').first(),
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
    if request.method == "POST":
        payment = Payment.objects.create(
            card_holder=request.POST.get('name'),
            card_number=request.POST.get('card-number'),
            cvc=request.POST.get('cvc'),
            expiry=request.POST.get('expiry'),
            terms_conditions=checkbox_check(request.POST.get('cbx')),
            payment_received=True
        )

        orders = Order.unpaid_objects.filter(table=request.session['seating_id']).order_by('time')
        for order in orders:
            order.paid = True
            order.payment = payment
            order.save()
        return redirect('/customer')

    orders = Order.unpaid_objects.filter(table=request.session['seating_id']).order_by('time')
    context = {
        'order': orders,
        'total': "£%.2f" % sum([order.total_price for order in orders])
    }
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
    unpaid_orders = Order.unpaid_objects.filter(table=request.session['seating_id'])
    active_orders = Order.active_objects.filter(table=request.session['seating_id'])
    orders = []
    for order in active_orders:
        orders.insert(0, order)
    for order in unpaid_orders:
        if order not in orders:
            orders.insert(0, order)
    seating_label = request.session['seating_label']
    return render(request, 'customer/statuses.html', {
        'orders': orders,
        'seating_label': seating_label,
    })

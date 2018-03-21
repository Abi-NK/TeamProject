from django.shortcuts import render, redirect
from core.models import Menu, Order, Payment, Seating
from django.views.decorators.csrf import ensure_csrf_cookie


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
    """
    Method for payment system.
    IF called with anything other then POST it will return, in context, two objects:
    'payment' - This contains the payment information for the most recent order of the current table
    'order' - This contains the order information of the most recent order of the current table

    If this method is accessed via a POST request then it will add a new payment to db, using force insert.
    The POST method also adds the payment, that was just made, to all orders of that table.

    Returns:
    if non post then return the payment page
    if post then return customer page (menu)
    """
    context = {
            'payment': Payment.objects.filter(order=request.session['seating_id']),
            'order': Order.objects.filter(table=request.session['seating_id']),
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

        for i in range(c):  # add payment object to all order items that have the same table
            # for every item in the order list add it to the same payment as it came from the same table
            nOrder = Order.objects.get(id=order[i].id)
            nOrder.payment = Payment.objects.filter(card_number=request.POST.get('card-number')).last()
            nOrder.save()

        return redirect('/customer')
    return render(request, "customer/e_payment.html", context)


def checkbox_check(val):
    """Converts html checkbox to django model format
    Takes: a value from a check box ('on' or 'of')
    Returns: true or false depending on value
    """
    if val == 'on':
        return "True"
    return "False"


def t_and_c(request):
    """Sets t and c field in DB from POST (not in html form)
    Takes: a request from render
    Sets a the payment as delivered
    """
    if request.method == "POST":
        payment_update = Payment.objects.get(terms_conditions=request.POST['t-c'])
        payment_update.delivered = True
        payment_update.save()


def statuses(request):
    """..."""
    orders = Order.objects.all()
    return render(request, 'customer/statuses.html', {'orders': orders})

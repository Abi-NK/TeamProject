from django.http import HttpResponse, HttpResponseNotFound
from .models import Order, Payment
from customer.models import Seating
from .models import Order, OrderExtra
from customer.models import Menu, Seating
import json
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from kitchen.views import index as waiter_index
from manager.views import index as manager_index
from django.contrib.auth.models import User
from django.db.models import Q


def group_check(user):
    return user.username.startswith('waiter')


def waiter_login(request):
    """Provide a login page for the user and handle login requests."""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            print("Logged in user %s" % user.username)
            if user.username.startswith('waiter'):
                return redirect(index)
            elif user.username.startswith('kitchen'):
                return redirect(waiter_index)
            elif user.username.startswith('manager'):
                return redirect(manager_index)
            else:
                return redirect('')
        else:
            # Return an 'invalid login' error message.
            return HttpResponse("Login failed")

    context = {}
    if request.user.username != "":
        context["username"] = request.user.username
    return render(request, "waiter/login.html", context)


def waiter_logout(request):
    """Log out the current user."""
    logout(request)
    return redirect('/login')


# list of orders that are ready is updated every time the page is accessed (refreshed)
@user_passes_test(group_check)
def index(request):
    """Return the waiter index page."""
    if request.method == "POST":
        order_update = Order.objects.get(pk=request.POST['delivery_id'])
        order_update.delivered = True
        order_update.save()
    return render(request, "waiter/index.html", {'menu': Menu.objects.all()})


@require_http_methods(["GET"])
@user_passes_test(group_check)
def get_payment(request):
    """Return all payment information."""
    payment = Payment.objects.all()
    return render(request, "waiter/ordercards.html", {'payment': payment})


@require_http_methods(["GET"])
@login_required
def get_orders_confirm(request):
    """Return all orders which need confirmation as formatted HTML."""
    orders = Order.objects.filter(confirmed=False, cancelled=False)
    return render(request, "waiter/ordercards.html", {'orders': orders, 'confirm': True})


# cancel orders get request
@require_http_methods(["GET"])
@login_required
def get_orders_cancel(request):
    """Return all orders which need cancelling as formatted HTML."""
    orders = Order.objects.filter(confirmed=False, cancelled=True)
    return render(request, "waiter/ordercards.html", {'orders': orders, 'confirm': True})


@require_http_methods(["GET"])
@user_passes_test(group_check)
def get_orders_delivery(request):
    """Return all orders which are ready to be delivered as formatted HTML."""
    orders = Order.objects.filter(confirmed=True, ready_delivery=True, delivered=False)
    return render(request, "waiter/ordercards.html", {'orders': orders, 'delivery': True})


@require_http_methods(["GET"])
@user_passes_test(group_check)
def get_orders_unpaid(request):
    """Return all orders which have been delivered but not paid for as formatted HTML."""
    orders = Order.objects.filter(Q(delivered=True) | Q(payment__payment_accepted=True)).order_by('time')
    # orders = Order.objects.filter(delivered=True, payment_accepted=True).order_by('time')
    return render(request, "waiter/ordercards.html", {'orders': orders, 'unpaid': True})

@require_http_methods(["GET"])
@user_passes_test(group_check)
def get_orders_paid(request):
    """Return all orders which have been delivered but not paid for as formatted HTML."""
    orders = Order.objects.filter(delivered=True, paid=True).order_by('time')
    return render(request, "waiter/ordercards.html", {'orders': orders})

@require_http_methods(["GET"])
@user_passes_test(group_check)
def get_alerts(request):
    want_assistance = Seating.objects.filter(assistance=True)
    return render(request, "waiter/alerts.html", {'want_assistance': want_assistance})


@require_http_methods(["GET"])
@user_passes_test(group_check)
def get_occupied_seating(request):
    """Returns the options for occupied seating."""
    seating = Seating.occupied_objects.all()
    return render(request, "waiter/get/occupiedseating.html", {'seating': seating})


@require_http_methods(["POST"])
def make_order(request):
    """Create an order from the provided JSON."""
    if "seating_id" not in request.session:
        print("A session without a seating ID tried to place an order.")
        return HttpResponseNotFound("no seating_id in session")

    order_json = json.loads(request.body.decode('utf-8'))["order"]
    order = Order.make_order(order_json, request.session["seating_id"])
    order.reduce_stock()
    return HttpResponse("recieved")


@require_http_methods(["POST"])
@login_required
def confirm_order(request):
    """Confirm the provided order in the database."""
    order_id = json.loads(request.body.decode('utf-8'))["id"]
    print("Recieved ID: " + str(order_id))
    order = Order.objects.get(pk=order_id)
    order.confirmed = True
    order.save()
    return HttpResponse("recieved")


# cancel orders post request
@require_http_methods(["POST"])
@login_required
def cancel_order(request):
    """Cancel the order, walkout data left in database."""
    order_id = json.loads(request.body.decode('utf-8'))["id"]
    print("Recieved ID: " + str(order_id))
    order = Order.objects.get(pk=order_id)
    order.confirmed = False
    order.cancelled = True
    order.refund_stock()
    order.save()
    return HttpResponse("recieved")


@require_http_methods(["POST"])
@login_required
def confirm_payment(request):
    """Confirm the provided payment in the database."""
    payment_id = json.loads(request.body.decode('utf-8'))["id"]
    print("Recieved ID: " + str(payment_id))
    payment = Order.objects.get(pk=payment_id).payment
    payment.payment_accepted = True
    payment.save()
    # sets order to paid
    # # order = Order.objects.get(pk=payment_id)
    # # order.paid = True
    # # order.save()
    return HttpResponse("recieved")


@require_http_methods(["POST"])
def request_help(request):
    if "seating_id" not in request.session:
        print("A session without a seating ID requested assistance.")
        return HttpResponseNotFound("no seating_id in session")

    Seating.objects.get(pk=request.session["seating_id"]).set_assistance_true()
    return HttpResponse("recieved")


@require_http_methods(["POST"])
def cancel_help(request):
    seating_id = json.loads(request.body.decode('utf-8'))["id"]
    Seating.objects.get(pk=seating_id).set_assistance_false()
    return HttpResponse("recieved")


@require_http_methods(["POST"])
def place_order_extra(request):
    """Create an OrderExtra from the provided JSON, or update an existing one."""
    received_json = json.loads(request.body.decode('utf-8'))
    seating_id = received_json["seating_id"]
    menu_item_id = received_json["menu_item_id"]
    quantity = received_json["quantity"]

    order_extra = None
    try:
        order_extra = OrderExtra.active_objects.get(seating=Seating.occupied_objects.get(pk=seating_id))
    except:
        order_extra = OrderExtra.objects.create(
            seating=Seating.occupied_objects.get(pk=seating_id),
            waiter=User.objects.get(username=request.user.username),
        )
    order_extra.add_item(menu_item_id, quantity)
    print(order_extra)
    return HttpResponse("recieved")


@require_http_methods(["POST"])
def remove_menu_item(request):
    '''No idea what to do here'''
    received_json = json.loads(request.body.decode('utf-8'))
    itemToRemoveID = received_json["itemToRemoveID"]
    menu_item = Menu.objects.get(pk=itemToRemoveID)
    menu_item.removed = True
    menu_item.save()
    return HttpResponse("received")

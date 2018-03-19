from django.http import HttpResponse, HttpResponseNotFound
from core.models import Menu, Order, OrderExtra, Payment, Seating, Waiter
from django.contrib.auth.models import User
import json
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from kitchen.views import index as waiter_index
from manager.views import index as manager_index
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


@require_http_methods(["GET"])
@login_required
def get_orders_cancel(request):
    """Return all orders which need cancelling as formatted HTML."""
    orders = Order.objects.filter(confirmed=False, cancelled=True)
    return render(request, "waiter/ordercards.html", {'orders': orders, 'confirm': True})


@require_http_methods(["GET"])
@user_passes_test(group_check)
def get_tables(request):
    """Get tables for waiter."""
    users_tables = Seating.objects.filter(waiter=request.user.username)
    waiter = Waiter.objects.get(name=request.user.username)
    return render(request, "waiter/get/users_tables.html", {'users_tables': users_tables, 'waiter': waiter})


@require_http_methods(["GET"])
@user_passes_test(group_check)
def get_seating(request):
    """Get all of the restaurant's seating."""
    seating = Seating.objects.all()
    names = {}
    for waiter in Waiter.objects.all():
        names[waiter.name] = User.objects.get(username=waiter.name).get_full_name()
    return render(request, "waiter/get/tables.html", {'seating': seating, 'names': names})


@require_http_methods(["GET"])
@user_passes_test(group_check)
def get_orders_delivery(request):
    """Return all orders which are ready to be delivered as formatted HTML."""
    orders = Order.objects.filter(confirmed=True, ready_delivery=True, delivered=False)
    return render(request, "waiter/ordercards.html", {'orders': orders, 'delivery': True})


@require_http_methods(["GET"])
@user_passes_test(group_check)
def get_orders_unpaid(request):  # what the user does not see, will not hurt them...
    """Return all orders which have been delivered but not paid for as formatted HTML."""
    # the order quiey bellow checks both the order model and the payment fk model
    orders = Order.objects.filter(Q(delivered=True, paid=False) | Q(payment__payment_accepted=False)).order_by('time')
    newORder=[]  # list to store orders to send but only once instnace of that order
    listOfTables=[]  # track tabkes that are already populated in waiter page
    for order in orders:
        if order.table in listOfTables:
            print("hide payment")
        else:
            # if the order is not in the table then add it the new order field and table
            newORder.append(order)
            listOfTables.append(order.table)
    return render(request, "waiter/ordercards.html", {'orders': newORder, 'unpaid': True})


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
def assign_to_seating(request):
    """Set the provided seating's current waiter to be the provided username."""
    username = json.loads(request.body.decode('utf-8'))["username"]
    seating_id = json.loads(request.body.decode('utf-8'))["seating_id"]
    seating = Seating.objects.get(pk=seating_id)
    seating.waiter = username
    seating.save()
    print("%s has been assigned to %s" % (username, seating.label))
    return HttpResponse("received")


@require_http_methods(["POST"])
@login_required
def unassign_from_seating(request):
    """Set the provided seating's current waiter to be the provided username."""
    username = json.loads(request.body.decode('utf-8'))["username"]
    seating_id = json.loads(request.body.decode('utf-8'))["seating_id"]
    seating = Seating.objects.get(pk=seating_id)
    seating.waiter = ""
    seating.save()
    print("%s has been unassigned from %s" % (username, seating.label))
    return HttpResponse("received")


@require_http_methods(["POST"])
@login_required
def waiter_on_duty(request):
    """Set the provided waiter to be on duty."""
    username = json.loads(request.body.decode('utf-8'))["name"]
    Waiter.objects.get(name=username).set_waiter_on_duty()
    return HttpResponse("received")


@require_http_methods(["POST"])
@login_required
def waiter_off_duty(request):
    """Set the provided waiter to be off duty."""
    username = json.loads(request.body.decode('utf-8'))["name"]
    Waiter.objects.get(name=username).set_waiter_off_duty()
    return HttpResponse("received")


@login_required
def auto_assign(request):
    """Automatically distribute assignment across all on-duty waiters."""
    onduty_waiters = [waiter for waiter in Waiter.objects.filter(onduty=True)]
    seating = [seating for seating in Seating.objects.all()]
    tables_per_waiter = len(seating) // len(onduty_waiters)
    remainder = len(seating) % len(onduty_waiters)
    print("CHECK %s, %s" % (tables_per_waiter, remainder))
    i = 0
    for waiter in onduty_waiters:
        for j in range(tables_per_waiter):
            seating[i].waiter = waiter.name
            seating[i].save()
            i += 1
        if remainder != 0:
            seating[i].waiter = waiter.name
            seating[i].save()
            remainder -= 1
            i += 1
    return HttpResponse("received")


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
def delay_order(request):
    """Delay the order."""
    order_id = json.loads(request.body.decode('utf-8'))["id"]
    print("Recieved ID: " + str(order_id))
    order = Order.objects.get(pk=order_id)
    order.delayed = True
    order.save()
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
    if (menu_item.removed):
        menu_item.removed = False
    else:
        menu_item.removed = True
    menu_item.save()
    return HttpResponse("received")

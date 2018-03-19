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
    newORder = []  # list to store orders to send but only once instnace of that order
    listOfTables = []  # track tabkes that are already populated in waiter page
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

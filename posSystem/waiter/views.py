from django.http import HttpResponse, HttpResponseNotFound
from .models import Order, Payment
from customer.models import Seating
import json
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from kitchen.views import index as waiter_index


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
    return render(request, "waiter/index.html")


@require_http_methods(["GET"])
@login_required
def get_orders_confirm(request):
    """Return all orders which need confirmation as formatted HTML."""
    orders = Order.get_not_confirmed_orders(all)
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
    orders = Order.objects.filter(delivered=True) and Payment.objects.filter(payment_accepted=False)
    return render(request, "waiter/ordercards.html", {'orders': orders, 'unpaid': True})


@require_http_methods(["GET"])
@user_passes_test(group_check)
def get_alerts(request):
    want_assistance = Seating.objects.filter(assistance=True)
    return render(request, "waiter/alerts.html", {'want_assistance': want_assistance})


@require_http_methods(["POST"])
def make_order(request):
    """Create an order from the provided JSON."""
    Order.make_order(request)
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

from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from .models import Order
from customer.models import Menu, Seating
import json
from django.utils import timezone
from django.shortcuts import render, redirect
from django.core.serializers import serialize
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
    unconfirmed_orders = Order.objects.filter(confirmed=False)
    undelivered_orders = Order.objects.filter(delivered=False, confirmed=True, ready_delivery=True)
    return render(request, "waiter/index.html", {'undelivered': Order.objects.filter(delivered=False),
                                                 'unconfirmed_orders': unconfirmed_orders,
                                                 'undelivered_orders': undelivered_orders})


@user_passes_test(group_check)
def deliveries(request):
    """Return the waiter delivery page and confirm deliveries using django forms"""
    """Changes the order table when the delivered button has been pressed"""
    delivery = Order.objects.filter(confirmed=True, ready_delivery=True, delivered=False)
    if request.method == "POST":
        order_update = Order.objects.get(pk=request.POST['delivery_id'])
        order_update.delivered = True
        order_update.save()

    return render(request, "waiter/deliveries.html", {'delivery': delivery})


@user_passes_test(group_check)
def orders(request):
    """Return the page for viewing all orders."""
    return render(request, "waiter/orders.html")


@require_http_methods(["GET"])
@login_required
def get_orders(request):
    """Return all orders as formatted HTML."""
    orders = Order.get_not_confirmed_orders(all)
    return render(request, "waiter/ordercards.html", {'orders': orders})


@require_http_methods(["GET"])
@login_required
def ready_orders(request):
    """Return all ready orders as JSON."""
    json = serialize('json', Order.get_ready_orders(all))
    return JsonResponse(json, safe=False)


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

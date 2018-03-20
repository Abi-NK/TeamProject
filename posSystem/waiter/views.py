from django.http import HttpResponse
from core.models import Menu, Order, Payment, Seating, Waiter
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from kitchen.views import index as waiter_index
from manager.views import index as manager_index


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


@user_passes_test(group_check)
def index(request):
    """Return the waiter index page."""
    if request.method == "POST":
        order_update = Order.objects.get(pk=request.POST['delivery_id'])
        order_update.delivered = True
        order_update.save()
    return render(request, "waiter/index.html", {'menu': Menu.objects.all()})

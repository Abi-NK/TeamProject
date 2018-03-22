"""

Views for the waiter section of the system. Views take a web request and return a web response.

"""


from django.http import HttpResponse
from core.models import Menu, Order, Payment, Seating, Waiter
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from kitchen.views import index as waiter_index
from manager.views import index as manager_index


def group_check(user)
    """

    For login. Checks that the username of the user is a username for a waiter.

    :param user: user authentication object
    :return: Boolean
             True if the username starts with 'waiter' or false otherwise

    """
    return user.username.startswith('waiter')


def waiter_login(request):
    """

     The waiter login page that handles login requests.

    :param request: HTTPrequest
    :return: HTTPresponse
             Returns a success page for the type of user logging in if the login was successful.
             Returns a failure page otherwise.

    """
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
    """

     A log out of the current user.

    :param request: HTTPrequest
    :return: HTTPresponse
             Returns the login page after logging out the user.

    """
    logout(request)
    return redirect('/login')


@user_passes_test(group_check)
def index(request):
    """

     The waiter index page.

    :param request: HTTPrequest
    :return: HTTPresponse
             Returns the index page for a waiter.

    """
    if request.method == "POST":
        order_update = Order.objects.get(pk=request.POST['delivery_id'])
        order_update.delivered = True
        order_update.save()
    return render(request, "waiter/index.html", {'menu': Menu.objects.all()})

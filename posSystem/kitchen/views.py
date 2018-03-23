"""

Views for the kitchen section of the system. Views take a web request and return a web response.

"""

try:
    from core.models import Order
    from django.shortcuts import render
    from django.views.decorators.csrf import ensure_csrf_cookie
    from django.contrib.auth.decorators import user_passes_test
except ImportError:
    print("failed import")

def group_check(user):
    """

    For login. Checks that the username of the user is a username for kitchen staff.

    :param user: user authentication object
    :return: Boolean
             True if the username starts with 'kitchen' or false otherwise

    """

    return user.username.startswith('kitchen')


def index(request):
    """

     The kitchen index page.

    :param request: HTTPrequest
    :return: HTTPresponse
             Returns the index page for kitchen workers.

    """

    return render(request, 'kitchen/status.html', {'all_menu': Order.get_all_orders(all)})

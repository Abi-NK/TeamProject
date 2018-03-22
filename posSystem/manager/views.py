'''

Views for the manager section of the system. Views take a web request and return a web response.

'''


from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from core.models import OrderExtra
from django.contrib.auth.models import User


def group_check(user):
    '''

    For login. Checks that the username of the user is a username for a manager.

    :param user: user authentication object
    :return: Boolean
             True if the username starts with 'manager' or false otherwise

    '''
    return user.username.startswith('manager')


@user_passes_test(group_check)
def index(request):
    """

     The manager index page.

    :param request: HTTPrequest
    :return: HTTPresponse
             Returns the index page for a manager.

    """
    return render(request, 'manager/index.html')


@user_passes_test(group_check)
def data(request):
    '''

     The live updating data page.

    :param request: HTTPrequest
    :return: HTTPresponse
             Returns the live data page for a manager.

    '''
    return render(request, 'manager/data.html')


@user_passes_test(group_check)
def employee(request):
    '''

     Employee data page showing information about the employees of this branch of Oaxaca.

    :param request: HTTPrequest
    :return: HTTPresponse
             Returns the employee data page.

    '''
    waiter_data = []
    for waiter in User.objects.filter(username__startswith="waiter"):
        today_total = sum([item.get_total() for item in OrderExtra.used_today_objects.filter(waiter=waiter)])
        week_total = sum([item.get_total() for item in OrderExtra.used_week_objects.filter(waiter=waiter)])
        waiter_data.append({
            "waiter": waiter,
            "extra_sales_daily": "£%.2f" % today_total,
            "extra_sales_weekly": "£%.2f" % week_total,
        })
    return render(request, 'manager/employee.html', {
        "managers": User.objects.filter(username__startswith="manager"),
        "kitchen_staff": User.objects.filter(username__startswith="kitchen"),
        "waiters": waiter_data,
    })


@user_passes_test(group_check)
def waiter_assignments(request):
    '''

     The waiter seating assignments page.

    :param request: HTTPrequest
    :return: HTTPresponse
             Returns the waiter-seating assignment page.

    '''
    return render(request, 'manager/assignments.html')

try:
    from django.http import HttpResponse
    from django.shortcuts import render
    from django.contrib.auth.decorators import login_required
    from django.views.decorators.http import require_http_methods
    from core.models import Seating, Waiter
    from django.contrib.auth.models import User
except ImportError:
    print("failed import")
import json

def waiter_on_duty(request):
    """
    Set the provided waiter to be on duty.

    :param request:
    :return: HTTP Response
                "received" message
    """
    username = json.loads(request.body.decode('utf-8'))["name"]
    Waiter.objects.get(name=username).set_waiter_on_duty()
    return HttpResponse("received")


def waiter_off_duty(request):
    """
    Set the provided waiter to be off duty.

    :param request:
    :return:HTTP Response
                "received" message
    """
    username = json.loads(request.body.decode('utf-8'))["name"]
    Waiter.objects.get(name=username).set_waiter_off_duty()
    return HttpResponse("received")


def get_assignments(request):
    """
    Get all of the restaurant's seating.

    :param request:
    :return: render to "core/waiter/assignments.html", including seating, on duty waiters and names in context
    """
    seating = Seating.objects.all()
    waiters = Waiter.objects.filter(onduty=True)
    names = {}
    for waiter in Waiter.objects.all():
        names[waiter.name] = User.objects.get(username=waiter.name).get_full_name()
    return render(request, "core/waiter/assignments.html", {
        'seating': seating,
        'onduty_waiters': waiters,
        'names': names
    })


def get_waiters(request):
    """
    Get all of the restaurant's seating.

    :param request:
    :return:render to "core/waiter/waiters.html" including waiters in context
    """
    waiters = Waiter.objects.all()
    return render(request, "core/waiter/waiters.html", {'waiters': waiters})


def auto_assign(request):
    """
    Automatically distribute assignment across all on-duty waiters.

    :param request:
    :return:HTTP Response
                "received" message
    """
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

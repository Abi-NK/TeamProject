try:
    from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
    from django.shortcuts import render
    from core.models import Order, Seating, Waiter
    from django.contrib.auth.models import User
    from django.views.decorators.http import require_http_methods
    from django.contrib.auth.decorators import login_required
except ImportError:
    print("failed import")
import json


def take_seat(request):
    """
    Marks the provided seating as unavailable in the database.

    :param request: HTTPrequest
    :return:HTTP Response
                "received" message
    """
    table_id = json.loads(request.body.decode('utf-8'))["tableID"]
    Seating.objects.get(pk=table_id).set_unavailable()
    request.session['seating_id'] = table_id
    request.session['seating_label'] = Seating.objects.get(pk=table_id).label
    return HttpResponse("received")


def free_seat(request):
    """
    Marks the provided seating as unavailable in the database.

    :param request: HTTPrequest
    :return: HTTP Response
                "received" message
    """
    if request.method == "GET":
        if "seating_id" in request.session:
            table_id = request.session['seating_id']
            Seating.objects.get(pk=table_id).set_available()
            del request.session['seating_id']
            del request.session['seating_label']
    if request.method == "POST":
        seating_id = json.loads(request.body.decode('utf-8'))["seatingID"]
        Seating.objects.get(pk=seating_id).set_available()
    return HttpResponse("received")


def assign_to_seating(request):
    """
    Set the provided seating's current waiter to be the provided username.

    :param request: HTTPrequest
    :return:HTTP Response
                "received" message
    """
    username = json.loads(request.body.decode('utf-8'))["username"]
    seating_id = json.loads(request.body.decode('utf-8'))["seating_id"]
    seating = Seating.objects.get(pk=seating_id)
    seating.waiter = username
    seating.save()
    print("%s has been assigned to %s" % (username, seating.label))
    return HttpResponse("received")


def unassign_from_seating(request):
    """
    Set the provided seating's current waiter to be the provided username.

    :param request: HTTPrequest
    :return:HTTP Response
                "received" message
    """
    username = json.loads(request.body.decode('utf-8'))["username"]
    seating_id = json.loads(request.body.decode('utf-8'))["seating_id"]
    seating = Seating.objects.get(pk=seating_id)
    seating.waiter = ""
    seating.save()
    print("%s has been unassigned from %s" % (username, seating.label))
    return HttpResponse("received")


def request_help(request):
    """
    Sets the seating assistance field to true. Notifies waiter that a table needs assistance.

    :param request: HTTPrequest
    :return: returns Http response not found "no seating_id in session", Sends a 404 with the HTTP responce.
    :return: HTTP Response
                "received" message
    """
    if "seating_id" not in request.session:
        print("A session without a seating ID requested assistance.")
        return HttpResponseNotFound("no seating_id in session")

    Seating.objects.get(pk=request.session["seating_id"]).set_assistance_true()
    return HttpResponse("recieved")


def cancel_help(request):
    """
    Sets the assistance field for the order to false. Meaning that the customer does not need help

    :param request: HTTPrequest
    :return: HTTP Response
                "received" message
    """
    seating_id = json.loads(request.body.decode('utf-8'))["id"]
    Seating.objects.get(pk=seating_id).set_assistance_false()
    return HttpResponse("recieved")


def seating_live_info(request):
    """
    Customer page lives updates, using "can_pay" to check if the customer can pay
    "seatingAvaliable" updates on what seats are free
    To updates the pay button to become active once a order is confirmed.

    :param request: HTTPrequest
    :return: JSON response, a set of "can_pay" and "seatingAvaliable"
    """
    json_to_send = {}
    json_to_send["can_pay"] = Order.unpaid_objects.filter(table=request.session['seating_id']).count() > 0
    if "seating_id" in request.session:
        json_to_send["seatingAvailable"] = Seating.objects.get(pk=request.session["seating_id"]).available
    else:
        json_to_send["seatingAvailable"] = False
    return JsonResponse(json_to_send)


# HTML rendering views are listed below


def html_waiters_seating_list(request):
    """
    Get tables for waiter.

    :param request: HTTPrequest
    :return: render to "core/seating/waiters_seating_list.html" and a set that contains: user_Tables and waiter
    """
    users_tables = Seating.objects.filter(waiter=request.user.username)
    waiter = Waiter.objects.get(name=request.user.username)
    return render(request, "core/seating/waiters_seating_list.html", {'users_tables': users_tables, 'waiter': waiter})


def html_assignment_list(request):
    """
    Get all of the restaurant's seating.

    :param request: HTTPrequest
    :return: render to "core/seating/assignment_list.html" and a set that contains: seating and names
    """
    seating = Seating.objects.all()
    names = {}
    for waiter in Waiter.objects.all():
        names[waiter.name] = User.objects.get(username=waiter.name).get_full_name()
    return render(request, "core/seating/assignment_list.html", {'seating': seating, 'names': names})


def html_occupied_seating_dropdown(request):
    """
    Returns the options for occupied seating.

    :param request: HTTPrequest
    :return: render to "core/seating/occupied_seating_dropdown.html" and a set that contains: seating
    """
    seating = Seating.occupied_objects.all()
    return render(request, "core/seating/occupied_seating_dropdown.html", {'seating': seating})


def html_assistance_alerts(request):
    """
    Used to update a alert for tables that need assistance

    :param request: HTTPrequest
    :return: render to "core/seating/assistance_alerts.html" and a set that contains: want_assistance
    """
    want_assistance = Seating.objects.filter(assistance=True)
    return render(request, "core/seating/assistance_alerts.html", {'want_assistance': want_assistance})

def html_manager_list(request):
    """
    Return all tables in formatted HTML.

    :param request: HTTPrequest
    :return: render to 'core/seating/manager_list.html' and a set that contains: context
    """
    context = {
        "seating": Seating.objects.all(),
    }
    return render(request, 'core/seating/manager_list.html', context)

from django.http import HttpResponse, HttpResponseNotFound
from core.models import Seating
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json


@require_http_methods(["POST"])
def take_seat(request):
    """Marks the provided seating as unavailable in the database."""
    table_id = json.loads(request.body.decode('utf-8'))["tableID"]
    Seating.objects.get(pk=table_id).set_unavailable()
    request.session['seating_id'] = table_id
    request.session['seating_label'] = Seating.objects.get(pk=table_id).label
    return HttpResponse("received")


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

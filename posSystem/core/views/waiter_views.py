from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Seating, Waiter
from django.contrib.auth.models import User


@login_required
def get_assignments(request):
    """Get all of the restaurant's seating."""
    seating = Seating.objects.all()
    waiters = Waiter.objects.filter(onduty=True)
    names = {}
    for waiter in Waiter.objects.all():
        names[waiter.name] = User.objects.get(username=waiter.name).get_full_name()
    return render(request, "manager/get/assignments.html", {
        'seating': seating,
        'onduty_waiters': waiters,
        'names': names
    })


@login_required
def get_waiters(request):
    """Get all of the restaurant's seating."""
    waiters = Waiter.objects.all()
    return render(request, "manager/get/waiters.html", {'waiters': waiters})

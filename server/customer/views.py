from django.http import HttpResponse
from django.shortcuts import render
from .models import Menu, Seating
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
import json


@ensure_csrf_cookie
def index(request):
    """Return the menu page."""
    return render(request, 'customer/menu.html', {
        'all_menu': Menu.objects.all(),
        'seating': Seating.objects.filter(available=True),
    })


def detail(request, menu_id):
    """Return a detail page for the requested menu item."""
    menu_item = Menu.objects.get(pk=menu_id)
    return render(request, 'customer/menu_item_detail.html', {'menu_item': menu_item})


@require_http_methods(["POST"])
def take_seat(request):
    """Marks the provided seating as unavailable in the database."""
    table_id = json.loads(request.body.decode('utf-8'))["tableID"]
    Seating.objects.get(pk=table_id).set_unavailable()
    return HttpResponse("received")

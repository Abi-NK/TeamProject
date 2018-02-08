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
    table_id = json.loads(request.body.decode('utf-8'))["tableID"]
    print("Recieved seating ID %s" % str(table_id))
    table = Seating.objects.get(pk=table_id)
    print("%s has been taken" % table.label)
    table.available = False
    table.save()
    return HttpResponse("recieved")

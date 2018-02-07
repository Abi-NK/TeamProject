from django.http import HttpResponse
from django.shortcuts import render
from .models import Menu
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
import json

number_of_tables = 20
seating = [{"id": i, "available": True, "label": "Table " + str(i+1)} for i in range(number_of_tables)]


@ensure_csrf_cookie
def index(request):
    """Return the menu page."""
    return render(request, 'customer/menu.html', {
        'all_menu': Menu.objects.all(),
        'seating': [seat for seat in seating if seat["available"]],
    })


def detail(request, menu_id):
    """Return a detail page for the requested menu item."""
    menu_item = Menu.objects.get(pk=menu_id)
    return render(request, 'customer/menu_item_detail.html', {'menu_item': menu_item})


@require_http_methods(["POST"])
def take_seat(request):
    table_id = json.loads(request.body.decode('utf-8'))["tableID"]
    print("%s has been taken" % [seat["label"] for seat in seating if seat["id"] == table_id][0])
    for seat in seating:
        if seat["id"] == table_id:
            seat["available"] = False
    return HttpResponse("recieved")

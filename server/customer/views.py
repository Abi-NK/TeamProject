from django.shortcuts import render
from .models import Menu
from django.views.decorators.csrf import ensure_csrf_cookie

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

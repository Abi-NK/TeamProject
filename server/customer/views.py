from django.shortcuts import render
from .models import Menu
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def index(request):
    """Return the menu page."""
    return render(request, 'customer/menu.html', {'all_menu': Menu.objects.all()})


def detail(request, menu_id):
    """Return a detail page for the requested menu item."""
    return render(request, 'customer/menu_item_detail.html', {'menu_item_id': menu_id})

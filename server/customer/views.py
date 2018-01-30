from django.shortcuts import render
from .models import Menu
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def index(request):
    # returns a menu page which a customer can use to place an order
    return render(request, 'customer/menu.html', {'all_menu': Menu.objects.all()})


def detail(request, menu_id):
    # This page is shown when a link/item is clicked on the menu page.
    return render(request, 'customer/menu_item_detail.html', {'menu_item_id': menu_id})

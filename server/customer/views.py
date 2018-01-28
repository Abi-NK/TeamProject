from django.shortcuts import render
from .models import Menu
from django.views.decorators.csrf import ensure_csrf_cookie


# A view is a simple function that returns html.
@ensure_csrf_cookie
def index(request):
    # This is basically an SQL Query that gets the contents of the
    # menu and puts it into a variable. Select specific parts of
    # the table with different queries.
    all_menu = Menu.objects.all()

    # Context gets sent straight into the html file, this is needed because it's
    # better to keep all the html code separated from all the python logic.
    # There should never be raw html inside the python files.
    context = {
        'all_menu': all_menu,
    }

    # Returns the rendered template as a response.
    return render(request, 'customer/menu.html', context)


def detail(request, menu_id):
    # This page is shown when a link/item is clicked on the menu page.
    return render(request, 'customer/menu_item_detail.html', {'menu_item_id': menu_id})

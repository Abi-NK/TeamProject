from django.shortcuts import render
from django.http import HttpResponse
from .models import Menu
from django.template import loader


# A view is a simple function that returns html.
def index(request):
    # This is basically an SQL Query that gets the contents of the
    # menu and puts it into a variable. Select specific parts of
    # the table with different queries.
    all_menu = Menu.objects.all()

    # Loads the html file as a template.
    template = loader.get_template('customer/index.html')

    # Context gets sent straight into the html file, this is needed because it's
    # better to keep all the html code separated from all the python logic.
    # There should never be raw html inside the python files.
    context = {
        'all_menu': all_menu,
    }

    # Returns the template as a response.
    return HttpResponse(template.render(context, request))



def detail(request, menu_id):
    # This page is shown when a link/item is clicked on the menu page.
    return HttpResponse("<h2>Unique menu ID: " + str(menu_id) + "</h2>")
from django.http import HttpResponse
from django.shortcuts import render
from core.models import Menu
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from manager.forms import AdjustMenuForm
import json


def adjust_menu(request):
    """
    Shows the menu in formatted HTML and updates the table based on inputs by the manager.

    :param request: HTTPrequest
    :return: HTTPresponse
             The formatted HTML menu with updated table.

    """
    if request.method == "POST":

        form_name = request.POST['menu_name']
        form_price = request.POST['menu_price']
        form_description = request.POST['menu_description']
        form_course = request.POST['menu_course']
        form_category = request.POST['menu_category']
        form_allergy = request.POST['menu_allergy']
        form_calories = request.POST['menu_calories']
        form_image = request.POST['menu_image'],
        form_vegetarian = request.POST['menu_vegetarian']
        form_vegan = request.POST['menu_vegan']
        form_meat = request.POST['menu_meat']
        form_stock = request.POST['menu_stock']
        form_cost = request.POST['menu_cost']

        # VALIDATION: check if form inputs are valid then send it to database
        form = AdjustMenuForm(data={'name': form_name, 'price': form_price, 'description': form_description,
                                    'course': form_course, 'category': form_category, 'allergy': form_allergy,
                                    'calories': form_calories, 'image': form_image, 'vegetarian': form_vegetarian,
                                    'vegan': form_vegan, 'meat': form_meat, 'stock': form_stock, 'cost': form_cost})

        # if the confirm change button was pressed, check form for validation and update menu
        if form.is_valid():
            if 'confirm' in request.POST:
                print("item changed")
                Menu.objects.filter(pk=request.POST['menu_id']).update(
                    name=form_name, price=form_price, description=form_description, course=form_course,
                    category=form_category, allergy=form_allergy, calories=form_calories, image=form_image,
                    vegetarian=form_vegetarian, vegan=form_vegan, meat=form_meat, stock=form_stock)

            # if the delete button was pressed, remove the item from menu
            elif 'delete' in request.POST:
                Menu.objects.filter(pk=request.POST['menu_id']).delete()

            elif 'add_item' in request.POST:
                Menu.objects.create(name=form_name, price=form_price, description=form_description, course=form_course,
                                    category=form_category, allergy=form_allergy, calories=form_calories,
                                    image=form_image, vegetarian=form_vegetarian, vegan=form_vegan, meat=form_meat,
                                    stock=form_stock)

    context = {"menu": Menu.objects.all()}
    return render(request, 'manager/managermenu.html', context)


@require_http_methods(["POST"])
def remove_menu_item(request):
    """
    Formats HTML to remove a menu item"

    :param request: HTTPrequest
    :return: HTTPresponse
             The formatted HTML to remove a menu item.

    """

    received_json = json.loads(request.body.decode('utf-8'))
    item_to_remove_id = received_json["itemToRemoveID"]
    menu_item = Menu.objects.get(pk=item_to_remove_id)
    if menu_item.removed:
        menu_item.removed = False
    else:
        menu_item.removed = True
    menu_item.save()
    return HttpResponse("received")


# HTML rendering views are listed below


@login_required
def html_stock_list(request):
    """
    Shows the stock data for the menu.

    :param request: HTTPrequest
    :return: HTTPresponse
             The formatted menu stock data.

    """
    context = {
        "menu": Menu.objects.all(),
    }
    return render(request, 'core/menu/stock_list.html', context)

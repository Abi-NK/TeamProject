from django.http import HttpResponse
from django.shortcuts import render
from core.models import Menu
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from manager.forms import AdjustMenuForm
import json


def adjust_menu(request):
    """Return the menu in formatted HTML and update the table based on inputs by the manager."""
    if request.method == "POST":

        # VALIDATION: check if form inputs are valid then send it to database
        form = AdjustMenuForm(data={'name': request.POST['menu_name'], 'price': request.POST['menu_price'],
                                    'description': request.POST['menu_description'],
                                    'course': request.POST['menu_course'], 'category': request.POST['menu_category'],
                                    'allergy': request.POST['menu_allergy'], 'calories': request.POST['menu_calories'],
                                    'image': request.POST['menu_image'], 'vegetarian': request.POST['menu_vegetarian'],
                                    'vegan': request.POST['menu_vegan'], 'meat': request.POST['menu_meat'],
                                    'stock': request.POST['menu_stock'], 'cost': request.POST['menu_cost']})

        # if the confirm change button was pressed, check form for validation and update menu
        if form.is_valid():
            if 'confirm' in request.POST:
                print("item changed")
                Menu.objects.filter(pk=request.POST['menu_id']).update(
                    name=request.POST['menu_name'], price=request.POST['menu_price'],
                    description=request.POST['menu_description'], course=request.POST['menu_course'],
                    category=request.POST['menu_category'], allergy=request.POST['menu_allergy'],
                    calories=request.POST['menu_calories'], image=request.POST['menu_image'],
                    vegetarian=request.POST['menu_vegetarian'], vegan=request.POST['menu_vegan'],
                    meat=request.POST['menu_meat'], stock=request.POST['menu_stock'], cost=request.POST['menu_cost'])

            # if the delete button was pressed, remove the item from menu
            elif 'delete' in request.POST:
                Menu.objects.filter(pk=request.POST['menu_id']).delete()

            elif 'add_item' in request.POST:
                Menu.objects.create(name=request.POST['menu_name'], price=request.POST['menu_price'],
                                    description=request.POST['menu_description'], course=request.POST['menu_course'],
                                    category=request.POST['menu_category'], allergy=request.POST['menu_allergy'],
                                    calories=request.POST['menu_calories'], image=request.POST['menu_image'],
                                    vegetarian=request.POST['menu_vegetarian'], vegan=request.POST['menu_vegan'],
                                    meat=request.POST['menu_meat'], stock=request.POST['menu_stock'],
                                    cost=request.POST['menu_cost'])

    context = {"menu": Menu.objects.all()}
    return render(request, 'manager/managermenu.html', context)


@require_http_methods(["POST"])
def remove_menu_item(request):
    """Return formatted HTML to remove a menu item"""
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
    """Return stock data for the menu in formatted HTML."""
    context = {
        "menu": Menu.objects.all(),
    }
    return render(request, 'core/menu/stock_list.html', context)

from django.http import HttpResponse
from django.shortcuts import render
from core.models import Menu
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from manager.forms import AdjustMenuForm
import json


def adjust_menu(request):
    """Return the menu in formatted HTML and update the table based on inputs."""
    if request.method == "POST":

        # VALIDATION: check if form inputs are valid then send it to database
        form = AdjustMenuForm(data={'id': request.POST['menu_id'], 'name': request.POST['menu_name'],
                                    'price': request.POST['menu_price'],
                                    'description': request.POST['menu_description'],
                                    'course': request.POST['menu_course'], 'category': request.POST['menu_category'],
                                    'allergy': request.POST['menu_allergy'], 'calories': request.POST['menu_calories'],
                                    'image': request.POST['menu_image'], 'vegetarian': request.POST['menu_vegetarian'],
                                    'vegan': request.POST['menu_vegan'], 'meat': request.POST['menu_meat'],
                                    'stock': request.POST['menu_stock']})

        # if the confirm change button was pressed, check form for validation and update menu
        if form.is_valid():
            if 'confirm' in request.POST:
                print("item changed")
                menu_update = Menu.objects.get(pk=request.POST['menu_id'])
                menu_update.name = request.POST['menu_name']
                menu_update.price = request.POST['menu_price']
                menu_update.description = request.POST['menu_description']
                menu_update.course = request.POST['menu_course']
                menu_update.category = request.POST['menu_category']
                menu_update.allergy = request.POST['menu_allergy']
                menu_update.calories = request.POST['menu_calories']
                menu_update.image = request.POST['menu_image']
                menu_update.vegetarian = request.POST['menu_vegetarian']
                menu_update.vegan = request.POST['menu_vegan']
                menu_update.meat = request.POST['menu_meat']
                menu_update.stock = request.POST['menu_stock']
                menu_update.save()

            # if the delete button was pressed, remove the item from menu
            elif 'delete' in request.POST:
                Menu.objects.filter(pk=request.POST['menu_id']).delete()

            elif 'add_item' in request.POST:
                Menu.objects.create(name=request.POST['menu_name'], price=request.POST['menu_price'],
                                    description=request.POST['menu_description'], course=request.POST['menu_course'],
                                    category=request.POST['menu_category'], allergy=request.POST['menu_allergy'],
                                    calories=request.POST['menu_calories'], image=request.POST['menu_image'],
                                    vegetarian=request.POST['menu_vegetarian'], vegan=request.POST['menu_vegan'],
                                    meat=request.POST['menu_meat'], stock=request.POST['menu_stock'])

    context = {"menu": Menu.objects.all()}
    return render(request, 'manager/managermenu.html', context)


@require_http_methods(["POST"])
def remove_menu_item(request):
    '''No idea what to do here'''
    received_json = json.loads(request.body.decode('utf-8'))
    itemToRemoveID = received_json["itemToRemoveID"]
    menu_item = Menu.objects.get(pk=itemToRemoveID)
    if (menu_item.removed):
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

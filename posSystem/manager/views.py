from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from customer.models import Seating, Menu
from waiter.models import Order
from .forms import AdjustMenuForm


def group_check(user):
    return user.username.startswith('manager')


@user_passes_test(group_check)
def index(request):
    """Return the manager page."""
    return render(request, 'manager/index.html')


@user_passes_test(group_check)
def data(request):
    """Return the live updating data page."""
    return render(request, 'manager/data.html')


@user_passes_test(group_check)
def get_summary(request):
    """Return a summary of restaurant data in formatted HTML."""
    context = {
        "seating_data": {
            "occupied_count": len(Seating.occupied_objects.all()),
            "available_count": len(Seating.available_objects.all()),
        },
        "order_data": {
            "active_count": len(Order.active_objects.all()),
            "unconfirmed_count": len(Order.unconfirmed_objects.all()),
            "confirmed_count": len(Order.confirmed_objects.all()),
            "ready_count": len(Order.ready_objects.all()),
            "delivered_today": len(Order.delivered_today_objects.all()),
        },
    }
    return render(request, 'manager/get/summary.html', context)


@user_passes_test(group_check)
def get_orders(request):
    """Return all active orders in formatted HTML."""
    context = {
        "orders": Order.active_objects.all(),
    }
    return render(request, 'manager/get/orders.html', context)


@user_passes_test(group_check)
def get_tables(request):
    """Return all occupied tables in formatted HTML."""
    context = {
        "seating": Seating.occupied_objects.all(),
    }
    return render(request, 'manager/get/tables.html', context)


def show_menu(request):
    """Return the menu in formatted HTML and update the table based on inputs."""
    if request.method == "POST":

        # check if form inputs are valid then send it to database
        form = AdjustMenuForm(data={'name': request.POST['menu_name'], 'price': request.POST['menu_price'],
                                    'description': request.POST['menu_description'],
                                    'course': request.POST['menu_course'], 'category': request.POST['menu_category'],
                                    'allergy': request.POST['menu_allergy'], 'calories': request.POST['menu_calories'],
                                    'image': request.POST['menu_image']})

        # if the confirm change button was pressed, do this
        if 'confirm' in request.POST:
            if form.is_valid():
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
                menu_update.save()

        # if the delete button was pressed, do this
        elif 'delete' in request.POST:
            Menu.objects.filter(pk=request.POST['menu_id']).delete()

    context = {"menu": Menu.objects.all(),}
    return render(request, 'manager/managermenu.html', context)

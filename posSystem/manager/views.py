from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from core.models import Menu, Order, OrderExtra, Seating
from django.contrib.auth.models import User


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
def employee(request):
    """Return the employee data page."""
    waiter_data = []
    for waiter in User.objects.filter(username__startswith="waiter"):
        today_total = sum([item.get_total() for item in OrderExtra.used_today_objects.filter(waiter=waiter)])
        week_total = sum([item.get_total() for item in OrderExtra.used_week_objects.filter(waiter=waiter)])
        waiter_data.append({
            "waiter": waiter,
            "extra_sales_daily": "£%.2f" % today_total,
            "extra_sales_weekly": "£%.2f" % week_total,
        })
    return render(request, 'manager/employee.html', {
        "managers": User.objects.filter(username__startswith="manager"),
        "kitchen_staff": User.objects.filter(username__startswith="kitchen"),
        "waiters": waiter_data,
    })


@user_passes_test(group_check)
def waiter_assignments(request):
    """Return the waiter seating assignments page."""
    return render(request, 'manager/assignments.html')


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
            "delivered_week": len(Order.delivered_week_objects.all()),
            "cancelled_today": len(Order.cancelled_today_objects.all()),
            "cancelled_week": len(Order.cancelled_week_objects.all()),
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
        "seating": Seating.objects.all(),
    }
    return render(request, 'manager/get/tables.html', context)


@user_passes_test(group_check)
def get_stock(request):
    """Return stock data for the menu in formatted HTML."""
    context = {
        "menu": Menu.objects.all(),
    }
    return render(request, 'manager/get/stock.html', context)

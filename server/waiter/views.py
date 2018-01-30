from django.http import HttpResponse, JsonResponse
from .models import Order
from customer.models import Menu
import json
from django.utils import timezone
from django.shortcuts import render
from django.core.serializers import serialize


def index(request):
    return HttpResponse("This page has the potential to be the best page ever... it's just not there yet")


def make_order(request):
    if request.is_ajax():
        if request.method == 'POST':
            all_orders = json.loads(request.body.decode('utf-8'))
            print("Recieved order from front-end: ", all_orders)

            order_contents = [Menu.objects.get(pk=key) for key in all_orders]
            total_price = sum([item.price * all_orders[str(item.id)] for item in order_contents])
            new_order = Order(
                table="0",
                complete=False,
                time=timezone.now(),
                items=", ".join([str(item) for item in order_contents]),
                cooking_instructions='none',
                purchase_method='none',
                total_price=total_price,
                delivered=False,
                table_assistance=False)
            new_order.save(force_insert=True)

            return HttpResponse("recieved")
    return HttpResponse("Post order JSON to this endpoint.")


# used to confirm an order
def confirm_order(request):
    if request.is_ajax():
        if request.method == 'POST':
            order_id = json.loads(request.body.decode('utf-8'))["id"]
            print("Recieved ID: " + str(order_id))
            order = Order.objects.get(pk=order_id)
            print(order)
            order.complete = True
            order.save()
            print(Order.objects.values_list('complete'))
            return HttpResponse("recieved")
    return HttpResponse("Post orderID to confirm to this endpoint.")


def order_status(request):
    orderstatus = order_update()
    orderstatus = {
        'orderstatus': orderstatus,
    }
    # can use the readorders within the HTML in a template to access a list of ready orders
    return HttpResponse(ready_orders)  # this line returns the http with the list of ready orders
    # return HttpResponse()  # this line returns an empty page (the effects can be seen in the terminal)

    # This method is used to check the db every 30 seconds
    # to see if the order has updated.


def ready_orders(request):
    readyorders = order_update_ready_only()
    readyorders = {
        'readyorders': readyorders,
    }
    # can use the readorders within the HTML in a template to access a list of ready orders
    return HttpResponse(readyorders)  # this line returns the http with the list of ready orders
    # return HttpResponse()  # this line returns an empty page (the effects can be seen in the terminal)

    # This method is used to check the db every 30 seconds
    # to see if the order has updated.


# page for displaying all orders
def orders(request):
    return render(request, "waiter/orders.html")


# returns JSON of all orders from orders table
def get_orders(request):
    orders_json = serialize('json', Order.objects.all())
    return JsonResponse(orders_json, safe=False)


def order_update_ready_only():
    print ("-----checking for order update-----")
    readyorders = Order.objects.filter(complete=True)
    # readyorders = Order.objects.all
    # print (Order.objects.all())
    try:
        for curIt in readyorders:
            # Note -- add a method here to send the readyorders object i.e. through JSON.
            print (str(curIt.id) + ' -> ' + 'READY ')  # str(curIt.orderStatus))
    except:
        print("error printing")
    return readyorders


def order_update():
    print ("-----checking for order update-----")
    readyorders = Order.objects.all()
    realyreadyorders = Order.objects.filter(complete=True)
    notreadyorders = Order.objects.filter(complete=False)
    # readyorders = Order.objects.all
    # print (Order.objects.all())
    try:
        for curIt in realyreadyorders:
            # Note -- add a method here to send the readyorders object i.e. through JSON.
            print (str(curIt.id) + ' -> ' + 'READY ')  # str(curIt.orderStatus))
        for curIt in notreadyorders:
            # Note -- add a method here to send the readyorders object i.e. through JSON.
            print (str(curIt.id) + ' -> ' + 'NOT READY ')  # str(curIt.orderStatus))
    except:
        print("error printing")
    return readyorders

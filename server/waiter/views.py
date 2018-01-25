from django.http import HttpResponse
from .models import Order

# list of orders that are ready is updated every time the page is accessed (refreshed)


def index(request):
    return HttpResponse("This page has the potential to be the best page ever... it's just not there yet")


def make_order(request):
    try:
        take_order(request)
        print("order taken")
        return HttpResponse("order taken")
    except:
        print("problem taking order")
        return HttpResponse("Error taking order")


def order_status(request):
    orderstatus = order_update()
    orderstatus = {
        'orderstatus': orderstatus,
    }
    # can use the readorders within the HTML in a template to access a list of ready orders
    return HttpResponse(readyorders)  # this line returns the http with the list of ready orders
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


def orders(request):
    # this method returnes all the orders and all there columns
    allorders = get_all_orders()
    allorders = {
        'allorders': allorders,
    }
    return HttpResponse(allorders)


def order_update_ready_only():
    print ("-----checking for order update-----")
    readyorders = Order.objects.filter(order_complete=True)
    # readyorders = Order.objects.all
    # print (Order.objects.all())
    try:
        for curIt in readyorders:
            # Note -- add a method here to send the readyorders object i.e. through JSON.
            print (str(curIt.id) + ' -> ' + 'READY ')  # str(curIt.orderStatus))
    except:
        print("error printing")
    return readyorders


def get_all_orders():
    print("-----geting all orders-----")
    try:
        allorders = Order.objects.all()
    except:
        print("chould not get orders")
    return allorders


def order_update():
    print ("-----checking for order update-----")
    readyorders = Order.objects.all()
    realyreadyorders = Order.objects.filter(order_complete=True)
    notreadyorders = Order.objects.filter(order_complete=False)
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


def take_order(request):
    # testdata = Order.create(customer_name='test')
    # testdata.save()
    O = Order(customer_name="Bruce", order_complete=False, time_taken=timezone.now(), order_contents='none',
              cooking_instructions='none', purchase_method='none', total_price=100)
    O.save(force_insert=True)
    return HttpResponse("OK")




from django.http import HttpResponse
from django.db import models
from django.db.models import permalink
from waiter.models import Order

# list of orders that are ready is updated every time the page is accessed (refreshed)



def index(request):
    readyorders = orderupdate()
    orderContext = {
        'readyorders': readyorders,
    }
    # can use the readorders within the HTML in a template to access a list of ready orders
    return HttpResponse(readyorders)  # this line returns the http with the list of ready orders
    # return HttpResponse()  # this line returns an empty page (the effects can be seen in the terminal)


# This method is used to check the db every 30 seconds
# to see if the order has updated.
def orderupdate():
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



from .models import Order
from django.http import JsonResponse
from django.http import HttpResponse


# list of orders that are ready is updated every time the page is accessed (refreshed)

def index(request):
    readyorders = orderupdate()
    context = {
        'readyorders': readyorders,
    }
    # can use the readorders within the HTML in a template to access a list of ready orders
    return HttpResponse(readyorders)


# This method is used to check the db every 30 seconds
# to see if the order has updated.
def orderupdate():
    print ("-----checking for order update-----")
    readyorders = Order.objects.filter(orderStatus=True)
    try:
        for curIt in readyorders:
            # Note -- add a method here to send the readyorders object i.e. through JSON.
            print (str(curIt.orderNumber) + ' -> ' + str(curIt.orderStatus))
    except:
        print("error printing")
    return readyorders


#def takeOrder():
    # method to take an order this involves added a new order to the table



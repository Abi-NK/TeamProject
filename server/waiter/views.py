from .models import Order
from django.http import JsonResponse
from django.http import HttpResponse
#from django.utils import simplejson
from django.core import serializers


# list of orders that are ready is updated every time the page is accessed (refreshed)

def index(request):
    readyorders = orderupdate()
    context = {
        'readyorders': readyorders,
    }
    # can use the readorders within the HTML in a template to access a list of ready orders
    # return HttpResponse(readyorders) # this line returns the http with the list of ready orders
    return HttpResponse()  # this line returns an empty page (the effects can be seen in the terminal)


# This method is used to check the db every 30 seconds
# to see if the order has updated.
def orderupdate():
    print ("-----checking for order update-----")
    readyorders = Order.objects.filter(orderStatus=True)
    try:
        for curIt in readyorders:
            # Note -- add a method here to send the readyorders object i.e. through JSON.
            print (str(curIt.orderNumber) + ' -> ' + 'READY')  # str(curIt.orderStatus))
    except:
        print("error printing")
    return readyorders


def takeOrder(request, orderdata):
    # method to take an order this involves added a new order to the table.
    if request.HttpRequest.POST:
        try:
            for obj in serializers.deserialize("json", orderdata):
                print (obj)
        except:
            print("failed to deserialise json data from frontend")

    # request.POST

    # alternative
    # data = simplejson.loads(request.POST['data'])



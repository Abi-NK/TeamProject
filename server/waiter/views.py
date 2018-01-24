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
    takeorder(request)
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


def takeorder(request):
    # method to take an order this involves added a new order to the table.
    #if request.HttpRequest.POST:
        if request.method == 'POST':
            print 'Raw Data: "%s"' % request.body
            parsed_json = req.body
            # should be equivalent to:
            # parsed_json = {"1": 3, "2": 6, "3": 1}
            parsed_json["1"] = 3
            # or
            for key, value in parsed_json:
                # key is the primary key of the menu item
                # value is quantity ordered
        return HttpResponse("OK")


    # request.POST.get(data to get) data i.e. orderNumber

    # alternative
    # data = simplejson.loads(request.POST['data'])



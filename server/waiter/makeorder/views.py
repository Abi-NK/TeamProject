from django.http import HttpResponse
from waiter.models import Order

def index(request):
    try:
        takeorder(request)
        print("order taken")
        return HttpResponse("order taken")
    except:
        print("problem taking order")
        return HttpResponse("Error taking order")



def takeorderTest(request):
    # method to take an order this involves added a new order to the table.
    #if request.HttpRequest.POST:
        if request.method == 'POST':
            #print 'Raw Data: "%s' % request.body
            print ('Raw Data: ' + request.body)
        return HttpResponse(request.body)


def takeorder(request):
    # method to take an order this involves added a new order to the table.
    #if request.HttpRequest.POST:
        if request.method == 'POST':
            #print 'Raw Data: "%s' %request.body
            print ('Raw Data: ' + request.body)
            parsed_json = request.body
            for key, value in parsed_json:
                # key is the primary key of the menu item
                Order.object.create(order_contents=key)
                # value is quantity ordered
                Order.object.create(order_contents=value)
        return HttpResponse("OK")


    # request.POST.get(data to get) data i.e. orderNumber

    # alternative
    # data = simplejson.loads(request.POST['data'])
from django.http import HttpResponse


# list of orders that are ready is updated every time the page is accessed (refreshed)

def index(request):
    return HttpResponse("This page has the potential to be the best page ever... it's just not there yet")


def makeordr(request):
    try:
        takeorder(request)
        print("order taken")
        return HttpResponse("order taken")
    except:
        print("problem taking order")
        return HttpResponse("Error taking order")

def orderstatus(request):
    readyorders = orderupdate()
    orderContext = {
        'readyorders': readyorders,
    }
    # can use the readorders within the HTML in a template to access a list of ready orders
    return HttpResponse(readyorders)  # this line returns the http with the list of ready orders
    # return HttpResponse()  # this line returns an empty page (the effects can be seen in the terminal)

    # This method is used to check the db every 30 seconds
    # to see if the order has updated.

def readyorders(request):
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


def takeorderTest(request):
    # method to take an order this involves added a new order to the table.
    # if request.HttpRequest.POST:
    # if request.method == 'POST':
    # print 'Raw Data: "%s' % request.body
    # print ('Raw Data: ' + request.body)
    return HttpResponse(request.body)


def takeorder(request):
    # testdata = Order.create(customer_name='test')
    # testdata.save()
    O = Order(customer_name="Bruce", order_complete=False, time_taken=timezone.now(), order_contents='none',
              cooking_instructions='none', purchase_method='none', total_price=100)
    O.save(force_insert=True)
    return HttpResponse("OK")




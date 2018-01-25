from django.http import HttpResponse
from waiter.models import Order
from django.utils import timezone

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
    # if request.HttpRequest.POST:
        # if request.method == 'POST':
            # print 'Raw Data: "%s' % request.body
            # print ('Raw Data: ' + request.body)
        return HttpResponse(request.body)


def takeorder(request):
    # testdata = Order.create(customer_name='test')
    # testdata.save()
    O = Order(customer_name="Bruce", order_complete=False, time_taken=timezone.now(), order_contents='none', cooking_instructions='none', purchase_method='none', total_price=100)
    O.save(force_insert=True)
    return HttpResponse("OK")
    # method to take an order this involves added a new order to the table.
    # if request.HttpRequest.POST:
        # if request.method == 'POST':
            # print 'Raw Data: "%s' %request.body
    #print ('Raw Data: ' + request.body)

    # parsed_json = request.body
   # for key, value in parsed_json:
        # key is the primary key of the menu item
    #    Order.object.create(order_contents='test')
        # value is quantity ordered




    # request.POST.get(data to get) data i.e. orderNumber

    # alternative
    # data = simplejson.loads(request.POST['data'])
from django.http import HttpResponse

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
            # should be equivalent to:
            # parsed_json = {"1": 3, "2": 6, "3": 1}
            parsed_json["1"] = 3
            # or
            #for key, value in parsed_json:
                # key is the primary key of the menu item
                # value is quantity ordered
        return HttpResponse("OK")


    # request.POST.get(data to get) data i.e. orderNumber

    # alternative
    # data = simplejson.loads(request.POST['data'])
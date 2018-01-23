from .models import order
from django.http import JsonResponse
from django.http import HttpResponse


def index(request):
    orderUpdate()
    return HttpResponse()


#This method is used to check the db every 30 seconds
# to see if the order has updated.
def orderUpdate():
    print ("-----chekcing for order update-----")
    readyOrders = order.objects.filter(orderStatus=True)
    print (readyOrders)

#def takeOrder():


from .models import Order
from django.http import JsonResponse
from django.http import HttpResponse


def index(request):
    orderupdate()
    return HttpResponse()


#This method is used to check the db every 30 seconds
# to see if the order has updated.
def orderupdate():
    print ("-----checking for order update-----")
    readyorders = Order.objects.filter(orderStatus=True)
    print (readyorders)

#def takeOrder():
    #method to take an order this involves added a new order to the tablecd


from django.http import HttpResponse


# list of orders that are ready is updated every time the page is accessed (refreshed)

def index(request):
    return HttpResponse("This page has the potential to be the best page ever... it's just not there yet")





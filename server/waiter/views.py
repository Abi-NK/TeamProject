from django.http import HttpResponse
from django.shortcuts import render

# list of orders that are ready is updated every time the page is accessed (refreshed)


def index(request):
    return render(request, 'waiter_index.html')



from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):

    if request.method == 'GET':
    	return HttpResponse("Menu:")
    return HttpResponse("Hello, world. You're at the polls index.")
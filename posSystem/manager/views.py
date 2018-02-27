from django.shortcuts import render


def index(request):
    """Return the manager page."""
    return render(request, 'manager/index.html')

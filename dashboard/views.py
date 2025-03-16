from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# when running the server, this will be the initial page
def index(request):
    return render(request, 'dashboard/index.html')

# if we add '/staff' to the url of the page, it redirects to staff page
def staff(request): 
    return render(request, 'dashboard/staff.html')

# if we add '/manager' to the url of the page, it redirects to manager page
def manager(request):
    return render(request, 'dashboard/manager.html')



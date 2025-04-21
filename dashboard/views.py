from django.http import HttpResponse
from django.shortcuts import render


# when running the server, this will be the initial page
def index(request):
    return render(request, 'dashboard/login.html')

# if we add '/staff' to the url of the page, it redirects to staff page
def staff(request): 
    return render(request, 'dashboard/staff.html')

# if we add '/manager' to the url of the page, it redirects to manager page
def manager(request):
    return render(request, 'dashboard/manager.html')

def stock(request):
    return render(request, 'dashboard/stock.html') 

# if we add '/schedule' to the url of the page, it redirects to schedule page
def schedule(request):
    return render(request, 'dashboard/schedule.html')





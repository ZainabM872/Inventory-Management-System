from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.db.models import Prefetch

from dashboard.models import *

# when running the server, this will be the initial page
def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #user = authenticate(request, username=username, password=password)
        user = User.objects.filter(name=username, password=password).first()
        # authenticate function checks if the user is valid
        if user:
            if Staff.objects.filter(user=user).exists():
                return redirect('dashboard-staff')
            elif Manager.objects.filter(user=user).exists():
                return redirect('dashboard-manager')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('dashboard-login')
    return render(request, 'dashboard/login.html') # otherwise if its a get request or user is not valid, it will render the login page


# if we add '/staff' to the url of the page, it redirects to staff page
def staff(request):
    return render(request, 'dashboard/staff.html')

# if we add '/manager' to the url of the page, it redirects to manager page
def manager(request):
    return render(request, 'dashboard/manager.html')

def stock(request):
    return render(request, 'dashboard/stock.html')

def suppliers(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        supplier = Supplier.objects.create(company_name=company_name)
        ContactInfo.objects.create(supplier=supplier, email=email, phone=phone)

        return redirect('suppliers-page')

    suppliers = Supplier.objects.prefetch_related(
        Prefetch('contactinfo_set')
    )
    return render(request, 'dashboard/suppliers.html', {'suppliers': suppliers})

def orders(request):
    return render(request, 'dashboard/orders.html')



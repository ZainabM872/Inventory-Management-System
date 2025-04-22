import json
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

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


def get_logged_in_staff(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(name=username, password=password).first()
        if user:
            # return staff object, not just exists()
            staff = Staff.objects.filter(user=user).first()
            return staff
    return None
# if we add '/staff' to the url of the page, it redirects to staff page


'''@login_required
def staff(request):
    user = get_logged_in_staff(request)
    staff_user = Staff.objects.filter(user=user).first()

    if not staff_user:
        return redirect('dashboard-login')

    schedule = get_object_or_404(Schedule, staff=staff_user)

    weekly_schedule = [
        {"day": "Sunday", "date": "13", "shifts": schedule.sunday or []},
       # {"day": "Monday", "date": "14", "shifts": schedule.monday or []},
        {"day": "Tuesday", "date": "15", "shifts": schedule.tuesday or []},
        {"day": "Wednesday", "date": "16", "shifts": schedule.wednesday or []},
        {"day": "Thursday", "date": "17", "shifts": schedule.thursday or []},
        {"day": "Friday", "date": "18", "shifts": schedule.friday or []},
        {"day": "Saturday", "date": "19", "shifts": schedule.saturday or []},
    ]

    return render(request, "dashboard/staff.html", {
        "schedule_json": json.dumps(weekly_schedule)
    })'''
def staff(request):
    schedules = Schedule.objects.all()
    return render(request, 'dashboard/staff.html', {'schedules': schedules})

# if we add '/manager' to the url of the page, it redirects to manager page
def manager(request):
    return render(request, 'dashboard/manager.html')

def stock(request):
    return render(request, 'dashboard/stock.html') 

# if we add '/schedule' to the url of the page, it redirects to schedule page
def schedule(request):
    return render(request, 'dashboard/schedule.html')





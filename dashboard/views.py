from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# when running the server, this will be the initial page
def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        userID = request.POST.get('user_id')
        user = authenticate(request, username=username, password=password, user_id=userID)

        # authenticate function checks if the user is valid
        if user is not None:
            login(request, user)
            if(user.is_staff):
                return redirect('dashboard/staff.html')
            elif(user.is_manager):
                return redirect('dashboard/manager.html')
            #return redirect('dashboard/login.html')
        else:
            return redirect('dashboard-login', {
                'error': 'Invalid username or password'
            })

    return render(request, 'dashboard/login.html')


# if we add '/staff' to the url of the page, it redirects to staff page
def staff(request): 
    return render(request, 'dashboard/staff.html')

# if we add '/manager' to the url of the page, it redirects to manager page
def manager(request):
    return render(request, 'dashboard/manager.html')

def stock(request):
    return render(request, 'dashboard/stock.html') 



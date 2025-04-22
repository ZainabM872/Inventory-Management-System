
import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

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
                # Store the staff's ID in the session
                request.session['user_name'] = user.name
                return redirect('dashboard-staff')
            elif Manager.objects.filter(user=user).exists():
                return redirect('dashboard-manager')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('dashboard-login')
    return render(request, 'dashboard/login.html') # otherwise if its a get request or user is not valid, it will render the login page


def staff(request):
    user_name = request.session.get('user_name')
    user = User.objects.filter(name=user_name).first()  # get the user object
    # get the staff linked to that user
    staff = Staff.objects.filter(user=user).first()

    # filter schedule for that staff only
    schedules = Schedule.objects.filter(staff=staff)
    return render(request, 'dashboard/staff.html', {'schedules': schedules})

def staff_menu_orders(request):
    if request.method == 'POST':
        item_id = request.POST.get('item')
        item_quantity = int(request.POST.get('item_quantity'))

        user_name = request.session.get('user_name')
        user = User.objects.filter(name=user_name).first()
        staff = Staff.objects.filter(user=user).first()

        if not staff:
            return redirect('staff-menu-orders')

        menu_item = MenuItem.objects.get(item_name=item_id)

        # Create the MenuOrder
        MenuOrder.objects.create(
            item=menu_item,
            item_quantity=item_quantity,
            staff=staff
        )

        # Deduct ingredients from inventory
        ingredients_used = MenuItemIngredient.objects.filter(menu_item=menu_item)
        for entry in ingredients_used:
            ingredient = entry.ingredient
            required_quantity = entry.quantity_used * item_quantity
            ingredient.quantity_in_stock -= required_quantity
            ingredient.update_stock_status()

        return redirect('staff-menu-orders')

    # Handle GET
    orders = MenuOrder.objects.select_related('item', 'staff__user')
    for order in orders:
        order.total_price = order.item.price * order.item_quantity

    menu_items = MenuItem.objects.all()

    return render(request, 'dashboard/staff_menu_orders.html', {
        'orders': orders,
        'menu_items': menu_items
    })

    
# if we add '/manager' to the url of the page, it redirects to manager page
def manager(request):
    return render(request, 'dashboard/manager.html')

def stock(request):
    if request.method == 'POST':
        ingredient = request.POST.get('ingredient')
        quantity = request.POST.get('quantity_in_stock')
        unit = request.POST.get('unit')
        reorder_level = request.POST.get('reorder_level')
        stock_status = request.POST.get('stock_status')

        InventoryItem.objects.create(
            ingredient=ingredient,
            quantity_in_stock=quantity,
            unit=unit,
            reorder_level=reorder_level,
            stock_status=stock_status
        )
        return redirect('stock-page')

    inventory_items = InventoryItem.objects.all()
    return render(request, 'dashboard/stock.html', {'inventory_items': inventory_items})

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
    if request.method == 'POST':
        supplier_id = request.POST.get('supplier')
        ingredient_id = request.POST.get('ingredient')
        quantity = int(request.POST.get('quantity'))
        delivery_date = request.POST.get('delivery_date')
        total_cost = Decimal(request.POST.get('total_cost'))
        status = request.POST.get('status')

        supplier = Supplier.objects.get(id=supplier_id)
        ingredient = InventoryItem.objects.get(ingredient=ingredient_id)

        # Assuming the manager is tied to the logged-in user
        # manager = Manager.objects.filter(user=request.user).first()   # uncomment this once auth is done
        manager = Manager.objects.first()
        if not manager:
            messages.error(request, "No manager stored. Please add one.")
            return redirect('orders-page')

        # Create the order
        order = SupplyOrder.objects.create(
            supplier=supplier,
            manager=manager,
            delivery_date=delivery_date,
            total_cost=total_cost,  # You can calculate cost based on quantity if you want
            status=status
        )

        # Create the order detail
        SupplyOrderDetail.objects.create(
            supply_order=order,
            supplier=supplier,
            ingredient=ingredient,
            quantity_ordered=quantity
        )

        return redirect('orders-page')

    orders = SupplyOrder.objects.select_related('manager__user', 'supplier', 'supplyorderdetail__ingredient').order_by('-order_date')
    suppliers = Supplier.objects.all()
    ingredients = InventoryItem.objects.all()

    return render(request, 'dashboard/orders.html', {
        'orders': orders,
        'suppliers': suppliers,
        'ingredients': ingredients
    })

# if we add '/schedule' to the url of the page, it redirects to schedule page
def schedule(request):
    return render(request, 'dashboard/schedule.html')





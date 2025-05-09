
import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Sum, F, DecimalField
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from dashboard.models import *


# when running the server, this will be the initial page
def index(request):
    # If the user is already logged in (session exists), redirect accordingly
    if 'user_name' in request.session:
        user_name = request.session['user_name']
        user = User.objects.filter(name=user_name).first()

        if user:
            if Staff.objects.filter(user=user).exists():
                return redirect('dashboard-staff')
            elif Manager.objects.filter(user=user).exists():
                return redirect('dashboard-manager')

    # Handle login form submission
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(name=username, password=password).first()

        if user:
            request.session['user_name'] = user.name
            if Staff.objects.filter(user=user).exists():
                return redirect('dashboard-staff')
            elif Manager.objects.filter(user=user).exists():
                return redirect('dashboard-manager')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('dashboard-login')

    # If no session and no POST login, show the login page
    return render(request, 'dashboard/login.html')

    '''if request.method == 'POST':
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
                request.session['user_name'] = user.name
                return redirect('dashboard-manager')
        elif request.session.session_key:
            if Staff.objects.filter(user=user).exists():
                # Store the staff's ID in the session
                request.session['user_name'] = user.name
                return redirect('dashboard-staff')

            elif Manager.objects.filter(user=user).exists():
                request.session['user_name'] = user.name
                return redirect('dashboard-manager')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('dashboard-login')
    return render(request, 'dashboard/login.html') # otherwise if its a get request or user is not valid, it will render the login page'''


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
        items = request.POST.getlist('items[]')
        quantities = request.POST.getlist('quantities[]')

        user_name = request.session.get('user_name')
        user = User.objects.filter(name=user_name).first()
        staff = Staff.objects.filter(user=user).first()

        if not staff:
            return redirect('staff-menu-orders')

        order = MenuOrder.objects.create(staff=staff)

        # Process each item in the order
        for item_id, qty in zip(items, quantities):
            qty = int(qty)
            menu_item = MenuItem.objects.get(item_name=item_id)

            # Check ingredient stock
            ingredients_used = MenuItemIngredient.objects.filter(menu_item=menu_item)
            for entry in ingredients_used:
                ingredient = entry.ingredient
                required_quantity = entry.quantity_used * qty
                if ingredient.quantity_in_stock < required_quantity:
                    messages.error(request, f"Not enough stock for {ingredient.ingredient}.")
                    order.delete()  # cleanup partial order
                    return redirect('staff-menu-orders')


        # All stock is valid — add the items
        for item_id, qty in zip(items, quantities):
            qty = int(qty)
            menu_item = MenuItem.objects.get(item_name=item_id)
            MenuOrderItem.objects.create(order=order, item=menu_item, quantity=qty)

            # Deduct inventory
            for entry in MenuItemIngredient.objects.filter(menu_item=menu_item):
                ingredient = entry.ingredient
                required_quantity = entry.quantity_used * qty
                ingredient.quantity_in_stock -= required_quantity
                ingredient.update_stock_status()
                ingredient.save()
                # call create alert function to check if any alerts need to be generate and displayed
                createAlert(ingredient)

        return redirect('staff-menu-orders')

    # Handle GET
    orders = MenuOrder.objects.select_related('staff__user').all()

    for order in orders:
        items = order.items.select_related('item')  # prefetch item info too
        # order.total_price = sum(i.item.price * i.quantity for i in items)
        order.item_list = items

    menu_items = MenuItem.objects.all()

    return render(request, 'dashboard/staff_menu_orders.html', {
        'orders': orders,
        'menu_items': menu_items
    })


def createAlert(ingredient):
    # Check if the stock level is out of stock
    if ingredient.quantity_in_stock == 0:
        # First, resolve any low stock alerts if they exist
        low_stock_alerts = Alert.objects.filter(
            ingredient=ingredient, alert_type='Low Stock', resolved=False)
        if low_stock_alerts.exists():
            # Mark low stock alerts as resolved
            low_stock_alerts.update(resolved=True)

        # Create an out-of-stock alert if not already present
        if not Alert.objects.filter(ingredient=ingredient, alert_type='Out of Stock', resolved=False).exists():
            # Create a new out-of-stock alert
            Alert.objects.create(ingredient=ingredient,
                                 alert_type='Out of Stock', resolved=False)

    elif ingredient.quantity_in_stock <= ingredient.reorder_level:
        # Check if there is already an out-of-stock alert and resolve it if present
        out_of_stock_alerts = Alert.objects.filter(
            ingredient=ingredient, alert_type='Out of Stock', resolved=False)
        if out_of_stock_alerts.exists():
            # Mark out-of-stock alerts as resolved
            out_of_stock_alerts.update(resolved=True)

        # Create a low stock alert if not already present
        if not Alert.objects.filter(ingredient=ingredient, alert_type='Low Stock', resolved=False).exists():
            # Create a new low stock alert
            Alert.objects.create(ingredient=ingredient,
                                 alert_type='Low Stock', resolved=False)


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


def alert(request):
    # Fetch unresolved alerts to display
    unresolved_alerts = Alert.objects.filter(resolved=False)
    unresolved_alerts_count = unresolved_alerts.count()

    return render(request, 'dashboard/alerts.html', {
        'unresolved_alerts': unresolved_alerts,
        'unresolved_alerts_count': unresolved_alerts_count,
    })

def manager(request):
    now = timezone.now()
    current_month_orders = MenuOrder.objects.filter(
        order_date__year=now.year,
        order_date__month=now.month
    )

    # Sum total = sum of item.price * quantity for each MenuOrderItem in current month
    monthly_total = MenuOrderItem.objects.filter(
        order__in=current_month_orders
    ).aggregate(
        total=Sum(F('item__price') * F('quantity'), output_field=DecimalField())
    )['total'] or 0

    user_name = request.session.get('user_name')
    user = User.objects.filter(name=user_name).first()  # get the user object
    manager = Manager.objects.filter(user=user).first()

    pending_supply = SupplyOrder.objects.filter(status='Pending')
    total_pending_orders = pending_supply.count()

    alert_items = Alert.objects.filter(resolved=False)
    total_alerts = alert_items.count()


    return render(request, 'dashboard/manager.html', {
        'alert_items': alert_items,
        'total_alerts': total_alerts,
        'pending_supply': total_pending_orders,
        'manager_name': manager.user.name if manager else 'Manager',
        'montly_sales': monthly_total
    })


def resolve_alert(request, alert_id):
    alert = Alert.objects.get(id=alert_id)
    alert.resolved = True
    alert.save()
    return redirect('dashboard-manager')


def staff_menu(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'dashboard/staff_menu.html', {'menu_items': menu_items})
  
def logout_view(request):
    request.session.flush()  # This clears all session data
    return redirect('dashboard-login')  # Redirect to login page

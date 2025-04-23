from django.db import models


class User(models.Model):
    '''User Table'''
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Manager(models.Model):
    '''Manager Table'''
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"{self.user.name}"

class Staff(models.Model):
    '''Staff Table'''
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"{self.user.name}"

class Schedule(models.Model):
    '''Schedule Table'''
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, primary_key=True)
    tuesday = models.CharField(max_length=20)
    wednesday = models.CharField(max_length=20)
    thursday = models.CharField(max_length=20)
    friday = models.CharField(max_length=20)
    saturday = models.CharField(max_length=20)
    sunday = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.staff}'s schedule"

class Supplier(models.Model):
    '''Supplier Table'''
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name

class ContactInfo(models.Model):
    '''ContactInfo Table'''
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    class Meta:
        unique_together = ('supplier', 'email', 'phone')


class InventoryItem(models.Model):
    '''InventoryItem Table'''
    ingredient = models.CharField(max_length=20, primary_key=True)
    quantity_in_stock = models.IntegerField(default=0)
    unit = models.CharField(max_length=20)
    reorder_level = models.IntegerField(default=10)

    IN_STOCK_CHOICES = [
        ('In Stock', 'In Stock'),
        ('Low Stock', 'Low Stock'),
        ('Out of Stock', 'Out of Stock'),
    ]
    stock_status = models.CharField(max_length=20, choices=IN_STOCK_CHOICES, default='In Stock')

    def __str__(self):
        return self.ingredient


class SupplyOrder(models.Model):
    '''SupplyOrder Table'''
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.supplier} - ${self.total_cost}"


class SupplyOrderDetail(models.Model):
    '''SupplyOrderDetail Table'''
    supply_order = models.OneToOneField(SupplyOrder, on_delete=models.CASCADE, primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    ingredient = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, null=True)
    quantity_ordered = models.IntegerField()

    def __str__(self):
        return f"{self.supply_order} - {self.ingredient} ({self.quantity_ordered})"


class MenuItem(models.Model):
    '''MenuItem Table (Individual items on the menu)'''
    item_name = models.CharField(max_length=50, primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.item_name


class MenuOrder(models.Model):
    '''MenuOrder Table (Customer entire order)'''
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.staff.user.name if self.staff else 'Unknown'}"

    @property
    def total_price(self):
        return sum(item.item.price * item.quantity for item in self.items.all())


class MenuOrderItem(models.Model):
    '''Intermediate table for MenuOrder and MenuItem.
    (Contains each individual item in customer's order)'''
    order = models.ForeignKey(MenuOrder, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('order', 'item')

    def __str__(self):
        return f"{self.order} - {self.item} ({self.quantity})"


class MenuItemIngredient(models.Model):
    '''MenuItemIngredient Table'''
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity_used = models.IntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('menu_item', 'ingredient')

    def __str__(self):
        return f"{self.menu_item} - {self.ingredient} ({self.quantity_used})"


class Alert(models.Model):
    '''Alert Table'''
    ingredient = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=20, choices=[('Low Stock', 'Low Stock'), ('Out of Stock', 'Out of Stock')])
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.ingredient} - ({self.alert_type})"



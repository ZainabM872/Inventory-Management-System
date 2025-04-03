from django.contrib import admin

from .models import (
    User, 
    Manager, 
    Staff, 
    Schedule, 
    Supplier, 
    ContactInfo, 
    InventoryItem, 
    SupplyOrder, 
    SupplyOrderDetail,
    MenuItem,
    MenuOrder, 
    MenuItemIngredient, 
    Alert
)

admin.site.register(User)
admin.site.register(Manager)
admin.site.register(Staff)
admin.site.register(Schedule)
admin.site.register(Supplier)
admin.site.register(ContactInfo)
admin.site.register(InventoryItem)
admin.site.register(SupplyOrder)
admin.site.register(SupplyOrderDetail)
admin.site.register(MenuItem)
admin.site.register(MenuOrder)
admin.site.register(MenuItemIngredient)
admin.site.register(Alert)

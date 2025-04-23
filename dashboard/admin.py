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
    Alert,
    MenuOrderItem
)

# This will make the suppliers' contact info show up together on the admin page.
class ContactInfoInline(admin.StackedInline):
    model = ContactInfo
    extra = 0

class SupplierAdmin(admin.ModelAdmin):
    inlines = [ContactInfoInline]


admin.site.register(Supplier, SupplierAdmin)
admin.site.register(User)
admin.site.register(Manager)
admin.site.register(Staff)
admin.site.register(Schedule)
admin.site.register(InventoryItem)
admin.site.register(SupplyOrder)
admin.site.register(SupplyOrderDetail)
admin.site.register(MenuItem)
admin.site.register(MenuOrder)
admin.site.register(MenuOrderItem)
admin.site.register(MenuItemIngredient)
admin.site.register(Alert)

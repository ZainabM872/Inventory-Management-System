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

@admin.register(MenuOrder)
class MenuOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'staff', 'order_date')  # Add fields you want to display
    list_filter = ('order_date',)
    ordering = ('-order_date',)
    search_fields = ('staff__user__name',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'price')
    search_fields = ('item_name',)

@admin.register(MenuItemIngredient)
class MenuItemIngredientAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'ingredient', 'quantity_used')
    search_fields = ('menu_item__item_name', 'ingredient__name')

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'quantity_in_stock', 'stock_status')
    list_filter = ('stock_status',)
    search_fields = ('name',)

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'resolved')
    list_filter = ('resolved',)
    search_fields = ('ingredient__name',)


admin.site.register(Supplier, SupplierAdmin)
admin.site.register(User)
admin.site.register(Manager)
admin.site.register(Staff)
admin.site.register(Schedule)
admin.site.register(SupplyOrder)
admin.site.register(SupplyOrderDetail)
admin.site.register(MenuOrderItem)

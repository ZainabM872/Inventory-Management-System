from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='dashboard-login'),
    path('staff/', views.staff, name='dashboard-staff'),
    path('manager/', views.manager, name='dashboard-manager'),
    path('stock/', views.stock, name='stock-page'),
    path('schedule/', views.schedule, name='dashboard-schedule'),
    path('suppliers/', views.suppliers, name='suppliers-page'),
    path('orders/', views.orders, name='orders-page'),
    path('alerts/<int:alert_id>/resolve/', views.resolve_alert, name='resolve-alert'),
    path('staff/menuorders/', views.staff_menu_orders, name='staff-menu-orders'),
    path('alerts/', views.alert, name='alert-page'),
    path('staff/menu/', views.staff_menu, name='staff_menu')
]

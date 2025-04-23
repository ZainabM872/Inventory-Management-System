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
    path('staff/menuorders/', views.staff_menu_orders, name='staff-menu-orders'),
    # path('logout/', LogoutView.as_view(next_page='dashboard-login'), name='logout')
]

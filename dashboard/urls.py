from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='dashboard-login'),
    path('staff/', views.staff, name='dashboard-staff'),
    path('manager/', views.manager, name='dashboard-manager'),
    path('stock/', views.stock, name='stock-page')
]

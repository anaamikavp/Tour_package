from django.contrib import admin
from django.urls import path,include
from administrator import views

urlpatterns = [
    path('admin_index/', views.admin_index),
    path('packages/', views.admin_packages),
    path('package_details/<int:id>', views.package_details),
    path('approve_package/<int:id>', views.approve_package),
    path('reject_package/<int:id>', views.reject_package),
    path('view_bookings/', views.view_bookings),
    path('view_vendors/', views.view_vendors),
]

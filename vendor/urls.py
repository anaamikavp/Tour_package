from django.contrib import admin
from django.urls import path,include
from vendor import views

urlpatterns = [
    path('register/',views.register),
    path('vendor_registration/', views.vendor_registration),
    path('vendor_index/', views.vendor_index),
    path('package_form/', views.package_form),
    path('create_package/',views.package_creation),
    path('view_package/',views.package_view),
    path('edit_package/<int:id>',views.package_edit),
    path('update_package/<int:id>',views.package_updation),
    path('bookings/',views.bookings),
]

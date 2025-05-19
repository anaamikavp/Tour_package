from django.contrib import admin
from django.urls import path,include
from user import views

urlpatterns = [

    path('',views.display_index),

    path('user_register/',views.display_user_registration),
    path('user_registration/', views.user_registration),
    path('login/',views.display_login),
    path('sign_in/',views.login),
    path('show_packages/',views.display_packages),
    path('booking_form/',views.booking_form),
    path('booking/',views.booking),
    path('payment/',views.payment_page),
    path('transaction/<int:id>',views.transaction),
    path('logout/',views.logout_view),
    path('package_readmore/<int:id>',views.package_readmore),
    path('create_order/<int:booking_id>/', views.create_order, name='create_order'),
    path('payment/success/', views.payment_success, name='payment_success'),

]

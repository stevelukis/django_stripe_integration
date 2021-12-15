from django.urls import path

from orders import views

path('checkout/<int:product>/', views.Checkout.as_view())

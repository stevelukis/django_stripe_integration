from django.urls import path

from orders import views

urlpatterns = [
    path('checkout/<int:product>/', views.Checkout.as_view())
]

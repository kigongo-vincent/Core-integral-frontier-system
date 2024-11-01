from django.urls import path 
from . import views

urlpatterns = [
    path("", views.welcome),
    path('token', views.CustomTokenObtainPairView.as_view()),
    path('signup', views.signup),
    path('products/<str:category>', views.get_products),
    path('add_product', views.add_product),
    path('delete_product/<str:pk>', views.delete_product),
    path('update_product/<str:pk>', views.update_product),
    path('all_products', views.all_products),
    path('customer_orders/<str:pk>', views.customer_orders),
    path('change_password/<str:pk>', views.change_password),
    path('search/<str:query>', views.search),
    path('services', views.services),
    path('orders', views.orders),
    path('update_order/<str:pk>', views.update_order),
    path('customers/', views.customers),
    path('update_customer/<str:pk>', views.update_customer),
    path('statistics', views.statistics)
]
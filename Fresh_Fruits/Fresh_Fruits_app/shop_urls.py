from django.urls import path
from .shop_views import *


urlpatterns = [
    path('',RenterHomeView.as_view()),
    path('fruits_product',fruits_product.as_view()),
    path('fruits_product_view',Fruits_View_Product.as_view()),
    path('Fruits_update_product',Fruits_update_product.as_view()),
    path('Fruits_view_bookings',Fruits_view_bookings.as_view()),
    path('feedback',feed_booking.as_view()),





    
  

   
]
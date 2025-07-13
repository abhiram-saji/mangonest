from django.urls import path
from .user_view import *

urlpatterns = [
    path('',UserHomeView.as_view()),
    path('User_product_View',UserproductView.as_view()),
    path('Cart_View',CartProductView.as_view()),
    path('details_product',UserproductDetails.as_view()),
    path('RemovecartView',RejectcartView.as_view()),
    path('payment_method',payments.as_view()),
    path('order_view',Orderview.as_view()),
    path('feedback_method',feedback_method.as_view()),
    path('delete_booking',cancel_order.as_view()),
   
]
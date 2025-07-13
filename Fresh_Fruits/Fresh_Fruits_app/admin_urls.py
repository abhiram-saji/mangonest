from django.urls import path
from .admin_views import *


urlpatterns = [
    path('',AdminHomeView.as_view()),
    path('verify_user',AdminuserView.as_view()),
    path('verify_shop',AdminshopView.as_view()),
    path('admin_approve',admin_approve.as_view()),
    path('admin_reject',admin_reject.as_view()),
    path('admin_view_bookings',admin_view_bookings.as_view()),
    path('feedback',feedback_view.as_view()),
]
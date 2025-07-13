"""
URL configuration for Fresh_Fruits project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from Fresh_Fruits_app import admin_urls, user_urls,shop_urls
from Fresh_Fruits_app.views import *


urlpatterns = [
    
    path('', HomeView.as_view()),
    path('login',LoginView.as_view()),
    path('register',RegisterView.as_view()),
    path('shop_reg',shopView.as_view()),

    path('admin/', include(admin_urls)),
    path('user/', include(user_urls)),
    path('shop/', include(shop_urls)),

]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

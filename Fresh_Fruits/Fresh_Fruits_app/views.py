from django.shortcuts import render, redirect
from django.views.generic import TemplateView   
from django.contrib.auth.models import User
import pyttsx3
from django.contrib.auth import authenticate, login, logout
from.models import *


# Create your views here.

class HomeView(TemplateView):
    template_name='index.html'

class LoginView(TemplateView):
    template_name='login.html'
    def post(self, request,*args,**kwargs):
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            if user.last_name == '1':
                try:
                    if user.is_superuser:
                            return redirect('admin/')
                    elif UserType.objects.get(user_id=user.id).type == "user":
                            return redirect('user/')
                    elif UserType.objects.get(user_id=user.id).type == "shop":
                            return redirect('shop/')
                    
                except UserType.DoesNotExist:
                    return render(request,'index.html',{'message':"User Account Not Authenticated"})
                
            else:
                
                return render(request,'index.html',{'message':"User Account Not Authenticated"})
                
        else:
            return render(request,'index.html',{'message':"invalid username and password"})
            


class RegisterView(TemplateView):
    template_name='register.html'

    def post(self, request,*args,**kwargs):
        name=request.POST['name']
        email=request.POST['email']
        phone_number=request.POST['phone_number']
        address=request.POST['address']
        username=request.POST['username']
        password=request.POST['password']
        if User.objects.filter(username=username):
            return render(request,'index.html',{'message':"already added the username or email"})
        elif User.objects.filter(email=email):
             return render(request,'index.html',{'message':"already added the username or email"})
        else:
            user=User.objects.create_user(username=username,password=password,email=email,first_name=name,last_name='0')
            user.save()
            user_address=user_reg(user=user,address=address,phone=phone_number)
            user_address.save()
            user_type=UserType(user=user,type='user')
            user_type.save()
            print ('success')
            return render(request,'index.html',{'message':"Account Registered successfully"})
            engine = pyttsx3.init()
            msg = " Account Registered successfully"
            engine.say(msg)
            engine.runAndWait()
            return redirect('/')


class shopView(TemplateView):
    template_name='shop.html'
    def post(self, request,*args,**kwargs):
        shop_name=request.POST['shop_name']
        email=request.POST['email']
        owner_first_name=request.POST['owner_first_name']
        phone_number=request.POST['phone_number']
        shop_address=request.POST['shop_address']
        city=request.POST['city']
        image=request.FILES['image']
        username=request.POST['username']
        password=request.POST['password']

        if User.objects.filter(username=username):
            print ('pass')
            return render(request,'index.html',{'message':"already added the username or email"})
        elif User.objects.filter(email=email):
             return render(request,'index.html',{'message':"already added the username or email"})
        else:
            user=User.objects.create_user(username=username,password=password,email=email,first_name=shop_name,last_name='0')
            user.save()
            user_address=shop_reg(user=user,address=shop_address,phone=phone_number,image=image,shop_owner_name=owner_first_name,city=city)
            user_address.save()
            user_type=UserType(user=user,type='shop')
            user_type.save()
            print ('success')
            return render(request,'index.html',{'message':"Account Registered successfully"})

            engine = pyttsx3.init()
            msg = " Account Registered successfully"
            engine.say(msg)
            engine.runAndWait()
            return redirect('/')
           

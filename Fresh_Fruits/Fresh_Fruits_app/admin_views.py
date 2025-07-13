from django.views.generic import TemplateView , View
import pyttsx3
from .models import *
from django.shortcuts import render ,redirect

class AdminHomeView(TemplateView):
    template_name='admin/index.html'

class AdminuserView(TemplateView):
    template_name='admin/verify_user.html'
    def get_context_data(self, **kwargs):
        context = super(AdminuserView,self).get_context_data(**kwargs)
        user = user_reg.objects.filter(user__last_name='0',user__is_staff='0',user__is_active='1')
        users = user_reg.objects.filter(user__last_name='1',user__is_active='1')
        context['user'] = user
        context['users'] = users
        return context
    
   

class AdminshopView(TemplateView):
    template_name='admin/verify_shop.html'

    def get_context_data(self, **kwargs):
        context = super(AdminshopView,self).get_context_data(**kwargs)
        shop = shop_reg.objects.filter(user__last_name='0',user__is_staff='0',user__is_active='1')
        shops = shop_reg.objects.filter(user__last_name='1',user__is_active='1')
        context['shop'] = shop
        context['shops'] = shops

        return context
    

class admin_approve(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['user_id']
        user = User.objects.get(pk=id)
        user.last_name='1'
        user.save()
        return render(request,'admin/index.html',{'message':"Account Approved"})
        engine = pyttsx3.init()
        msg = "Account Approved"
        engine.say(msg)
        engine.runAndWait()
        return redirect('/admin')


class admin_reject(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['user_id']
        user = User.objects.get(pk=id)
        user.last_name='0'
        user.is_active='0'
        user.save()
        return render(request,'admin/index.html',{'message':"Account reject"})
        engine = pyttsx3.init()
        msg = "Account reject"
        engine.say(msg)
        engine.runAndWait()
        return redirect('/admin')



class admin_view_bookings(TemplateView):
    template_name='admin/view_booking.html'
    def get_context_data(self, **kwargs):
        context = super(admin_view_bookings, self).get_context_data(**kwargs)
        bookings = Booking.objects.all()
        context['bookings'] = bookings
        return context
    
class feedback_view(TemplateView):
    template_name='admin/feedback.html'
    def get_context_data(self, **kwargs):
        context = super(feedback_view, self).get_context_data(**kwargs)
        feed = Feedback.objects.all()
        context['feed'] = feed
        return context
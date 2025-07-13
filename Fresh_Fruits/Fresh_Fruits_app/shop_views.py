from django.views.generic import TemplateView ,View
from django.shortcuts import render,redirect
import pyttsx3
from .models import *
from django.contrib import messages

class RenterHomeView(TemplateView):
    template_name='shop/index.html'
  
   
class fruits_product(TemplateView):
    template_name='shop/add_product.html'
    def post(self, request,*args,**kwargs):
        user=shop_reg.objects.get(user_id=self.request.user.id)
        product_name=request.POST['product_name']
        product_price=request.POST['product_price']
        category=request.POST['category']
        quantity=request.POST['quantity']
        discount=request.POST['discount']
        description=request.POST['description']
        product_image=request.FILES['product_image']
        discount_price = int(product_price) - (int(product_price) * int(discount) / 100)
        if Fruits.objects.filter(name=product_name).exists():
            return render(request, 'shop/index.html', {'message': "Product name already exists."})
            
        else:
            product = Fruits.objects.create(
            user=user,  
            name=product_name,
            price=product_price,
            category=category,
            quantity=quantity,
            discount=discount,
            description=description,
            image=product_image,
            discountprice=discount_price
            )
            return render(request,'shop/index.html',{'message':"successfully added the product"})

            



class Fruits_View_Product(TemplateView):
    template_name = 'shop/view_product.html'
    def get_context_data(self, **kwargs):
        context = super(Fruits_View_Product, self).get_context_data(**kwargs)
        shop = shop_reg.objects.get(user_id=self.request.user.id)
        pro = Fruits.objects.filter(user_id=shop)
        context['prod'] = pro
        return context
    
    
class Fruits_update_product(TemplateView):
    template_name ='shop/update_product.html'
    def get_context_data(self, **kwargs):
        context = super(Fruits_update_product, self).get_context_data(**kwargs)
        shop=shop_reg.objects.get(user_id=self.request.user.id)
        product_id=self.request.GET['product_id']
        pr=Fruits.objects.get(user_id=shop,id=product_id)
        context['product']=pr
        return context
    
    def post(self, request, *args, **kwargs):
        product_id=request.GET['product_id']
        pr=Fruits.objects.get(id=product_id)
        pr.name=request.POST['name']
        if request.POST['category']:
            pr.category=request.POST['category']
        pr.discount=request.POST['dsprice']
        pr.price=request.POST['price']
        pr.description=request.POST['description']
        if request.FILES.get('image'):
            pr.image=request.FILES['image']
        pr.quantity=request.POST['quantity']
        pr.discountprice = int(request.POST['price']) - (int(request.POST['price']) * int(request.POST['dsprice']) / 100)
        pr.save()
        return render(request,'shop/index.html',{'message':"successfull update"})
    
class Fruits_view_bookings(TemplateView):
    template_name='shop/view_booking.html'
    def get_context_data(self, **kwargs):
        context = super(Fruits_view_bookings, self).get_context_data(**kwargs)
        user=shop_reg.objects.get(user_id=self.request.user.id)
        bookings = Booking.objects.filter(product__user_id=user,action_in=['paid','Cancelled'])
        context['bookings'] = bookings
        return context
    def post(self,request, *args, **kwargs):
        book_id=request.POST['booking_id']
        status=request.POST['status']
        book=Booking.objects.get(id=book_id)
        book.status=status
        book.save()
        return render(request,'shop/index.html',{'message':"Delivered updated"})
    
class feed_booking(TemplateView):
    template_name='shop/feedback.html'
    def get_context_data(self, **kwargs):
        context = super(feed_booking, self).get_context_data(**kwargs)
        user=shop_reg.objects.get(user_id=self.request.user.id)
        feed = Feedback.objects.filter(booking__product__user_id=user)
        context['feed'] = feed
        return context
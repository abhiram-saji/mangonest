from datetime import timezone,timedelta,datetime
from django.shortcuts import redirect,render
from django.views.generic import TemplateView 
from .models import *
from django.contrib import messages
from django.db.models import Q

from django.utils.timezone import now



class UserHomeView(TemplateView):
    template_name='user/index.html'

class UserproductView(TemplateView):
    template_name='user/view_product.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_option = self.request.GET.get('sort', '')
        search_query = self.request.GET.get('search_query', '')

        
        products = Fruits.objects.all()

        if search_query:
            products = Fruits.objects.filter(Q(name__icontains=search_query) )

        if sort_option == 'low_to_high':
            products = products.order_by('discountprice')
        elif sort_option == 'high_to_low':
            products = products.order_by('-discountprice')
        elif sort_option == 'popular':
            popular_products = Booking.objects.values('product').annotate(count=models.Count('id')).order_by('-count')
            products = Fruits.objects.filter(id__in=popular_products.values('product')).order_by('-discount')[:4]
            
        context['prod'] = products
        context['sort_option'] = sort_option
        context['search_query'] = search_query 

        
        context['veg'] = Fruits.objects.filter(category='Vegetables')  
        context['fruits'] = Fruits.objects.filter(category='Fruits') 
        context['herb'] = Fruits.objects.filter(category='Herb')
        return context 
    
class UserproductDetails(TemplateView):
    template_name='user/view_product_details.html'
    def get_context_data(self, **kwargs):
        context = super(UserproductDetails, self).get_context_data(**kwargs)
        user=user_reg.objects.get(user_id=self.request.user.id)
        p_id=self.request.GET['p_id']
        context['products'] =Fruits.objects.filter(pk=p_id) 
        context['prod'] =Fruits.objects.all() 
        context['Fruits_count'] = Fruits.objects.filter(category='Fruits').distinct().count()
        context['Vegetables_count'] = Fruits.objects.filter(category='Vegetables').distinct().count()
        context['Herb_count'] = Fruits.objects.filter(category='Herb').distinct().count()       
        return context 
    def post(self, request, *args, **kwargs):
        p_id=self.request.GET['p_id']
        qnt=request.POST['quantity']
        user=user_reg.objects.get(user_id=self.request.user.id)
        prd =Fruits.objects.get(pk=p_id)
        existing=Booking.objects.filter(user=user,product=prd,action='Add To Cart').first() 
        total=int(qnt)*int(prd.discountprice)
        if existing:
            existing.quantity=int(existing.quantity)+int(qnt)
            existing.totalprice=existing.quantity*existing.product.discountprice
            existing.save()
            messages.success(request,"Cart updated")
        else:
            book=Booking.objects.create(quantity=qnt,user=user,product=prd,action='Add To Cart',totalprice=total) 
            messages.success(request,"Add To Cart")
        return redirect('/user/Cart_View')
    
class CartProductView(TemplateView):
    template_name='user/cart_product.html'
    def get_context_data(self, **kwargs):
        context = super(CartProductView, self).get_context_data(**kwargs)
        user=user_reg.objects.get(user_id=self.request.user.id)
        cart_items = Booking.objects.filter(user=user, action='Add To Cart')
        context['pro'] = cart_items
        total=0
        for i in cart_items:
            total=total+int(i.totalprice)
        context['total'] = total
        
        return context
class RejectcartView(TemplateView):
    def dispatch(self,request,*args,**kwargs):
        book_id = request.GET['book_id']
        Booking.objects.get(id=book_id).delete()
        return redirect(request.META['HTTP_REFERER'])
       
class payments(TemplateView):
    template_name='user/checkout.html'
    def get_context_data(self, **kwargs):
        context = super(payments, self).get_context_data(**kwargs)
        user=user_reg.objects.get(user_id=self.request.user.id)
        cart_items = Booking.objects.filter(user=user, action='Add To Cart')
        context['pro'] = cart_items
        total=0
        for i in cart_items:
            total=total+int(i.totalprice)
        context['total'] = total
        context['current_month'] = datetime.now().strftime('%Y-%m')
        return context
    def post(self, request, *args, **kwargs):
            user=user_reg.objects.get(user_id=self.request.user.id)
            cart_items = Booking.objects.filter(user=user, action='Add To Cart')
            for item in cart_items:
                item.action = 'paid'
                item.product.quantity = int(item.product.quantity) - int(item.quantity)
                item.product.save()  
                item.save()
            messages.success(request, "payment has been made!")
            return redirect('/user/')

class Orderview(TemplateView):
    template_name='user/order.html'
    def get_context_data(self, **kwargs):
        context = super(Orderview, self).get_context_data(**kwargs)
        user=user_reg.objects.get(user_id=self.request.user.id)
        # cart_items = Booking.objects.filter(user=user, action='paid')
        # context['feed_exists'] =Feedback.objects.all() 
        # context['feed_exists'] =Feedback.objects.filter(booking__in=cart_items).exists()
        # feed_exists = {booking.id: Feedback.objects.filter(booking=booking).exists() for booking in cart_items}
        # context['pro'] = cart_items
        # context['feed_exists'] = feed_exists 
        # return context
        cart_items = Booking.objects.filter(user=user, action='paid') 
        booking_ids = cart_items.values_list('id')
        feedbacks = Feedback.objects.filter(booking_id__in=booking_ids)
        feedback_dict = {fb.booking_id: True for fb in feedbacks}
        context['feedback_dict'] = feedback_dict
        context['pro'] = cart_items
        return context
    
class feedback_method(TemplateView):
    template_name='user/feedback.html'
    def post(self, request, *args, **kwargs):
        emoji_reaction = request.POST['rating']
        feedback_message = request.POST['feedbackComment']
        book_id=request.GET['book_id']
        bookings = Booking.objects.get(id=book_id)
        user=user_reg.objects.get(user_id=self.request.user.id)
        se=Feedback(
            user=user,
            booking=bookings,
            reaction=emoji_reaction,
            feedback_message=feedback_message,
        )
        se.save()
        messages.success(request, 'Thank you for your feedback!')
        return redirect('/user/')


class cancel_order(TemplateView):
    def dispatch(self,request,*args,**kwargs):
        book_id = request.GET['book_id']
        Booking.objects.filter(id=book_id).update(status='Cancelled')
        messages.success(request, 'Order Cancelled!')
        return redirect('/user/order_view')
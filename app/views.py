from django.db.models import Count, Avg
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import razorpay
from . models import Cart, Customer, Payment, Product, Wishlist, OrderPlaced
from . forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages 
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Import the reviews API client
from .utils.reviews_api import ReviewsAPI

@login_required
def home(request):  
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/home.html",locals())
@login_required
def about(request):  

    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/about.html",locals())
@login_required
def contact(request):  
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/contact.html",locals())
@method_decorator(login_required, name='dispatch')
class CategoryView(View):
    def get(self, request,val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, 'app/category.html',locals())
@method_decorator(login_required, name='dispatch')
class CategoryTitle(View):
    def get(self, request,val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, 'app/category.html',locals())
    
@method_decorator(login_required, name='dispatch')  
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        
        # Fetch reviews from the API
        reviews_data = ReviewsAPI.get_product_reviews(
            product_id=product.id,
            product_title=product.title,
            category=product.category
        )
        
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        
        context = {
            'product': product,
            'wishlist': wishlist,
            'totalitem': totalitem,
            'wishitem': wishitem,
            'reviews': reviews_data['reviews'],
            'avg_rating': reviews_data['average_rating'],
            'star_range': range(1, 6),  # For star display
            'reviews_count': reviews_data['count'],
            'user': request.user,  # Add the user to the context
        }
        
        return render(request, 'app/productdetail.html', context)
    
    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        user = request.user
        
        # Get form data
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')
        
        if rating and review_text:
            # Submit review to the API
            user_name = f"{user.first_name} {user.last_name}" if user.first_name else user.username
            response = ReviewsAPI.submit_review(
                product_id=product.id,
                user_name=user_name,
                rating=int(rating),
                review_text=review_text,
                user_id=user.id  # Pass user ID for permission control
            )
            
            if response['status'] == 'success':
                messages.success(request, "Thank you for your review!")
            else:
                messages.error(request, "There was an error submitting your review. Please try again.")
        else:
            messages.error(request, "Please provide both a rating and review text.")
        
        return redirect('product-detail', pk=pk)
 
class CustomerRegistrationView(View):
    def get(self,request): 
        form = CustomerRegistrationForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request,'app/customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! You have successfully registered")
        else:
            messages.warning(request,"Invalid registration")
        return render(request, 'app/customerregistration.html',locals())
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request , 'app/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid(): 
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congratulations! Profile save successfully')
        else:
            messages.warning(request,'Invalid Input Data')
        return render(request , 'app/profile.html',locals())
    
@login_required
def address(request):
        add = Customer.objects.filter(user=request.user)
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request ,'app/address.html', locals())
@method_decorator(login_required, name='dispatch')        
class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))

        return render (request, 'app/updateAddress.html',locals())

    def post(self, request, pk):
        form = CustomerProfileForm (request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success (request, "Congratulations! Profile Update Successfully")
        else:
            messages.warning (request, "Invalid Input Data")
        return redirect("address")
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    
    # Check if product already exists in cart
    cart_item = Cart.objects.filter(user=user, product=product).first()
    
    if cart_item:
        # If product exists, increase quantity
        cart_item.quantity += 1
        cart_item.save()
    else:
        # If product doesn't exist, create new cart item
        Cart(user=user, product=product).save()
    
    return redirect("/cart")

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value 
    totalamount = amount + 40
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/addtocart.html',locals())

@login_required
def show_wishlist(request):
    user = request.user
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Wishlist.objects.filter(user=user)
    return render (request, "app/wishlist.html", locals())

# @method_decorator(login_required, name='dispatch')
class checkout(View):
    def get(self,request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        user = request.user
        add=Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value 
        totalamount = famount + 40
        razoramount = int(totalamount*100)
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        data =  ({'amount':razoramount, 'currency':'INR', 'receipt': 'order_rcptid_12'}) 
        payment_response = client.order.create(data=data)
        print(payment_response)
        # {'amount': 11500, 'amount_due': 11500, 'amount_paid': 0, 'attempts': 0, 'created_at': 1740471550, 'currency': 'INR', 'entity': 'order', 'id': 'order_PzsItTU65uXOwO', 'notes': [], 'offer_id': None, 'receipt': 'order_rcptid_12', 'status': 'created'}
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status = order_status
            )
            payment.save()
            

        return render(request, 'app/checkout.html',locals())

def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    #print("payment_done: oid = ",order_id," pid = ", payment_id," cid = ", cust_id)
    user=request.user
    #return redirect("orders")
    customer=Customer.objects.get(id=cust_id)
    #To update payment status and payment id
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    #To save order details
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment).save()
        c.delete()
    return redirect("orders")

def orders(request):
    order_placed=OrderPlaced.objects.filter(user=request.user)
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/orders.html',locals())

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount,
        }
        return JsonResponse(data)
@login_required
@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        
        # Automatic removal when quantity reaches 0
        if c.quantity == 0:
            c.delete()
        
        # Calculate updated cart totals
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value
        
        totalamount = amount + 40  # Including shipping
        
        # Handle case where item was removed
        response_data = {
            'quantity': c.quantity if c.quantity > 0 else 0,
            'amount': amount,
            'totalamount': totalamount
        }
        
        return JsonResponse(response_data)

# def minus_cart(request):
#     if request.method == 'GET':
#         prod_id=request.GET['prod_id']
#         c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
#         c.quantity-=1
#         c.save()
#         user = request.user
#         cart = Cart.objects.filter(user=user)
#         amount = 0
#         for p in cart:
#             value = p.quantity * p.product.discounted_price
#             amount = amount + value
#         totalamount = amount + 40
#         data={
#             'quantity':c.quantity,
#             'amount':amount,
#             'totalamount':totalamount
#         }
#         return JsonResponse(data)
    
       

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
@login_required
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).save()
        data={
        'message': 'Wishlist Added Successfully',
        }
        return JsonResponse(data)
@login_required
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data={
        'message': 'Wishlist Remove Successfully',
        }
        return JsonResponse(data)
@login_required
def search(request):
    query = request.GET['search']
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request,"app/search.html", locals())

@login_required
def edit_review(request, review_id):
    # Get the review to edit
    review = ReviewsAPI.get_review_by_id(review_id)
    
    if not review:
        messages.error(request, "Review not found.")
        return redirect('home')
    
    # Check if the user has permission to edit this review
    if review.get('user_id') and review['user_id'] != request.user.id:
        messages.error(request, "You don't have permission to edit this review.")
        return redirect('product-detail', pk=review['product_id'])
    
    product = Product.objects.get(pk=review['product_id'])
    
    if request.method == 'POST':
        # Process the form submission
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')
        
        if rating and review_text:
            # Update the review via the API
            response = ReviewsAPI.edit_review(
                review_id=review_id,
                rating=int(rating),
                review_text=review_text,
                user_id=request.user.id  # Pass user ID for permission control
            )
            
            if response['status'] == 'success':
                messages.success(request, "Your review has been updated successfully!")
                return redirect('product-detail', pk=product.id)
            else:
                messages.error(request, response['message'])
        else:
            messages.error(request, "Please provide both a rating and review text.")
    
    # For GET requests or failed POST requests
    context = {
        'product': product,
        'review': review,
        'star_range': range(1, 6),  # For star display
    }
    
    return render(request, 'app/edit_review.html', context)

@login_required
def delete_review(request, review_id):
    # Get the review to delete
    review = ReviewsAPI.get_review_by_id(review_id)
    
    if not review:
        messages.error(request, "Review not found.")
        return redirect('home')
    
    # Check if the user has permission to delete this review
    if review.get('user_id') and review['user_id'] != request.user.id:
        messages.error(request, "You don't have permission to delete this review.")
        return redirect('product-detail', pk=review['product_id'])
    
    product = Product.objects.get(pk=review['product_id'])
    
    if request.method == 'POST':
        # Process the deletion confirmation
        response = ReviewsAPI.delete_review(
            review_id=review_id,
            user_id=request.user.id  # Pass user ID for permission control
        )
        
        if response['status'] == 'success':
            messages.success(request, "Your review has been deleted successfully!")
            return redirect('product-detail', pk=product.id)
        else:
            messages.error(request, response['message'])
            return redirect('product-detail', pk=product.id)
    
    # For GET requests, show the confirmation page
    context = {
        'product': product,
        'review': review,
        'star_range': range(1, 6),  # For star display
    }
    
    return render(request, 'app/delete_review.html', context)
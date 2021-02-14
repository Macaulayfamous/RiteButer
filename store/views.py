from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product,Cart, CartItem, Order, OrderItem
from django.views.generic import DetailView
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request, category_slug=None):
    
    
    category_page = None
    products = None
    if category_slug!=None:
        category_page = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category=category_page,available=True).order_by('-created')
    else:
        products = Product.objects.all().filter(available=True).order_by('-created')   
    
    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        products = products.filter(name__icontains=item_name,available=True) 
   

    return render(request, 'store/home.html',{'category':category_page,'products':products})

class ProductDetailView(DetailView):
    model = Product


# def detail(request, id):
#       product = Product.objects.get(id=id)
#       category = get_object_or_404(Category, slug=slug)
#       return render(request, 'store/detail.html',{'product':product,'category':category})


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart    

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
             cart_id = _cart_id(request)
  

        )    
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
             product = product,
             quantity = 1,
             cart = cart
        )
        cart_item.save()
    return redirect('cart_detail')    

@login_required
def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for  cart_item in cart_items:
            total += (cart_item.product.discounted_price *cart_item.quantity)
            counter +=  cart_item.quantity

    except ObjectDoesNotExist:
        pass  
    stripe.api_key = settings.STRIPE_SECRET_KEY   
    stripe_total = int(total *100)
    description = 'Z-store new order'
    data_key = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        try:
          token = request.POST['stripeToken']
          email = request.POST['stripeEmail'] 
          billingName = request.POST['stripeBillingName']
          billingAddress1 = request.POST['stripeBillingAddress1']
          billingCity = request.POST['stripeBillingCity']
          billingPostcode= request.POST['stripeBillingPostcode']
          billingCountry  = request.POST['stripeBillingCountry ']
          shippingName =request.POST['stripeShippingName']
          shippingAddress1 = request.POST['stripeshippingAddress1']
          shippingCity = request.POST['stripeshippingCity']
          shippingPostCode = request.POST['stripeShippingPostCode']
          shippingCountry = request.POST['stripeShippingCountry']

          customer = stripe.Customer.create(
               email=email,
               source = token
          )
          charge = stripe.Charge.create(
               amount =stripe_total,
               currency='usd',
               description = description,
               custormer = customer.id
          )
          try:
              order_details = Order.objects.create(

                  token = token,
                  total = total,
                  billingName = billingName,
                  billingAddress1 = billingAddress1,
                  billingCity = billingCity ,
                  billingPostcode =billingPostcode,
                  billingCountry =billingCountry,
                  shippingName=shippingName,
                  shippingAddress1 =shippingAddress1,
                  shippingCity = shippingCity,
                  shippingPostCode =shippingPostCode,
                  shippingCountry = shippingCountry

                  )
              order_details.save() 
              for  order_item in cart_items:
                  or_item = OrderItem.objects.create(
                      product = or_item.product.name,
                      quantity = order_item.quantity,
                      price = order_item.product.price,
                      order= order_details
                  )
                  order_item.save() 

                  products = Product.objects.get(id=order_item.product.id)
                  products.stock = int(order_item.product.stock - order_item.quantity)
                  products.save()
                  order_item.delete()

                  print('your oder has been created')
                  return redirect('home')
          except ObjectDoesNotExist:
              pass
           




        except stripe.error.CardError as e:
            return False, e
    return render(request,'store/cart.html',dict(cart_items=cart_items,total=total,counter=counter,data_key=data_key,stripe_total=stripe_total,description=description)) 
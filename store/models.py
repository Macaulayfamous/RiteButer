from django.db import models
from django.urls import  reverse
from django.utils import timezone
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255,unique=True)
    description =models.TextField(blank=True)
    image = models.ImageField(upload_to='images/',blank=True)

    class Meta:
        ordering = ['name']
        verbose_name ='category'
        verbose_name_plural = 'categories'
    

    def get_url(self):
        return reverse('products_by_category',args=[self.slug])
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255,unique=True)
    description =models.TextField(blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    old_price = models.DecimalField(max_digits=10, decimal_places=2) 
    current_price = models.DecimalField(max_digits=10, decimal_places=2) 
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)  
    image = models.ImageField(upload_to='images/',blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering = ['name']
        verbose_name ='product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name
              
    


class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Cart'
        ordering = ['-date_added']

    
    def __str__(self):
        return self.cart_id 

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart =  models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity  = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'CartItem'
    def sub_total(self):
        return self.product.discounted_price * self.quantity 

    def __str__(self):
        return self.product 
                       








class Order(models.Model):
    token = models.CharField(max_length=250,blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='USD order total')
    email = models.EmailField(max_length=250, blank=True,verbose_name='Email Adress')
    created = models.DateTimeField(auto_now_add=True) 
    billingName = models.CharField(max_length=255,blank=True)
    billingAddress1 = models.CharField(max_length=255,blank=True)                      
    billingCity = models.CharField(max_length=255,blank=True) 
    billingPostcode = models.CharField(max_length=255,blank=True) 
    billingCountry = models.CharField(max_length=255,blank=True) 
    shippingName = models.CharField(max_length=255,blank=True) 
    shippingAddress1 = models.CharField(max_length=255,blank=True) 
    shippingCity = models.CharField(max_length=255,blank=True) 
    shippingPostCode = models.CharField(max_length=255,blank=True) 
    shippingCountry = models.CharField(max_length=255,blank=True) 

    class meta:
        db_table = 'Order'
        odering = ['-created']

    def __str__(self):
        return  str(self.id)

class OrderItem(models.Model):
    product = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2, verbose_name='USD order price')
    order = models.ForeignKey(Order,on_delete=models.CASCADE)

    class meta:
        db_table = "OderItem"

    def sub_total(self):
        return self.quantity * self.price   

    def __str__(self):
        return self.product
             
         



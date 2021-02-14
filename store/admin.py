from django.contrib import admin

from .models import Category,Product, Order, OrderItem

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug': ('name',)}

    
admin.site.register(Category, CategoryAdmin) 

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','current_price','stock','available','created', 'update']
    list_editable = ['current_price','stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page =20

admin.site.register(Product, ProductAdmin)    


# class OrderItemAdmin(admin.TabularInline):
#     model =OrderItem
#     fieldsets = [ 
#         ('products',{'fields':['product'],}),
#         ('Quantity',{'fields':['quantity'],}),
#         ('Price',{'fields':['price'],}),

#     ]
#     readonly_fields = {'product','quantity','price'}

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['id','billingName', 'email','created']
#     list_display_links = ('id','billingName')
#     search_fields =  ['id', 'billingName', 'email']
#     readonly_fields = ['id','token','total','email','created', 
#     'billingName','billingAddress1', 'billingCity', 'billingPostcode',
#     'billingCountry', 'shippingName', 'shippingAddress1', 'shippingCity',
#     'shippingPostCode', 'shippingCountry',
#     ]
    

#     inlines = (
#          OrderItemAdmin,

#     )
       
      
    

    

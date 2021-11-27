from django.contrib import admin
from .models import Product, Contact, Ads, Order, OrderUpdate, Transaction

admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(OrderUpdate)
admin.site.register(Transaction)
admin.site.register(Ads)

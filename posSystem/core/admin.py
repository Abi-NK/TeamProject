from django.contrib import admin
from core.models import Menu, Order, OrderExtra, OrderItem, Payment, Seating, Waiter

admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(OrderExtra)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Seating)
admin.site.register(Waiter)

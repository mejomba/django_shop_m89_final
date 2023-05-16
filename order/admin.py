from django.contrib import admin

from . import models


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = ('user',)
    fields = ('user',)

    class Meta:
        model = models.Cart


@admin.register(models.CartItem)
class CartAdmin(admin.ModelAdmin):

    list_display = ('cart', 'product', 'count')
    fields = ('cart', 'product', 'count')

    class Meta:
        model = models.CartItem


@admin.register(models.Order)
class CartAdmin(admin.ModelAdmin):

    list_display = ('user', 'status',)
    fields = ('user', 'status', 'shipping', 'address', 'time_for_pay')

    class Meta:
        model = models.Order


@admin.register(models.OrderItem)
class CartAdmin(admin.ModelAdmin):

    list_display = ('order', 'product', 'count')
    fields = ('order', 'product', 'count')

    class Meta:
        model = models.OrderItem


@admin.register(models.Transaction)
class CartAdmin(admin.ModelAdmin):

    list_display = ('user', 'order', 'total_price', 'status')
    fields = ('user', 'order', 'total_price', 'status')

    class Meta:
        model = models.Transaction

from django.contrib import admin

# from prettyjson import PrettyJSONWidget
# from django.contrib.postgres.fields import JSONField
from . import models


class ProductImageAdmin(admin.StackedInline):
    model = models.ProductImage
    fields = ('image', 'is_deleted', 'product')


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

    list_display = ('name', 'brand', 'price', 'quantity', 'get_price_apply_discount', 'get_price_apply_tax')
    list_filter = ['category', 'brand']
    fields = ('name',
              'slug',
              'brand',
              'price',
              'quantity',
              'tax',
              'thumbnail',
              'meta_description',
              'description',
              'extra_data',
              'discount',
              'category',
              'tag',
              'magic_sale',
              )
    # formfield_overrides = {
    #     JSONField: {'widget': PrettyJSONWidget}
    # }
    # widgets = {
    #     'extra_data': PrettyJSONWidget(),
    # }

    prepopulated_fields = {'slug': ('name',)}

    class Meta:
        model = models.Product


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ('name',)

    class Meta:
        model = models.Tag


@admin.register(models.Category)
class TagAdmin(admin.ModelAdmin):

    fields = ('title',
              'meta_title',
              'meta_description',
              'description',
              'show_in_menu',
              'parent_category',
              'discount',)

    class Meta:
        model = models.Category


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):

    fields = (
              'content',
              'rating',
              'parent_comment',
              'product',
              'user',)

    class Meta:
        model = models.Comment


@admin.register(models.WishList)
class CommentAdmin(admin.ModelAdmin):

    fields = ('product',
              'user',)

    class Meta:
        model = models.WishList


admin.site.register(models.MagicSale)
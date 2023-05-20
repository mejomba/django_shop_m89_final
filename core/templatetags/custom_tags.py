from django import template

register = template.Library()


@register.inclusion_tag('base/single_product.html')
def show_single_product(single_product_object):
    product = {'product': single_product_object}
    return product
    
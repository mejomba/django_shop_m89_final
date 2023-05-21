from django import template

register = template.Library()


@register.inclusion_tag('base/single_product.html')
def show_single_product(single_product_object):
    product = {'product': single_product_object}
    return product
    

@register.inclusion_tag('shop/partial/post_image_gallery.html')
def show_image_gallery(thumbnail, images):
    img = [i.image for i in images]
    img.insert(0, thumbnail)
    return {'images': img}


@register.inclusion_tag('shop/partial/product_basic_info.html')
def show_product_basic_info(product):
    return {'product': product}


@register.inclusion_tag('shop/partial/product_action.html')
def show_product_action(product):
    return {'product': product}


@register.inclusion_tag('shop/partial/product_full_info.html')
def show_product_full_info(product):
    return {'product': product}


@register.inclusion_tag('shop/partial/product_comments.html')
def show_product_comments(comments):
    return {'comments': comments}
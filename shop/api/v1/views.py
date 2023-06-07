from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import redirect, reverse

from core.models import Address
from order.models import Cart, CartItem, Order, OrderItem
from .serializers import ProductSerializer, CartSerializer, CartItemSerializer, CartSerializer2, OrderSerializer, \
    AddressSerializer
from shop.models import Product
from core.mixins import StaffOrJwtLoginRequiredMixin


class CartItemAPI(APIView):
    def get(self, request, pk):
        if not request.user.is_authenticated and (cart_item := request.session.get('cart')):
            product = Product.objects.filter(pk=pk).first()
            product_serializer_ = ProductSerializer(product)
            cart_item['current_product'] = product_serializer_.data
            return Response(cart_item, status=status.HTTP_200_OK)

        if request.user.is_authenticated and (cart_item := request.session.get('cart')):
            cart = Cart.objects.get_or_create(user=request.user)[0]
            for idx, item in enumerate(cart_item['cartitem_set']):
                product = Product.objects.filter(pk=item['product']['id']).first()
                cart_item = CartItem.objects.update_or_create(cart=cart,
                                                              product=product,
                                                              count=item['count'],
                                                              is_deleted=False)[0]
            else:
                del request.session['cart']
            return Response()

        elif request.user.is_authenticated:
            if product := Product.objects.filter(pk=pk, quantity__gt=0).first():
                cart = Cart.objects.filter(user=request.user)[0]
                cart.current_product = product
                serializer_ = CartSerializer(instance=cart)
                return Response(serializer_.data)
            else:
                return Response({'detail': 'اتمام موجودی'}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'detail': None})
        # return redirect(reverse('shop:landing_page'))

    def post(self, request, pk):
        if request.user.is_authenticated:
            print('========== add item > user authenticated')
            cart = Cart.objects.get_or_create(user=request.user)[0]
            product = Product.objects.filter(pk=pk).first()
            cart.current_product = product
            cart_item = CartItem.objects.update_or_create(cart=cart, product=product, count=1, is_deleted=False)[0]

            serializer_ = CartSerializer(instance=cart)
            print(serializer_.data)
            return Response(serializer_.data, status=status.HTTP_201_CREATED)
        else:
            request.session.modified = True
            print('========== add item > user anonymous')
            cart_session = 'cart'
            product = Product.objects.filter(pk=pk).first()
            # product_serializer_ = ProductSerializer(product)
            serializer_ = ProductSerializer(product)

            if not request.session.get(cart_session):
                print('create cart item')
                request.session[cart_session] = {
                    'cartitem_set': [{'product': serializer_.data, 'count': 1}],
                    'current_product': serializer_.data
                }
            else:
                request.session[cart_session]['cartitem_set'].append({'product': serializer_.data, 'count': 1})
                request.session[cart_session]['current_product'] = serializer_.data
            session_cart_item = request.session.get(cart_session)

            return Response(session_cart_item, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        if request.user.is_authenticated:
            cart_item = CartItem.objects.filter(cart=request.user.cart, product=pk, is_deleted=False).first()
            cart_item.is_deleted = True
            cart_item.delete_date = timezone.now()
            cart_item.save()
            return Response({'detail': 'success'}, status=status.HTTP_204_NO_CONTENT)
        else:
            cart_session = 'cart'
            for idx, item in enumerate(request.session[cart_session]['cartitem_set']):
                if item['product']['id'] == pk:
                    del request.session[cart_session]['cartitem_set'][idx]
                    request.session.modified = True
                    print('========== delete product')
            return Response({'detail': 'success'}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        print('========== start update cart')
        action = request.data.get('action')

        if not request.user.is_authenticated and action in ['+', '-']:
            request.session.modified = True
            print('========== update item > user anonymous')
            cart_session = 'cart'
            product = Product.objects.filter(pk=pk).first()
            serializer_ = ProductSerializer(product)

            for idx, item in enumerate(request.session[cart_session]['cartitem_set']):
                if item['product']['id'] == pk:
                    request.session.modified = True
                    count = request.session[cart_session]['cartitem_set'][idx]['count']
                    if action == '+' and product.quantity >= count + 1:
                        request.session[cart_session]['cartitem_set'][idx]['count'] += 1
                        status_ = status.HTTP_206_PARTIAL_CONTENT

                    elif action == "-" and count and count == 1:
                        del request.session[cart_session]['cartitem_set'][idx]
                        status_ = status.HTTP_204_NO_CONTENT

                    elif action == '+' and product.quantity < count + 1:
                        status_ = status.HTTP_404_NOT_FOUND
                        return Response({'detail': 'موجودی کمتر از تعداد خواسته شده'}, status=status_)

                    elif action == '-' and count > 1:
                        request.session[cart_session]['cartitem_set'][idx]['count'] -= 1
                        status_ = status.HTTP_206_PARTIAL_CONTENT
                        # request.session[cart_session]['cartitem_set'][idx]['count'] -= 1

                    print('========== update product')
                    request.session[cart_session]['current_product'] = serializer_.data
                    session_cart_item = request.session.get(cart_session)
                    return Response(session_cart_item, status=status_)

            return Response({'detail': 'reject'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item = CartItem.objects.filter(cart=request.user.cart, product=pk, is_deleted=False).first()
        product = Product.objects.filter(pk=pk).first()

        if action not in ['+', '-']:
            return Response({'detail': 'invalid action only +, -'}, status=status.HTTP_400_BAD_REQUEST)

        elif action == '+' and product.quantity >= cart_item.count + 1:
            cart_item.count += 1
            cart_item.save()
            status_ = status.HTTP_206_PARTIAL_CONTENT

        elif action == '+' and product.quantity < cart_item.count + 1:
            status_ = status.HTTP_404_NOT_FOUND
            return Response({'detail': 'موجودی کمتر از تعداد خواسته شده'}, status=status_)

        elif action == '-' and cart_item.count and cart_item.count == 1:
            cart_item.count = 0
            cart_item.is_deleted = True
            cart_item.delete_date = timezone.now()
            cart_item.save()
            status_ = status.HTTP_204_NO_CONTENT

        elif action == '-' and cart_item.count > 1:
            cart_item.count -= 1
            cart_item.save()
            status_ = status.HTTP_206_PARTIAL_CONTENT

        cart = Cart.objects.filter(user=request.user).first()
        cart.current_product = product

        serializer_ = CartSerializer(instance=cart)

        print('========== end update cart')
        return Response(serializer_.data, status=status_)


class CartAPI(StaffOrJwtLoginRequiredMixin, APIView):
    def get(self, request):
        if request.user.is_authenticated:
            print('jwt user =======')
            cart = Cart.objects.filter(user=request.user).first()
            # cart.current_product = Product.objects.filter(pk=12).first()
            serializer_ = CartSerializer2(instance=cart)
            return Response(serializer_.data, status=status.HTTP_200_OK)
        else:
            cart = request.session.get('cart')
            serializer_ = CartSerializer2(instance=cart)
            return Response(serializer_.data, status=status.HTTP_200_OK)
            # return Response({'detail': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if cart.cartitem_set.filter(is_deleted=False):
            cart_items = cart.cartitem_set.filter(is_deleted=False)
            address = Address.objects.filter(user=request.user).first()

            if not address:
                return Response({'detail': 'حساب کاربری شما فاقد آدرس است، ابتدا یک آدرس وارد کنید'}, status=status.HTTP_400_BAD_REQUEST)
            # check product quantity
            for item in cart_items:
                product = Product.objects.filter(pk=item.product.id).first()
                if item.count > product.quantity:
                    return Response({'detail': f'تعدا کالای {item.product.name} بیشتر از موجودی '}, status=status.HTTP_404_NOT_FOUND)
            order = Order.objects.create(user=request.user, address=address)

            for item in cart_items:
                product = Product.objects.filter(pk=item.product.id).first()
                product.quantity -= item.count
                product.save()
                order_item = OrderItem.objects.create(product=product, order=order, count=item.count)
                item.is_deleted = True
                item.save()
                print("======", item, '---', item.count)


            serializer_ = OrderSerializer(instance=order)
            print('============')
            print(serializer_.data)
            print('============')

            return Response(serializer_.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'empty'}, status=status.HTTP_404_NOT_FOUND)


class OrderAPI(StaffOrJwtLoginRequiredMixin, APIView):

    def get(self, request, pk):
        order = Order.objects.filter(pk=pk).first()
        if order.address:
            serializer_ = OrderSerializer(instance=order)
            return Response(serializer_.data)
        return Response({'detail': 'no address'})


class OrderListAPI(StaffOrJwtLoginRequiredMixin, APIView):
    def get(self, request):
        orders = Order.objects.filter(user=request.user, is_deleted=False).order_by('-create_at')
        serializers_ = OrderSerializer(orders, many=True)
        return Response(serializers_.data)


class Payment(StaffOrJwtLoginRequiredMixin, APIView):
    def post(self, request):
        payment_status = request.data.get('status')
        order_id = request.data.get('order_id')
        try:
            order_obj = Order.objects.get(pk=order_id)

            if payment_status == 'success':
                order_obj.status = '2'
                order_obj.save()
            elif payment_status == 'fail':
                order_obj.status = '3'
                order_obj.save()
            return Response({'detail': 'ok'})
        except Exception as e:
            print(e)
            return Response({'detail': 'error'}, status=status.HTTP_400_BAD_REQUEST)

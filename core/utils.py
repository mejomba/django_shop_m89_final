from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
import random
from core.tasks import send_sms, send_otp_email


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def discount_solver(product_instance):
    sum_mablagh = 0
    sum_percent = 0
    categories = product_instance.category.all()

    all_discounts = [c.discount.all() for c in categories]
    all_discounts.append(product_instance.discount.all())

    for queryset in all_discounts:
        for discount in queryset:
            limit = discount.limit
            if limit is None or limit > 0:
                if (p := discount.percent) and (m := discount.mablagh):
                    if product_instance.price * (p / 100) > m:
                        sum_mablagh += m
                    else:
                        sum_percent += p
                elif p := discount.percent:
                    sum_percent += p
                elif m := discount.mablagh:
                    sum_mablagh += m

    return sum_mablagh, sum_percent


def get_otp_code():
    return random.randint(1111, 9999)


def cache_in_redis(otp_code, user):
    cache.set(otp_code, user.id, CACHE_TTL)


def perform_2step_verification(user, auth_type):
    print('perform 2step ============')
    otp_code = get_otp_code()
    cache_in_redis(otp_code, user)
    if auth_type == 'sms':
        send_sms.delay(user.phone, otp_code)
    elif auth_type == 'email':
        send_otp_email.delay(user.email, otp_code)
    print('otp: ', otp_code)
    print('end perform 2step ==========')


def remove_related_object(instance):
    if instance.related_name:
        for obj in instance.related_name.all():
            obj.is_deleted = True
            obj.delete_date = timezone.now()
            obj.save()
            print("obj in for loop =====", obj)
            return remove_related_object(obj)

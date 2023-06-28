from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
import random
from core.tasks import send_sms, send_otp_email


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def get_otp_code():
    return random.randint(1111, 9999)


def cache_in_redis(otp_code, user):
    cache.set(otp_code, user.id, CACHE_TTL)


def perform_2step_verification(user, auth_type):
    otp_code = get_otp_code()
    cache_in_redis(otp_code, user)
    if auth_type == 'sms':
        send_sms.delay(user.phone, otp_code)
    elif auth_type == 'email':
        # send_otp_email.delay(user.email, otp_code)
        send_otp_email(user.email, otp_code)
    print('otp: ', otp_code)



def remove_related_object(instance):
    if instance.related_name:
        for obj in instance.related_name.all():
            obj.is_deleted = True
            obj.delete_date = timezone.now()
            obj.save()
            print("obj in for loop =====", obj)
            return remove_related_object(obj)

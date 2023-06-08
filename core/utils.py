import time

from celery import shared_task

from django.utils import timezone
from django.core.cache import cache
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.text import gettext_lazy as _
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
import six
import random
from .raigansms import restfulapi
from core.tasks import send_sms, send_otp_email


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# class TokenGenerator(PasswordResetTokenGenerator):
#     def _make_hash_value(self, user, timestamp):
#         return (
#             six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
#         )
#
#
# account_activation_token = TokenGenerator()


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


# @shared_task
# def send_confirmation_email(current_site, email, user_id):
#     user = get_user_model().objects.filter(id=user_id).first()
#     # current_site = get_current_site(request)
#
#     print('current_site=====', current_site)
#     mail_subject = _('فعال سازی حساب کاربری')
#     context = {
#         'user': user,
#         'domain': current_site,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': account_activation_token.make_token(user)
#     }
#
#     msg = render_to_string('core/account_activation_email.html', context)
#     print(msg)
#     to_email = email
#     email = EmailMessage(mail_subject, msg, to=[to_email])
#     email.send()
#     # messages.success(request, _('ایمیل فعال سازی برای شما ارسال شد'))
#     # messages.success(request['request'], _('ایمیل فعال سازی برای شما ارسال شد'))
#     # return HttpResponse(_('برو ایمیل چک کن'))


# def send_otp_email(user, otp_code):
#     # user = get_user_model().objects.filter(id=user_id).first()
#     # current_site = get_current_site(request)
#     mail_subject = _('کد ورود یکبار مصرف')
#     context = {
#         'user': user,
#     }
#
#     # msg = render_to_string('core/otp_email.html', context)
#     msg = f"کد ورود شما: {otp_code}"
#     to_email = user.email
#     email = EmailMessage(mail_subject, msg, to=[to_email])
#     email.send()
#     # return HttpResponse(_('برو ایمیل چک کن'))


def get_otp_code():
    return random.randint(1111, 9999)


def cache_in_redis(otp_code, user):
    cache.set(otp_code, user.id, CACHE_TTL)


# def send_sms(user, otp_code):
#     # phone_number = '983000685995'
#     # phone_number2 = '985000248725'
#     group_id = random.randint(0, 99999999)
#     ws = restfulapi(settings.SMS_USER, settings.SMS_PASSWORD)
#     msg = f'با سلام کد احراز هویت شما \n {otp_code}'
#     res = ws.SendMessage(PhoneNumber=settings.SMS_USER, Message=msg, Mobiles=[user.phone],
#                          UserGroupID=str(group_id), SendDateInTimeStamp=time.time())
#     print(res)


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

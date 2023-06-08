import time
from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.text import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
import random
from core.raigansms import restfulapi

# from core.utils import account_activation_token


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()

@shared_task
def send_confirmation_email(current_site, email, user_id):
    user = get_user_model().objects.filter(id=user_id).first()
    # current_site = get_current_site(request)

    print('current_site=====', current_site)
    mail_subject = _('فعال سازی حساب کاربری')
    context = {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user)
    }

    msg = render_to_string('core/account_activation_email.html', context)
    print(msg)
    to_email = email
    email = EmailMessage(mail_subject, msg, to=[to_email])
    email.send()
    # messages.success(request, _('ایمیل فعال سازی برای شما ارسال شد'))
    # messages.success(request['request'], _('ایمیل فعال سازی برای شما ارسال شد'))
    # return HttpResponse(_('برو ایمیل چک کن'))


@shared_task
def send_otp_email(email, otp_code):
    print(otp_code)
    # user = get_user_model().objects.filter(id=user_id).first()
    # current_site = get_current_site(request)
    mail_subject = _('کد ورود یکبار مصرف')
    # context = {
    #     'user': user,
    # }

    # msg = render_to_string('core/otp_email.html', context)
    msg = f"کد ورود شما: {otp_code}"
    to_email = email
    email = EmailMessage(mail_subject, msg, to=[to_email])
    email.send()
    # return HttpResponse(_('برو ایمیل چک کن'))


@shared_task
def send_sms(phone, otp_code):
    print(otp_code)
    # phone_number = '983000685995'
    # phone_number2 = '985000248725'
    group_id = random.randint(0, 99999999)
    ws = restfulapi(settings.SMS_USER, settings.SMS_PASSWORD)
    msg = f'با سلام کد احراز هویت شما \n {otp_code}'
    res = ws.SendMessage(PhoneNumber=settings.SMS_USER, Message=msg, Mobiles=[phone],
                         UserGroupID=str(group_id), SendDateInTimeStamp=time.time())
    print(res)
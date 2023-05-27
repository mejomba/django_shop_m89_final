from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.text import gettext_lazy as _
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
import six


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


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


def send_confirmation_email(request, user_id):
    user = get_user_model().objects.filter(id=user_id).first()
    current_site = get_current_site(request)
    mail_subject = _('فعال سازی حساب کاربری')
    context = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user)
    }

    msg = render_to_string('core/account_activation_email.html', context)
    to_email = request.email
    email = EmailMessage(mail_subject, msg, to=[to_email])
    email.send()
    messages.success(request, _('ایمیل فعال سازی برای شما ارسال شد'))
    # return HttpResponse(_('برو ایمیل چک کن'))

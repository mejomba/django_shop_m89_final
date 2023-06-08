from rest_framework.exceptions import APIException
from django.utils.translation import gettext as _


class PasswordValidation(APIException):
    status_code = 400
    default_detail = _('رمز عبور نامعتبر، حداقل شامل ۸ کاراکتر ترکیبی از اعداد و حروف')
    default_code = 'invalid_password'

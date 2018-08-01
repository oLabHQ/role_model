from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, _lazy_re_compile


validate_mobile = RegexValidator
validate_mobile_message = _('Enter a valid mobile number.')
validate_abn_message = _('Enter a valid ABN number.')


mobile_validator = RegexValidator(
    _lazy_re_compile(r'^04[0-9]{8}$'),
    message=validate_mobile_message,
    code='invalid')


def validate_mobile(value):
    if len(value) > 14:
        raise ValidationError(validate_mobile_message)
    return mobile_validator(value.replace(" ", ""))


abn_validator = RegexValidator(
    _lazy_re_compile(r'^\d\d ?\d\d\d ?\d\d\d ?\d\d\d$'),
    message=validate_abn_message,
    code='invalid')


def validate_abn(value):
    if len(value) > 14:
        raise ValidationError(validate_abn_message)
    return abn_validator(value.replace(" ", ""))

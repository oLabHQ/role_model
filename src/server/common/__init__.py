from django.urls import reverse
from django.utils.html import format_html


def admin_change_url(instance):
    return reverse('admin:{}_{}_change'.format(
        instance._meta.app_label.lower(),
        instance._meta.model_name.lower()
    ), args=(instance.id,))


def admin_change_link(instance, label=str):
    return format_html(
        "<a href='{0}'>{1}</a>",
        admin_change_url(instance),
        label(instance) or str(instance.id))

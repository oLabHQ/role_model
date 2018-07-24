from django.urls import reverse


def admin_change_url(instance):
    return reverse('admin:{}_{}_change'.format(
        instance._meta.app_label.lower(),
        instance._meta.model_name.lower()
    ), args=(instance.id,))

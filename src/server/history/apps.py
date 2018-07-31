from django.apps import AppConfig, apps
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


history_models = set()


class HistoryConfig(AppConfig):
    _requires_register_models = False
    name = 'history'

    def ready(self):
        try:
            register_models()
        except LookupError:
            HistoryConfig._requires_register_models = True


def register_models():
    """
    Load model strings specified in settings.HISTORY_MODELS.
    """
    from django.contrib.contenttypes.fields import GenericRelation

    for model_name in settings.HISTORY_MODELS:
        model = apps.get_model(model_name)
        if model not in history_models:
            history_models.add(model)
            relation = GenericRelation('history.History',
                                       related_query_name='{}_{}' \
                                        .format(
                                            model._meta.app_label,
                                            model._meta.model_name))
            field_name = getattr(settings, 'HISTORY_FIELD_NAME', '_history')
            relation.contribute_to_class(model, field_name)


def model_is_registered(model):
    if not history_models or HistoryConfig._requires_register_models:
        register_models()
        HistoryConfig._requires_register_models = False

    if model in history_models:
        return True

    return False


@receiver(post_save)
def log_model_instance_delta(sender, instance=None, created=False, **kwargs):
    """
    Every time a model is updated, and the model is specified in
    settings.HISTORY_MODELS, compute and store a new history log for that
    instance.
    """
    from history.models import History

    if model_is_registered(instance.__class__):
        History.objects.append_history(instance, created)

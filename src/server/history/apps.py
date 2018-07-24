from django.apps import AppConfig, apps
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


history_models = set()


class HistoryConfig(AppConfig):
    name = 'history'


def register_models():
    """
    Load model strings specified in settings.HISTORY_MODELS.
    """
    for model_name in settings.HISTORY_MODELS:
        history_models.add(apps.get_model(model_name))


def model_is_registered(model):
    if not history_models:
        register_models()

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
        History.objects.append_history(instance)

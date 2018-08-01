from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate


def site_get_or_create(sender, **kwargs):
    from django.contrib.sites.models import Site
    from allauth.socialaccount.models import SocialApp

    try:
        site = Site.objects.get(id=settings.SITE_ID)
    except Site.DoesNotExist:
        site = Site()

    site.__dict__.update(dict(
        id=settings.SITE_ID,
        domain=settings.SITE_DOMAIN,
        name=settings.SITE_NAME
    ))
    site.save()

    try:
        social_app = SocialApp.objects.get(id=settings.SITE_ID)
    except SocialApp.DoesNotExist:
        social_app = SocialApp()

    social_app.__dict__.update(dict(
        id=settings.ALLAUTH_GOOGLE_SOCIALAPP_ID,
        name=settings.ALLAUTH_GOOGLE_SOCIALAPP_NAME,
        client_id=settings.ALLAUTH_GOOGLE_SOCIALAPP_CLIENT_ID,
        secret_key=settings.ALLAUTH_GOOGLE_SOCIALAPP_SECRET_KEY,
    ))
    site.save()


class ServerConfig(AppConfig):
    name = 'server'

    def ready(self):
        post_migrate.connect(site_get_or_create, sender=self)

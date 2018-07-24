import json
import textwrap

from django.core import serializers
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.postgres.fields import JSONField
from django.db import models

from django_extensions.db.models import TimeStampedModel

from jsondiff import diff


class HistoryManager(models.Manager):
    def previous(self, instance):
        """
        Return the latest history object for a given instance, if it exists.
        Return None otherwise.
        Since we're using UUID's, there's no need to filter for content types.
        """
        return self.filter(object_id=instance.id).order_by('-id').first()

    def append_history(self, instance):
        """
        Append to and return a history, a modification involving `instance`.
        A comparison is made between the instance and it's last known state.
        The delta is stored as part of the history.
        """
        previous_history = History.objects.previous(instance)
        serialized_data = serializers.serialize("json", [instance])
        serialized_data = json.loads(serialized_data).pop()

        delta = diff(
            serialized_data,
            previous_history.serialized_data,
            syntax='symmetric') if previous_history else None

        return History.objects.create(
            instance=instance,
            serialized_data=serialized_data,
            delta=delta)


class History(TimeStampedModel):
    """
    This model uses an auto-increment ID so we can keep track of the exact
    ordering of the history of models specified in `settings.HISTORY_MODELS`.

    This model only works with models with a UUID primary key.
    """
    content_type = models.ForeignKey('contenttypes.ContentType',
                                     on_delete='CASCADE')

    object_id = models.UUIDField(editable=False)
    instance = GenericForeignKey('content_type', 'object_id')

    delta = JSONField(null=True, blank=True)
    serialized_data = JSONField()

    objects = HistoryManager()

    class Meta:
        verbose_name_plural = "histories"
        ordering = ['-id']

    def changes(self):
        changes = []
        if self.delta and 'fields' in self.delta:
            for field, values in self.delta['fields'].items():
                values = [textwrap.shorten(str(value), width=32)
                          for value in values]
                changes.append((field, values))

        return changes

    def modification(self):
        if not self.delta:
            return "created"
        return "updated"

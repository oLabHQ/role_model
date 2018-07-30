import graphene
import json

from django.apps import apps
from django.conf import settings
from django.core import serializers
from django.db import connection
from graphene_django import DjangoObjectType

from role_model.models import Deliverable as DeliverableModel
from history.models import History as HistoryModel


class SerializedInstance(graphene.ObjectType):
    pk = graphene.String()
    model = graphene.String()
    fields = graphene.JSONString()


class History(DjangoObjectType):
    pk = graphene.String()
    changes = graphene.JSONString()
    event = graphene.String()
    serialized_instance = graphene.Field(SerializedInstance)

    class Meta:
        model = HistoryModel
        interfaces = (graphene.Node, )

    def resolve_changes(self, info):
        return dict(self.changes()) or None

    def resolve_event(self, info):
        return self.modification

    def resolve_serialized_instance(self, info):
        return SerializedInstance(
            pk=self.serialized_data['pk'],
            model=self.serialized_data['model'],
            fields=self.serialized_data['fields'])


class Query(graphene.ObjectType):
    organization_events = graphene.List(History)

    def resolve_organization_events(self, info):
        deliverable = DeliverableModel.objects.get(
            name=settings.DEMO_DELIVERABLE_NAME)

        return deliverable.history().order_by('id')


schema = graphene.Schema(query=Query, types=[
    History,
    SerializedInstance])

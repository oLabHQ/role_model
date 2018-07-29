import graphene

from django.apps import apps
from django.conf import settings
from graphene_django import DjangoObjectType

from role_model.models import Deliverable as DeliverableModel
from history.models import History as HistoryModel


class Instance(graphene.Interface):
    pk = graphene.String()
    model = graphene.String()


history_model_object_types = {}

for model_name in settings.HISTORY_MODELS:
    model = apps.get_model(model_name)

    class Meta:
        interfaces = (Instance, graphene.Node)
        model = model
        name = model._meta.model_name.title()

    object_type = type(
        model._meta.model_name.title(),
        (DjangoObjectType,),
        {'Meta': Meta})

    history_model_object_types[model_name.lower()] = object_type



class History(DjangoObjectType):
    pk = graphene.String()
    fields = graphene.JSONString()
    event = graphene.String()
    instance = graphene.Field(Instance)

    class Meta:
        model = HistoryModel
        interfaces = (graphene.Node, )

    def resolve_changes(self, info):
        return dict(self.changes())

    def resolve_event(self, info):
        return self.modification

    def resolve_instance(self, info):
        data = self.serialized_data
        model_name = data['model']
        object_type = history_model_object_types[model_name]
        return object_type(
            pk=data['pk'],
            model=model_name,
            **self.serialized_data['fields'])


class Query(graphene.ObjectType):
    organization_events = graphene.List(History)

    def resolve_organization_events(self, info):
        deliverable = DeliverableModel.objects.get(
            name=settings.DEMO_DELIVERABLE_NAME)

        return deliverable.history().all()


schema = graphene.Schema(query=Query, types=[History, Instance] +
                         list(history_model_object_types.values()))

import graphene

from graphene_django import DjangoObjectType

from role_model.models import Deliverable as DeliverableModel


class Deliverable(DjangoObjectType):
    class Meta:
        model = DeliverableModel


class Query(graphene.ObjectType):
    deliverable = graphene.List(Deliverable)

    def resolve_deliverable(self, info):
        return DeliverableModel.objects.all()


schema = graphene.Schema(query=Query, types=[Deliverable])

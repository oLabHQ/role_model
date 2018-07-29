import graphene

from django.conf import settings
from graphene_django import DjangoObjectType

from role_model.models import Deliverable as DeliverableModel
from history.models import History as HistoryModel


class History(DjangoObjectType):
    class Meta:
        model = HistoryModel


class Query(graphene.ObjectType):
    organization_history = graphene.List(History)

    def resolve_organization_history(self, info):
        deliverable = DeliverableModel.objects.get(
            name=settings.DEMO_DELIVERABLE_NAME)

        return deliverable.history().all()


#
# entries = []
# for entry in deliverable.history().all():
#     entries.append(serialize_history(entry))

schema = graphene.Schema(query=Query, types=[History])

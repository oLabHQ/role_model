from django.conf.urls import url
from role_model import views
from graphene_django.views import GraphQLView


urlpatterns = [
    url(r'^graphql', GraphQLView.as_view(graphiql=True), name='graphql'),
    url(r'^deliverable_organization_chart/(?P<deliverable_id>[0-9a-f-]+)$$',
        views.deliverable_organization_chart,
        name='deliverable_organization_chart')
]

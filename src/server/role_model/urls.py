from django.conf.urls import url
from role_model import views
from graphene_django.views import GraphQLView


urlpatterns = [
    url(r'^graphql', GraphQLView.as_view(graphiql=True), name='graphql'),
    url(r'^deliverable_chart/(?P<deliverable_id>[0-9a-f-]+)$',
        views.deliverable_chart,
        name='deliverable_chart',
        kwargs={
            'collapsed': False
        }),
    url(r'^deliverable_chart/collapsed/(?P<deliverable_id>[0-9a-f-]+)$',
        views.deliverable_chart,
        name='deliverable_chart_collapsed',
        kwargs={
            'collapsed': True
        })
]

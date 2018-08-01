from django.conf.urls import url
from graphene_django.views import GraphQLView
from role_model import views


urlpatterns = [
    url(r'^graphql', GraphQLView.as_view(graphiql=True), name='graphql'),
    url(r'^role_chart/(?P<role_id>[0-9a-f-]+)$',
        views.role_chart,
        name='role_chart'),
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
        }),
    url(r'^deliverable_content_type_chart/(?P<deliverable_id>[0-9a-f-]+)$',
        views.deliverable_content_type_chart,
        name='deliverable_content_type_chart'),
]

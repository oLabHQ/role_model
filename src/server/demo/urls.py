from django.conf.urls import url
from graphene_django.views import GraphQLView

from demo import views


urlpatterns = [
    url(r'^graphql', GraphQLView.as_view(graphiql=True), name='graphql'),
    url(r'^$', views.index, name='index'),
]

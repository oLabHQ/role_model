from django.conf.urls import url
from demo import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
]

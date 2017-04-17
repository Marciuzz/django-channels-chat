from django.conf.urls import url
from chat.views import home, get_messages


urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^get_messages/(?P<room>.+)/$', get_messages, name="get_messages"),
]
from django.conf.urls import url
from chat.views import home, get_messages, upload_photo


urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^get_messages/(?P<room>.+)/$', get_messages, name="get_messages"),
    url(r'^upload_photo/$', upload_photo, name="upload_photo"),
]
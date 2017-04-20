from django.conf.urls import url
from chat.views import home, get_messages, upload_photo, RoomEditView


urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^(?P<roomID>\d+)/$', home, name="home_with_id"),
    url(r'^get_messages/(?P<room>.+)/$', get_messages, name="get_messages"),
    url(r'^upload_photo/$', upload_photo, name="upload_photo"),
    url(r'^room-edit/(?P<room>.+)/$', RoomEditView.as_view(), name="edit_room"),
]
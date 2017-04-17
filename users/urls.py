from django.conf.urls import url
from users.views import RegisterView, home, view_profile, EditProfileView, ChangePasswordView, change_friends, LoginView
from django.contrib.auth.views import login, logout


urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^login/$', LoginView.as_view(), name="login"),

    url(r'^logout/$', logout, {'next_page': 'chat:home'}, name="logout"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^view/$', view_profile, name="view_profile"),
    url(r'^edit/$', EditProfileView.as_view(), name="edit_profile"),
    url(r'^change-password/$', ChangePasswordView.as_view(), name="change_password"),
    url(r'^connect/(?P<action>.+)/(?P<pk>\d+)$', change_friends, name="change_friends"),
]
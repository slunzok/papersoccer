from django.urls import re_path

from . import views

app_name = 'schemes'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^kurnik/(?P<player_name>([a-zA-Z0-9]+))/$', views.kurnik_user, name='kurnik_user'),
    re_path(r'^kurnik/(?P<player1_name>([a-zA-Z0-9]+))/(?P<player2_name>([a-zA-Z0-9]+))/$', views.kurnik_user_battles, name='kurnik_user_battles'),
    re_path(r'^partia/(?P<replay_id>\d+)/$',  views.create_scheme, name='create_scheme'),
]

from django.urls import re_path

from . import views

app_name = 'schemes'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    # Schemes
    re_path(r'^schematy/$',  views.user_scheme_directories, name='user_scheme_directories'),
    re_path(r'^schematy/(?P<username>([a-zA-Z0-9_\-]+))/$',  views.user_public_scheme_directories, name='user_public_scheme_directories'),
    re_path(r'^schematy/katalog/(?P<directory_id>\d+)/user/(?P<username>([a-zA-Z0-9_\-]+))/$', views.user_official_schemes, name='user_official_schemes'),
    re_path(r'^schematy/katalog/(?P<directory_id>\d+)/$', views.show_scheme_directory, name='show_scheme_directory'),
    re_path(r'^schematy/katalog/(?P<directory_id>\d+)/edytuj/$', views.edit_scheme_directory, name='edit_scheme_directory'),
    re_path(r'^schematy/katalog/(?P<directory_id>\d+)/usun/$', views.delete_scheme_directory, name='delete_scheme_directory'),
    re_path(r'^schematy/szukaj/(?P<search_scheme>([a-zA-Z0-9_\s\-\+\@\.]+))/$', views.search_scheme, name='search_scheme'),
    re_path(r'^partia/(?P<replay_id>\d+)/$',  views.create_scheme, name='create_scheme'),
    re_path(r'^schemat/(?P<scheme_id>\d+)/$',  views.show_scheme, name='show_scheme'),
    re_path(r'^schemat/(?P<scheme_id>\d+)/edytuj/$',  views.edit_scheme, name='edit_scheme'),
    re_path(r'^schemat/(?P<scheme_id>\d+)/usun/$',  views.delete_scheme, name='delete_scheme'),
    # Kurnik
    re_path(r'^kurnik/(?P<player_name>([a-zA-Z0-9]+))/$', views.kurnik_user, name='kurnik_user'),
    re_path(r'^kurnik/(?P<player1_name>([a-zA-Z0-9]+))/(?P<player2_name>([a-zA-Z0-9]+))/$', views.kurnik_user_battles, name='kurnik_user_battles'),
]

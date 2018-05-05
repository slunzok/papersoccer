from django.urls import re_path

from . import views

app_name = 'schemes'

urlpatterns = [
    # Static and other sites
    re_path(r'^$', views.index, name='index'),
    re_path(r'^online/$',  views.online_users, name='online_users'),
    re_path(r'^headhunter/$',  views.search_kurnik_player, name='search_kurnik_player'),
    # Schemes
    re_path(r'^schematy/$',  views.user_scheme_directories, name='user_scheme_directories'),
    re_path(r'^schematy/(?P<username>([a-zA-Z0-9_\-]+))/$',  views.user_public_scheme_directories, name='user_public_scheme_directories'),
    re_path(r'^schematy/katalog/(?P<directory_id>\d+)/user/(?P<username>([a-zA-Z0-9_\-]+))/$', views.user_official_schemes, name='user_official_schemes'),
    re_path(r'^schematy/katalog/(?P<directory_id>\d+)/$', views.show_scheme_directory, name='show_scheme_directory'),
    re_path(r'^schematy/katalog/(?P<directory_id>\d+)/edytuj/$', views.edit_scheme_directory, name='edit_scheme_directory'),
    re_path(r'^schematy/katalog/(?P<directory_id>\d+)/usun/$', views.delete_scheme_directory, name='delete_scheme_directory'),
    re_path(r'^schematy/szukaj/(?P<search_scheme>([a-zA-Z0-9_\s\-\+\@\.]+))/$', views.search_scheme, name='search_scheme'),
    re_path(r'^partia/(?P<replay_id>\d+)/$',  views.create_scheme, name='create_scheme'),
    re_path(r'^partia/(?P<replay_id>\d+)/dodaj/$',  views.add_to_user_replay_directory, name='add_to_user_replay_directory'),
    re_path(r'^schemat/(?P<scheme_id>\d+)/$',  views.show_scheme, name='show_scheme'),
    re_path(r'^schemat/(?P<scheme_id>\d+)/edytuj/$',  views.edit_scheme, name='edit_scheme'),
    re_path(r'^schemat/(?P<scheme_id>\d+)/usun/$',  views.delete_scheme, name='delete_scheme'),
    # Virtual Replays
    re_path(r'^partie/$',  views.user_replay_directories, name='user_replay_directories'),
    re_path(r'^partie/(?P<username>([a-zA-Z0-9_\-]+))/$',  views.user_public_replay_directories, name='user_public_replay_directories'),
    re_path(r'^partie/katalog/(?P<directory_id>\d+)/$', views.show_replay_directory, name='show_replay_directory'),
    re_path(r'^partie/katalog/(?P<directory_id>\d+)/edytuj/$', views.edit_replay_directory, name='edit_replay_directory'),
    re_path(r'^partie/katalog/(?P<directory_id>\d+)/usun/$', views.delete_replay_directory, name='delete_replay_directory'),
    re_path(r'^wirtualny/(?P<vreplay_id>\d+)/edytuj/$',  views.edit_vreplay, name='edit_vreplay'),
    re_path(r'^wirtualny/(?P<vreplay_id>\d+)/usun/$',  views.delete_vreplay, name='delete_vreplay'),
    re_path(r'^partie/katalog/(?P<directory_id>\d+)/sprawdz-wiele/$', views.manage_vreplays, name='manage_vreplays'),
    # Training
    re_path(r'^orlik/$',  views.training_independent, name='training_independent'),
    re_path(r'^orlik/(?P<replay_id>\d+)/$',  views.training_dependent, name='training_dependent'),
    re_path(r'^orlik/partie/$',  views.custom_ureplays, name='custom_ureplays'),
    re_path(r'^orlik/partie/(?P<username>([a-zA-Z0-9_\-]+))/$',  views.custom_public_ureplays, name='custom_public_ureplays'),
    re_path(r'^orlik/partia/(?P<replay_id>\d+)/$',  views.create_scheme_from_custom_ureplay, name='create_scheme_from_custom_ureplay'),
    re_path(r'^orlik/partia/(?P<replay_id>\d+)/edytuj/$',  views.edit_ureplay, name='edit_ureplay'),
    re_path(r'^orlik/partia/(?P<replay_id>\d+)/usun/$',  views.delete_ureplay, name='delete_ureplay'),
    re_path(r'^orlik/partia/(?P<replay_id>\d+)/dodaj/$',  views.add_ureplay_to_user_replay_directory, name='add_ureplay_to_user_replay_directory'),
    # Kurnik
    re_path(r'^kurnik/(?P<player_name>([a-zA-Z0-9]+))/$', views.kurnik_user, name='kurnik_user'),
    re_path(r'^kurnik/(?P<player1_name>([a-zA-Z0-9]+))/(?P<player2_name>([a-zA-Z0-9]+))/$', views.kurnik_user_battles, name='kurnik_user_battles'),
    re_path(r'^kurnik/(?P<player1_name>([a-zA-Z0-9]+))/(?P<player2_name>([a-zA-Z0-9]+))/utworz-kopiuj/$', views.create_and_add_vreplays, name='create_and_add_vreplays'),
    re_path(r'^kurnik/(?P<player1_name>([a-zA-Z0-9]+))/(?P<player2_name>([a-zA-Z0-9]+))/kopiuj/$', views.add_vreplays, name='add_vreplays'),
    re_path(r'^kurnik-mecze/$',  views.kurnik_users_games, name='kurnik_users_games'),
    re_path(r'^kurnik-ranking/$',  views.kurnik_users_ranking, name='kurnik_users_ranking'),
    # Registration
    re_path(r'^zarejestruj/$',  views.register_account, name='register_account'),
    re_path(r'^zaloguj/$',  views.login_user, name='login_user'),
    re_path(r'^wyloguj/$',  views.logout_user, name='logout_user'),
    # Microblog
    re_path(r'^trybuna/$',  views.microblog, name='microblog'),
    re_path(r'^trybuna/wpis/(?P<entry_id>\d+)/$',  views.show_entry, name='show_entry'),
    re_path(r'^trybuna/wpis/(?P<entry_id>\d+)/edytuj/$',  views.edit_entry, name='edit_entry'),
    re_path(r'^trybuna/komentarz/(?P<comment_id>\d+)/edytuj/$',  views.edit_comment, name='edit_comment'),
    re_path(r'^powiadomienia/$',  views.show_notifications, name='show_notifications'),
    # User profile/settings
    re_path(r'^kibic/(?P<username>([a-zA-Z0-9_\-]+))/$',  views.show_user_profile, name='show_user_profile'),
    re_path(r'^zmien-haslo/$',  views.change_password, name='change_password'),
    re_path(r'^edytuj-profil/$',  views.edit_user_profile, name='edit_user_profile'),
]

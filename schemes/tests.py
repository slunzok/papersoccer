from django.urls import resolve, reverse
from django.test import TestCase

from .views import index, kurnik_user, kurnik_user_battles, create_scheme
from .models import KurnikReplay

class HomeTests(TestCase):
    def test_index_view_status_code(self):
        url = reverse('schemes:index')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_index_url_resolves_index_view(self):
        view = resolve('/')
        self.assertEquals(view.func, index)

class KurnikUserTests(TestCase):
    def setUp(self):
        self.game = KurnikReplay.objects.create(name='62134874', \
            player1='smoke2blunts', player2='skromny18', \
            replay_date='14.04.2015', replay_time='12:05:53', \
            replay_round='60', player1_elo='2190', player2_elo='2012', \
            moves='0 0 5 0 3636 3 2 3 6', result='0-1')
        url = reverse('schemes:kurnik_user', kwargs={'player_name': \
            'skromny18'})
        self.response = self.client.get(url)

    def test_kurnik_user_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_kurnik_user_url_resolves_kurnik_user_view(self):
        view = resolve('/kurnik/smoke2blunts/')
        self.assertEquals(view.func, kurnik_user)

    def test_kurnik_user_view_contains_link_to_opponent_page(self):
        opponent_url = reverse('schemes:kurnik_user_battles', \
            kwargs={'player1_name': self.game.player1, \
            'player2_name': self.game.player2})
        self.assertContains(self.response, 'href="{0}"'.format(opponent_url))

class KurnikUserBattlesTests(TestCase):
    def setUp(self):
        self.game = KurnikReplay.objects.create(name='62134874', \
            player1='smoke2blunts', player2='skromny18', \
            replay_date='14.04.2015', replay_time='12:05:53', \
            replay_round='60', player1_elo='2190', player2_elo='2012', \
            moves='0 0 5 0 3636 3 2 3 6', result='0-1')
        url = reverse('schemes:kurnik_user_battles', kwargs={'player1_name': \
            self.game.player1, 'player2_name': self.game.player2})
        self.response = self.client.get(url)

    def test_kurnik_user_battles_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_kurnik_user_battles_url_resolves_kurnik_user_battles(self):
        view = resolve('/kurnik/smoke2blunts/skromny18/')
        self.assertEquals(view.func, kurnik_user_battles)

    def test_kurnik_user_battles_view_contains_link_to_replays(self):
        replays_url = reverse('schemes:create_scheme', kwargs= {'replay_id': \
            self.game.name})
        self.assertContains(self.response, 'href="{0}"'.format(replays_url))

class CreateSchemeTests(TestCase):
    def setUp(self):
        KurnikReplay.objects.create(name='61972037', player1='alt', \
            player2= 'ujb', replay_date='17.03.2015', replay_time='14:40:28', \
            replay_round='60', player1_elo='1937', player2_elo='1760', \
            moves='3 6 3 4 7 22 754', result='0-1')

    def test_create_scheme_view_success_status_code(self):
        url = reverse('schemes:create_scheme', kwargs={'replay_id': '61972037'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_create_scheme_view_not_found_status_code(self):
        url = reverse('schemes:create_scheme', kwargs={'replay_id': '61972999'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_create_scheme_url_resolves_create_scheme_view(self):
        view = resolve('/partia/61972037/')
        self.assertEquals(view.func, create_scheme)


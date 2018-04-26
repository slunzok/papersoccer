from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from django.db.models import Q
from .models import KurnikReplay

def index(request):
    return HttpResponse("Initial view")

def kurnik_user(request, player_name):
    replays = KurnikReplay.objects.filter(Q(player1=player_name) | Q(player2=player_name))

    if replays:

        keys = []
        players = []
        i = 0

        for replay in replays:

            if replay.result == "1-0":

                # player 1 - WIN
                try:
                    position = int(keys.index(replay.player1))
                except ValueError:
                    position = -1

                if position > -1:
                    players[position]['sums'] = str(int(players[position]['sums']) + int(replay.player1_elo))
                    players[position]['games'] = str(int(players[position]['games']) + 1)
                    players[position]['wins'] = str(int(players[position]['wins']) + 1)
                    players[position]['rank'] = str(round(int(players[position]['sums'])/int(players[position]['games'])))
                else:
                    i += 1
                    players.append({'id': str(i), 'name': replay.player1, 'rank': replay.player1_elo, 'sums': replay.player1_elo, 'games': '1', 'wins': '1', 'losses': '0'})
                    keys.append(replay.player1)

                # player 2 - LOSS
                try:
                    position = int(keys.index(replay.player2))
                except ValueError:
                    position = -1

                if position > -1:
                    players[position]['sums'] = str(int(players[position]['sums']) + int(replay.player2_elo))
                    players[position]['games'] = str(int(players[position]['games']) + 1)
                    players[position]['losses'] = str(int(players[position]['losses']) + 1)
                    players[position]['rank'] = str(round(int(players[position]['sums'])/int(players[position]['games'])))
                else:
                    i += 1
                    players.append({'id': str(i), 'name': replay.player2, 'rank': replay.player2_elo, 'sums': replay.player2_elo, 'games': '1', 'wins': '0', 'losses': '1'})
                    keys.append(replay.player2)

            else:

                # player 2 - WIN
                try:
                    position = int(keys.index(replay.player2))
                except ValueError:
                    position = -1

                if position > -1:
                    players[position]['sums'] = str(int(players[position]['sums']) + int(replay.player2_elo))
                    players[position]['games'] = str(int(players[position]['games']) + 1)
                    players[position]['wins'] = str(int(players[position]['wins']) + 1)
                    players[position]['rank'] = str(round(int(players[position]['sums'])/int(players[position]['games'])))
                else:
                    i += 1
                    players.append({'id': str(i), 'name': replay.player2, 'rank': replay.player2_elo, 'sums': replay.player2_elo, 'games': '1', 'wins': '1', 'losses': '0'})
                    keys.append(replay.player2)

                # player 1 - LOSS
                try:
                    position = int(keys.index(replay.player1))
                except ValueError:
                    position = -1

                if position > -1:
                    players[position]['sums'] = str(int(players[position]['sums']) + int(replay.player1_elo))
                    players[position]['games'] = str(int(players[position]['games']) + 1)
                    players[position]['losses'] = str(int(players[position]['losses']) + 1)
                    players[position]['rank'] = str(round(int(players[position]['sums'])/int(players[position]['games'])))
                else:
                    i += 1
                    players.append({'id': str(i), 'name': replay.player1, 'rank': replay.player1_elo, 'sums': replay.player1_elo, 'games': '1', 'wins': '0', 'losses': '1'})
                    keys.append(replay.player1)

        players2 = sorted(players, key=lambda k: (int(k['games']), int(k['rank'])), reverse=True)
        return render(request, 'schemes/kurnik_user.html', {'players': players2})
    else:
        return HttpResponse('Nie znaleziono gracza!')

def kurnik_user_battles(request, player1_name, player2_name):
    replays = KurnikReplay.objects.filter(Q(player1=player1_name, player2=player2_name) | Q(player1=player2_name, player2=player1_name))

    if replays:

        keys = []
        players = []
        i = 0

        for replay in replays:

            if replay.result == "1-0":

                # player 1 - WIN
                try:
                    position = int(keys.index(replay.player1))
                except ValueError:
                    position = -1

                if position > -1:
                    players[position]['sums'] = str(int(players[position]['sums']) + int(replay.player1_elo))
                    players[position]['games'] = str(int(players[position]['games']) + 1)
                    players[position]['wins'] = str(int(players[position]['wins']) + 1)
                    players[position]['rank'] = str(round(int(players[position]['sums'])/int(players[position]['games'])))
                else:
                    i += 1
                    players.append({'id': str(i), 'name': replay.player1, 'rank': replay.player1_elo, 'sums': replay.player1_elo, 'games': '1', 'wins': '1', 'losses': '0'})
                    keys.append(replay.player1)

                # player 2 - LOSS
                try:
                    position = int(keys.index(replay.player2))
                except ValueError:
                    position = -1

                if position > -1:
                    players[position]['sums'] = str(int(players[position]['sums']) + int(replay.player2_elo))
                    players[position]['games'] = str(int(players[position]['games']) + 1)
                    players[position]['losses'] = str(int(players[position]['losses']) + 1)
                    players[position]['rank'] = str(round(int(players[position]['sums'])/int(players[position]['games'])))
                else:
                    i += 1
                    players.append({'id': str(i), 'name': replay.player2, 'rank': replay.player2_elo, 'sums': replay.player2_elo, 'games': '1', 'wins': '0', 'losses': '1'})
                    keys.append(replay.player2)

            else:

                # player 2 - WIN
                try:
                    position = int(keys.index(replay.player2))
                except ValueError:
                    position = -1

                if position > -1:
                    players[position]['sums'] = str(int(players[position]['sums']) + int(replay.player2_elo))
                    players[position]['games'] = str(int(players[position]['games']) + 1)
                    players[position]['wins'] = str(int(players[position]['wins']) + 1)
                    players[position]['rank'] = str(round(int(players[position]['sums'])/int(players[position]['games'])))
                else:
                    i += 1
                    players.append({'id': str(i), 'name': replay.player2, 'rank': replay.player2_elo, 'sums': replay.player2_elo, 'games': '1', 'wins': '1', 'losses': '0'})
                    keys.append(replay.player2)

                # player 1 - LOSS
                try:
                    position = int(keys.index(replay.player1))
                except ValueError:
                    position = -1

                if position > -1:
                    players[position]['sums'] = str(int(players[position]['sums']) + int(replay.player1_elo))
                    players[position]['games'] = str(int(players[position]['games']) + 1)
                    players[position]['losses'] = str(int(players[position]['losses']) + 1)
                    players[position]['rank'] = str(round(int(players[position]['sums'])/int(players[position]['games'])))
                else:
                    i += 1
                    players.append({'id': str(i), 'name': replay.player1, 'rank': replay.player1_elo, 'sums': replay.player1_elo, 'games': '1', 'wins': '0', 'losses': '1'})
                    keys.append(replay.player1)

        players2 = sorted(players, key=lambda k: (int(k['games']), int(k['rank'])), reverse=True)
        return render(request, 'schemes/kurnik_user_battles.html', {'replays': replays, 'players': players2, 'player1': player1_name, 'player2': player2_name})

    else:
        return HttpResponse('Nie znaleziono gracza!')

def create_scheme(request, replay_id):
    replay = get_object_or_404(KurnikReplay, name=replay_id)
    return render(request, 'schemes/create_scheme.html', {'replay': replay})


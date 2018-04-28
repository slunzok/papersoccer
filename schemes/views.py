from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.models import User
from django.db.models import Q, Count

from .models import KurnikReplay, SchemeDirectory, Scheme
from .forms import SchemeDirectoryForm, SchemeForm

def index(request):
    return render(request, 'schemes/index.html')

# Schemes

# 01. /schematy/
def user_scheme_directories(request):
    if request.user.is_authenticated:
        directories = SchemeDirectory.objects.filter(parent_dir=None, user=request.user).order_by('name')
        schemes = SchemeDirectory.objects.filter(parent_dir__gt=0, scheme_access=1, schemes__user=request.user).annotate(user_official_schemes=Count('name'))

        if request.method == 'POST':
            add_directory_form = SchemeDirectoryForm(request.POST, user_id=request.user)
            if add_directory_form.is_valid():
                add_directory = add_directory_form.save(commit=False)
                add_directory.user = request.user
                add_directory.save()
                return HttpResponseRedirect(reverse('schemes:show_scheme_directory', args=(add_directory.id,)))
        else:
            add_directory_form = SchemeDirectoryForm(user_id=request.user)

        return render(request, 'schemes/user_scheme_directories.html', {'directories': directories, 'schemes': schemes, 'add_directory_form': add_directory_form})

    else:
        return HttpResponse("Opcja dostępna tylko dla zalogowanych użytkowników!")

# 02. /schematy/<username>/
def user_public_scheme_directories(request, username):
    user = get_object_or_404(User, username=username)
    directories = SchemeDirectory.objects.filter(parent_dir=None, user=user, scheme_access=2).order_by('name')
    return render(request, 'schemes/user_public_scheme_directories.html', {'user': user, 'directories': directories})

# 03. /schematy/katalog/<directory_id>/user/<username>/
def user_official_schemes(request, directory_id, username):
    directory = get_object_or_404(SchemeDirectory, pk=directory_id, scheme_access=1)
    user = get_object_or_404(User, username=username)
    schemes = Scheme.objects.filter(directory=directory, user=user)
    return render(request, 'schemes/user_official_schemes.html', {'directory': directory, 'schemes': schemes})

# 04. /schematy/katalog/<id>/
def show_scheme_directory(request, directory_id):
    directory = get_object_or_404(SchemeDirectory, pk=directory_id)

    if directory.user == request.user:
        if request.method == 'POST':
            add_directory_form = SchemeDirectoryForm(request.POST, user_id=request.user)
            if add_directory_form.is_valid():
                add_directory = add_directory_form.save(commit=False)
                add_directory.parent_dir = directory
                add_directory.user = request.user
                add_directory.save()
                return HttpResponseRedirect(reverse('schemes:show_scheme_directory', args=(add_directory.id,)))
        else:
            add_directory_form = SchemeDirectoryForm(user_id=request.user)

        return render(request, 'schemes/show_scheme_directory.html', {'directory': directory, 'add_directory_form': add_directory_form})

    else:
        if directory.scheme_access == '3':
            return HttpResponse('Prywatny katalog!')
        else:
            return render(request, 'schemes/show_scheme_directory.html', {'directory': directory})

# 05. /schematy/katalog/<id>/edytuj/
def edit_scheme_directory(request, directory_id):
    directory = get_object_or_404(SchemeDirectory, pk=directory_id)

    if directory.user == request.user:
        user_directories = SchemeDirectory.objects.filter(user=request.user)
        if request.method == 'POST':
            edit_directory_form = SchemeDirectoryForm(request.POST, instance=directory, user_id=request.user)
            if edit_directory_form.is_valid():
                edit_directory_form.save()
                return HttpResponseRedirect(reverse('schemes:edit_scheme_directory', args=(directory.id,)))
        else:
            edit_directory_form = SchemeDirectoryForm(instance=directory, user_id=request.user)

        return render(request, 'schemes/edit_scheme_directory.html', {'directory': directory, 'edit_directory_form': edit_directory_form, 'user_directories': user_directories})

    else:
        return HttpResponse("Nie jesteś właścicielem tego katalogu!")

# 06. /schematy/katalog/<id>/usun/
def delete_scheme_directory(request, directory_id):
    directory = get_object_or_404(SchemeDirectory, pk=directory_id)

    if directory.user == request.user:
        if request.method == 'POST':
            directory.delete()
            return HttpResponse("Katalog (wraz z podkatalogami i schematami) usunięty!")
        else:
            return render(request, 'schemes/delete_scheme_directory.html', {'directory': directory})
    else:
        return HttpResponse("Nie jesteś właścicielem tego katalogu!")

# 07. /schematy/szukaj/<search_scheme>/
def search_scheme(request, search_scheme):
    if request.user.is_authenticated:
        search_scheme = SchemeDirectory.objects.filter(Q(user=request.user, parent_dir__name__contains=search_scheme) | Q(user=request.user, name__contains=search_scheme)| Q(parent_dir__gt=0, scheme_access=1, parent_dir__name__contains=search_scheme) | Q(parent_dir__gt=0, scheme_access=1, name__contains=search_scheme))

        if search_scheme:
            return render(request, 'schemes/search_scheme.html', {'search_scheme': search_scheme})
        else:
            return HttpResponse('Nie znaleziono schematu!')

    else:
        return HttpResponse('Opcja dostępna tylko dla zalogowanych użytkowników!')

# 08. /partia/<replay_id>/
def create_scheme(request, replay_id):
    replay = get_object_or_404(KurnikReplay, name=replay_id)

    if request.method == 'POST':
        if request.user.is_authenticated:
            scheme_form = SchemeForm(request.POST, user_id=request.user.id)
            if scheme_form.is_valid():
                scheme = scheme_form.save(commit=False)
                scheme.replay = replay
                scheme.user = request.user
                scheme.save()
                return HttpResponse("OK")
        else:
            return HttpResponse("Tylko zalogowani użytkownicy mogą dodawać schematy!")
    else:
        scheme_form = SchemeForm(user_id=request.user.id)

    return render(request, 'schemes/create_scheme.html', {'replay': replay, 'scheme_form': scheme_form})

# 09. /schemat/<scheme_id>/
def show_scheme(request, scheme_id):
    scheme = get_object_or_404(Scheme, pk=scheme_id)

    if scheme.user != request.user and scheme.directory.scheme_access == '3':
        return HttpResponse("Schemat prywatny!")
    else:
        return render(request, 'schemes/show_scheme.html', {'scheme': scheme})

# 10. /schemat/<scheme_id>/edytuj/
def edit_scheme(request, scheme_id):
    scheme = get_object_or_404(Scheme, pk=scheme_id)

    if scheme.user == request.user:
        user_directories = SchemeDirectory.objects.filter(Q(user=request.user) | Q(parent_dir__gt=0, scheme_access=1))
        if request.method == 'POST':
            scheme_form = SchemeForm(request.POST, instance=scheme, user_id=request.user.id)
            if scheme_form.is_valid():
                scheme_form.save()
                return HttpResponseRedirect(reverse('schemes:edit_scheme', args=(scheme.id,)))
        else:
            scheme_form = SchemeForm(instance=scheme, user_id=request.user.id)

        return render(request, 'schemes/edit_scheme.html', {'scheme': scheme, 'scheme_form': scheme_form, 'user_directories': user_directories})
    else:
        return HttpResponse("Nie jesteś właścicielem tego schematu!")

# 11. /schemat/<scheme_id>/usun/
def delete_scheme(request, scheme_id):
    scheme = get_object_or_404(Scheme, pk=scheme_id)

    if scheme.user == request.user:
        if request.method == 'POST':
            scheme.delete()
            return HttpResponse("Schemat usunięty!")
        else:
            return render(request, 'schemes/delete_scheme.html', {'scheme': scheme})
    else:
        return HttpResponse("Nie jesteś właścicielem tego schematu!")

# Kurnik

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


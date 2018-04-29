from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.forms.models import inlineformset_factory

from .models import KurnikReplay, SchemeDirectory, Scheme, ReplayDirectory, Replay
from .forms import SchemeDirectoryForm, SchemeForm, ReplayDirectoryForm, ReplayForm, CheckReplayForm, BaseReplayFormSet, UserReplayForm

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

# 08A. /partia/<replay_id>/
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

# 08B. /partia/<replay_id>/dodaj/
def add_to_user_replay_directory(request, replay_id):
    replay = get_object_or_404(KurnikReplay, name=replay_id)

    if request.user.is_authenticated:
        user_directories = ReplayDirectory.objects.filter(user=request.user)
        if request.method == 'POST':
            replay_form = ReplayForm(request.POST, user_id=request.user.id)
            if replay_form.is_valid():
                add_replay = replay_form.save(commit=False)
                add_replay.replay = replay
                add_replay.user = request.user
                add_replay.save()
                return HttpResponse("OK")
        else:
            replay_form = ReplayForm(user_id=request.user.id)

        return render(request, 'schemes/add_replay.html', {'replay': replay, 'replay_form': replay_form, 'user_directories': user_directories})
    else:
        return HttpResponse('Opcja dostępna tylko dla zalogowanych użytkowników!')

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

# Virtual Replays

# 01. /partie/
def user_replay_directories(request):
    if request.user.is_authenticated:
        directories = ReplayDirectory.objects.filter(parent_dir=None, user=request.user).order_by('name')

        if request.method == 'POST':
            add_directory_form = ReplayDirectoryForm(request.POST, user_id=request.user)
            if add_directory_form.is_valid():
                add_directory = add_directory_form.save(commit=False)
                add_directory.user = request.user
                add_directory.save()
                return HttpResponseRedirect(reverse('schemes:show_replay_directory', args=(add_directory.id,)))
        else:
            add_directory_form = ReplayDirectoryForm(user_id=request.user)

        return render(request, 'schemes/user_replay_directories.html', {'directories': directories, 'add_directory_form': add_directory_form})

    else:
        return HttpResponse("Opcja dostępna tylko dla zalogowanych użytkowników!")

# 02. /partie/<username>/
def user_public_replay_directories(request, username):
    user = get_object_or_404(User, username=username)
    directories = ReplayDirectory.objects.filter(parent_dir=None, user=user, replay_access=2).order_by('name')
    return render(request, 'schemes/user_public_replay_directories.html', {'user': user, 'directories': directories})

# 03. /partie/katalog/<id>/
def show_replay_directory(request, directory_id):
    directory = get_object_or_404(ReplayDirectory, pk=directory_id)

    if directory.user == request.user:
        if request.method == 'POST':
            add_directory_form = ReplayDirectoryForm(request.POST, user_id=request.user)
            if add_directory_form.is_valid():
                add_directory = add_directory_form.save(commit=False)
                add_directory.parent_dir = directory
                add_directory.user = request.user
                add_directory.save()
                return HttpResponseRedirect(reverse('schemes:show_replay_directory', args=(add_directory.id,)))
        else:
            add_directory_form = ReplayDirectoryForm(user_id=request.user)

        return render(request, 'schemes/show_replay_directory.html', {'directory': directory, 'add_directory_form': add_directory_form})

    else:
        if directory.replay_access == '3':
            return HttpResponse('Prywatny katalog!')
        else:
            return render(request, 'schemes/show_replay_directory.html', {'directory': directory})

# 04. /partie/katalog/<id>/edytuj/
def edit_replay_directory(request, directory_id):
    directory = get_object_or_404(ReplayDirectory, pk=directory_id)

    if directory.user == request.user:
        user_directories = ReplayDirectory.objects.filter(user=request.user)
        if request.method == 'POST':
            edit_directory_form = ReplayDirectoryForm(request.POST, instance=directory, user_id=request.user)
            if edit_directory_form.is_valid():
                edit_directory_form.save()
                return HttpResponseRedirect(reverse('schemes:edit_replay_directory', args=(directory.id,)))
        else:
            edit_directory_form = ReplayDirectoryForm(instance=directory, user_id=request.user)

        return render(request, 'schemes/edit_replay_directory.html', {'directory': directory, 'edit_directory_form': edit_directory_form, 'user_directories': user_directories})

    else:
        return HttpResponse("Nie jesteś właścicielem tego katalogu")

# 05. /partie/katalog/<id>/usun/
def delete_replay_directory(request, directory_id):
    directory = get_object_or_404(ReplayDirectory, pk=directory_id)

    if directory.user == request.user:
        if request.method == 'POST':
            directory.delete()
            return HttpResponse("Katalog (wraz z podkatalogami i schematami) usunięty!")
        else:
            return render(request, 'schemes/delete_replay_directory.html', {'directory': directory})
    else:
        return HttpResponse("Nie jesteś właścicielem tego katalogu")

# 06. /wirtualny/<id>/edytuj/
def edit_vreplay(request, vreplay_id):
    vreplay = get_object_or_404(Replay, pk=vreplay_id)

    if vreplay.user == request.user:
        user_directories = ReplayDirectory.objects.filter(user=request.user)
        if request.method == 'POST':
            vreplay_form = ReplayForm(request.POST, instance=vreplay, user_id=request.user.id)
            if vreplay_form.is_valid():
                vreplay_form.save()
                return HttpResponseRedirect(reverse('schemes:edit_vreplay', args=(vreplay.id,)))
        else:
            vreplay_form = ReplayForm(instance=vreplay, user_id=request.user.id)

        return render(request, 'schemes/edit_vreplay.html', {'vreplay': vreplay, 'vreplay_form': vreplay_form, 'user_directories': user_directories})
    else:
        return HttpResponse("Nie jesteś właścicielem tego pliku!")

# 07. /wirtualny/<id>/usun/
def delete_vreplay(request, vreplay_id):
    vreplay = get_object_or_404(Replay, pk=vreplay_id)

    if vreplay.user == request.user:
        if request.method == 'POST':
            vreplay.delete()
            return HttpResponse("vreplay usunięty!")
        else:
            return render(request, 'schemes/delete_vreplay.html', {'vreplay': vreplay})
    else:
        return HttpResponse("Nie jesteś właścicielem tego pliku!")

# 08. /partie/katalog/<id>/sprawdz-wiele/
def manage_vreplays(request, directory_id):
    directory = get_object_or_404(ReplayDirectory, pk=directory_id)

    if directory.user == request.user:
        ReplaysFormSet = inlineformset_factory(ReplayDirectory, Replay, form=CheckReplayForm, formset=BaseReplayFormSet, extra=0, can_delete=True)
        if request.method == 'POST':
            replays_formset = ReplaysFormSet(request.POST, instance=directory)
            if replays_formset.is_valid():
                #for form in replays_formset.forms:
                    #if form.has_changed():
                        #form.save()

                replays_formset.save()
                return HttpResponseRedirect(reverse('schemes:manage_vreplays', args=(directory.id,)))
        else:
            replays_formset = ReplaysFormSet(instance=directory)

        return render(request, 'schemes/manage_virtual_replays.html', {'directory': directory, 'replays_formset': replays_formset})

    else:
        return HttpResponse("Nie jesteś właścicielem katalogu!")

# Training

# 01. /orlik/
def training_independent(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user_replay_form = UserReplayForm(request.POST)
            if user_replay_form.is_valid():
                user_replay = user_replay_form.save(commit=False)
                user_replay.user = request.user
                user_replay.save()
                return HttpResponse("OK")
        else:
            return HttpResponse("Tylko zalogowani użytkownicy mogą dodawać partie treningowe!")
    else:
        user_replay_form = UserReplayForm()

    return render(request, 'schemes/training_independent.html', {'user_replay_form': user_replay_form})

# 02. /orlik/<replay_id>/
def training_dependent(request, replay_id):
    replay = get_object_or_404(KurnikReplay, name=replay_id)

    if request.method == 'POST':
        if request.user.is_authenticated:
            user_replay_form = UserReplayForm(request.POST)
            if user_replay_form.is_valid():
                user_replay = user_replay_form.save(commit=False)
                user_replay.parent_replay = replay
                user_replay.user = request.user
                user_replay.save()
                return HttpResponse("OK")
        else:
            return HttpResponse("Tylko zalogowani użytkownicy mogą dodawać partie treningowe!")
    else:
        user_replay_form = UserReplayForm()

    return render(request, 'schemes/training_dependent.html', {'replay': replay, 'user_replay_form': user_replay_form})

# Kurnik

def kurnik_user(request, player_name):
    replays = KurnikReplay.objects.filter(Q(player1=player_name) | Q(player2=player_name)).order_by('name')

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
    replays = KurnikReplay.objects.filter(Q(player1=player1_name, player2=player2_name) | Q(player1=player2_name, player2=player1_name)).order_by('name')

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

def create_and_add_vreplays(request, player1_name, player2_name):
    if request.user.is_authenticated:
        replays = KurnikReplay.objects.filter(Q(player1=player1_name, player2=player2_name) | Q(player1=player2_name, player2=player1_name)).order_by('name')

        if replays:
            user_directories = ReplayDirectory.objects.filter(user=request.user)

            if request.method == 'POST':
                add_directory_form = ReplayDirectoryForm(request.POST, user_id=request.user)
                if add_directory_form.is_valid():
                    add_directory = add_directory_form.save(commit=False)
                    add_directory.user = request.user
                    add_directory.save()

                    for replay in replays:
                        add_vreplay = Replay(directory=add_directory, replay=replay, user=request.user, checked="0")
                        add_vreplay.save()

                    return HttpResponseRedirect(reverse('schemes:show_replay_directory', args=(add_directory.id,)))
            else:
                add_directory_form = ReplayDirectoryForm(user_id=request.user)

            return render(request, 'schemes/create_and_add_vreplays.html', {'player1': player1_name, 'player2': player2_name, 'add_directory_form': add_directory_form, 'user_directories': user_directories})
        else:
            return HttpResponse("Nie znaleziono jednego z gracza, błąd.")
    else:
        return HttpResponse("Tylko zalogowani użytkownicy mają dostęp do tej opcji!")


def add_vreplays(request, player1_name, player2_name):
    if request.user.is_authenticated:
        replays = KurnikReplay.objects.filter(Q(player1=player1_name, player2=player2_name) | Q(player1=player2_name, player2=player1_name)).order_by('name')

        if replays:
            user_directories = ReplayDirectory.objects.filter(user=request.user)

            if request.method == 'POST':
                add_replay_form = ReplayForm(request.POST, user_id=request.user)
                if add_replay_form.is_valid():
                    replay_directory = ReplayDirectory.objects.get(pk=request.POST.get('directory', '1'))

                    for replay in replays:
                        add_vreplay = Replay(directory=replay_directory, replay=replay, user=request.user, checked=request.POST.get('checked', '0'))
                        add_vreplay.save()

                    return HttpResponseRedirect(reverse('schemes:show_replay_directory', args=(replay_directory.id,)))
            else:
                add_replay_form = ReplayForm(user_id=request.user)

            return render(request, 'schemes/add_vreplays.html', {'add_replay_form': add_replay_form, 'user_directories': user_directories})
        else:
            return HttpResponse("Nie znaleziono jednego z gracza, błąd.")
    else:
        return HttpResponse("Tylko zalogowani użytkownicy mają dostęp do tej opcji!")


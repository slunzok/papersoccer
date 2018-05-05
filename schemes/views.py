from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q, Count
from django.forms.models import inlineformset_factory

from .models import KurnikReplay, SchemeDirectory, Scheme, ReplayDirectory, Replay, UserReplay, \
    Profile, Entry, Comment, Notification
from .forms import SchemeDirectoryForm, SchemeForm, ReplayDirectoryForm, ReplayForm, \
    CheckReplayForm, BaseReplayFormSet, UserReplayForm, UserCreateForm, EntryForm, CommentForm, \
    UserChangePasswordForm, UserEditProfileForm

from random import randint
from django.utils import timezone
from datetime import timedelta
import re

def index(request):
    papersoccer = User.objects.get(username="papersoccer")
    all_entries = Entry.objects.filter(user=papersoccer).order_by('-created')
    paginator = Paginator(all_entries, 2)
  
    page = request.GET.get('strona')
    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        entries = paginator.page(1)
    except EmptyPage:
        entries = paginator.page(paginator.num_pages)
    is_paged = paginator.num_pages > 1

    online_users = User.objects.filter(last_login__range=(timezone.now()-timedelta(days=1), timezone.now())).count()

    return render(request, 'schemes/index.html', {'last_entries': entries, 'is_paginated' : is_paged, 'online_users': online_users, 'active': 1})

def online_users(request):
    online_users = User.objects.filter(last_login__range=(timezone.now()-timedelta(days=1), timezone.now())).order_by('-last_login')
    return render(request, 'schemes/online_users.html', {'online_users': online_users, 'active': 1})

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

        update_last_login = User.objects.get(username=request.user)
        update_last_login.last_login = timezone.now()
        update_last_login.save()

        return render(request, 'schemes/user_scheme_directories.html', {'directories': directories, 'schemes': schemes, 'add_directory_form': add_directory_form, 'active': 2})

    else:
        return HttpResponse("Opcja dostępna tylko dla zalogowanych użytkowników!")

# 02. /schematy/<username>/
def user_public_scheme_directories(request, username):
    user = get_object_or_404(User, username=username)
    directories = SchemeDirectory.objects.filter(parent_dir=None, user=user, scheme_access=2).order_by('name')
    return render(request, 'schemes/user_public_scheme_directories.html', {'user': user, 'directories': directories, 'active': 2})

# 03. /schematy/katalog/<directory_id>/user/<username>/
def user_official_schemes(request, directory_id, username):
    directory = get_object_or_404(SchemeDirectory, pk=directory_id, scheme_access=1)
    user = get_object_or_404(User, username=username)
    schemes = Scheme.objects.filter(directory=directory, user=user)
    return render(request, 'schemes/user_official_schemes.html', {'directory': directory, 'user': user, 'schemes': schemes, 'active': 2})

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

        return render(request, 'schemes/show_scheme_directory.html', {'directory': directory, 'add_directory_form': add_directory_form, 'active': 2})

    else:
        if directory.scheme_access == '3':
            return HttpResponse('Prywatny katalog!')
        else:
            return render(request, 'schemes/show_scheme_directory.html', {'directory': directory, 'active': 2})

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

        return render(request, 'schemes/edit_scheme_directory.html', {'directory': directory, 'edit_directory_form': edit_directory_form, 'user_directories': user_directories, 'active': 2})

    else:
        return HttpResponse("Nie jesteś właścicielem tego katalogu!")

# 06. /schematy/katalog/<id>/usun/
def delete_scheme_directory(request, directory_id):
    directory = get_object_or_404(SchemeDirectory, pk=directory_id)

    if directory.user == request.user:
        if request.method == 'POST':
            directory.delete()
            return HttpResponseRedirect(reverse('schemes:user_scheme_directories'))
        else:
            return render(request, 'schemes/delete_scheme_directory.html', {'directory': directory, 'active': 2})
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
                scheme.name = replay.name
                scheme.save()
                return HttpResponseRedirect(reverse('schemes:show_scheme', args=(scheme.id,)))
        else:
            return HttpResponse("Tylko zalogowani użytkownicy mogą dodawać schematy!")
    else:
        scheme_form = SchemeForm(user_id=request.user.id)

    return render(request, 'schemes/create_scheme.html', {'replay': replay, 'scheme_form': scheme_form, 'active': 2})

# 09. /partia/<replay_id>/dodaj/
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
                add_replay.name = replay.name
                add_replay.save()
                return HttpResponseRedirect(reverse('schemes:show_replay_directory', args=(add_replay.directory.id,)))
        else:
            replay_form = ReplayForm(user_id=request.user.id)

        return render(request, 'schemes/add_replay.html', {'replay': replay, 'replay_form': replay_form, 'user_directories': user_directories, 'active': 2})
    else:
        return HttpResponse('Opcja dostępna tylko dla zalogowanych użytkowników!')

# 10. /schemat/<scheme_id>/
def show_scheme(request, scheme_id):
    scheme = get_object_or_404(Scheme, pk=scheme_id)

    if scheme.user != request.user and scheme.directory.scheme_access == '3':
        return HttpResponse("Schemat prywatny!")
    else:
        return render(request, 'schemes/show_scheme.html', {'scheme': scheme, 'active': 2})

# 11. /schemat/<scheme_id>/edytuj/
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

        return render(request, 'schemes/edit_scheme.html', {'scheme': scheme, 'scheme_form': scheme_form, 'user_directories': user_directories, 'active': 2})
    else:
        return HttpResponse("Nie jesteś właścicielem tego schematu!")

# 12. /schemat/<scheme_id>/usun/
def delete_scheme(request, scheme_id):
    scheme = get_object_or_404(Scheme, pk=scheme_id)

    if scheme.user == request.user:
        if request.method == 'POST':
            scheme.delete()
            return HttpResponseRedirect(reverse('schemes:show_scheme_directory', args=(scheme.directory.id,)))
        else:
            return render(request, 'schemes/delete_scheme.html', {'scheme': scheme, 'active': 2})
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

        update_last_login = User.objects.get(username=request.user)
        update_last_login.last_login = timezone.now()
        update_last_login.save()

        return render(request, 'schemes/user_replay_directories.html', {'directories': directories, 'add_directory_form': add_directory_form, 'active': 2})

    else:
        return HttpResponse("Opcja dostępna tylko dla zalogowanych użytkowników!")

# 02. /partie/<username>/
def user_public_replay_directories(request, username):
    user = get_object_or_404(User, username=username)
    directories = ReplayDirectory.objects.filter(parent_dir=None, user=user, replay_access=2).order_by('name')
    return render(request, 'schemes/user_public_replay_directories.html', {'user': user, 'directories': directories, 'active': 2})

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

        return render(request, 'schemes/show_replay_directory.html', {'directory': directory, 'add_directory_form': add_directory_form, 'active': 2})

    else:
        if directory.replay_access == '3':
            return HttpResponse('Prywatny katalog!')
        else:
            return render(request, 'schemes/show_replay_directory.html', {'directory': directory, 'active': 2})

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

        return render(request, 'schemes/edit_replay_directory.html', {'directory': directory, 'edit_directory_form': edit_directory_form, 'user_directories': user_directories, 'active': 2})

    else:
        return HttpResponse("Nie jesteś właścicielem tego katalogu")

# 05. /partie/katalog/<id>/usun/
def delete_replay_directory(request, directory_id):
    directory = get_object_or_404(ReplayDirectory, pk=directory_id)

    if directory.user == request.user:
        if request.method == 'POST':
            directory.delete()
            return HttpResponseRedirect(reverse('schemes:user_replay_directories'))
        else:
            return render(request, 'schemes/delete_replay_directory.html', {'directory': directory, 'active': 2})
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

        return render(request, 'schemes/edit_vreplay.html', {'vreplay': vreplay, 'vreplay_form': vreplay_form, 'user_directories': user_directories, 'active': 2})
    else:
        return HttpResponse("Nie jesteś właścicielem tego pliku!")

# 07. /wirtualny/<id>/usun/
def delete_vreplay(request, vreplay_id):
    vreplay = get_object_or_404(Replay, pk=vreplay_id)

    if vreplay.user == request.user:
        if request.method == 'POST':
            vreplay.delete()
            return HttpResponseRedirect(reverse('schemes:show_replay_directory', args=(vreplay.directory.id,)))
        else:
            return render(request, 'schemes/delete_vreplay.html', {'vreplay': vreplay, 'active': 2})
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
                return HttpResponseRedirect(reverse('schemes:show_replay_directory', args=(directory.id,)))
        else:
            replays_formset = ReplaysFormSet(instance=directory)

        return render(request, 'schemes/manage_virtual_replays.html', {'directory': directory, 'replays_formset': replays_formset, 'active': 2})

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
                return HttpResponseRedirect(reverse('schemes:custom_ureplays'))
        else:
            return HttpResponse("Tylko zalogowani użytkownicy mogą dodawać partie treningowe!")
    else:
        user_replay_form = UserReplayForm()

    return render(request, 'schemes/training_independent.html', {'user_replay_form': user_replay_form, 'active': 1})

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
                return HttpResponseRedirect(reverse('schemes:custom_ureplays'))
        else:
            return HttpResponse("Tylko zalogowani użytkownicy mogą dodawać partie treningowe!")
    else:
        user_replay_form = UserReplayForm()

    return render(request, 'schemes/training_dependent.html', {'replay': replay, 'user_replay_form': user_replay_form, 'active': 1})

# 03. /orlik/partie/
def custom_ureplays(request):
    if request.user.is_authenticated:
        ureplays = UserReplay.objects.filter(user=request.user).order_by('name')
        return render(request, 'schemes/custom_ureplays.html', {'ureplays': ureplays, 'active': 2})
    else:
        return HttpResponse("Opcja dostępna tylko dla zalogowanych użytkowników!")

# 04. /orlik/partie/<username>/
def custom_public_ureplays(request, username):
    user = get_object_or_404(User, username=username)
    ureplays = UserReplay.objects.filter(user=user, replay_access=2).order_by('name')
    return render(request, 'schemes/custom_public_ureplays.html', {'user': user, 'ureplays': ureplays, 'active': 2})

# 05. /orlik/partia/<replay_id>/
def create_scheme_from_custom_ureplay(request, replay_id):
    ureplay = get_object_or_404(UserReplay, pk=replay_id)

    if ureplay.user != request.user and ureplay.replay_access == "3":
        return HttpResponse("Prywatna partia treningowa!")
    else:
        if request.method == 'POST':
            if request.user.is_authenticated:
                scheme_form = SchemeForm(request.POST, user_id=request.user.id)
                if scheme_form.is_valid():
                    scheme = scheme_form.save(commit=False)
                    scheme.ureplay = ureplay
                    scheme.user = request.user
                    scheme.name = ureplay.name
                    scheme.save()
                    return HttpResponseRedirect(reverse('schemes:show_scheme', args=(scheme.id,)))
            else:
                return HttpResponse("Tylko zalogowani użytkownicy mogą dodawać schematy!")
        else:
            scheme_form = SchemeForm(user_id=request.user.id)

        return render(request, 'schemes/create_scheme_from_custom_ureplay.html', {'ureplay': ureplay, 'scheme_form': scheme_form, 'active': 2})

# 06. /orlik/partia/<replay>/edytuj/
def edit_ureplay(request, replay_id):
    ureplay = get_object_or_404(UserReplay, pk=replay_id)

    if ureplay.user == request.user:
        if request.method == 'POST':
            ureplay_form = UserReplayForm(request.POST, instance=ureplay)
            if ureplay_form.is_valid():
                ureplay_form.save()
                return HttpResponseRedirect(reverse('schemes:edit_ureplay', args=(ureplay.id,)))
        else:
            ureplay_form = UserReplayForm(instance=ureplay)

        return render(request, 'schemes/edit_ureplay.html', {'ureplay': ureplay, 'ureplay_form': ureplay_form, 'active': 2})
    else:
        return HttpResponse("Nie jesteś właścicielem tej partii treningowej!")

# 07. /orlik/partia/<replay>/usun/
def delete_ureplay(request, replay_id):
    ureplay = get_object_or_404(UserReplay, pk=replay_id)

    if ureplay.user == request.user:
        if request.method == 'POST':
            ureplay.delete()
            return HttpResponseRedirect(reverse('schemes:custom_ureplays'))
        else:
            return render(request, 'schemes/delete_ureplay.html', {'ureplay': ureplay, 'active': 2})
    else:
        return HttpResponse("Nie jesteś właścicielem tej partii treningowej!")

# 08. /orlik/partia/<replay_id>/dodaj/
def add_ureplay_to_user_replay_directory(request, replay_id):
    ureplay = get_object_or_404(UserReplay, pk=replay_id)

    if ureplay.user != request.user and ureplay.replay_access == "3":
        return HttpResponse("Prywatna partia treningowa!")
    else:
        if request.user.is_authenticated:
            user_directories = ReplayDirectory.objects.filter(user=request.user)
            if request.method == 'POST':
                ureplay_form = ReplayForm(request.POST, user_id=request.user.id)
                if ureplay_form.is_valid():
                    add_replay = ureplay_form.save(commit=False)
                    add_replay.ureplay = ureplay
                    add_replay.user = request.user
                    add_replay.name = ureplay.name
                    add_replay.save()
                    return HttpResponseRedirect(reverse('schemes:show_replay_directory', args=(add_replay.directory.id,)))
            else:
                ureplay_form = ReplayForm(user_id=request.user.id)

            return render(request, 'schemes/add_ureplay_to_user_replay_directory.html', {'ureplay': ureplay, 'ureplay_form': ureplay_form, 'user_directories': user_directories, 'active': 2})
        else:
            return HttpResponse("Opcja dostępna tylko dla zalogowanych użytkowników!")

# Kurnik

# 01. /kurnik/<player_name>/
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
        return render(request, 'schemes/kurnik_user.html', {'players': players2, 'active': 1})
    else:
        return HttpResponse('Nie znaleziono gracza!')

# 02. /kurnik/<player1_name>/<player2_name>/
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
        return render(request, 'schemes/kurnik_user_battles.html', {'replays': replays, 'players': players2, 'player1': player1_name, 'player2': player2_name, 'active': 1})

    else:
        return HttpResponse('Nie znaleziono gracza!')

# 03. /kurnik/<player1_name>/<player2_name>/utworz-kopiuj/
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
                        add_vreplay = Replay(directory=add_directory, replay=replay, user=request.user, name=replay.name, checked="0")
                        add_vreplay.save()

                    return HttpResponseRedirect(reverse('schemes:show_replay_directory', args=(add_directory.id,)))
            else:
                add_directory_form = ReplayDirectoryForm(user_id=request.user)

            return render(request, 'schemes/create_and_add_vreplays.html', {'player1': player1_name, 'player2': player2_name, 'add_directory_form': add_directory_form, 'user_directories': user_directories, 'active': 1})
        else:
            return HttpResponse("Nie znaleziono jednego z gracza, błąd.")
    else:
        return HttpResponse("Tylko zalogowani użytkownicy mają dostęp do tej opcji!")

# 04. /kurnik/<player1_name>/<player2_name>/kopiuj/
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
                        add_vreplay = Replay(directory=replay_directory, replay=replay, user=request.user, name=replay.name, checked=request.POST.get('checked', '0'))
                        add_vreplay.save()

                    return HttpResponseRedirect(reverse('schemes:show_replay_directory', args=(replay_directory.id,)))
            else:
                add_replay_form = ReplayForm(user_id=request.user)

            return render(request, 'schemes/add_vreplays.html', {'add_replay_form': add_replay_form, 'user_directories': user_directories, 'active': 1})
        else:
            return HttpResponse("Nie znaleziono jednego z gracza, błąd.")
    else:
        return HttpResponse("Tylko zalogowani użytkownicy mają dostęp do tej opcji!")

# Registration

# 01. /zarejestruj/
def register_account(request):
    if request.user.is_authenticated:
        return HttpResponse("Wyloguj się, jeśli chcesz zarejestrować nowe konto ;)")
    else:
        replay_id = randint(61000000, 62000000)

        for check_replay in range(replay_id, replay_id+10):
            get_replay = KurnikReplay.objects.get(name=check_replay)
            if len(get_replay.moves.split()) > 20:
                moves = get_replay.moves.split()[0:20]
                replay = " ".join(moves)
                break

        if request.method == 'POST':
            register_user_form = UserCreateForm(request.POST)
            if register_user_form.is_valid():
                register_user_form.save()

                username = request.POST.get('username', '')
                password = request.POST.get('password1', '')
                kurnik = request.POST.get('kurnik', '')

                new_user = authenticate(username=username, password=password)

                p = Profile(user=new_user, kurnik_name=kurnik)
                p.save()

                login(request, new_user)

                return HttpResponseRedirect(reverse('schemes:user_scheme_directories'))
        else:
            register_user_form = UserCreateForm()

        return render(request, 'schemes/register_account.html', {'replay': replay, 'register_user_form': register_user_form, 'active': 2})

# 02. /zaloguj/
def login_user(request):
    if request.user.is_authenticated:
        return HttpResponse("Przecież jesteś już zalogowany ;)")
    else:
        if request.method == 'POST':
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('schemes:user_scheme_directories'))
            else:
                return HttpResponseRedirect(reverse('schemes:login_user'))

        return render(request, 'schemes/login_user.html', {'active': 2})

# 03. /wyloguj/
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('schemes:index'))

# Microblog

# 01. /trybuna/
def microblog(request):
    all_entries = Entry.objects.all().order_by('-created')
    paginator = Paginator(all_entries, 10)
  
    page = request.GET.get('strona')
    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        entries = paginator.page(1)
    except EmptyPage:
        entries = paginator.page(paginator.num_pages)
    is_paged = paginator.num_pages > 1

    if request.user.is_authenticated:
        if request.method == 'POST':
            entry_form = EntryForm(request.POST)
            if entry_form.is_valid():
                entry = entry_form.save(commit=False)
                entry.user = request.user
                entry.save()

                find_users = re.findall(r'@([a-zA-Z0-9_\-]+)', entry.content)
                for check_user in find_users:
                    try:
                        notificated_user = User.objects.get(username=check_user)
                    except ObjectDoesNotExist: 
                        notificated_user = '0'

                    if notificated_user != '0':
                        add_notification = Notification(sender=request.user, receiver=notificated_user, entry=entry)
                        add_notification.save()

                return HttpResponseRedirect(reverse('schemes:show_entry', args=(entry.id,)))
        else:
            entry_form = EntryForm()

        update_last_login = User.objects.get(username=request.user)
        update_last_login.last_login = timezone.now()
        update_last_login.save()

        return render(request, 'schemes/microblog.html', {'entry_form': entry_form, 'last_entries': entries, 'is_paginated' : is_paged, 'active': 1})
    else:
        return render(request, 'schemes/microblog.html', {'last_entries': entries, 'is_paginated' : is_paged, 'active': 1})

# 02. /trybuna/wpis/<entry_id>/
def show_entry(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)

    if request.user.is_authenticated:
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.entry = entry
                comment.user = request.user
                comment.save()

                find_users = re.findall(r'@([a-zA-Z0-9_\-]+)', comment.content)
                for check_user in find_users:
                    try:
                        notificated_user = User.objects.get(username=check_user)
                    except ObjectDoesNotExist: 
                        notificated_user = '0'

                    if notificated_user != '0':
                        add_notification = Notification(sender=request.user, receiver=notificated_user, entry=entry)
                        add_notification.save()

                return HttpResponseRedirect(reverse('schemes:show_entry', args=(entry.id,)))
        else:
            comment_form = CommentForm()

        return render(request, 'schemes/show_entry.html', {'entry': entry, 'comment_form': comment_form, 'active': 1})
    else:
        return render(request, 'schemes/show_entry.html', {'entry': entry, 'active': 1})

# 03. /trybuna/wpis/<entry_id>/edytuj/
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)

    if entry.user == request.user:
        if request.method == 'POST':
            entry_form = EntryForm(request.POST, instance=entry)
            if entry_form.is_valid():
                entry_form.save()
                return HttpResponseRedirect(reverse('schemes:show_entry', args=(entry.id,)))
        else:
            entry_form = EntryForm(instance=entry)

        return render(request, 'schemes/edit_entry.html', {'entry': entry, 'entry_form': entry_form, 'active': 1})
    else:
        return HttpResponse("Nie jesteś autorem wpisu!")

# 04. /trybuna/komentarz/<comment_id>/edytuj/
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.user == request.user:
        if request.method == 'POST':
            comment_form = CommentForm(request.POST, instance=comment)
            if comment_form.is_valid():
                comment_form.save()
                return HttpResponseRedirect(reverse('schemes:show_entry', args=(comment.entry.id,)))
        else:
            comment_form = CommentForm(instance=comment)

        return render(request, 'schemes/edit_comment.html', {'comment': comment, 'comment_form': comment_form, 'active': 1})
    else:
        return HttpResponse("Nie jesteś autorem komentarza!")

# 05. /powiadomienia/
def show_notifications(request):
    if request.user.is_authenticated:
        new_notifications = Notification.objects.filter(receiver=request.user, created__gt=request.user.profile.notifications).order_by('-created')
        old_notifications = Notification.objects.filter(receiver=request.user, created__range=(request.user.profile.notifications-timedelta(days=14), request.user.profile.notifications)).order_by('-created')

        update_notifications = Profile.objects.get(user=request.user)
        update_notifications.notifications = timezone.now()
        update_notifications.save()

        update_last_login = User.objects.get(username=request.user)
        update_last_login.last_login = timezone.now()
        update_last_login.save()

        paginator = Paginator(old_notifications, 10)
      
        page = request.GET.get('strona')
        try:
            notifications = paginator.page(page)
        except PageNotAnInteger:
            notifications = paginator.page(1)
        except EmptyPage:
            notifications = paginator.page(paginator.num_pages)
        is_paged = paginator.num_pages > 1

        return render(request, 'schemes/show_notifications.html', {'new_notifications': new_notifications, 'notifications': notifications, 'is_paginated' : is_paged, 'active': 2})

    else:
        return HttpResponse("Opcja dostępna tylko dla zalogowanych użytkowników!")

# User profile/settings

# 01. /kibic/<username>/
def show_user_profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    return render(request, 'schemes/show_user_profile.html', {'user_profile': user_profile, 'active': 2})

# 02. /zmien-haslo/
def change_password(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        if request.method == 'POST':
            change_password_form = UserChangePasswordForm(request.POST, instance=user)
            if change_password_form.is_valid():
                change_password = change_password_form.save(commit=False)
                change_password.set_password(request.POST.get('password', ''))
                change_password.save()
                return HttpResponseRedirect(reverse('schemes:login_user'))
        else:
            change_password_form = UserChangePasswordForm(instance=user)

        return render(request, 'schemes/change_password.html', {'change_password_form': change_password_form, 'active': 2})
    else:
        return HttpResponse("Opcja dostępna tylko dla zalogowanych użytkowników!")

# 03. /edytuj-profil/
def edit_user_profile(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        if request.method == 'POST':
            edit_profile_form = UserEditProfileForm(request.POST, instance=profile)
            if edit_profile_form.is_valid():
                edit_profile_form.save()
                return HttpResponseRedirect(reverse('schemes:show_user_profile', args=(request.user.username,)))
        else:
            edit_profile_form = UserEditProfileForm(instance=profile)

        return render(request, 'schemes/edit_user_profile.html', {'edit_profile_form': edit_profile_form, 'active': 2})
    else:
        return HttpResponse("Opcja dostępna tylko dla zalogowanych użytkowników!")


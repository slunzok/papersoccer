from django import forms
from django.db.models import Q

from .models import SchemeDirectory, Scheme, ReplayDirectory, Replay, UserReplay, Entry, Comment, Profile
#from .models import SCHEME_ACCESS, SCHEME_TYPE
from .models import BOARD_TYPE, REPLAY_ACCESS, REPLAY_STATUS

from django.forms.models import BaseInlineFormSet

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

import re

SCHEME_ACCESS = (
    ('', '---------'),
    ('2', 'publiczny'),
    ('3', 'prywatny'),
)

SCHEME_TYPE = (
    ('', '---------'),
    ('1', 'obrona'),
    ('2', 'atak'),
    ('3', 'inne'),
)

class SchemeDirectoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'scheme'}), label='Nazwa')
    scheme_access = forms.ChoiceField(choices=SCHEME_ACCESS, label='Schemat')
    scheme_type = forms.ChoiceField(choices=SCHEME_TYPE, label='Rodzaj')
    description = forms.CharField(widget=forms.Textarea, required=False, label='Opis')

    class Meta:
        model = SchemeDirectory
        fields = ('parent_dir', 'name', 'scheme_access', 'scheme_type', 'description')

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        super(SchemeDirectoryForm, self).__init__(*args, **kwargs)
        #if self.instance:
            #self.fields['parent_dir'].queryset = SchemeDirectory.objects.filter(user=self.user_id)

    def clean_parent_dir(self):
        parent_dir = self.cleaned_data['parent_dir']

        if parent_dir != None:
            user_directory = SchemeDirectory.objects.filter(pk=parent_dir.id, user=self.user_id)
            if not user_directory:
                raise forms.ValidationError("To katalog innego użytkownika!")

        return parent_dir

    def clean_scheme_access(self):
        scheme_access = self.cleaned_data['scheme_access']

        if scheme_access == '1':
            raise forms.ValidationError("Na razie nie można dodawać oficjalnych!")

        return scheme_access

class SchemeForm(forms.ModelForm):
    elements = forms.CharField(widget=forms.TextInput(attrs={'class': 'scheme'}), label='Elementy')
    board = forms.ChoiceField(choices=BOARD_TYPE, label='Boisko')
    comment = forms.CharField(widget=forms.Textarea, required=False, label='Opis')
    
    class Meta:
        model = Scheme
        fields = ('elements', 'board', 'directory', 'comment')

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        super(SchemeForm, self).__init__(*args, **kwargs)

    def clean_directory(self):
        directory = self.cleaned_data['directory']

        user_directory = SchemeDirectory.objects.filter(Q(pk=directory.id, user=self.user_id) | Q(pk=directory.id, parent_dir__gt=0, scheme_access=1))

        if not user_directory:
            raise forms.ValidationError("To katalog innego użytkownika!")

        return directory

class ReplayDirectoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'scheme'}), label='Nazwa')
    replay_access = forms.ChoiceField(choices=REPLAY_ACCESS, label='Dostęp')

    class Meta:
        model = ReplayDirectory
        fields = ('parent_dir', 'name', 'replay_access')

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        super(ReplayDirectoryForm, self).__init__(*args, **kwargs)
        #if self.instance:
            #self.fields['parentId'].queryset = ReplayDirectory.objects.filter(user=self.user_id)

    def clean_parent_dir(self):
        parent_dir = self.cleaned_data['parent_dir']

        if parent_dir != None:
            user_directory = ReplayDirectory.objects.filter(pk=parent_dir.id, user=self.user_id)
            if not user_directory:
                raise forms.ValidationError("To katalog innego użytkownika!")

        return parent_dir

class ReplayForm(forms.ModelForm):
    checked = forms.ChoiceField(choices=REPLAY_STATUS, label='Status')

    class Meta:
        model = Replay
        fields = ('directory', 'checked')

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        super(ReplayForm, self).__init__(*args, **kwargs)
        #if self.instance:
            #self.fields['directory'].queryset = ReplayDirectory.objects.filter(user=self.user_id)

    def clean_directory(self):
        directory = self.cleaned_data['directory']

        user_directory = ReplayDirectory.objects.filter(pk=directory.id, user=self.user_id)

        if not user_directory:
            raise forms.ValidationError("Katalog nie znajduje się w twojej bibliotece! " + str(directory.id))

        return directory

class CheckReplayForm(forms.ModelForm):
    checked = forms.ChoiceField(choices=REPLAY_STATUS, label='Status')

    class Meta:
        model = Replay
        fields = ('checked',)

class BaseReplayFormSet(BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return

        for form in self.forms:
            replay = form.cleaned_data['id']
            directory = form.cleaned_data['directory']
            valid_replay = Replay.objects.filter(pk=replay.id, directory=directory.id)
            if not valid_replay:
                raise forms.ValidationError("Partia nie należy do tego katalogu!")

class UserReplayForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'scheme'}), label='Nazwa')
    replay_access = forms.ChoiceField(choices=REPLAY_ACCESS, label='Dostęp')
    moves = forms.CharField(widget=forms.Textarea, label='Ruchy')
    
    class Meta:
        model = UserReplay
        fields = ('name', 'replay_access', 'moves')

    def clean_moves(self):
        moves = self.cleaned_data['moves']

        all_moves = moves.split()

        # 1. Initial board
        i = 9
        j = 13
        board = [[""] * j for k in range(i)]

        board[0][0] = "01234567"
        board[1][0] = "01234567"
        board[2][0] = "01234567"
        board[3][0] = "0124567"
        board[4][0] = "01267"
        board[5][0] = "0123467"
        board[6][0] = "01234567"
        board[7][0] = "01234567"
        board[8][0] = "01234567"

        board[0][1] = "0124567"
        board[1][1] = "01267"
        board[2][1] = "01267"
        board[3][1] = "067"
        board[5][1] = "012"
        board[6][1] = "01267"
        board[7][1] = "01267"
        board[8][1] = "0123467"

        board[0][11] = "0234567"
        board[1][11] = "23456"
        board[2][11] = "23456"
        board[3][11] = "456"
        board[5][11] = "234"
        board[6][11] = "23456"
        board[7][11] = "23456"
        board[8][11] = "0123456"

        board[0][12] = "01234567"
        board[1][12] = "01234567"
        board[2][12] = "01234567"
        board[3][12] = "0234567"
        board[4][12] = "23456"
        board[5][12] = "0123456"
        board[6][12] = "01234567"
        board[7][12] = "01234567"
        board[8][12] = "01234567"

        for i in range(2,11):
            board[0][i] = "04567"
            board[8][i] = "01234"

        cursor_x = 4
        cursor_y = 6

        for i in range(len(all_moves)):
            if all_moves[i].isdigit() == False:
                raise forms.ValidationError("Tylko cyfry!")
            else:
                # 2. Check move
                for j in range(len(all_moves[i])):
                    if all_moves[i][j] == "0":
                        if "0" in board[cursor_x][cursor_y]:
                            raise forms.ValidationError("Błąd, w tym miejscu jest już zrobiona linia!")
                        elif cursor_x == 4 and cursor_y == 12:
                            raise forms.ValidationError("Błąd, piłka w środku bramki: nie możesz zrobić ruchu " + str(all_moves[i][j]))
                        elif len(board[cursor_x][cursor_y-1]) == 0 and len(all_moves[i])-1 != j:
                            raise forms.ValidationError("Błąd, połączyłeś ruchy: " + str(i+1) + " i " + str(i+2))
                        elif len(board[cursor_x][cursor_y-1]) in range(1,7) and len(all_moves[i])-1 == j and cursor_y-1 != 0:
                            raise forms.ValidationError("Błąd, rozdzieliłeś ruch: " + str(i+1))
                        else:
                            board[cursor_x][cursor_y] = board[cursor_x][cursor_y] + "0"
                            board[cursor_x][cursor_y-1] = board[cursor_x][cursor_y-1] + "4"  
                            cursor_y = cursor_y - 1
                    elif all_moves[i][j] == "1":
                        if "1" in board[cursor_x][cursor_y]:
                            raise forms.ValidationError("Błąd, w tym miejscu jest już zrobiona linia!")
                        elif cursor_x == 4 and cursor_y == 12:
                            raise forms.ValidationError("Błąd, piłka w środku bramki: nie możesz zrobić ruchu " + str(all_moves[i][j]))
                        elif len(board[cursor_x+1][cursor_y-1]) == 0 and len(all_moves[i])-1 != j:
                            raise forms.ValidationError("Błąd, połączyłeś ruchy: " + str(i+1) + " i " + str(i+2))
                        elif len(board[cursor_x+1][cursor_y-1]) in range(1,7) and len(all_moves[i])-1 == j and cursor_y-1 != 0:
                            raise forms.ValidationError("Błąd, rozdzieliłeś ruch: " + str(i+1))
                        else:
                            board[cursor_x][cursor_y] = board[cursor_x][cursor_y] + "1"
                            board[cursor_x+1][cursor_y-1] = board[cursor_x+1][cursor_y-1] + "5"
                            cursor_x = cursor_x + 1
                            cursor_y = cursor_y - 1
                    elif all_moves[i][j] == "2":
                        if "2" in board[cursor_x][cursor_y]:
                            raise forms.ValidationError("Błąd, w tym miejscu jest już zrobiona linia!")
                        elif len(board[cursor_x+1][cursor_y]) == 0 and len(all_moves[i])-1 != j:
                            raise forms.ValidationError("Błąd, połączyłeś ruchy: " + str(i+1) + " i " + str(i+2))
                        elif len(board[cursor_x+1][cursor_y]) in range(1,7) and len(all_moves[i])-1 == j:
                            raise forms.ValidationError("Błąd, rozdzieliłeś ruch: " + str(i+1))
                        else:
                            board[cursor_x][cursor_y] = board[cursor_x][cursor_y] + "2"
                            board[cursor_x+1][cursor_y] = board[cursor_x+1][cursor_y] + "6"  
                            cursor_x = cursor_x + 1
                    elif all_moves[i][j] == "3":
                        if "3" in board[cursor_x][cursor_y]:
                            raise forms.ValidationError("Błąd, w tym miejscu jest już zrobiona linia!")
                        elif cursor_x == 4 and cursor_y == 0:
                            raise forms.ValidationError("Błąd, piłka w środku bramki: nie możesz zrobić ruchu " + str(all_moves[i][j]))
                        elif len(board[cursor_x+1][cursor_y+1]) == 0 and len(all_moves[i])-1 != j:
                            raise forms.ValidationError("Błąd, połączyłeś ruchy: " + str(i+1) + " i " + str(i+2))
                        elif len(board[cursor_x+1][cursor_y+1]) in range(1,7) and len(all_moves[i])-1 == j and cursor_y+1 != 0:
                            raise forms.ValidationError("Błąd, rozdzieliłeś ruch: " + str(i+1))
                        else:
                            board[cursor_x][cursor_y] = board[cursor_x][cursor_y] + "3"
                            board[cursor_x+1][cursor_y+1] = board[cursor_x+1][cursor_y+1] + "7"
                            cursor_x = cursor_x + 1
                            cursor_y = cursor_y + 1
                    elif all_moves[i][j] == "4":
                        if "4" in board[cursor_x][cursor_y]:
                            raise forms.ValidationError("Błąd, w tym miejscu jest już zrobiona linia!")
                        elif cursor_x == 4 and cursor_y == 0:
                            raise forms.ValidationError("Błąd, piłka w środku bramki: nie możesz zrobić ruchu " + str(all_moves[i][j]))
                        elif len(board[cursor_x][cursor_y+1]) == 0 and len(all_moves[i])-1 != j:
                            raise forms.ValidationError("Błąd, połączyłeś ruchy: " + str(i+1) + " i " + str(i+2))
                        elif len(board[cursor_x][cursor_y+1]) in range(1,7) and len(all_moves[i])-1 == j and cursor_y+1 != 0:
                            raise forms.ValidationError("Błąd, rozdzieliłeś ruch: " + str(i+1))
                        else:
                            board[cursor_x][cursor_y] = board[cursor_x][cursor_y] + "4"
                            board[cursor_x][cursor_y+1] = board[cursor_x][cursor_y+1] + "0"  
                            cursor_y = cursor_y + 1
                    elif all_moves[i][j] == "5":
                        if "5" in board[cursor_x][cursor_y]:
                            raise forms.ValidationError("Błąd, w tym miejscu jest już zrobiona linia!")
                        elif cursor_x == 4 and cursor_y == 0:
                            raise forms.ValidationError("Błąd, piłka w środku bramki: nie możesz zrobić ruchu " + str(all_moves[i][j]))
                        elif len(board[cursor_x-1][cursor_y+1]) == 0 and len(all_moves[i])-1 != j:
                            raise forms.ValidationError("Błąd, połączyłeś ruchy: " + str(i+1) + " i " + str(i+2))
                        elif len(board[cursor_x-1][cursor_y+1]) in range(1,7) and len(all_moves[i])-1 == j and cursor_y+1 != 0:
                            raise forms.ValidationError("Błąd, rozdzieliłeś ruch: " + str(i+1))
                        else:
                            board[cursor_x][cursor_y] = board[cursor_x][cursor_y] + "5"
                            board[cursor_x-1][cursor_y+1] = board[cursor_x-1][cursor_y+1] + "1"
                            cursor_x = cursor_x - 1
                            cursor_y = cursor_y + 1
                    elif all_moves[i][j] == "6":
                        if "6" in board[cursor_x][cursor_y]:
                            raise forms.ValidationError("Błąd, w tym miejscu jest już zrobiona linia!")
                        elif len(board[cursor_x-1][cursor_y]) == 0 and len(all_moves[i])-1 != j:
                            raise forms.ValidationError("Błąd, połączyłeś ruchy: " + str(i+1) + " i " + str(i+2))
                        elif len(board[cursor_x-1][cursor_y]) in range(1,7) and len(all_moves[i])-1 == j:
                            raise forms.ValidationError("Błąd, rozdzieliłeś ruch: " + str(i+1))
                        else:
                            board[cursor_x][cursor_y] = board[cursor_x][cursor_y] + "6"
                            board[cursor_x-1][cursor_y] = board[cursor_x-1][cursor_y] + "2"  
                            cursor_x = cursor_x - 1
                    elif all_moves[i][j] == "7":
                        if "7" in board[cursor_x][cursor_y]:
                            raise forms.ValidationError("Błąd, w tym miejscu jest już zrobiona linia!")
                        elif cursor_x == 4 and cursor_y == 12:
                            raise forms.ValidationError("Błąd, piłka w środku bramki: nie możesz zrobić ruchu " + str(all_moves[i][j]))
                        elif len(board[cursor_x-1][cursor_y-1]) == 0 and len(all_moves[i])-1 != j:
                            raise forms.ValidationError("Błąd, połączyłeś ruchy: " + str(i+1) + " i " + str(i+2))
                        elif len(board[cursor_x-1][cursor_y-1]) in range(1,7) and len(all_moves[i])-1 == j and cursor_y-1 != 0:
                            raise forms.ValidationError("Błąd, rozdzieliłeś ruch: " + str(i+1))
                        else:
                            board[cursor_x][cursor_y] = board[cursor_x][cursor_y] + "7"
                            board[cursor_x-1][cursor_y-1] = board[cursor_x-1][cursor_y-1] + "3"
                            cursor_x = cursor_x - 1
                            cursor_y = cursor_y - 1
                    else:
                        raise forms.ValidationError("Możliwe ruchy: 0, 1, 2, 3, 4, 5, 6, 7")

        return moves

class UserCreateForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'scheme'}), label='Nick')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'scheme'}), label='Hasło')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'scheme'}), label='Powtórz')
    email = forms.EmailField(widget=forms.TextInput(attrs={'class' : 'scheme'}), required=False, label='*Email')
    kurnik = forms.CharField(widget=forms.TextInput(attrs={'class' : 'scheme'}), required=False, label='*Kurnik')

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")

    def clean_username(self):
        username = self.cleaned_data['username']

        user = User.objects.filter(username=username)
        if user:
            raise forms.ValidationError("Nazwa użytkownika zajęta!")
        elif not re.search(r'^([a-zA-Z0-9_\-]+)$', username):
            raise forms.ValidationError("Wprowadź poprawną nazwę użytkownika. Może ona zawierać tylko litery, liczby i znaki: _ -")

        return username

    def clean_kurnik(self):
        kurnik = self.cleaned_data['kurnik']

        if kurnik != '':
            if not re.search(r'^([a-zA-Z0-9\,\s]+)$', kurnik):
                raise forms.ValidationError("Wprowadź poprawną nazwę użytkownika z kurnika. Może ona zawierać tylko litery, liczby, przecinek i spacje.")

        return kurnik

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class EntryForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, label='Treść')

    class Meta:
        model = Entry
        fields = ('content',)

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, label='Treść')

    class Meta:
        model = Comment
        fields = ('content',)

class UserChangePasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'scheme'}), label='Hasło')

    class Meta:
        model = User
        fields = ('password',)

    def clean_password(self):
        password = self.cleaned_data['password']

        if not re.search(r'^([a-zA-Z0-9]+)$', password):
            raise forms.ValidationError("Hasło może zawierać tylko litery i liczby.")

        return password

class UserEditProfileForm(forms.ModelForm):
    kurnik_name = forms.CharField(widget=forms.Textarea, label='Kurnik')

    class Meta:
        model = Profile
        fields = ('kurnik_name',)

    def clean_kurnik_name(self):
        kurnik_name = self.cleaned_data['kurnik_name']

        if kurnik_name != '':
            if not re.search(r'^([a-zA-Z0-9\,\s]+)$', kurnik_name):
                raise forms.ValidationError("Wprowadź poprawną nazwę użytkownika z kurnika. Może ona zawierać tylko litery, liczby, przecinek i spacje.")

        return kurnik_name


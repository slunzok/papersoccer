from django import forms
from django.db.models import Q

from .models import SchemeDirectory, Scheme, ReplayDirectory, Replay
#from .models import SCHEME_ACCESS, SCHEME_TYPE
from .models import BOARD_TYPE, REPLAY_ACCESS, REPLAY_STATUS

from django.forms.models import BaseInlineFormSet

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


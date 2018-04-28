from django import forms
from django.db.models import Q

from .models import SchemeDirectory, Scheme
#from .models import SCHEME_ACCESS, SCHEME_TYPE
from .models import BOARD_TYPE

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


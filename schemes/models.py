from django.contrib.auth.models import User
from django.db import models

# Works for versions greater than Django 1.9
# https://stackoverflow.com/questions/1208698/how-do-i-use-commaseparatedintegerfield-in-django
from django.core.validators import validate_comma_separated_integer_list

SCHEME_ACCESS = (
    ('1', 'oficjalny'),
    ('2', 'publiczny'),
    ('3', 'prywatny'),
)

SCHEME_TYPE = (
    ('1', 'obrona'),
    ('2', 'atak'),
    ('3', 'inne'),
)

BOARD_TYPE = (
    ('0', 'normalne'),
    ('1', 'odwrócone'),
)

REPLAY_ACCESS = (
    ('2', 'publiczny'),
    ('3', 'prywatny'),
)

REPLAY_STATUS = (
    ('0', 'niesprawdzone'),
    ('1', 'sprawdzone'),
)

class KurnikReplay(models.Model):
    name = models.CharField(max_length=10)
    player1 = models.CharField(max_length=20)
    player2 = models.CharField(max_length=20)
    replay_date = models.CharField(max_length=10)
    replay_time = models.CharField(max_length=8)
    replay_round = models.CharField(max_length=3)
    player1_elo = models.CharField(max_length=4)
    player2_elo = models.CharField(max_length=4)
    moves = models.TextField(max_length=1000, blank=True)
    result = models.CharField(max_length=3)

    def __str__(self):
        return self.name

class UserReplay(models.Model):
    parent_replay = models.ForeignKey(KurnikReplay, blank=True, null=True, related_name="children_kreplay", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name="ureplay_owner", on_delete=models.CASCADE) 
    replay_access = models.CharField(max_length=1, choices=REPLAY_ACCESS)
    moves = models.TextField(max_length=2000)

    def __str__(self):
        return self.name

class SchemeDirectory(models.Model):
    parent_dir = models.ForeignKey('self', blank=True, null=True, related_name="children_scheme_directory", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name="scheme_directory_owner", on_delete=models.CASCADE)
    scheme_access = models.CharField(max_length=1, choices=SCHEME_ACCESS)
    scheme_type = models.CharField(max_length=1, choices=SCHEME_TYPE)
    description = models.TextField(max_length=4000, blank=True)

    def __str__(self):
        return self.name

class Scheme(models.Model):
    directory = models.ForeignKey(SchemeDirectory, related_name="schemes", on_delete=models.CASCADE)
    replay = models.ForeignKey(KurnikReplay, blank=True, null=True, related_name="replays", on_delete=models.CASCADE)
    ureplay = models.ForeignKey(UserReplay, blank=True, null=True, related_name="ureplays", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="scheme_creator", on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    elements = models.CharField(validators=[validate_comma_separated_integer_list], max_length=100)
    board = models.CharField(max_length=1, choices=BOARD_TYPE)
    comment = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class ReplayDirectory(models.Model):
    parent_dir = models.ForeignKey('self', blank=True, null=True, related_name="children_replay_directory", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name="replay_directory_owner", on_delete=models.CASCADE)
    replay_access = models.CharField(max_length=1, choices=REPLAY_ACCESS)

    def __str__(self):
        return self.name

class Replay(models.Model):
    directory = models.ForeignKey(ReplayDirectory, related_name="vreplays", on_delete=models.CASCADE)
    replay = models.ForeignKey(KurnikReplay, blank=True, null=True, related_name="kreplays", on_delete=models.CASCADE)
    ureplay = models.ForeignKey(UserReplay, blank=True, null=True, related_name="treplays", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="vreplay_owner", on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    checked = models.CharField(max_length=1, choices=REPLAY_STATUS)

    def __str__(self):
        return self.checked

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kurnik_name = models.CharField(max_length=20)
    notifications = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.kurnik_name

class Entry(models.Model):
    user = models.ForeignKey(User, related_name="entry_author", on_delete=models.CASCADE)
    content = models.TextField(max_length=5000)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class Comment(models.Model):
    entry = models.ForeignKey(Entry, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="comment_author", on_delete=models.CASCADE)
    content = models.TextField(max_length=5000)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class Notification(models.Model):
    sender = models.ForeignKey(User, related_name="sender_user", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver_user", on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, related_name="notifications", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created)

class KurnikRanking(models.Model):
    player = models.CharField(max_length=20)
    games = models.IntegerField()
    ranking = models.IntegerField()

    def __str__(self):
        return self.player


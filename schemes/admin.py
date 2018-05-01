from django.contrib import admin

from .models import KurnikReplay, UserReplay, SchemeDirectory, Scheme, ReplayDirectory, Replay, \
    Profile, Entry, Comment

class KurnikReplayAdmin(admin.ModelAdmin):
    list_display = ('name', 'player1', 'player2')

class UserReplayAdmin(admin.ModelAdmin):
    list_display = ('parent_replay', 'name', 'user', 'replay_access', 'moves')

class SchemeDirectoryAdmin(admin.ModelAdmin):
    list_display = ('parent_dir', 'name', 'user', 'scheme_access', 'scheme_type')

class SchemeAdmin(admin.ModelAdmin):
    list_display = ('directory', 'replay', 'ureplay', 'user', 'elements', 'board')

class ReplayDirectoryAdmin(admin.ModelAdmin):
    list_display = ('parent_dir', 'name', 'user', 'replay_access')

class ReplayAdmin(admin.ModelAdmin):
    list_display = ('directory', 'replay', 'ureplay', 'user', 'checked',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'kurnik_name',)

class EntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('entry', 'user', 'content', 'created',)

admin.site.register(KurnikReplay, KurnikReplayAdmin)
admin.site.register(UserReplay, UserReplayAdmin)
admin.site.register(SchemeDirectory, SchemeDirectoryAdmin)
admin.site.register(Scheme, SchemeAdmin)
admin.site.register(ReplayDirectory, ReplayDirectoryAdmin)
admin.site.register(Replay, ReplayAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Comment, CommentAdmin)

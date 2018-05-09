from django.contrib import admin

from .models import KurnikReplay, UserReplay, SchemeDirectory, Scheme, ReplayDirectory, Replay, \
    Profile, Entry, Comment, Notification, KurnikRanking

class KurnikReplayAdmin(admin.ModelAdmin):
    list_display = ('name', 'player1', 'player2')

class UserReplayAdmin(admin.ModelAdmin):
    list_display = ('parent_replay', 'name', 'user', 'replay_access', 'moves', 'created_at', 'updated_at')

class SchemeDirectoryAdmin(admin.ModelAdmin):
    list_display = ('parent_dir', 'name', 'user', 'scheme_access', 'scheme_type', 'created_at', 'updated_at')

class SchemeAdmin(admin.ModelAdmin):
    list_display = ('directory', 'replay', 'ureplay', 'user', 'name', 'elements', 'board', 'created_at', 'updated_at')

class ReplayDirectoryAdmin(admin.ModelAdmin):
    list_display = ('parent_dir', 'name', 'user', 'replay_access', 'created_at', 'updated_at')

class ReplayAdmin(admin.ModelAdmin):
    list_display = ('directory', 'replay', 'ureplay', 'user', 'name', 'checked', 'created_at', 'updated_at')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'kurnik_name', 'notifications',)

class EntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created', 'updated')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('entry', 'user', 'content', 'created', 'updated')

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'entry', 'created',)

class KurnikRankingAdmin(admin.ModelAdmin):
    list_display = ('player', 'games', 'ranking')

admin.site.register(KurnikReplay, KurnikReplayAdmin)
admin.site.register(UserReplay, UserReplayAdmin)
admin.site.register(SchemeDirectory, SchemeDirectoryAdmin)
admin.site.register(Scheme, SchemeAdmin)
admin.site.register(ReplayDirectory, ReplayDirectoryAdmin)
admin.site.register(Replay, ReplayAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(KurnikRanking, KurnikRankingAdmin)


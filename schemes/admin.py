from django.contrib import admin

from .models import KurnikReplay, SchemeDirectory, Scheme

class KurnikReplayAdmin(admin.ModelAdmin):
    list_display = ('name', 'player1', 'player2')

class SchemeDirectoryAdmin(admin.ModelAdmin):
    list_display = ('parent_dir', 'name', 'user', 'scheme_access', 'scheme_type')

class SchemeAdmin(admin.ModelAdmin):
    list_display = ('directory', 'replay', 'elements', 'board')

admin.site.register(KurnikReplay, KurnikReplayAdmin)
admin.site.register(SchemeDirectory, SchemeDirectoryAdmin)
admin.site.register(Scheme, SchemeAdmin)

from django.contrib import admin

from .models import KurnikReplay

class KurnikReplayAdmin(admin.ModelAdmin):
    list_display = ('name', 'player1', 'player2')

admin.site.register(KurnikReplay, KurnikReplayAdmin)

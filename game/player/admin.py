from django.contrib import admin

from player.models import Faction, Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(Faction)
class FactionAdmin(admin.ModelAdmin):
    pass
from django.db import models

from player.models import Faction, Player
from utils.generic_models import CommonFields


class Hero(CommonFields):
    title = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    faction = models.ForeignKey(Faction, blank=True, null=True)
    player = models.ForeignKey(Player)

    # attributes
    movement = models.DecimalField(max_digits=1, decimal_places=0)
    melee = models.DecimalField(max_digits=1, decimal_places=0)
    ballistic = models.DecimalField(max_digits=1, decimal_places=0)
    strength = models.DecimalField(max_digits=1, decimal_places=0)
    toughness = models.DecimalField(max_digits=1, decimal_places=0)
    wounds = models.DecimalField(max_digits=1, decimal_places=0)
    initiative = models.DecimalField(max_digits=1, decimal_places=0)
    attacks = models.DecimalField(max_digits=1, decimal_places=0)
    moral = models.DecimalField(max_digits=1, decimal_places=0)

    def __str__(self):
        faction_name = self.faction.name if self.faction else None
        return '({}) {} {} {}'.format(
            faction_name, self.title, self.first_name, self.last_name)

    class Meta:
        app_label = 'hero'

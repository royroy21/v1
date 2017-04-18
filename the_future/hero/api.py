from restless.preparers import FieldsPreparer

from utils.generic_resources import (
    COMMON_PREPARE_FIELDS, GenericCrudResource
)
from .forms import HeroForm
from .models import Hero


class HeroResource(GenericCrudResource):
    model_cls = Hero
    form_cls = HeroForm

    hero_fields = {
        'player_url': 'player.detail_url',
        'title': 'title',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'faction_url': 'faction.detail_url',
        'movement': 'movement',
        'melee': 'melee',
        'ballistic': 'ballistic',
        'strength': 'strength',
        'toughness': 'toughness',
        'wounds': 'wounds',
        'initiative': 'initiative',
        'attacks': 'attacks',
        'moral': 'moral',
    }
    hero_fields.update(COMMON_PREPARE_FIELDS)
    preparer = FieldsPreparer(fields=hero_fields)
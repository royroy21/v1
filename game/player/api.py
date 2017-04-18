from restless.preparers import FieldsPreparer

from utils.generic_resources import (
    COMMON_PREPARE_FIELDS, GenericCrudResource, GenericReadOnlyResource
)
from player.forms import PlayerForm
from player.models import Faction, Player


class PlayerResource(GenericCrudResource):
    model_cls = Player
    form_cls = PlayerForm

    player_fields = {
        'account_url': 'account.detail_url',
        'title': 'title',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'faction_url': 'faction.detail_url',
    }
    player_fields.update(COMMON_PREPARE_FIELDS)
    preparer = FieldsPreparer(fields=player_fields)


class FactionResource(GenericReadOnlyResource):
    model_cls = Faction

    faction_fields = {
        'name': 'name',
        'description': 'description',
        'self': 'detail_url',
        'is_active': 'is_active',
    }
    faction_fields.update(COMMON_PREPARE_FIELDS)
    preparer = FieldsPreparer(fields=faction_fields)
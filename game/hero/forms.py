from django.forms import ModelForm

from account.models import Account
from player.models import Faction, Player
from utils.custom_form_fields import RelationshipUrlField

from .models import Hero


class HeroForm(ModelForm):
    player_url = RelationshipUrlField(
        model_type=Player, required=True,
    )
    faction_url = RelationshipUrlField(
        model_type=Faction, required=True,
    )

    def save(self, commit=True, user=None):
        if self.cleaned_data['player_url'] is not None:
            self.instance.player = self.cleaned_data['player_url']
        if self.cleaned_data['faction_url'] is not None:
            self.instance.faction = self.cleaned_data['faction_url']

        if user:
            account = Account.objects.get(user=user)
            if not self.instance.created_by:
                self.instance.created_by = account
            self.instance.modified_by = account

        return super(HeroForm, self).save(commit)

    class Meta:
        model = Hero
        exclude = (
            'faction',
            'player',
            'created',
            'modified',
            'created_by',
            'modified_by',
            'is_active',
        )
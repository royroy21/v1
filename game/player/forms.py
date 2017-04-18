from django.forms import ModelForm

from account.models import Account
from player.models import Faction, Player
from utils.custom_form_fields import RelationshipUrlField


class PlayerForm(ModelForm):
    account_url = RelationshipUrlField(
        model_type=Account,
        required=True
    )
    faction_url = RelationshipUrlField(
        model_type=Faction,
        required=False
    )

    def save(self, commit=True, user=None):
        if self.cleaned_data['faction_url'] is not None:
            self.instance.faction = self.cleaned_data['faction_url']
        if self.cleaned_data['account_url'] is not None:
            self.instance.account = self.cleaned_data['account_url']

        if user:
            account = Account.objects.get(user=user)
            if not self.instance.created_by:
                self.instance.created_by = account
            self.instance.modified_by = account

        return super(PlayerForm, self).save(commit)

    class Meta:
        model = Player
        exclude = (
            'account',
            'faction',
            'created',
            'modified',
            'created_by',
            'modified_by',
            'is_active',
        )
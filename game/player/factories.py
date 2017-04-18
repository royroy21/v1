import factory
import random

from account.factories import AccountFactory
from player.models import Faction, Player
from utils.factory_functions import CommonFields


class FactionFactory(CommonFields):
    name = random.choice(['Vampires', 'Werewolves'])
    description = factory.Faker('text')

    class Meta:
        model = Faction


class PlayerFactory(CommonFields):
    account = factory.SubFactory(AccountFactory)
    title = random.choice(['Sir', 'Master', 'The Amazing!'])
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    faction = factory.SubFactory(FactionFactory)

    class Meta:
        model = Player
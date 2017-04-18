import factory
import random

from player.factories import FactionFactory, PlayerFactory
from utils.factory_functions import CommonFields

from .models import Hero


class HeroFactory(CommonFields):
    title = random.choice(['Sir', 'Master', 'The Amazing!'])
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    faction = factory.SubFactory(FactionFactory)
    player = factory.SubFactory(PlayerFactory)

    # attributes
    movement = random.choice(range(10))
    melee = random.choice(range(10))
    ballistic = random.choice(range(10))
    strength = random.choice(range(10))
    toughness = random.choice(range(10))
    wounds = random.choice(range(10))
    initiative = random.choice(range(10))
    attacks = random.choice(range(10))
    moral = random.choice(range(10))

    class Meta:
        model = Hero
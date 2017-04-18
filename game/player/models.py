from django.conf import settings
from django.db import models

import jwt

from account.models import Account
from utils.generic_models import CommonFields


class Faction(CommonFields):
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'player'


class Player(CommonFields):
    account = models.ForeignKey(Account)
    title = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    faction = models.ForeignKey(Faction, blank=True, null=True)

    def __str__(self):
        faction_name = self.faction.name if self.faction else None
        return '({}) {} {} {}'.format(
            faction_name, self.title, self.first_name, self.last_name)

    class Meta:
        app_label = 'player'

    def get_jwt(self):
        user = self.account.user
        payload = {'email': user.email, 'user_id': user.pk}
        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            'HS256').decode('utf-8')
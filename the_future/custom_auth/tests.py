import json

from django.test import TestCase

from player.factories import FactionFactory
from utils.generic_tests import CreateUser

from django.test.utils import override_settings


@override_settings(DEBUG=True)
class JwtTests(TestCase, CreateUser):
    url = '/api/jwt/'

    def setUp(self):
        self.user, self.token, self.account = self.create_user()
        self.faction = FactionFactory()

    def test_get_and_authenticate_with_jwt(self):
        get_faction_no_auth = self.client.get(self.faction.detail_url)
        self.assertEqual(get_faction_no_auth.status_code, 401)

        get_faction_with_auth = self.client.get(
            self.faction.detail_url,
            HTTP_AUTHORIZATION='Bearer {}'.format(self.token)
        )
        self.assertEqual(get_faction_with_auth.status_code, 200)
        self.assertEqual(
            json.loads(get_faction_with_auth.content.decode('utf8'))['name'],
            self.faction.name
        )

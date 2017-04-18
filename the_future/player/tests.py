import json

from django.test import TestCase

from player.factories import FactionFactory, PlayerFactory
from player.models import Player
from utils.generic_tests import GenericDetailListTests


class PlayerTests(GenericDetailListTests, TestCase):
    factory_cls = PlayerFactory
    url = '/api/player/'

    def create_obj_variables(self):
        faction = FactionFactory()

        return {
            'account': self.account,
            'title': 'Sir',
            'first_name': 'Roy',
            'last_name': 'Hanley',
            'faction': faction,
        }

    def test_create_player(self):
        convert_fields = [
            'account', 'faction',
        ]
        data = self.convert_fields_to_detail_url(
            self.create_obj_variables(), convert_fields
        )

        resp = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(self.token)
        )

        r_data = json.loads(resp.content.decode('utf8'))
        self.assertEqual(resp.status_code, 201)

        for k, v in data.items():
            self.assertEqual(r_data[k], str(v))

    def test_update_player(self):
        player_obj = PlayerFactory()

        get_resp = self.client.get(
            player_obj.detail_url,
            HTTP_AUTHORIZATION='Bearer {}'.format(self.token),
        )
        get_data = json.loads(get_resp.content.decode('utf8'))

        first_name = 'Cat'
        last_name = 'Meow'
        get_data['first_name'] = first_name
        get_data['last_name'] = last_name

        put_resp = self.client.put(
            player_obj.detail_url,
            data=json.dumps(get_data),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(self.token),
        )
        put_data = json.loads(put_resp.content.decode('utf8'))

        self.assertEqual(put_resp.status_code, 202)
        self.assertEqual(put_data['first_name'], first_name)
        self.assertEqual(put_data['last_name'], last_name)

    def test_delete_player(self):
        player_obj = PlayerFactory()
        self.assertTrue(
            Player.objects.filter(id=player_obj.id, is_active=True).exists()
        )

        resp = self.client.delete(
            player_obj.detail_url,
            HTTP_AUTHORIZATION='Bearer {}'.format(self.token),
        )
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(
            Player.objects.filter(id=player_obj.id, is_active=True).exists()
        )

    def test_get_jwt(self):
        player_obj = PlayerFactory(title='test')

        bad_resp = self.client.get(player_obj.detail_url)
        self.assertEqual(bad_resp.status_code, 401)

        good_resp = self.client.get(
            player_obj.detail_url,
            HTTP_AUTHORIZATION='Bearer {}'.format(player_obj.get_jwt()))
        self.assertEqual(good_resp.status_code, 200)
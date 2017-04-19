import json

from django.test import TestCase

from player.factories import FactionFactory, PlayerFactory
from player.models import Player
from utils.url_to_object import url_to_object
from utils.generic_tests import CreateUser


class PlayerTests(TestCase, CreateUser):
    factory_cls = PlayerFactory
    url = '/api/player/'

    def setUp(self):
        self.user, self.token, self.account = self.create_user()
        self.test_obj = self._create_test_obj()

    def _create_test_obj(self):
        return self.factory_cls()

    def create_obj_variables(self):
        faction = FactionFactory()

        return {
            'account': self.account,
            'title': 'Sir',
            'first_name': 'Roy',
            'last_name': 'Hanley',
            'faction': faction,
        }

    def convert_fields_to_detail_url(self, data, field_array):
        """Converts fields in data so to be JSON friendly
        """
        for field in field_array:
            data['{}_url'.format(field)] = data[field].detail_url
            del data[field]

        return data

    def test_create_player(self):
        data = self.convert_fields_to_detail_url(
            self.create_obj_variables(), ['account', 'faction'],
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

    def _test_fields(self, resp_data):
        # testing self field to object
        self.assertEquals(
            resp_data['self'], getattr(self.test_obj, 'detail_url'))
        self.assertIn('account_url', resp_data)

        # testing account field to object
        obj_value = getattr(self.test_obj, 'account')
        self.assertEquals(resp_data['account_url'], obj_value.detail_url)

        # testing faction field to object
        obj_value = getattr(self.test_obj, 'faction')
        self.assertEquals(resp_data['faction_url'], obj_value.detail_url)

        self.assertIn('title', resp_data)
        self.assertIn('first_name', resp_data)
        self.assertIn('last_name', resp_data)
        self.assertIn('active_for_game', resp_data)
        self.assertIn('ip_address', resp_data)
        self.assertIn('latitude', resp_data)
        self.assertIn('longitude', resp_data)

    def test_get_jwt(self):
        player_obj = PlayerFactory(title='test')

        bad_resp = self.client.get(player_obj.detail_url)
        self.assertEqual(bad_resp.status_code, 401)

        good_resp = self.client.get(
            player_obj.detail_url,
            HTTP_AUTHORIZATION='Bearer {}'.format(player_obj.get_jwt()))
        self.assertEqual(good_resp.status_code, 200)

    def test_detail(self):
        resp = self.client.get(
            '{}{}/'.format(self.url, self.test_obj.id),
            HTTP_AUTHORIZATION='Bearer {}'.format(self.token))

        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.content.decode('utf8'))
        self._test_fields(resp_data)

    def test_list(self):
        resp = self.client.get(
            self.url, HTTP_AUTHORIZATION='Bearer {}'.format(self.token))

        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.content.decode('utf8'))['objects'][0]
        self._test_fields(resp_data)

    def test_url_to_object(self):
        new_obj = url_to_object(self.test_obj.detail_url)
        self.assertEqual(new_obj, self.test_obj)
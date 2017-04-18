import json

from django.test import TestCase

from account.models import Account


class AccountTests(TestCase):
    url = '/api/account/'
    jwt_api_url = '/api/jwt/'

    def _create_user_through_api(self, username, password_1, password_2):
        data = {
            'username': username,
            'password_1': password_1,
            'password_2': password_2,
        }
        return self.client.post(
            self.url, data=json.dumps(data), content_type='application/json'
        )

    def _get_jwt(self, username, password):
        jwt_data = {
            'username': username,
            'password': password,
        }
        return self.client.post(
            self.jwt_api_url,
            json.dumps(jwt_data),
            content_type='application/json',
        )

    def test_create(self):
        username = 'mr_cat'
        password = 'Pa$$w0rD'
        resp = self._create_user_through_api(username, password, password)
        self.assertEqual(resp.status_code, 201)

        resp_data = json.loads(resp.content.decode('utf8'))
        self.assertEqual(resp_data['username'], username)

        self.assertEqual(
            Account.objects.filter(
                user__username=username, user__is_active=True
            ).count(), 1
        )

        # get jwt
        jwt_resp = self._get_jwt(username, password)
        self.assertTrue(json.loads(jwt_resp.content.decode('utf8'))['token'])

    def test_create_with_mismatched_passwords(self):
        username = 'mr_dog'
        resp = self._create_user_through_api('mr_dog', 'Pa$$w0rD', 'Pa$$w0Dx')
        self.assertEqual(resp.status_code, 400)

        self.assertEqual(
            Account.objects.filter(
                user__username=username, user__is_active=True
            ).count(), 0
        )

    def test_delete(self):
        username_1 = 'mr_cat'
        password_1 = 'Pa$$w0rD'
        create_resp_1 = self._create_user_through_api(
            username_1, password_1, password_1
        )
        create_data_1 = json.loads(create_resp_1.content.decode('utf8'))
        jwt_resp_1 = self._get_jwt(username_1, password_1)
        jwt_1 = json.loads(jwt_resp_1.content.decode('utf8'))['token']

        # create another user to try to delete with first user
        # this should fail as users are only allowed to delete
        # or update themselves.
        username_2 = 'mr_dog'
        password_2 = 'Pa$$w0rD'
        self._create_user_through_api(username_2, password_2, password_2)
        jwt_resp_2 = self._get_jwt(username_2, password_2)
        jwt_2 = json.loads(jwt_resp_2.content.decode('utf8'))['token']

        delete_resp_2 = self.client.delete(
            create_data_1['self'], HTTP_AUTHORIZATION='Bearer {}'.format(jwt_2)
        )
        self.assertEqual(delete_resp_2.status_code, 401)

        self.assertEqual(
            Account.objects.filter(
                user__username=username_1, user__is_active=True
            ).count(), 1
        )

        # delete with correct user jwt
        delete_resp_1 = self.client.delete(
            create_data_1['self'], HTTP_AUTHORIZATION='Bearer {}'.format(jwt_1)
        )
        self.assertEqual(delete_resp_1.status_code, 204)

        self.assertEqual(
            Account.objects.filter(
                user__username=username_1, user__is_active=False
            ).count(), 1
        )
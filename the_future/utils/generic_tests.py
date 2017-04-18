import json

from django.contrib.auth.models import User

from account.models import Account
from utils.url_to_object import url_to_object


class CreateUser(object):

    jwt_api_url = '/api/jwt/'
    username = 'Cat'
    password = 'CatNip1980'

    def create_user(self, is_superuser=False):
        create_user_params = {
            'username': self.username,
            'password': self.password
        }
        if is_superuser:
            create_user_params['is_superuser'] = True

        user = User.objects.create_user(**create_user_params)
        account = Account.objects.create(user=user)

        return user, self._get_jwt(), account

    def _get_jwt(self):
        data = {
            'username': self.username,
            'password': self.password,
        }
        resp = self.client.post(
            self.jwt_api_url,
            json.dumps(data),
            content_type='application/json',
        )
        return json.loads(resp.content.decode('utf8'))['token']


class GenericDetailListTests(CreateUser):
    url = None
    factory_cls = None

    def setUp(self):
        self.user, self.token, self.account = self.create_user()
        self.test_obj = self._create_test_obj()

    def _create_test_obj(self):
        return self.factory_cls()

    def convert_fields_to_detail_url(self, data, field_array):
        """Converts fields in data so to be JSON friendly
        """
        for field in field_array:
            if isinstance(data[field], list):
                data['{}_urls'.format(field)] = [d.detail_url
                                                 for d in data[field]]
            else:
                data['{}_url'.format(field)] = data[field].detail_url

            del data[field]

        return data

    def _test_fields(self, data):
        for k, v in data.items():
            try:
                self.assertEquals(str(v), str(getattr(self.test_obj, k)))
            except (AssertionError, AttributeError):
                # testing standard URL field
                if k.endswith('_url'):
                    obj_value = getattr(self.test_obj, k.replace('_url', ''))
                    if not obj_value:
                        self.assertFalse(v)
                    else:
                        self.assertEquals(v, obj_value.detail_url)
                # testing many to many fields
                elif k.endswith('_urls'):
                    obj_value = getattr(self.test_obj, k.replace('_urls', ''))
                    self.assertEqual(
                        [o.detail_url for o in obj_value.all()], v
                    )
                # self vs detail_url
                elif k == 'self':
                    self.assertEquals(
                        str(v), str(getattr(self.test_obj, 'detail_url'))
                    )
                else:
                    self.fail('problem testing "{}" field'.format(k))

    def test_detail(self):
        resp = self.client.get(
            '{}{}/'.format(self.url, self.test_obj.id),
            HTTP_AUTHORIZATION='Bearer {}'.format(self.token)
        )

        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.content.decode('utf8'))
        self._test_fields(resp_data)

    def test_list(self):
        resp = self.client.get(
            self.url, HTTP_AUTHORIZATION='Bearer {}'.format(self.token)
        )

        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.content.decode('utf8'))['objects'][0]

        self._test_fields(resp_data)

    def test_url_to_object(self):
        new_obj = url_to_object(self.test_obj.detail_url)
        self.assertEqual(new_obj, self.test_obj)

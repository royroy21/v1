import json

from django.contrib.auth.models import User

from account.models import Account


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
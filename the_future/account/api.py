from restless.exceptions import BadRequest, NotFound
from restless.preparers import FieldsPreparer

from utils.generic_resources import GenericReadOnlyResource

from .forms import AccountCreateForm
from .models import Account


class AccountResource(GenericReadOnlyResource):
    model_cls = Account

    preparer = FieldsPreparer(fields={
        'self': 'detail_url',
        'username': 'user.username'
    })

    def is_authenticated(self):
        # TODO - this probably won't be good enough for UPDATE
        if self.request.method == 'POST':
            return True

        # if no account id in url then list method called
        try:
            account_id = self.request.path.split('/')[3]
        except IndexError:
            return self.request.user.is_authenticated()

        # users can only update or delete their own account
        account_obj = self.reference_object(account_id)
        user_is_updating_self = self.request.user.id == account_obj.user.id
        return (self.request.user.is_authenticated()
                and user_is_updating_self)

    def reference_object(self, pk):
        try:
            return self.model_cls.objects.get(id=pk, user__is_active=True)
        except self.model_cls.DoesNotExist:
            raise NotFound

    def create(self):
        form = AccountCreateForm(data=self.data)
        if form.is_valid():
            return form.save()
        raise BadRequest(form.errors.as_json())

    # TODO - create update form + logic
    def update(self, pk):
        pass

    def delete(self, pk):
        obj = self.reference_object(pk)
        obj.user.is_active = False
        obj.user.save()
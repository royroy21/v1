import factory

from account.factories import AccountFactory


class CommonFields(factory.django.DjangoModelFactory):
    created_by = factory.SubFactory(AccountFactory)
    modified_by = factory.SubFactory(AccountFactory)
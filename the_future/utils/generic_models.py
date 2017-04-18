from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone

from account.models import Account
from utils.model_functions import DetailURLMixin


class CommonFields(models.Model, DetailURLMixin):
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    # TODO - make these fields required + populate dynamically
    created_by = models.ForeignKey(Account, related_name='+',
                                   null=True, blank=True)
    modified_by = models.ForeignKey(Account, related_name='+',
                                    null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def detail_url(self):
        return self.get_detail_url()


class ModifierField(models.Model):
    """Used if an item has an affect on a hero
    """
    modifiers = JSONField(null=True, blank=True)

    class Meta:
        abstract = True


class MonetaryField(models.Model):
    """Used to determine value of an item
    """
    monetary_value = models.DecimalField(max_digits=7, decimal_places=0)

    class Meta:
        abstract = True
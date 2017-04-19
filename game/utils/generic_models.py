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
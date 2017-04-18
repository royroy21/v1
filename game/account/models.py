from django.contrib.auth.models import User

from django.db import models

from utils.model_functions import DetailURLMixin


class Account(models.Model, DetailURLMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def detail_url(self):
        return self.get_detail_url()

    def __str__(self):
        return self.user.username
from django.contrib.auth.models import User
from django import forms

from .models import Account


class AccountCreateForm(forms.ModelForm):
    username = forms.CharField(required=True)
    password_1 = forms.CharField(required=True)
    password_2 = forms.CharField(required=True)
    user = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()

        if self.data['password_1'] != self.data['password_2']:
            raise forms.ValidationError('passwords do not match')
        return cleaned_data

    def save(self, *args, **kwargs):
        user = User.objects.create_user(
            username=self.data['username'],
            password=self.data['password_1'],
        )
        self.instance.user = user
        return super().save(*args, **kwargs)

    class Meta:
        model = Account
        exclude = ('username', 'password', 'is_active')

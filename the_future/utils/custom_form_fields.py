from django import forms
from django.core.exceptions import ValidationError

from restless.exceptions import NotFound
from utils.url_to_object import url_to_object


class RelationshipUrlField(forms.CharField):
    def __init__(self, model_type=None, *args, **kwargs):
        self.model_type = model_type
        super(RelationshipUrlField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        resolved_object = None
        if value:
            try:
                resolved_object = url_to_object(value)
            except NotFound:
                raise ValidationError(
                    'The given URL could not be resolved to an object')

        return resolved_object

    def validate(self, value):
        super(RelationshipUrlField, self).validate(value)

        if value and self.model_type and not isinstance(value, self.model_type):
            raise ValidationError(
                'URL should resolve to an object of type {}'.format(
                    self.model_type
                ))


class RelationshipMultipleUrlField(RelationshipUrlField):

    def to_python(self, value):
        if not value:
            return []
        elif not isinstance(value, (list, tuple)):
            raise ValidationError('A list of URLs must be given')

        resolved = []
        for url in value:
            try:
                resolved.append(url_to_object(url))
            except NotFound:
                raise ValidationError(
                    'The given URL could not be resolved to an object')

        return resolved

    def validate(self, value):
        if self.required and not value:
            raise ValidationError(
                self.error_messages['required'], code='required')

        for instance in value:
            if self.model_type and not isinstance(instance, self.model_type):
                raise ValidationError(
                    'URLs should resolve to correct objects {}'.format(
                        self.model_type
                    ))
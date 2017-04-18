from restless.dj import DjangoResource
from restless.exceptions import BadRequest, NotFound


COMMON_PREPARE_FIELDS = {
    'self': 'detail_url',
    'created_by_url': 'created_by.detail_url',
    'modified_by_url': 'modified_by.detail_url',

    # TODO - isoformat causes 500
    # 'created': 'created.isoformat',

    'is_active': 'is_active'
}


class GenericReadOnlyResource(DjangoResource):
    factory_cls = None
    form_cls = None

    def is_authenticated(self):
        return self.request.user.is_authenticated()

    def list(self):
        return self.model_cls.objects.filter(is_active=True)

    def detail(self, pk):
        return self.model_cls.objects.get(id=pk, is_active=True)


class GenericCrudResource(GenericReadOnlyResource):

    def reference_object(self, pk):
        try:
            return self.model_cls.objects.get(id=pk, is_active=True)
        except self.model_cls.DoesNotExist:
            raise NotFound

    def create(self):
        form = self.form_cls(data=self.data)
        if form.is_valid():
            return form.save(user=self.request.user)
        raise BadRequest(form.errors.as_json())

    def update(self, pk):
        obj = self.reference_object(pk)
        form = self.form_cls(data=self.data, instance=obj)
        if form.is_valid():
            return form.save(user=self.request.user)
        raise BadRequest(form.errors.as_json())

    def delete(self, pk):
        obj = self.reference_object(pk)
        obj.is_active = False
        obj.save()
from django.contrib.contenttypes.models import ContentType


def url_to_object(obj_url):
    _, _, slug, id, *_ = obj_url.split('/')

    ct = ContentType.objects.get(model=slug.replace('-', '').lower())
    return ct.model_class().objects.get(id=id)
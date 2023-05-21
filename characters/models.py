import uuid

from django.db import models
from django.utils.deconstruct import deconstructible


@deconstructible
class RandomFileName:
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        extension = filename.split('.')[-1]
        filename = f'{uuid.uuid4()}.{extension}'
        return self.path + filename


class Collection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    csv_file = models.FileField(upload_to=RandomFileName('characters/'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.created_at.strftime("%B %d, %Y, %H:%M %p")
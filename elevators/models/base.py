import datetime
import uuid
from django.db import models


class BaseModelMixin(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    meta = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        self.updated_on = datetime.datetime.now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True

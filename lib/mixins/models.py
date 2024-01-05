from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils import timezone

NULL = {"null": True, "blank": True}


class BaseModelMixin(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    created_at = models.DateTimeField(default=timezone.localtime, editable=False)
    updated_at = models.DateTimeField(**NULL)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        related_name="%(app_label)s_%(model_name)s_created_by",
        editable=False,
        **NULL,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        related_name="%(app_label)s_%(model_name)s_updated_by",
        **NULL,
    )
    search_fields = ()

    class Meta:
        abstract = True
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.updated_at = timezone.localtime()
        return super().save(*args, **kwargs)

    @classmethod
    def get_searchable_fields(cls):
        _fields = []
        for field in cls._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                _fields.append(field.name)

        return _fields

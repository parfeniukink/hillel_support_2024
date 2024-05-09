from django.db import models


class TimestampMixin(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
from django.db import models


class Issue(models.Model):
    junior_id = models.IntegerField()
    senior_id = models.IntegerField()
    title = models.CharField(max_length=100)
    body = models.TextField()

    def __repr__(self) -> str:
        return f"Issue[{self.pk} {self.title[:10]}]"

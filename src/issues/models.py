from django.db import models
from django.db.models import Q
from users.models import User
from shared.django import TimestampMixin

# from enum import IntEnum
# class IssueStatusChoices(IntEnum):
#     OPENED = 1
#     IN_PROGRESS = 2

#     def choices(cls): ...

ISSUE_STATUS_CHOICES = (
    (1, "Opened"),
    (2, "In progress"),
    (3, "Closed"),
)


class IssuesManager(models.Manager):
    def filter_by_participant(self, user: User):
        return self.filter(Q(junior=user) | Q(senior=user))


class Issue(TimestampMixin):
    title = models.CharField(max_length=100)
    body = models.TextField(null=True)
    status = models.PositiveSmallIntegerField(choices=ISSUE_STATUS_CHOICES)

    junior = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="junior_issues",
    )
    senior = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="senior_issues",
        null=True,
    )

    objects = IssuesManager()

    def __repr__(self) -> str:
        return f"Issue[{self.pk} {self.title[:10]}]"

    def __str__(self) -> str:
        return self.title[:10]


# first_issue: Issue | None = Issue.objects.first()
# instance: Issue = Issue.objects.get(id=1)
# issue: Issue = Issue.objects.get(id=1)
# issue.title
# issue.status
# issue.junior.password
# issue.message_set


class Message(models.Model):
    # class Meta:
    #     db_table = "messages"

    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)

    # update on any update in the column
    # updated_at = models.DateTimeField(auto_now=True)

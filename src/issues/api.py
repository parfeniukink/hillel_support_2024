from django.db.models import Q
from rest_framework import generics, response, serializers
from rest_framework.decorators import api_view
from rest_framework.request import Request
from users.enums import Role

from .enums import Status
from .models import Issue, Message


class IssueSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(required=False)
    junior = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Issue
        # fields = ["id", "title", "body", "junior_id"]
        # exclude = ["id"]
        fields = "__all__"

    def validate(self, attrs):
        attrs["status"] = Status.OPENED
        return attrs

    def get(self, request, *args, **kwargs):
        """Get issues from the database."""
        return super().get(request, *args, **kwargs)


class IssuesAPI(generics.ListCreateAPIView):
    http_method_names = ["get", "post"]
    serializer_class = IssueSerializer

    def get_queryset(self):
        if self.request.user.role == Role.JUNIOR:
            return Issue.objects.filter(junior=self.request.user)
        elif self.request.user.role == Role.SENIOR:
            return Issue.objects.filter(
                Q(senior=self.request.user)
                | (Q(senior=None) & Q(status=Status.OPENED))
            )
        else:
            return Issue.objects.all()

    def post(self, request):
        if request.user.role == Role.SENIOR:
            raise Exception("The role is Senior")

        return super().post(request)


class IssuesRetrieveUpdateDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "put", "patch", "delete"]
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()
    lookup_url_kwarg = "id"


# Old example
# ====================================================
# class MessagesCreateAPI(generics.CreateAPIView):
#     serializer_class = MessageSerializer

# class MessagesListAPI(generics.RetrieveAPIView):
#     lookup_url_kwarg = "id"
#     serializer_class = MessageSerializer


#     def get_queryset(self):

#         return Message.objects.filter(issue__id=self.request)

# HTTP POST /issues/messages
#   {
#       "body": "text",
#       "issue": 13
#   }

# HTTP GET /issues/13/messages
# => []
# ======================================================


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    issue = serializers.PrimaryKeyRelatedField(queryset=Issue.objects.all())

    class Meta:
        model = Message
        fields = "__all__"

    def save(self):
        if (user := self.validated_data.pop("user", None)) is not None:
            self.validated_data["user_id"] = user.id

        if (issue := self.validated_data.pop("issue", None)) is not None:
            self.validated_data["issue_id"] = issue.id

        return super().save()


@api_view(["GET", "POST"])
def messages_api_dispatcher(request: Request, issue_id: int):
    if request.method == "GET":
        # messages = Message.objects.filter(
        #     Q(
        #         issue__id=issue_id,
        #         issue__junior=request.user,
        #     )
        #     | Q(
        #         issue__id=issue_id,
        #         issue__senior=request.user,
        #     )
        # ).order_by("timestamp")
        messages = Message.objects.filter(
            Q(
                issue__id=issue_id,
            )
            & (
                Q(
                    issue__senior=request.user,
                )
                | Q(
                    issue__junior=request.user,
                )
            )
        ).order_by("-timestamp")
        serializer = MessageSerializer(messages, many=True)

        return response.Response(serializer.data)
    else:
        issue = Issue.objects.get(id=issue_id)
        payload = request.data | {"issue": issue.id}
        serializer = MessageSerializer(
            data=payload, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(serializer.validated_data)


# HTTP PUT /issues/13/close

# HTTP PUT /issues/13
# request.body = {"status": "CLOSED"}

# class UserRelatedToIssue(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         ...


@api_view(["PUT"])
# @permission_classes([UserRelatedToIssue])
def issues_close(request: Request, id: int):
    issue = Issue.objects.update(id=id, status=Status.CLOSED)
    serializer = IssueSerializer(issue)

    return response.Response(serializer.data)


@api_view(["PUT"])
def issues_take(request: Request, id: int):
    issue = Issue.objects.get(id=id)

    if request.user.role != Role.SENIOR:
        raise PermissionError("Only senior users can take issues")

    if (issue.status != Status.OPENED) or (issue.senior is not None):
        return response.Response(
            {"message": "Issue is not Opened or senior is set..."},
            status=422,
        )
    else:
        issue.senior = request.user
        issue.status = Status.IN_PROGRESS
        issue.save()

    serializer = IssueSerializer(issue)

    return response.Response(serializer.data)

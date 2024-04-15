from django.db.models import Q
from rest_framework import generics, response, serializers
from rest_framework.decorators import api_view, permission_classes
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


class IssuesAPI(generics.ListCreateAPIView):
    http_method_names = ["get", "post"]
    serializer_class = IssueSerializer

    def get_queryset(self):
        # TODO: Separate for each role
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


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    issue = serializers.PrimaryKeyRelatedField(queryset=Issue.objects.all())

    class Meta:
        model = Message
        fields = "__all__"


# how to add the message from url params???
# class MessagesAPI(generics.ListCreateAPIView):
#     http_method_names = ["get", "post"]
#     serializer_class = MessageSerializer

#     def get_queryset(self):
#         return Message.objects.all()

#     def post(self, request, issue_id: int):
#         breakpoint()
#         return super().post(request)


# Permissions class
# class UserRelatedToIssuePermission:
#     def has_object_permission(self, request, view, obj):
#         raise NotImplementedError
#         # return obj.junior == request.user or obj.senior == request.user

#     def has_permission(self, request, view):
#         return True


@api_view(["GET", "POST"])
# @permission_classes([UserRelatedToIssuePermission])
def messages_api_dispatcher(request, issue_id: int):
    if request.method == "GET":
        messages = Message.objects.filter(issue_id=issue_id).order_by(
            "-timestamp"
        )
        serializer = MessageSerializer(messages, many=True)

        return response.Response(serializer.data)

    else:
        # or add more validations
        issue = Issue.objects.get(id=issue_id)
        payload = request.data | {"issue": issue.id}
        serializer = MessageSerializer(
            data=payload, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(serializer.data)


@api_view(["PUT"])
# @permission_classes([UserRelatedToIssuePermission])
def close_issue(request, id: int):
    issue = Issue.objects.update(id=id, status=Status.CLOSED)
    serializer = IssueSerializer(issue)

    return response.Response(serializer.data)

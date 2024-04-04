import json

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from issues.models import Issue


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        # fields = ["id", "title", "body", "junior_id"]
        # exclude = ["id"]
        fields = "__all__"



@api_view()
def get_issues(request) -> Response:
    issues = Issue.objects.all()
    results = [IssueSerializer(issue).data for issue in issues]

    return Response(data={"results": results})


@api_view()
def retrieve_issue(request, issue_id: int) -> Response:
    instance = get_object_or_404(Issue, id=issue_id)
    # try:
    #     instance = Issue.objects.get(id=issue_id)
    # except Issue.DoesNotExist:
    #     raise Http404

    return Response(data={"result": IssueSerializer(instance).data})


@api_view(["POST"])
def create_issue(request) -> Response:
    try:
        payload: dict = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        raise Exception("Request Body is invalid ")

    serializer = IssueSerializer(data=payload)
    serializer.is_valid(raise_exception=True)

    issue = Issue.objects.create(**serializer.validated_data)

    return Response(data=IssueSerializer(issue).data)

    # issues = Issue.objects.all()
    # results = [IssueSerializer(issue).data for issue in issues]

    return Response(data={"results": results})

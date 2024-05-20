from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from issues.api import (
    IssuesAPI,
    IssuesRetrieveUpdateDeleteAPI,
    issues_close,
    issues_take,
    messages_api_dispatcher,
)
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView  # noqa
from rest_framework_simplejwt.views import token_obtain_pair  # noqa
from users.api import UserListCreateAPI, resend_activation_mail, foo

# HTTP GET /issues
# HTTP POST /issues
# HTTP GET /issues/ID
# HTTP PUT /issues/ID
# HTTP PATCH /issues/ID
# HTTP DELETE /issues/ID

# HTTP PUT /issues/ID/close


schema_view = get_schema_view(
    openapi.Info(
        title="Hillel Support APi",
        default_version="v1",
        description=(
            "The Backend API that allows you to "
            "interact with Support Core"
        ),
        contact=openapi.Contact(email="support.support@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("foo/", foo),

    # admin
    path("admin/", admin.site.urls),
    # users
    path("users/", UserListCreateAPI.as_view()),
    path("users/activation/resendActivation", resend_activation_mail),
    # issues
    path("issues/", IssuesAPI.as_view()),
    path("issues/<int:id>", IssuesRetrieveUpdateDeleteAPI.as_view()),
    path("issues/<int:id>/close", issues_close),
    path("issues/<int:id>/take", issues_take),
    # messages
    path("issues/<int:issue_id>/messages", messages_api_dispatcher),
    # Authentication
    # path("auth/token/", token_obtain_pair),
    path("auth/token/", TokenObtainPairView.as_view()),
    path(
        "swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]

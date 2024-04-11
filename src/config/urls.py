from django.contrib import admin
from django.urls import path
from issues.api import IssuesAPI, IssuesRetrieveUpdateDeleteAPI
from rest_framework_simplejwt.views import TokenObtainPairView  # noqa
from rest_framework_simplejwt.views import token_obtain_pair  # noqa
from users.api import UserListCreateAPI

# HTTP GET /issues
# HTTP POST /issues
# HTTP GET /issues/ID
# HTTP PUT /issues/ID
# HTTP PATCH /issues/ID
# HTTP DELETE /issues/ID

# HTTP PUT /issues/ID/close


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", UserListCreateAPI.as_view()),
    path("issues/", IssuesAPI.as_view()),
    path("issues/<int:id>", IssuesRetrieveUpdateDeleteAPI.as_view()),
    # Authentication
    # path("auth/token/", token_obtain_pair),
    path("auth/token/", TokenObtainPairView.as_view()),
]

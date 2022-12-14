from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from dj_rest_auth.jwt_auth import JWTCookieAuthentication

schema_view_param = {
    "public": True,
    # 'permission_classes': (permissions.IsAdminUser,),
    "url": getattr(settings, "SWAGGER_URL", None),
    "authentication_classes": (SessionAuthentication, JWTCookieAuthentication),
}

schema_view = get_schema_view(
    openapi.Info(
        title=" API",
        default_version="v1",
        description="Microservice description",
    ),
    **schema_view_param,
)

urlpatterns = [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

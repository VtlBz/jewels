from django.urls import include, path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from api.v1.views import DealsViewSet

router_v1 = DefaultRouter()

router_v1.register(
    'deals',
    DealsViewSet,
    basename='deals'
)

schema_view = get_schema_view(
    openapi.Info(
        title='Jewels Project API',
        default_version='v1',
        description='API documentation for Jewels project',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email='webmaster@vtlbz.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('', include(router_v1.urls)),
]

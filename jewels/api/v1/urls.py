from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import DealsViewSet, TopViewSet

router_v1 = DefaultRouter()

router_v1.register(
    'deals',
    DealsViewSet,
    basename='deals'
)

router_v1.register(
    'top',
    TopViewSet,
    basename='top'
)

urlpatterns = [
    path('', include(router_v1.urls)),
]

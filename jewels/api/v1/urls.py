from django.urls import include, path
from django.views.generic import TemplateView

from rest_framework.routers import DefaultRouter

from api.v1.views import DealsViewSet

router_v1 = DefaultRouter()

router_v1.register(
    'deals',
    DealsViewSet,
    basename='deals'
)

urlpatterns = [
    path('swagger/', TemplateView.as_view(
        template_name='swagger.html',
    ), name='swagger'),
    path('', include(router_v1.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TradeReportViewSet

router = DefaultRouter()
router.register(r'trade-reports', TradeReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

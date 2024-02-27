from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet, CollectViewSet, ReasonViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)
router.register(r'collects', CollectViewSet)
router.register(r'reasons', ReasonViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

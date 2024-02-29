from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet, CollectViewSet, ReasonViewSet

router = DefaultRouter()
router.register('payments', PaymentViewSet)
router.register('collects', CollectViewSet)
router.register('reasons', ReasonViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

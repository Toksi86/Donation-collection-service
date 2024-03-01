from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet, CollectViewSet, ReasonViewSet, RegisterView, LoginView

router = DefaultRouter()
router.register('payments', PaymentViewSet)
router.register('collects', CollectViewSet)
router.register('reasons', ReasonViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]

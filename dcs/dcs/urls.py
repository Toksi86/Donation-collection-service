from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

urlpatterns = [
    path('', include('donation_app.urls')),
    path('admin/', admin.site.urls),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Donation-collection API",
        default_version='v1',
        description="Документация для приложения dcs проекта Donation collection",
        # terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="test@test.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
)

urlpatterns += [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

from django.core.cache import cache
from django.db.models import Sum, Count
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Payment, Collect, Reason
from .serializers import PaymentSerializer, ReasonSerializer, CollectSerializer


class CacheMixin:
    def get_cached_data(self, cache_key, cache_time):
        cache_list = cache.get(cache_key)
        if cache_list:
            return cache_list

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        cache.set(cache_key, serializer.data, cache_time)
        return serializer.data


class PaymentViewSet(CacheMixin, viewsets.ModelViewSet):
    cache_key = 'payment-view'
    cache_time = 60 * 5
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    http_method_names = ['get', 'post', 'delete']

    def list(self, request, *args, **kwargs):
        return Response(self.get_cached_data(self.cache_key, self.cache_time), status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            cache.delete(self.cache_key)
        return response


class CollectViewSet(CacheMixin, viewsets.ModelViewSet):
    cache_key = 'collect-view'
    cache_time = 60 * 5
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    http_method_names = ['get', 'post', 'delete']

    def list(self, request, *args, **kwargs):
        cache_list = cache.get(self.cache_key)
        if cache_list:
            return Response(cache_list, status=status.HTTP_200_OK)

        response = super().list(request, *args, **kwargs)
        cache.set(self.cache_key, response.data, self.cache_time)
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            cache.delete(self.cache_key)
        return response

    def get_queryset(self):
        return Collect.objects.annotate(
            collected_amount=Sum('payments__amount'),
            contributors_count=Count('payments'),
        )

    @action(detail=True, methods=['get'])
    def payments_by_collect(self, request, pk=None):
        """Показывает все платежи одного конкретного сбора"""

        if pk is None:
            return Response({"error": "collect_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        payments = Payment.objects.filter(collect_id=pk)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)


class ReasonViewSet(viewsets.ModelViewSet):
    queryset = Reason.objects.all()
    http_method_names = ['get', 'post', 'delete']
    serializer_class = ReasonSerializer

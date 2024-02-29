from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Payment, Collect, Reason
from .serializers import PaymentSerializer, ListCollectSerializer, CreateCollectSerializer, ReasonSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    cache_key = 'payment-view'
    cache_time = 60 * 5
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    http_method_names = ['get', 'post', 'delete']

    def list(self, request, *args, **kwargs):
        cache_list = cache.get(self.cache_key)
        if cache_list:
            return Response(cache_list, status=status.HTTP_200_OK)
        else:
            response = super().list(request, *args, **kwargs)
            cache.set(self.cache_key, response.data, self.cache_time)
            return response

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            collect_id = serializer.validated_data.get('collect').id
            collect = Collect.objects.get(id=collect_id)
            payment = Payment.objects.create(**serializer.validated_data)
            payment.collect = collect
            collect.contributors_count += 1
            collect.collected_amount += payment.amount
            collect.save()
            payment.save()
            cache.delete(self.cache_key)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollectViewSet(viewsets.ModelViewSet):
    cache_key = 'collect-view'
    cache_time = 60 * 5
    queryset = Collect.objects.all()
    http_method_names = ['get', 'post', 'delete']

    def list(self, request, *args, **kwargs):
        cache_list = cache.get(self.cache_key)
        if cache_list:
            return Response(cache_list, status=status.HTTP_200_OK)
        else:
            response = super().list(request, *args, **kwargs)
            cache.set(self.cache_key, response.data, self.cache_time)
            return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            cache.delete(self.cache_key)
        return response

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListCollectSerializer
        elif self.request.method == 'POST':
            return CreateCollectSerializer
        return super().get_serializer_class()

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

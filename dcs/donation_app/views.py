from django.core.cache import cache
from django.core.mail import EmailMessage
from django.db.models import Sum, Count
from rest_framework import generics, permissions, viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Payment, Collect, Reason
from .permissions import IsAuthenticatedOrReadOnly
from .serializers import PaymentSerializer, ReasonSerializer, CollectSerializer, \
    UserSerializer, LoginSerializer


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
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        return Response(self.get_cached_data(self.cache_key, self.cache_time), status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            cache.delete(self.cache_key)
            self.send_confirmation_email(request)
        return response

    @staticmethod
    def send_confirmation_email(request):
        email = EmailMessage(
            'Успешное пожертвование',
            f'Вы успешно создали пожертвование.',
            'dcs@example.com',
            [request.user.email],
        )
        email.send()


class CollectViewSet(CacheMixin, viewsets.ModelViewSet):
    cache_key = 'collect-view'
    cache_time = 60 * 5
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        return Response(self.get_cached_data(self.cache_key, self.cache_time), status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        request.data['author'] = request.user.id
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            cache.delete(self.cache_key)
            self.send_confirmation_email(request)
        return response

    def get_queryset(self):
        return Collect.objects.annotate(
            collected_amount=Sum('payments__amount'),
            contributors_count=Count('payments'),
        )

    @action(detail=True, methods=['get'])
    def payments_by_collect(self, request, pk=None):
        if pk is None:
            return Response({"error": "collect_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        payments = Payment.objects.filter(collect_id=pk)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    @staticmethod
    def send_confirmation_email(request):
        email = EmailMessage(
            'Успешное создание сбора',
            f'Вы успешно создали сбор с заголовком {request.data['title']}.',
            'dcs@example.com',
            [request.user.email],
        )
        email.send()


class ReasonViewSet(viewsets.ModelViewSet):
    queryset = Reason.objects.all()
    http_method_names = ['get', 'post', 'delete']
    serializer_class = ReasonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)

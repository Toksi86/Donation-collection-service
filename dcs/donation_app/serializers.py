from rest_framework import serializers

from .models import Payment, Collect, Reason


# Разное отображение данных на Post и Get запросы
class ListCollectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collect
        fields = ('id', 'author', 'title', 'reason', 'planned_amount',
                  'collected_amount', 'contributors_count', 'end_date'
                  )


class CreateCollectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collect
        fields = ('id', 'author', 'title', 'reason', 'planned_amount', 'end_date')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'user', 'title', 'description', 'amount', 'collect')


class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ('id', 'title')

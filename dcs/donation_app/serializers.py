from rest_framework import serializers

from .models import Payment, Collect, Reason


# Разное отображение данных на Post и Get запросы
class CollectSerializer(serializers.ModelSerializer):
    collected_amount = serializers.DecimalField(max_digits=18, decimal_places=2, read_only=True)
    contributors_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Collect
        fields = (
            'id', 'author', 'title', 'reason', 'planned_amount', 'collected_amount', 'contributors_count', 'end_date'
        )


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'user', 'title', 'description', 'amount', 'collect')


class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ('id', 'title')

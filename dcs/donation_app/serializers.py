from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Payment, Collect, Reason

User = get_user_model()


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return {'user': user}
        raise serializers.ValidationError("Incorrect Credentials")

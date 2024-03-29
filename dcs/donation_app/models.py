from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Reason(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Причина"
        verbose_name_plural = "Причины"


class Collect(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_collects')
    title = models.CharField(max_length=255, blank=False, null=False)
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE, null=False, blank=False, related_name='collects')
    description = models.TextField(blank=False, null=False)
    planned_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    cover_image = models.ImageField(upload_to='collect_covers/', blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Сбор"
        verbose_name_plural = "Сборы"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_payments')
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    amount = models.DecimalField(max_digits=18, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    timestamp = models.DateTimeField(auto_now_add=True)
    collect = models.ForeignKey(Collect, on_delete=models.CASCADE, related_name='payments')

    def __str__(self):
        return f'{self.amount} от {self.user.username} для {self.collect.title}'

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

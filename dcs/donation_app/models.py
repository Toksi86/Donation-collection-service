from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()

SET_OF_REASONS = (
    ('birthday', 'День рождения'),
    ('wedding', 'Свадьба'),
    ('treatment', 'Лечение'),
)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False)
    amount = models.DecimalField(max_digits=18, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    timestamp = models.DateTimeField(auto_now_add=True)
    collect = models.ForeignKey('Collect', on_delete=models.CASCADE, related_name='payments')

    def __str__(self):
        return f'{self.amount} от {self.user.username} для {self.collect.title}'


class Collect(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, null=False)
    reason = models.CharField(max_length=255, choices=SET_OF_REASONS)
    description = models.TextField(blank=False, null=False)
    planned_amount = models.DecimalField(max_digits=18, decimal_places=2)
    collected_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0.0)
    contributors_count = models.IntegerField(default=0)
    cover_image = models.ImageField(upload_to='collect_covers/', blank=True, null=True)
    end_date = models.DateTimeField()
    donations = models.ManyToManyField(Payment, through='Donation', related_name='collects')

    def __str__(self):
        return f'{self.title}'


class Donation(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    collect = models.ForeignKey(Collect, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    date = models.DateTimeField()
    donor = models.ForeignKey(User, on_delete=models.CASCADE)

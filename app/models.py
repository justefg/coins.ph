from enum import Enum
from django.db import models
import uuid


class Account(models.Model):
    name = models.CharField(max_length=10, primary_key=True, unique=True)
    email = models.CharField(max_length=30)


class TransactionStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Payment(models.Model):
    id = models.BigAutoField(primary_key=True)
    source = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='src')
    destination = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='dest')
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    status = models.CharField(max_length=10, default=TransactionStatus.PENDING,
                              choices=TransactionStatus.choices())
    memo = models.CharField(max_length=30)

    class Meta:
        indexes = [models.Index(fields=['source',]),
                   models.Index(fields=['destination',]),
                    ]

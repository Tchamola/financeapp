from datetime import datetime

from django.db import models
from django.utils import timezone

# Create your models here.


class Account(models.Model):
    name = models.CharField(max_length=100)
    expense = models.FloatField(default=0)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    expense_list = models.ManyToManyField('Expense', blank=True)

    def __str__(self):
        return self.user


class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField(default=0)
    date = models.DateField(null=False, default=timezone.now)
    long_term = models.BooleanField(default=False)
    interest_rate = models.FloatField(default=0, null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    monthly_expense = models.FloatField(default=0, null=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        if self.long_term:
            self.monthly_expense = self.calculate_monthly_expense
            super().save(*args, **kwargs)


    def calculate_monthly_expense(self):
        if self.long_term:
            if self.interest_rate == 0:
                return self.amount / ((self.end_date - self.date) / 30)
            else:
                month = (self.end_date.year - datetime.now().year) * 12 + (self.end_date.month - datetime.now().month)
                monthly_rate = self.interest_rate / 100 / 12
                monthly_expense = (self.amount * monthly_rate) / (1 - (1 + monthly_rate) ** (-month))
        else:
            return self.monthly_expense






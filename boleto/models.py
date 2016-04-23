# coding: utf-8

from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class NameBaseModel(BaseModel):
    name = models.CharField(max_length=60)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Bank(NameBaseModel):
    pass


class Account(NameBaseModel):
    bank = models.ForeignKey(Bank)
    user = models.ForeignKey(User)

    @property
    def spent(self):
        return sum([payment.bill.total_value_without_user for payment in self.payments.all()])


class Benefited(NameBaseModel):
    extra_info = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    @property
    def received(self):
        return sum([bill.total_value for bill in self.bills.all() if bill.paid])


class Bill(NameBaseModel):
    due_date = models.DateField()
    benefited = models.ForeignKey(Benefited, related_name='bills')

    @property
    def total_value(self):
        return sum([item.value * item.amount for item in self.items.all()])

    @property
    def total_value_without_user(self):
        return sum([item.value * item.amount for item in self.items.all() if not item.user])

    @property
    def paid(self):
        return bool(self.payments.all())

    def __str__(self):
        return '{} - {} - {}'.format(self.name, self.due_date, self.benefited)


class Payment(BaseModel):
    bill = models.ForeignKey(Bill, blank=True, null=True, related_name='payments')
    date = models.DateField()
    paid_account = models.ForeignKey(Account, related_name='payments')

    @property
    def total_value(self):
        return sum([item.value * item.amount for item in self.bill.items.all()])

    def __str__(self):
        return 'Payment: {}'.format(self.bill)


class Item(NameBaseModel):
    bill = models.ForeignKey(Bill, related_name='items')
    value = models.DecimalField(max_digits=12, decimal_places=2)
    amount = models.PositiveSmallIntegerField(default=1)
    user = models.ForeignKey(User, blank=True, null=True)
    extra_info = models.TextField(blank=True, null=True)

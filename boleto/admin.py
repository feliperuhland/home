# coding: utf-8

from django.contrib import admin

from core.models import (
    Account,
    Bank,
    Benefited,
    Bill,
    Item,
    Payment,
)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'bank', 'user', 'created', 'modified')


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified')


class ItemInline(admin.TabularInline):
    model = Item
    extra = 1


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    def _paid(self, obj):
        return obj.paid

    _paid.boolean = True
    list_display = ('name', 'total_value', 'due_date', 'benefited', '_paid', 'created', 'modified')
    inlines = [ItemInline]


@admin.register(Benefited)
class BenefitedAdmin(admin.ModelAdmin):
    list_display = ('name', 'received', 'created', 'modified')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('bill', 'paid_account', 'date', 'created', 'modified')

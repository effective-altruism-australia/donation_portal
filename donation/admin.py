from django.contrib import admin
from models import Pledge, BankTransaction, Reconciliation

from reversion.admin import VersionAdmin
# Register your models here.


class PledgeAdmin(VersionAdmin):
    search_fields = ('first_name', 'last_name')
    class Meta:
        model = BankTransaction


class BankTransactionAdmin(VersionAdmin):
    # TODO make a filter for needs_to_be_reconciled transactions
    # https://docs.djangoproject.com/en/1.8/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter

    readonly_fields = ('date', 'amount', 'bank_statement_text', 'needs_to_be_reconciled')
    class Meta:
        model = BankTransaction
    fieldsets = (
        ("Bank Transaction", {
            'fields': ('date',
                       'amount',
                       'bank_statement_text',
                       'reference',
                       'needs_to_be_reconciled',
                       )
            }),
        ("Do not reconcile", {
            'fields': ('its_a_transfer_not_a_donation',
                       )
            }),
    )

admin.site.register(Pledge, PledgeAdmin)
admin.site.register(BankTransaction, BankTransactionAdmin)


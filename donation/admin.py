from __future__ import unicode_literals

from django.contrib import admin
from django.contrib import messages

from reversion.admin import VersionAdmin

from .models import Pledge, BankTransaction, Receipt, PartnerCharity, XeroReconciledDate, PaymentMethod


class BankTransactionReconciliationListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'reconciliation'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'reconciliation'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('Unreconciled', 'Unreconciled'),
            ('Reconciled', 'Reconciled'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if not self.value():
            return BankTransaction.objects.all()
        unreconciled = BankTransaction.objects.filter(pledge__isnull=True, do_not_reconcile=False)
        if self.value() == 'Unreconciled':
            return unreconciled
        else:  # 'Reconciled'
            return BankTransaction.objects.all().exclude(id__in=unreconciled.values('id'))


class PledgeFundsReceivedFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'funds received'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'funds_received'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('Yes', 'Received'),
            ('No', 'Not Received'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if not self.value():
            return Pledge.objects.all()
        # Only payments by bank transfer can be unpaid.
        paid_pledges_by_bank_transfer = BankTransaction.objects.filter(pledge__isnull=False).values_list('pledge__id', flat=True)
        unpaid = Pledge.objects.filter(payment_method=PaymentMethod.BANK).exclude(id__in=paid_pledges_by_bank_transfer)
        if self.value() == 'No':
            return unpaid
        else:  # 'No'
            return Pledge.objects.all().exclude(id__in=unpaid.values('id'))


class PledgeAdmin(VersionAdmin):
    search_fields = ('first_name', 'last_name', 'reference', 'email')
    readonly_fields = ('ip', 'completed_time')
    list_filter = (PledgeFundsReceivedFilter, )

    class Meta:
        model = Pledge


# TODO We're not really using this as an Inline and it has confusing presentation. Better to create our own widget.
class ReceiptInline(admin.TabularInline):
    readonly_fields = ('status',)
    model = Receipt
    extra = 0
    fields = ('status',)
    can_delete = False

    def has_add_permission(self, request):
        return False


class BankTransactionAdmin(VersionAdmin):
    # TODO make a filter for needs_to_be_reconciled transactions
    # https://docs.djangoproject.com/en/1.8/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter

    search_fields = ('bank_statement_text', )
    readonly_fields = ('date', 'amount', 'bank_statement_text', 'reconciled', 'pledge')
    list_filter = (BankTransactionReconciliationListFilter, )
    inlines = (ReceiptInline, )

    class Meta:
        model = BankTransaction

    fieldsets = (
        ("Bank Transaction", {
            'fields': ('date',
                       'amount',
                       'bank_statement_text',
                       'reference',
                       'reconciled',
                       'pledge',
                       )
        }),
        ("Do not reconcile", {
            'fields': ('do_not_reconcile',
                       )
        }),
    )

    def resend_receipts(self, request, queryset):
        bank_transactions = list(queryset.all())
        if len(bank_transactions) > 8:
            self.message_user(request, "Please select at most 8 transactions at once.", level=messages.WARNING)
            return

        for bank_transaction in bank_transactions:
            any_receipts_sent = False
            try:
                bank_transaction.resend_receipt()
                any_receipts_sent = True
            except BankTransaction.NotReconciledException:
                self.message_user(request, "Cannot send receipts for unreconciled transactions.", level=messages.ERROR)
        if any_receipts_sent:
            self.message_user(request, "Additional receipts sent.")

    resend_receipts.short_description = "Resend receipts for selected transactions"

    actions = ['resend_receipts']


class ReceiptAdmin(VersionAdmin):
    readonly_fields = ('status',)
    fields = ('status',)
    actions = ['send_receipts', ]


admin.site.register(Pledge, PledgeAdmin)
admin.site.register(BankTransaction, BankTransactionAdmin)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(PartnerCharity, VersionAdmin)
admin.site.register(XeroReconciledDate)

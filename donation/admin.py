from django.contrib import admin
from models import Pledge, BankTransaction, Receipt

from reversion.admin import VersionAdmin
# Register your models here.


class PledgeAdmin(VersionAdmin):
    search_fields = ('first_name', 'last_name', 'reference')
    readonly_fields = ('ip', 'completed_time')

    # TODO make recipient_org, frequency etc. have choices not be free text
    class Meta:
        model = BankTransaction


# TODO We're not really using this as an Inline and it has confusing presentation. Better to create our own widget.
class ReceiptInline(admin.TabularInline):
    readonly_fields = ('status', )
    model = Receipt
    extra = 0
    fields = ('status', )
    can_delete = False

    def has_add_permission(self, request):
        return False


class BankTransactionAdmin(VersionAdmin):
    # TODO make a filter for needs_to_be_reconciled transactions
    # https://docs.djangoproject.com/en/1.8/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter

    readonly_fields = ('date', 'amount', 'bank_statement_text', 'reconciled', 'pledge')
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
            'fields': ('its_not_a_donation',
                       )
            }),
    )

    def resend_receipts(self, request, queryset):
        for bank_transaction in queryset.all():
            bank_transaction.resend_receipt()
        self.message_user(request, "Additional receipts sent.")
    resend_receipts.short_description = "Resend receipts for selected transactions"

    actions = ['resend_receipts']


class ReceiptAdmin(VersionAdmin):
    def send_receipts(self, request, queryset):
        for receipt in queryset.filter(time_sent__isnull=True).all():
            receipt.send()
        self.message_user(request, "Selected receipts sent.")
    send_receipts.short_description = "Send receipts now"

    readonly_fields = ('status', )
    fields = ('status', )
    actions = ['send_receipts', ]

admin.site.register(Pledge, PledgeAdmin)
admin.site.register(BankTransaction, BankTransactionAdmin)
admin.site.register(Receipt, ReceiptAdmin)

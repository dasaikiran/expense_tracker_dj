from django.contrib import admin

from .models import CurrentBalance, TrackingHistory

# Register your models here.

admin.site.register(CurrentBalance)


class TrackingHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "amount",
        "description",
        "current_balance",
        "expense_type",
        "created_at",
    )


admin.site.register(TrackingHistory, TrackingHistoryAdmin)

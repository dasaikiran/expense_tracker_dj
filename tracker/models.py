from django.db import models

# Create your models here.


class CurrentBalance(models.Model):
    current_balance = models.FloatField(default=0)

    def __str__(self):
        return f"{self.current_balance}"


class TrackingHistory(models.Model):
    current_balance = models.ForeignKey(CurrentBalance, on_delete=models.CASCADE)
    amount = models.FloatField()
    description = models.CharField(max_length=200)
    expense_type = models.CharField(
        choices=(("CREDIT", "CREDIT"), ("DEBIT", "DEBIT")), max_length=200
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"the amount {self.amount} for {self.description} of expense_type {self.expense_type}"

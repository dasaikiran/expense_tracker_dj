from django.shortcuts import render, redirect
from .models import TrackingHistory, CurrentBalance
# Create your views here.


def index(request):

    if request.method == "POST":
        amount = request.POST.get("amount")
        description = request.POST.get("description")

        balance, _ = CurrentBalance.objects.get_or_create(id=1)

        expense_type = "CREDIT"

        if float(amount) < 0:
            expense_type = "DEBIT"

        transaction = TrackingHistory.objects.create(
            amount=float(amount),
            description=description,
            expense_type=expense_type,
            current_balance=balance,
        )
        balance.current_balance += transaction.amount
        balance.save()

        print(amount, description)

        return redirect("index")

    balance, _ = CurrentBalance.objects.get_or_create(id=1)
    income = 0
    expense = 0

    for transaction in TrackingHistory.objects.all():
        if transaction.expense_type == "CREDIT":
            income += transaction.amount
        else:
            expense += transaction.amount

    context = {
        "income": income,
        "expense": expense,
        "current_balance": balance,
        "transactions": TrackingHistory.objects.all(),
    }
    return render(request, "index.html", context=context)


def delete_transaction(request, id):
    transaction = TrackingHistory.objects.filter(id=id)
    if transaction.exists():
        balance = transaction[0].current_balance
        if transaction[0].expense_type == "CREDIT":
            balance.current_balance -= abs(transaction[0].amount)
        elif transaction[0].expense_type == "DEBIT":
            balance.current_balance += abs(transaction[0].amount)
        balance.save()
        transaction.delete()
    return redirect("index")

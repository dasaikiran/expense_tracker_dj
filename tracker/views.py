from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import CurrentBalance, TrackingHistory

# Create your views here.


def login_view(request):

    if request.method == "POST":
        username = request.POST.get("user_name")
        password = request.POST.get("password")

        user = User.objects.filter(username=username)
        if not user.exists():
            messages.error(request, "User not Found")
            return redirect("login")

        user = authenticate(username=username, password=password)
        if not user:
            messages.error(request, "Incorrect Password")
            return redirect("login")
        login(request, user)
        return redirect("index")
    return render(request, "login.html")


def register_view(request):

    if request.method == "POST":
        user_name = request.POST.get("user_name")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")

        user = User.objects.filter(username=user_name)
        if user.exists():
            messages.success(request, "Username is already taken")
            return redirect("register")

        user = User.objects.create(
            first_name=first_name, last_name=last_name, username=user_name
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Registration Successfull")
        messages.success(request, "Account is Created")
        return redirect("login")

    return render(request, "register.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def index(request):

    if request.method == "POST":
        amount = request.POST.get("amount")
        description = request.POST.get("description")

        balance, _ = CurrentBalance.objects.get_or_create(id=1)

        expense_type = "CREDIT"

        if amount == "" or float(amount) == 0:
            messages.error(request, "The amount cannot be zero or empty")
            return redirect("index")

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

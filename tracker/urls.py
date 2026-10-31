from django.urls import path

from .views import delete_transaction, index, login_view, logout_view, register_view

urlpatterns = [
    path("", index, name="index"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("/delete-transaction/<id>/", delete_transaction, name="delete_transaction"),
]

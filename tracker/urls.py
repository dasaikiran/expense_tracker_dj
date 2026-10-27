from django.urls import path

from .views import index, delete_transaction

urlpatterns = [
    path("", index, name="index"),
    path("/delete-transaction/<id>/", delete_transaction, name="delete_transaction"),
]

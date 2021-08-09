from django.urls import path
from . import views

urlpatterns = [
    path("create_user/<slug:name>/<slug:email>", views.create_user, name="create_user"),
    path("get_user/<slug:name>", views.get_user, name="get user info"),
    path("transfer/<slug:src>/<slug:dst>/<int:amount>", views.transfer, name="transfer")
]
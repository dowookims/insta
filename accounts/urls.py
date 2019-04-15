from django.urls import path, include
from django.conf import settings

from . import views

app_name = "accounts"

urlpatterns = [
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
]
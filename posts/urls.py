from django.urls import path, include
from . import views


app_name = "posts"

urlpatterns = [
    path('create/', views.create, name="create")
]
from django.urls import path
from .views import *

urlpatterns = [
    path('v1/command/', CommandView.as_view(), name='command'),
]

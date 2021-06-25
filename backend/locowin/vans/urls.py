from django.urls import path
from .views import *



urlpatterns = [
    path('dashboard',Dashboard.as_view(),name='dashboard'),
]
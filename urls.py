from django.urls import path
from . import views

urlpatterns = [
    path('histories/', views.histories, name='histories'),
]

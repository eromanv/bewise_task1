from django.urls import path, include

from . import views

urlpatterns = [
    path('api/v1/questions/<int:pk>/', views.get_question),
]
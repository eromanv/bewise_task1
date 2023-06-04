from django.urls import path
from . import views
from .api import PostQuestions

urlpatterns = [
    path('', views.home, name='home'),
    path('api/process_questions/', PostQuestions.as_view(), name='post_questions'),
]
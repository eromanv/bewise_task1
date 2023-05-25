from django.urls import path, include

from views import PostQuestions

urlpatterns = [
    path("process_questions/", PostQuestions.as_view(), name="post_question"),
]

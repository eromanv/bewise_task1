from rest_framework import serializers
from .models import Question_quiz


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("question", "id", "answer", "created_at")
        model = Question_quiz

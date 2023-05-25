from django.http import JsonResponse
from .models import Question_quiz
from .serializers import QuestionSerializer


def recieve_question(request, id):
    if request.method == "GET":
        get_question = Question_quiz.objects.get(id=id)
        serializer = QuestionSerializer(get_question).data
        return JsonResponse(serializer)

from django.http import JsonResponse
import requests
from rest_framework.views import APIView
from rest_framework.response import Response, 

from .models import Question_quiz
from .serializers import QuestionSerializer


def recieve_question(request, id):
    if request.method == "GET":
        get_question = Question_quiz.objects.get(id=id)
        serializer = QuestionSerializer(get_question).data
        return JsonResponse(serializer)


class PostQuestions(APIView):
    def post(self, request):
        questions_num = request.data.get("questions_num")

        # Выполнение запроса к публичному API
        response = requests.get(
            "https://jservice.io/api/random", params={"count": questions_num}
        )
        if response.status_code == 200:
            data = response.json()
            # Обработка полученных данных
            # В данном случае, просто возвращаем полученный JSON в ответ
            return Response(data)
        else:
            return Response(
                {"error": "Failed to fetch questions"}, status=response.status_code
            )

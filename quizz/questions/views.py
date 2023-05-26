from django.http import JsonResponse
import requests
from rest_framework.views import APIView
from rest_framework.response import Response, g
import psycopg2
import os
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
        response = requests.get(
            "https://jservice.io/api/random", params={"count": questions_num}
        )
        if response.status_code == 200:
            data = response.json()

            conn = psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT')
            )
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS questions (id serial PRIMARY KEY, question varchar, answer varchar, created_at timestamp);")
            for item in data:
                id = item.get('id')
                question = item.get('question')
                answer = item.get('answer')
                created_at = item.get('created_at')
                cursor.execute("INSERT INTO questions (id, question, answer, created_at) VALUES (%s, %s, %s, %s)", (id, question, answer, created_at))
            conn.commit()
            cursor.close()
            conn.close()
        else:
            return Response(
                {"error": "Failed to fetch questions"}, status=response.status_code
            )

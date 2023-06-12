import psycopg2
import requests
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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
                user="postgres",
                password="postgres",
                host="db",
                port="5432",
                database="postgres"
            )
            cursor = conn.cursor()
            create_table_query = '''CREATE TABLE IF NOT EXISTS questions
                (ID SERIAL PRIMARY KEY     NOT NULL,
                QUESTION           TEXT    NOT NULL,
                ANSWER             TEXT    NOT NULL,
                CREATED_AT         TIMESTAMP);'''

           
            cursor.execute(create_table_query)
            conn.commit()
            print("Table created successfully")
            unique_questions = set()
            previous_question = None
            while len(unique_questions) < questions_num:
                response = requests.get(
                    "https://jservice.io/api/random", params={"count": questions_num}
                )
                if response.status_code == 200:
                    data = response.json()
                    for item in data:
                        question = item.get('question')
                        if question not in unique_questions:
                            unique_questions.add(question)
                            id = item.get('id')
                            answer = item.get('answer')
                            created_at = item.get('created_at')
                            cursor.execute("INSERT INTO questions (ID, QUESTION, ANSWER, CREATED_AT) VALUES (%s, %s, %s, %s)", (id, question, answer, created_at))
                            conn.commit()
                            previous_question = {
                                'id': id,
                                'question': question,
                                'answer': answer,
                                'created_at': created_at
                                }
            cursor.close()
            conn.close()
            return Response(previous_question, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Failed to fetch questions"}, status=response.status_code
            )

import os
from typing import Any, Dict, List, Union

import psycopg2
import requests

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class PostQuestions(APIView):
    def post(self, request) -> Response:
        questions_num = request.data.get("questions_num")
        response = requests.get(
            "https://jservice.io/api/random", params={"count": questions_num}
        )
        if response.status_code == 200:
            data: List[Dict[str, Union[int, str]]] = response.json()
            conn = psycopg2.connect(
                user="postgres",
                password="postgres",
                host="localhost",
                port="5432",
                database="postgres"
            )
            cursor = conn.cursor()
            create_table_query: str = '''CREATE TABLE IF NOT EXISTS questions
                (ID SERIAL PRIMARY KEY     NOT NULL,
                QUESTION           TEXT    NOT NULL,
                ANSWER             TEXT    NOT NULL,
                CREATED_AT         TIMESTAMP);'''

            cursor.execute(create_table_query)
            conn.commit()
            print("Table created successfully")
            unique_questions: set = set()
            previous_question: Dict[str, Union[int, str, Any]] = None
            questions_num = int(request.data.get("questions_num"))
            while len(unique_questions) < questions_num:
                response = requests.get(
                    "https://jservice.io/api/random", params={"count": questions_num}
                )
                if response.status_code == 200:
                    data = response.json()
                    for item in data:
                        question: str = item.get('question')
                        if question not in unique_questions:
                            unique_questions.add(question)
                            id: int = item.get('id')
                            answer: str = item.get('answer')
                            created_at: str = item.get('created_at')
                            cursor.execute("INSERT INTO questions (ID, QUESTION, ANSWER, CREATED_AT) VALUES (%s, %s, %s, %s)", (
                                id, question, answer, created_at))
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


def get_quiz_questions(questions_num):
    response = requests.post(
        "http://localhost:8000/api/process_questions/",
        data={"questions_num": questions_num}
    )
    if response.status_code == 200:
        return response.json()
    return {"error": "Failed to fetch questions"}

